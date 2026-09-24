#!/usr/bin/env python3
"""Validate one outcome, cost-to-finish, and identity-bound QA handoffs."""
import argparse
import hashlib
import json
from pathlib import Path

from usage_guard import gate
from run_bounded import run

PHASES = ('implementation', 'qa', 'repair', 'integration')


def positive(value, allow_zero=False):
    return type(value) is int and value >= (0 if allow_zero else 1)


def receipt_ok(receipt, candidate):
    if not isinstance(receipt, dict) or not candidate or receipt.get('candidate') != candidate:
        return False
    if receipt.get('status') != 'passed' or receipt.get('skips') != 0 or not receipt.get('command'):
        return False
    try:
        p = Path(receipt['log'])
        digest = hashlib.sha256()
        with p.open('rb') as stream:
            for block in iter(lambda: stream.read(65536), b''):
                digest.update(block)
        return digest.hexdigest() == receipt['sha256']
    except (KeyError, OSError, TypeError):
        return False


def contract_check(contract, action, metrics, policy):
    reasons, warnings = [], []
    outcome = contract.get('outcome')
    acceptance = contract.get('acceptance')
    if not isinstance(outcome, str) or not outcome.strip() or not contract.get('actual_caller'):
        reasons.append('one_outcome_and_actual_caller_required')
    if not isinstance(acceptance, list) or not acceptance:
        reasons.append('acceptance_required')
        acceptance = []
    ids = []
    for row in acceptance:
        if not isinstance(row, dict) or not all(row.get(k) for k in ('id', 'assertion', 'check')):
            reasons.append('acceptance_must_map_to_a_check')
        else:
            ids.append(row['id'])
    if len(set(ids)) != len(ids):
        reasons.append('duplicate_acceptance_id')
    forecast = contract.get('remaining_forecast', {})
    total = 0
    for phase in PHASES:
        entry = forecast.get(phase, {})
        count, mean, output = (entry.get(k) for k in ('responses', 'mean_input_tokens', 'output_tokens'))
        if not positive(count, True) or not positive(mean) or not positive(output, True):
            reasons.append('invalid_completion_forecast:'+phase)
            continue
        if count == 0 and output != 0:
            reasons.append('output_without_responses:'+phase)
        total += count * mean + output
        if action in ('dispatch', 'repair') and phase in ('qa', 'repair', 'integration') and count == 0:
            reasons.append('completion_phase_not_reserved:'+phase)
    remaining = policy['max_processed_tokens'] - metrics['totals']['total_tokens']
    if total <= 0 or total > remaining:
        reasons.append('completion_forecast_does_not_fit')
    controller = contract.get('controller', {})
    current, responses = controller.get('current_input_tokens'), controller.get('remaining_responses')
    if not positive(current) or not positive(responses):
        reasons.append('controller_forecast_required')
    else:
        tax = current * responses
        if tax > total:
            reasons.append('controller_cost_missing_from_forecast')
        if total and tax / total > policy.get('target_controller_share', .15):
            warnings.append('controller_share_above_target')
        if current > policy.get('controller_input_warning_tokens', 80000):
            warnings.append('large_controller_context')
        if controller.get('mode') not in ('fresh_authorized', 'bounded_existing'):
            reasons.append('controller_strategy_required')
        if controller.get('mode') == 'bounded_existing' and not controller.get('mitigation'):
            reasons.append('existing_controller_requires_mitigation')
    if action in ('review', 'integrate'):
        candidate = contract.get('candidate')
        if contract.get('producer_self_check') != 'passed':
            reasons.append('producer_incomplete')
        if not candidate or not acceptance:
            reasons.append('frozen_candidate_and_coverage_required')
        for row in acceptance:
            if not isinstance(row, dict) or not receipt_ok(row.get('evidence'), candidate):
                reasons.append('missing_or_stale_acceptance_evidence')
        if action == 'integrate' and not receipt_ok(contract.get('independent_qa'), candidate):
            reasons.append('independent_qa_required')
    return {'admit': not reasons, 'reasons': sorted(set(reasons)), 'warnings': warnings,
            'forecast_remaining_tokens': total, 'available_tokens': remaining,
            'limitation': 'Checks claims and log identity, not assertion semantics or source truth; reviewer and root verify those.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('contract', 'metrics', 'policy', 'root-turn'):
        p.add_argument('--'+arg, required=True)
    p.add_argument('--action', choices=('dispatch', 'repair', 'review', 'integrate'), required=True)
    p.add_argument('--retired-worker', action='append', default=[])
    p.add_argument('--log')
    p.add_argument('--timeout', type=float, default=120)
    p.add_argument('--max-chars', type=int, default=2000)
    p.add_argument('--execute', nargs=argparse.REMAINDER)
    a = p.parse_args()
    try:
        contract, metrics, policy = [json.loads(Path(f).read_text()) for f in (a.contract, a.metrics, a.policy)]
        usage = gate(metrics, policy, a.root_turn, a.action, retired_workers=a.retired_worker)
        workflow = contract_check(contract, a.action, metrics, policy)
        result = {'admit': usage['admit'] and workflow['admit'], 'usage': usage, 'workflow': workflow}
        if not result['admit']:
            print(json.dumps(result))
            return 2
        if a.execute is not None:
            if not a.execute or not a.log:
                raise ValueError('--execute requires command and --log')
            execution = run(a.execute, a.log, a.max_chars, a.timeout)
            result['execution'] = execution
            print(json.dumps(result))
            code = execution['exit_code']
            return code if code >= 0 else 128-code
        print(json.dumps(result))
        return 0
    except (ValueError, KeyError, TypeError, OSError, AttributeError) as error:
        print(json.dumps({'admit': False, 'error': str(error)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
