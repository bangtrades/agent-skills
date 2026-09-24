import copy
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import unittest
import test_workflow_controls as fixtures
from test_workflow_controls import metrics, POLICY, NOW

HERE = Path(__file__).parent

class GuardedExecutionTests(unittest.TestCase):
    setUp = fixtures.WorkflowTests.setUp
    def invoke(self, change=None, command=None):
        m = metrics()
        p = copy.deepcopy(POLICY)
        paths = {}
        for name, data in [('contract', self.c), ('metrics', m), ('policy', p)]:
            path = Path(self.tmp.name)/(name+'.json')
            path.write_text(json.dumps(data))
            paths[name] = path
        if change:
            change(paths)
        marker = Path(self.tmp.name)/'MUTATION'
        argv = [sys.executable, str(HERE/'workflow_gate.py'), '--root-turn', 'run', '--action', 'dispatch']
        for name, path in paths.items():
            argv += ['--'+name, str(path)]
        argv += ['--log', str(Path(self.tmp.name)/'owned.log'), '--execute']
        argv += command or [sys.executable, '-c', 'from pathlib import Path; import sys; Path(sys.argv[1]).write_text("executed")', str(marker)]
        result = subprocess.run(argv, capture_output=True, text=True)
        return result, marker

    def test_admitted_command_executes_and_receipt_matches(self):
        r, marker = self.invoke()
        self.assertEqual(r.returncode, 0, r.stdout+r.stderr)
        self.assertTrue(marker.exists())
        self.assertEqual(json.loads(r.stdout)['execution']['exit_code'], 0)

    def test_denied_missing_malformed_stale_admission_never_mutates(self):
        def edit(paths, field, value):
            m=json.loads(paths['metrics'].read_text());m[field]=value
            paths['metrics'].write_text(json.dumps(m))
        cases = {
            'denied': lambda p: edit(p, 'totals', {'total_tokens': POLICY['max_processed_tokens'], 'output_tokens': 0}),
            'missing': lambda p: p['metrics'].unlink(),
            'malformed-json': lambda p: p['metrics'].write_text('{bad'),
            'missing-admission': lambda p: p['metrics'].write_text('{}'),
            'malformed-negative': lambda p: edit(p, 'responses', -1),
            'malformed-boolean': lambda p: edit(p, 'responses', True),
            'malformed-policy': lambda p: p['policy'].write_text('{"max_processed_tokens":NaN}'),
            'missing-contract': lambda p: p['contract'].unlink(),
            'stale': lambda p: edit(p, 'observed_at', (NOW-dt.timedelta(minutes=5)).isoformat()),
        }
        for name, change in cases.items():
            with self.subTest(name=name):
                r, marker = self.invoke(change)
                self.assertEqual(r.returncode, 2, r.stdout+r.stderr)
                self.assertFalse(marker.exists())
                self.assertFalse((Path(self.tmp.name)/'owned.log').exists())

    def test_admitted_failure_propagates(self):
        r, marker = self.invoke(command=[sys.executable, '-c', 'raise SystemExit(7)'])
        self.assertEqual(r.returncode, 7)
        self.assertFalse(marker.exists())

    def test_disabled_legacy_checkpoint_does_not_renew_workers(self):
        import usage_guard
        m=metrics();m['agents']['worker']['compactions']=1
        p=copy.deepcopy(POLICY);p['context_checkpoints']=False
        self.assertTrue(usage_guard.gate(m,p,'run','dispatch',NOW)['admit'])

if __name__ == '__main__': unittest.main()
