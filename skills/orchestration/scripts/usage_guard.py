#!/usr/bin/env python3
"""Read explicit usage files; no provider calls, prompt output or agent control."""
import argparse
import datetime as dt
import json
from pathlib import Path

FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens')

def stamp(value):
    parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timestamps must include timezone')
    return parsed

def records(path):
    with Path(path).open() as stream:
        first = stream.read(1)
        stream.seek(0)
        if first == '[':
            yield from json.load(stream)
        else:
            for line in stream:
                if line.strip():
                    yield json.loads(line)

def measure(paths, root_turn, since, until):
    start, end = stamp(since), stamp(until)
    if end < start:
        raise ValueError('end precedes start')
    selected = {}
    compactions = set()
    for path in paths:
        for event in records(path):
            if event.get('type') == 'compacted':
                compactions.add(event.get('payload', {}).get('compaction_response_id'))
                continue
            native = event.get('type') == 'token_usage_record'
            if event.get('type') and not native:
                continue
            payload = event.get('payload', {}) if native else event
            if payload.get('root_turn_id') != root_turn and payload.get('turn_id') != root_turn:
                continue  # No guessing that an unscoped child belongs to this run.
            at = stamp(event['timestamp'])
            if not start <= at <= end:
                continue
            usage = payload.get('usage', {}) if native else payload
            values = {key: usage[key] for key in FIELDS}
            if any(type(v) is not int or v < 0 for v in values.values()):
                raise ValueError('usage must contain nonnegative integer counters')
            if values['cached_input_tokens'] > values['input_tokens'] or values['reasoning_output_tokens'] > values['output_tokens']:
                raise ValueError('usage subset exceeds total')
            if values['total_tokens'] != values['input_tokens'] + values['output_tokens']:
                raise ValueError('total must equal input plus output')
            rid, tid = payload.get('response_id'), payload.get('thread_id')
            if not rid or not tid:
                raise ValueError('response_id and thread_id required')
            row = dict(timestamp=event['timestamp'], thread_id=tid, root=payload.get('turn_id') == root_turn, **values)
            if rid in selected and selected[rid] != row:
                raise ValueError('conflicting duplicate response_id')
            selected[rid] = row
    agents = {}
    for rid, row in sorted(selected.items(), key=lambda pair: stamp(pair[1]['timestamp'])):
        a = agents.setdefault(row['thread_id'], {'root': row['root'], 'responses': 0, 'input_tokens': 0, 'output_tokens': 0, 'processed_tokens': 0, 'first_input_tokens': row['input_tokens'], 'latest_input_tokens': 0, 'peak_input_tokens': 0, 'compactions': 0})
        a['responses'] += 1
        a['input_tokens'] += row['input_tokens']
        a['output_tokens'] += row['output_tokens']
        a['processed_tokens'] += row['total_tokens']
        a['latest_input_tokens'] = row['input_tokens']
        a['peak_input_tokens'] = max(a['peak_input_tokens'], row['input_tokens'])
        a['compactions'] += rid in compactions
    return {'schema_version': 1, 'root_turn_id': root_turn, 'since': since, 'observed_at': until, 'responses': len(selected), 'totals': {k: sum(r[k] for r in selected.values()) for k in FIELDS}, 'agents': agents}

def gate(metrics, policy, root_turn, action, now=None, retired_workers=()):
    now = now or dt.datetime.now(dt.timezone.utc)
    reasons = []
    if metrics['root_turn_id'] != root_turn:
        reasons.append('wrong_run')
    age = (now - stamp(metrics['observed_at'])).total_seconds()
    if age < -5 or age > policy['max_snapshot_age_seconds']:
        reasons.append('stale_or_future_snapshot')
    if not metrics['responses'] or not any(a['root'] for a in metrics['agents'].values()):
        reasons.append('missing_scoped_root_usage')
    values = {'max_processed_tokens': metrics['totals']['total_tokens'], 'max_output_tokens': metrics['totals']['output_tokens'], 'max_responses': metrics['responses'], 'max_elapsed_minutes': (now-stamp(metrics['since'])).total_seconds()/60}
    reserve = policy['reserve_fraction']
    if not 0 <= reserve < 1:
        raise ValueError('reserve_fraction must be in [0,1)')
    factor = 1-reserve if action in ('dispatch', 'repair') else 1
    for key, value in values.items():
        if type(policy[key]) not in (int, float) or policy[key] <= 0:
            raise ValueError('positive budget required: '+key)
        if value >= policy[key] * factor:
            reasons.append(key + ('_reserve' if factor < 1 else '_exhausted'))
    unknown = set(retired_workers) - set(metrics['agents'])
    if unknown:
        reasons.append('unknown_retired_worker')
    if any(metrics['agents'].get(i, {}).get('root') for i in retired_workers):
        reasons.append('cannot_retire_current_root')
    if action in ('dispatch', 'repair'):
        for ident, a in metrics['agents'].items():
            if not a['root'] and ident in retired_workers:
                continue
            limit = policy['max_root_responses' if a['root'] else 'max_worker_responses']
            if a['responses'] >= limit or a['compactions'] or a.get('peak_input_tokens', a['latest_input_tokens'])-a['first_input_tokens'] >= policy['max_context_growth_tokens']:
                reasons.append('renew_or_replan:'+ident)
    return {'admit': not reasons, 'action': action, 'reasons': reasons, 'enforcement': 'pre-dispatch check only; does not control native tools or billing'}


