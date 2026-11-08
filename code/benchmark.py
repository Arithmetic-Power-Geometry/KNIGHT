""" normalized CNF certificate benchmark; Python standard library only."""
import random,time,tracemalloc,statistics,json,platform,argparse
from pathlib import Path

def norm(cs):
 s={frozenset(c) for c in cs if not any(-x in c for x in c)}
 return frozenset(c for c in s if not any(d<c for d in s))
def parts(f,v):
 return ([c-{v} for c in f if v in c],[c-{-v} for c in f if -v in c],[c for c in f if v not in c and -v not in c])
def lower(p,n,b):
 return sum(not(any(x<=k for x in p) and any(y<=k for y in n)) for k in b)
def exact(f,v):
 p,n,b=parts(f,v);return norm(list(b)+[x|y for x in p for y in n])
def incremental(f,a,b):
 pa,na,ba=parts(f,a);pb,nb,bb=parts(f,b)
 la=lower(pa,na,ba);lb=lower(pb,nb,bb);A=set();remaining=len(pa)*len(na)
 if lb>la+remaining:return True
 for x in pa:
  for y in na:
   remaining-=1;q=x|y
   if not any(-z in q for z in q) and not any(r<=q for r in A):
    A={r for r in A if not q<r};A.add(q)
   if lb>la+len(A)+remaining:return True
 return False
def batch(f,a,b):
 pa,na,ba=parts(f,a);pb,nb,bb=parts(f,b)
 la=lower(pa,na,ba);lb=lower(pb,nb,bb)
 postings={}
 for j,n in enumerate(na):
  for lit in n:postings.setdefault(lit,set()).add(j)
 viable=[]
 for p in pa:
  excluded=set()
  for lit in p:excluded.update(postings.get(-lit,()))
  viable.append([j for j in range(len(na)) if j not in excluded])
 remaining=sum(map(len,viable));A=set()
 if lb>la+remaining:return True
 for i,js in enumerate(viable):
  for j in js:
   remaining-=1;q=pa[i]|na[j]
   if not any(r<=q for r in A):A={r for r in A if not q<r};A.add(q)
   if lb>la+len(A)+remaining:return True
 return False
def lookahead(f,a,b):return len(exact(f,a))<len(exact(f,b))
def fm(m):
 cs=[(1,3,10+i) for i in range(m)]+[(-1,-3,10000+j) for j in range(m)]+[(2,4),(-2,5)]
 return norm(cs)
def hk(k):
 cs=[(1,3,5),(1,4,6),(-1,3,5),(-1,4,6),(2,5),(2,6),(-2,7),(-2,8)]
 cs += [(3,4,5,6,9+i) for i in range(k)]
 cs += [(5,7),(5,8),(6,7),(6,8),(7,8)]
 return norm(cs)
def randomcnf(seed,n,m):
 rng=random.Random(seed);cs=[]
 for _ in range(m):
  vs=rng.sample(range(1,n+1),3);cs.append(tuple(v if rng.randrange(2) else -v for v in vs))
 return norm(cs)
def measure(fn,f,a,b,reps=7):
 times=[]
 for _ in range(reps):
  t=time.perf_counter_ns();out=fn(f,a,b);times.append(time.perf_counter_ns()-t)
 tracemalloc.start();fn(f,a,b);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
 return {'median_ms':round(statistics.median(times)/1e6,5),'peak_traced_kib':round(peak/1024,2),'result':out}
def run():
 cases=[('F',m,fm(m),1,2) for m in (10,40,80,160)]+[('H',k,hk(k),1,2) for k in (10,40,80)]+[('R',i,randomcnf(17000+i,12,35),1,2) for i in range(20)]
 rows=[];false_cert=0;missed=0
 for typ,k,f,a,b in cases:
  ref=lookahead(f,a,b);o=incremental(f,a,b);q=batch(f,a,b)
  assert not(o and not ref) and not(q and not ref),(typ,k,o,q,ref)
  false_cert+=int((o or q) and not ref);missed+=int(o!=q)
  measurements={name:measure(fn,f,a,b) for name,fn in [('incremental',incremental),('batch',batch),('exact',lookahead)]}
  rows.append({'family':typ,'parameter':k,'clauses':len(f),'exact_order':ref,'p25_certificate':o,'batch_certificate':q,'measurements':measurements})
 return {'status':'PASS','python':platform.python_version(),'platform':platform.platform(),'repetitions':7,'cases':len(rows),'false_certificates':false_cert,'certificate_disagreements':missed,'rows':rows}
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',default='benchmark_results.json');args=parser.parse_args()
 r=run();Path(args.output).write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({'status':r['status'],'cases':r['cases'],'disagreements':r['certificate_disagreements']}))
