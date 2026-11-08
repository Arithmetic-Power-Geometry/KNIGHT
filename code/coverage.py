""" portable coverage rerun. Run from this directory: python p378_reproduce.py"""
import json,time,statistics,platform
from pathlib import Path
import benchmark as b
def one_sided(f,a,v):
 pb,nb,bb=b.parts(f,v)
 return len(b.exact(f,a))<b.lower(pb,nb,bb)
def exact_compare(f,a,v):
 return len(b.exact(f,a))<len(b.exact(f,v))
def run():
 cases=[('F',m,b.fm(m)) for m in (10,40,80,160)]+[('H',k,b.hk(k)) for k in (10,40,80)]+[('R',i,b.randomcnf(50000+i,9,20)) for i in range(1000)]
 rows=[]
 for family,k,f in cases:
  truth=b.lookahead(f,1,2)
  methods={'incremental':b.incremental,'batch':b.batch,'one_sided':one_sided,'exact':exact_compare}
  outcomes={name:fn(f,1,2) for name,fn in methods.items()}
  assert outcomes['exact']==truth
  assert all(not result or truth for result in outcomes.values())
  rows.append(dict(family=family,id=k,clauses=len(f),favorable=truth,**outcomes))
 summaries={}
 for group in ('F','H','R'):
  subset=[r for r in rows if r['family']==group]
  summaries[group]={key:sum(bool(r[key]) for r in subset) for key in ('favorable','incremental','batch','one_sided','exact')}
  summaries[group]['cases']=len(subset)
 timing=[]
 for group,k,f in [('F',160,b.fm(160)),('H',80,b.hk(80))]+[('R',i,b.randomcnf(50000+i,9,20)) for i in range(20)]:
  for name,fn in [('incremental',b.incremental),('batch',b.batch),('one_sided',one_sided),('exact',exact_compare)]:
   vals=[]
   for _ in range(9):
    t=time.perf_counter_ns();fn(f,1,2);vals.append((time.perf_counter_ns()-t)/1e6)
   timing.append(dict(family=group,id=k,method=name,median_ms=statistics.median(vals)))
 return dict(status='PASS',python=platform.python_version(),summaries=summaries,timing=timing,limitations=['exact-a one-sided method computes full successor a','synthetic CNFs only','single-machine timings'])
if __name__=='__main__':
 result=run()
 Path('coverage_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result['summaries'],indent=2))