def worker_check(metrics, policy, root_turn, thread_id, budget_tokens, now=None):
    """Own-context check; deliberately does NOT claim aggregate run admission."""
    now = now or dt.datetime.now(dt.timezone.utc)
    reasons, warnings = [], []
    if type(budget_tokens) is not int or budget_tokens <= 0:
        raise ValueError('positive assigned worker budget required')
    if metrics['root_turn_id'] != root_turn:
        reasons.append('wrong_run')
    age = (now - stamp(metrics['observed_at'])).total_seconds()
    if age < -5 or age > policy['max_snapshot_age_seconds']:
        reasons.append('stale_or_future_snapshot')
    a = metrics['agents'].get(thread_id)
    if not a or not a['responses'] or a['root']:
        reasons.append('missing_scoped_worker_usage')
    else:
        growth = a.get('peak_input_tokens', a['latest_input_tokens'])-a['first_input_tokens']
        if growth >= policy.get('warn_context_growth_tokens', 18000):
            warnings.append('prepare_compact_checkpoint')
        if growth >= policy['max_context_growth_tokens'] or a['compactions']:
            reasons.append('renew_context_at_safe_boundary')
        if a['processed_tokens'] >= budget_tokens:
            reasons.append('assigned_worker_budget_replan')
        elif a['processed_tokens'] >= budget_tokens * 0.8:
            warnings.append('forecast_remaining_completion_cost')
        if a['responses'] >= policy['max_worker_responses']:
            reasons.append('worker_response_replan')
    return {'continue': not reasons, 'scope': 'worker_only', 'reasons': reasons,
            'warnings': warnings, 'next': 'checkpoint_and_replan' if reasons else 'continue_bounded_work',
            'enforcement': 'cooperative check; cannot interrupt agents or enforce billing'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    m = sub.add_parser('measure')
    m.add_argument('--files', nargs='+', required=True)
    m.add_argument('--root-turn', required=True)
    m.add_argument('--since', required=True)
    m.add_argument('--until', default=None)
    m.add_argument('--out', required=True)
    g = sub.add_parser('gate')
    g.add_argument('--metrics', required=True)
    g.add_argument('--policy', required=True)
    g.add_argument('--root-turn', required=True)
    g.add_argument('--action', choices=['dispatch','repair','review','integrate'], required=True)
    g.add_argument('--retired-worker', action='append', default=[], help='verified completed or replaced context; all other measured workers are active by default')
    w = sub.add_parser('worker-check')
    w.add_argument('--files', nargs='+', required=True)
    w.add_argument('--root-turn', required=True)
    w.add_argument('--since', required=True)
    w.add_argument('--thread-id', required=True)
    w.add_argument('--budget-tokens', type=int, required=True)
    w.add_argument('--policy', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'measure':
            result = measure(args.files, args.root_turn, args.since, args.until or dt.datetime.now(dt.timezone.utc).isoformat())
            Path(args.out).write_text(json.dumps(result, indent=2)+'\n')
            print(json.dumps({k:v for k,v in result.items() if k!='agents'}))
        elif args.command == 'worker-check':
            metrics = measure(args.files, args.root_turn, args.since, dt.datetime.now(dt.timezone.utc).isoformat())
            result = worker_check(metrics, json.loads(Path(args.policy).read_text()), args.root_turn,
                                  args.thread_id, args.budget_tokens)
            print(json.dumps(result))
            return 0 if result['continue'] else 2
        else:
            result = gate(json.loads(Path(args.metrics).read_text()), json.loads(Path(args.policy).read_text()), args.root_turn, args.action, retired_workers=args.retired_worker)
            print(json.dumps(result))
            return 0 if result['admit'] else 2
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(json.dumps({'admit':False,'error':str(error)}))
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
