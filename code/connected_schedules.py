"""independently implement explicit all-k connected schedules and phase-cost certificates."""
import json
C=(7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1)
A=(5,4,4,1,2,1,1,0,3,2,2,1,1,0,0,0)
def schedule(k,forced=False):
 assert k>=1
 masks=[0]*k;phases={}
 def pivot(i,v):
  bit=1<<(v-1)
  assert not masks[i]&bit
  masks[i]|=bit
  return 1+sum(A[m] for m in masks) if any(m in (7,15) for m in masks) else sum(C[m] for m in masks)
 def phase(name,steps):phases[name]=sum(pivot(i,v) for i,v in steps)
 if not forced:
  phase('activate',((0,v) for v in (1,2,3)))
  for v in (3,1,2):phase('other_'+str(v),((i,v) for i in range(1,k)))
  phase('finish',((i,4) for i in range(k)))
 else:
  phase('first4',[(0,4)])
  if k==1:phase('complete_copy0',((0,v) for v in (1,2,3)))
  else:
   phase('activate',((1,v) for v in (1,2,3)))
   phase('others3',((i,3) for i in range(2,k)))
   phase('copy0_3',[(0,3)])
   for v in (1,2):phase('others'+str(v),((i,v) for i in range(2,k)))
   phase('copy0_1',[(0,1)])
   phase('finish_others',((i,4) for i in range(1,k)))
   phase('copy0_2',[(0,2)])
 assert all(m==15 for m in masks)
 return sum(phases.values()),phases
def formula(k,forced=False):
 return ((11*k*k+25*k-16)//2 if forced and k>=2 else
         11 if forced else (11*k*k+19*k-10)//2)
def expected_phases(k,forced=False):
 if not forced:return dict(activate=19*k-10,
  other_3=(k-1)*(7*k-8)//2,other_1=(k-1)*(3*k-2)//2,
  other_2=k*(k-1)//2,finish=k)
 if k==1:return dict(first4=5,complete_copy0=6)
 return dict(first4=7*k-2,activate=19*k-16,
  others3=(k-2)*(7*k-9)//2,copy0_3=2*(k-1),
  others1=3*(k-2)*(k-1)//2,others2=(k-2)*(k+1)//2,
  copy0_1=1,finish_others=k-1,copy0_2=1)
def run():
 rows=[]
 for k in range(1,101):
  opt,ph=schedule(k)
  forced,fp=schedule(k,True)
  assert ph==expected_phases(k)
  assert fp==expected_phases(k,True),(k,fp,expected_phases(k,True))
  assert opt==formula(k) and forced==formula(k,True)
  rows.append(dict(k=k,constructive_cost=opt,forced_first_cost=forced,gap=forced-opt))
 assert [x['constructive_cost'] for x in rows[:8]]==[10,36,73,121,180,250,331,423]
 return dict(status="PASS",tested_k=100,rows_first_12=rows[:12],
  conclusion="Explicit all-k upper-bound schedules with phase-wise arithmetic-sum identities",
  limitation="No all-k matching lower bound polynomial or forced-first lower bound proved")
if __name__=="__main__":print(json.dumps(run(),indent=2))
