import copy
import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('guard', HERE/'usage_guard.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
POLICY = json.loads((HERE.parent/'references/budget-policy.json').read_text())
NOW = dt.datetime(2026,9,23,10,tzinfo=dt.timezone.utc)
START = '2026-09-23T09:59:00Z'
END = NOW.isoformat()

def record(rid='r', tid='root', turn='run', root='run', n=1000):
    return dict(timestamp=END, thread_id=tid, turn_id=turn, root_turn_id=root, response_id=rid,input_tokens=n,cached_input_tokens=n-10,output_tokens=100,reasoning_output_tokens=50,total_tokens=n+100)

class GuardTests(unittest.TestCase):
    def measure(self, rows):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'usage.json';p.write_text(json.dumps(rows))
            return g.measure([p], 'run', START, END)
    def admission(self,m,action='dispatch',retired=()):
        return g.gate(m,POLICY,'run',action,NOW,retired)['admit']
    def test_normal_and_no_double_counting(self):
        m=self.measure([record()]);self.assertEqual(m['totals']['total_tokens'],1100);self.assertTrue(self.admission(m))
    def test_duplicate_counted_once(self):
        self.assertEqual(self.measure([record(),record()])['responses'],1)
    def test_conflicting_duplicate_refused(self):
        with self.assertRaises(ValueError):self.measure([record(),record(n=2000)])
    def test_unrelated_turn_excluded(self):
        self.assertEqual(self.measure([record(),record('x',turn='other',root='other')])['responses'],1)
    def test_unscoped_child_not_assumed(self):
        self.assertEqual(self.measure([record(),record('x','child','child',None)])['responses'],1)
    def test_native_and_compaction_counted(self):
        r=record();p={k:v for k,v in r.items() if k not in g.FIELDS and k!='timestamp'};p['usage']={k:r[k] for k in g.FIELDS}
        m=self.measure([dict(type='token_usage_record',timestamp=END,payload=p),dict(type='compacted',payload={'compaction_response_id':'r'})])
        self.assertEqual(m['totals']['total_tokens'],1100);self.assertEqual(m['agents']['root']['compactions'],1);self.assertFalse(self.admission(m));self.assertTrue(self.admission(m,'review'))
    def test_empty_unknown_not_zero_pass(self):
        self.assertFalse(self.admission(self.measure([])))
    def test_child_only_not_complete(self):
        self.assertFalse(self.admission(self.measure([record('x','child','child')])))
    def test_bad_usage_subset(self):
        r=record();r['cached_input_tokens']=2000
        with self.assertRaises(ValueError):self.measure([r])
    def test_stale_future_wrong_run(self):
        for at in ['2026-09-23T09:57:00Z','2026-09-23T10:01:00Z']:
            m=self.measure([record()]);m['observed_at']=at;self.assertFalse(self.admission(m))
        m=self.measure([record()]);m['root_turn_id']='other';self.assertFalse(self.admission(m))
    def test_reserve_and_full_cap(self):
        m=self.measure([record(n=3999900)]);self.assertFalse(self.admission(m));self.assertTrue(self.admission(m,'review'))
        m=self.measure([record(n=4999900)]);self.assertFalse(self.admission(m,'integrate'))
    def test_response_and_time_caps(self):
        m=self.measure([record(str(i)) for i in range(24)]);self.assertFalse(self.admission(m))
        m=self.measure([record()]);m['since']='2026-09-23T09:00:00Z';self.assertFalse(self.admission(m,'review'))
    def test_context_growth_and_active_worker(self):
        a=record('a','worker','child');a['timestamp']=START
        m=self.measure([record(),a,record('b','worker','child',n=25000)])
        self.assertFalse(self.admission(m))
        self.assertTrue(self.admission(m,retired=['worker'])) # historical usage retained, context retired
        self.assertEqual(m['totals']['total_tokens'],27300)
    def test_completed_compaction_does_not_deadlock(self):
        m=self.measure([record(),record('x','completed','child')]);m['agents']['completed']['compactions']=1
        self.assertTrue(self.admission(m,retired=['completed']));self.assertFalse(self.admission(m))
        self.assertFalse(self.admission(m,retired=['missing']));self.assertFalse(self.admission(m,retired=['root']))
    def test_cli_fails_closed_on_missing_file(self):
        p=subprocess.run([sys.executable,str(HERE/'usage_guard.py'),'gate','--metrics','/nonexistent-guard-fixture','--policy',str(HERE.parent/'references/budget-policy.json'),'--root-turn','run','--action','dispatch'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2);self.assertFalse(json.loads(p.stdout)['admit'])

if __name__=='__main__':unittest.main()
