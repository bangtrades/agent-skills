import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import run_bounded as rb
import usage_guard as ug
import workflow_gate as wg

HERE = Path(__file__).parent
POLICY = json.loads((HERE.parent/'references/budget-policy.json').read_text())
NOW = dt.datetime.now(dt.timezone.utc)


def metrics():
    return {'root_turn_id':'run','since':(NOW-dt.timedelta(minutes=1)).isoformat(),
            'observed_at':NOW.isoformat(),'responses':2,
            'totals':{'total_tokens':72000,'output_tokens':200},
            'agents':{'root':{'root':True,'responses':1,'first_input_tokens':36000,'latest_input_tokens':36000,'peak_input_tokens':36000,'compactions':0},
                      'worker':{'root':False,'responses':1,'first_input_tokens':36000,'latest_input_tokens':36000,'peak_input_tokens':36000,'compactions':0,'processed_tokens':36100}}}


class WorkerTests(unittest.TestCase):
    def check(self, m, **kw):
        return ug.worker_check(m,POLICY,'run','worker',kw.get('budget',2000000),NOW)
    def test_worker_only_is_explicit(self):
        m=metrics();del m['agents']['root']
        r=self.check(m);self.assertTrue(r['continue']);self.assertEqual(r['scope'],'worker_only')
    def test_growth_warning_and_checkpoint(self):
        m=metrics();m['agents']['worker']['peak_input_tokens']=54000
        self.assertTrue(self.check(m)['continue']);self.assertIn('prepare_compact_checkpoint',self.check(m)['warnings'])
        m['agents']['worker']['peak_input_tokens']=60000
        self.assertFalse(self.check(m)['continue'])
    def test_lower_latest_does_not_erase_peak(self):
        m=metrics();m['agents']['worker'].update(peak_input_tokens=61000,latest_input_tokens=37000)
        self.assertFalse(self.check(m)['continue'])
        self.assertFalse(ug.gate(m,POLICY,'run','dispatch',NOW)['admit'])
    def test_compaction_and_budget_and_response_checkpoint(self):
        for key,value in [('compactions',1),('processed_tokens',2000000),('responses',POLICY['max_worker_responses'])]:
            m=metrics();m['agents']['worker'][key]=value;self.assertFalse(self.check(m)['continue'])
    def test_missing_wrong_stale_root_are_rejected(self):
        m=metrics();del m['agents']['worker'];self.assertFalse(self.check(m)['continue'])
        for field,value in [('root_turn_id','wrong'),('observed_at',(NOW-dt.timedelta(minutes=5)).isoformat())]:
            m=metrics();m[field]=value;self.assertFalse(self.check(m)['continue'])
        m=metrics();m['agents']['worker']['root']=True;self.assertFalse(self.check(m)['continue'])
    def test_no_invalid_assigned_allowance(self):
        for budget in [0,-1,True,1.5]:
            with self.assertRaises(ValueError):self.check(metrics(),budget=budget)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.log=Path(self.tmp.name)/'check.log';self.log.write_text('assertion and negative control pass\n')
        self.receipt={'candidate':'frozen','status':'passed','skips':0,'command':'required check','log':str(self.log),'sha256':hashlib.sha256(self.log.read_bytes()).hexdigest()}
        self.c={'outcome':'one behavior','actual_caller':'route -> worker','controller':{'mode':'bounded_existing','current_input_tokens':36000,'remaining_responses':2,'mitigation':'compact reports'},
                'remaining_forecast':{p:{'responses':5,'mean_input_tokens':60000,'output_tokens':1000} for p in wg.PHASES},
                'acceptance':[{'id':'a','assertion':'no stale send','check':'required check','evidence':self.receipt}],
                'producer_self_check':'passed','candidate':'frozen','independent_qa':copy.deepcopy(self.receipt)}
    def check(self,action='review',m=None):return wg.contract_check(self.c,action,m or metrics(),POLICY)
    def test_completed_slice_can_enter_review_and_integration(self):
        self.assertTrue(self.check()['admit']);self.assertTrue(self.check('integrate')['admit'])
    def test_known_incomplete_is_not_acceptance_qa(self):
        self.c['producer_self_check']='failed';self.assertFalse(self.check()['admit'])
    def test_stale_missing_wrong_identity_skipped_evidence_rejected(self):
        for key,value in [('candidate','old'),('status','failed'),('skips',1),('log','/nonexistent-test-log'),('sha256','bad')]:
            with self.subTest(key=key):
                old=self.receipt[key];self.receipt[key]=value;self.assertFalse(self.check()['admit']);self.receipt[key]=old
        self.log.write_text('changed after receipt');self.assertFalse(self.check()['admit'])
    def test_qa_is_mandatory_for_integration(self):
        self.c['independent_qa']=None;self.assertTrue(self.check()['admit']);self.assertFalse(self.check('integrate')['admit'])
    def test_require_actual_caller_and_all_assertions(self):
        for field,value in [('outcome',[]),('actual_caller',None),('acceptance',[])]:
            old=self.c[field];self.c[field]=value;self.assertFalse(self.check()['admit']);self.c[field]=old
        self.c['acceptance'].append(copy.deepcopy(self.c['acceptance'][0]));self.assertFalse(self.check()['admit'])
    def test_all_completion_phases_reserved_and_fit(self):
        self.assertTrue(self.check('dispatch')['admit'])
        self.c['remaining_forecast']['repair']['responses']=0;self.assertFalse(self.check('dispatch')['admit'])
        self.c['remaining_forecast']['repair']['responses']=500;self.assertFalse(self.check('dispatch')['admit'])
    def test_controller_cost_is_visible_and_warning_not_false_hard_limit(self):
        self.c['controller']['current_input_tokens']=200000
        r=self.check();self.assertTrue(r['admit']);self.assertIn('large_controller_context',r['warnings']);self.assertIn('controller_share_above_target',r['warnings'])
        self.c['controller']['remaining_responses']=100;self.assertFalse(self.check()['admit'])
    def test_missing_mitigation_and_fractional_forecast_rejected(self):
        del self.c['controller']['mitigation'];self.assertFalse(self.check()['admit'])
        self.c['controller']['mitigation']='limited';self.c['remaining_forecast']['qa']['responses']=1.5;self.assertFalse(self.check()['admit'])
    def test_cli_applies_usage_gate_even_for_complete_contract(self):
        paths={}
        m=metrics();m['totals']['total_tokens']=POLICY['max_processed_tokens']
        for name,data in [('contract',self.c),('metrics',m),('policy',POLICY)]:
            p=Path(self.tmp.name)/(name+'.json');p.write_text(json.dumps(data));paths[name]=str(p)
        command=[sys.executable,str(HERE/'workflow_gate.py'),'--root-turn','run','--action','review']
        for k,v in paths.items():command+=['--'+k,v]
        r=subprocess.run(command,capture_output=True,text=True);self.assertEqual(r.returncode,2);self.assertFalse(json.loads(r.stdout)['admit'])


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.log=Path(self.tmp.name)/'output.log'
    def test_flood_stored_complete_excerpt_bounded_exit_preserved(self):
        r=rb.run([sys.executable,'-c','import sys; print("x"*100000); print("FAILED_SENTINEL", file=sys.stderr); sys.exit(7)'],self.log,80)
        self.assertEqual(r['exit_code'],7);self.assertGreater(r['bytes'],100000);self.assertLessEqual(len(r['excerpt']),80)
        self.assertIn('FAILED_SENTINEL',self.log.read_text());self.assertEqual(r['sha256'],hashlib.sha256(self.log.read_bytes()).hexdigest())
        self.assertFalse(r['excerpt_is_complete'])
    def test_unicode_zero_excerpt_no_shell_expansion(self):
        r=rb.run([sys.executable,'-c','import sys; print(sys.argv[1]*100)','🧪$()'],self.log,13)
        self.assertLessEqual(len(r['excerpt']),13);self.assertIn('$()',self.log.read_text())
        r=rb.run([sys.executable,'-c','print("ok")'],Path(self.tmp.name)/'zero.log',0);self.assertEqual(r['excerpt'],'')
    def test_invalid_utf8_cannot_claim_truncated_excerpt_complete(self):
        r=rb.run([sys.executable,'-c','import sys; sys.stdout.buffer.write(bytes([255])*1000)'],self.log,400)
        self.assertEqual(len(r['excerpt']),400);self.assertFalse(r['excerpt_is_complete'])
        self.assertEqual(self.log.read_bytes(),bytes([255])*1000)
        r=rb.run([sys.executable,'-c','import sys; sys.stdout.buffer.write(bytes([255])*10)'],Path(self.tmp.name)/'short.log',400)
        self.assertTrue(r['excerpt_is_complete'])
    def test_existing_evidence_never_overwritten(self):
        self.log.write_text('original')
        with self.assertRaises(FileExistsError):rb.run([sys.executable,'-c','print("bad")'],self.log)
        self.assertEqual(self.log.read_text(),'original')
    def test_timeout_has_failure_exit_and_private_log(self):
        r=rb.run([sys.executable,'-c','import time; time.sleep(5)'],self.log,timeout=.05)
        self.assertTrue(r['timed_out']);self.assertEqual(r['exit_code'],124)
        if sys.platform!='win32':self.assertEqual(self.log.stat().st_mode & 0o777,0o600)
    def test_invalid_limits_do_not_create_file(self):
        with self.assertRaises(ValueError):rb.run([],self.log)
        with self.assertRaises(ValueError):rb.run(['anything'],self.log,-1)
        self.assertFalse(self.log.exists())


if __name__=='__main__':unittest.main()
