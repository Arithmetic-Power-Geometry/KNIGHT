"""independent exact forced-depth DP versus proved closed form for k=1..100."""
import json
C=(7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1)
A=(5,4,4,1,2,1,1,0,3,2,2,1,1,0,0,0)
UNIT={7,15}
def predicted(k,t):
 if k==1:return (5,3,2,1)[t-1]
 if t==1:return 7*k-2
 if t==2:return 7*k-4
 if t==3:return 7*k-7
 return max(1,3*k+1-t,5*k+6-3*t)
def independent_dp(k):
 # For other copies, compute separate knapsacks for pre-unit and unit-aware a-sum.
 before={0:0}
 after={(0,False):0}
 for _ in range(k-1):
  nb={};na={}
  for t,v in before.items():
   for m in range(16):
    if m in UNIT:continue
    q=t+m.bit_count()
    nb[q]=min(nb.get(q,10**30),v+C[m])
  for (t,u),v in after.items():
   for m in range(16):
    q=(t+m.bit_count(),u or m in UNIT)
    na[q]=min(na.get(q,10**30),v+A[m])
  before,after=nb,na
 values=[]
 for t in range(1,4*k+1):
  opts=[]
  for m in range(16):
   if not (m&8):continue
   rem=t-m.bit_count()
   if rem<0:continue
   if m not in UNIT and rem in before:opts.append(C[m]+before[rem])
   for u in (False,True):
    if (u or m in UNIT) and (rem,u) in after:
     opts.append(1+A[m]+after[(rem,u)])
  values.append(min(opts))
 return values
def run():
 checks=0;rows=[]
 for k in range(1,101):
  actual=independent_dp(k)
  target=[predicted(k,t) for t in range(1,4*k+1)]
  assert actual==target,(k,[(i+1,a,b) for i,(a,b) in enumerate(zip(actual,target)) if a!=b][:3])
  total=sum(actual)
  assert total==(11 if k==1 else (11*k*k+25*k-18)//2)
  rows.append(dict(k=k,depth_sum=total,corrected_optimum=total+(k>=2)))
  checks+=len(actual)
 return dict(status="PASS",k_range="1..100",depth_values_verified=checks,
  first_12=rows[:12],k_100=rows[-1],
  mathematical_scope="proof derives exact forced-first optimum for all k; CI independently checks 100 sizes")
if __name__=="__main__":print(json.dumps(run(),indent=2))
