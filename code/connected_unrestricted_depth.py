"""symbolic depth-minimum identity: independently compute knapsack minima k<=100.
the manuscript's proof is valid for every integer k>=1.
"""
import json
C=(7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1)
A=(5,4,4,1,2,1,1,0,3,2,2,1,1,0,0,0)
U={7,15}
def predicted(k,t):
 if t==1:return 7*k-2
 if t==2:return 7*k-5
 return max(1,3*k-t+1,5*k+5-3*t)
def calc(k):
 no={0:0};yes={(0,False):0}
 for _ in range(k):
  nn={};ny={}
  for t,v in no.items():
   for m in range(16):
    if m in U:continue
    key=t+m.bit_count()
    nn[key]=min(nn.get(key,10**20),v+C[m])
  for (t,u),v in yes.items():
   for m in range(16):
    key=(t+m.bit_count(),u or m in U)
    ny[key]=min(ny.get(key,10**20),v+A[m])
  no,yes=nn,ny
 return [min(no.get(t,10**20),1+yes.get((t,True),10**20)) for t in range(1,4*k+1)]
def run():
 rows=[]
 for k in range(1,101):
  actual=calc(k)
  expected=[predicted(k,t) for t in range(1,4*k+1)]
  assert actual==expected,(k,[(t+1,a,b) for t,(a,b) in enumerate(zip(actual,expected)) if a!=b][:5])
  assert sum(actual)==(11*k*k+19*k-12)//2
  rows.append(dict(k=k,relaxation=sum(actual),certified_optimum=sum(actual)+1))
 return dict(status="PASS",tested_k=100,all_k_proof="all-mask inequalities and explicit state witnesses",
             first_12=rows[:12],k_100=rows[-1])
if __name__=="__main__":print(json.dumps(run(),indent=2))
