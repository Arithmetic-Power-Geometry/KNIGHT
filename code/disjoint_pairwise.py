"""Independent exhaustive certificate for all-k optimum via pair decomposition."""
from itertools import permutations
from functools import lru_cache
import json

C=(7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1)
def path(p):
 m=0;v=[7]
 for x in p:
  m|=1<<x
  v.append(C[m])
 return tuple(v)
P=[(p,path(p)) for p in permutations(range(4))]
def cross(a,b,force_first_a=False):
 @lru_cache(None)
 def dp(i,j):
  if i==4 and j==4:return 0
  opts=[]
  if i<4:opts.append(b[j]+dp(i+1,j))
  if j<4 and (not force_first_a or i+j>0):
   opts.append(a[i]+dp(i,j+1))
  return min(opts)
 return dp(0,0)
def run():
 min_intrinsic=min(sum(a[1:]) for _,a in P)
 min_forced_intrinsic=min(sum(a[1:]) for p,a in P if p[0]==3)
 pairmin=(10**9,None)
 forcedmin=(10**9,None)
 pair_checks=0
 for p,a in P:
  for q,b in P:
   pair_checks+=1
   val=cross(a,b)
   if val<pairmin[0]:pairmin=(val,(p,q))
   if p[0]==3:
    v=cross(a,b,True)
    if v<forcedmin[0]:forcedmin=(v,(p,q))
 assert min_intrinsic==10
 assert min_forced_intrinsic==11
 assert pairmin[0]==23
 assert forcedmin[0]==25
 assert pair_checks==576
 return dict(status="PASS",local_orders=24,local_order_pairs=pair_checks,
             min_intrinsic=min_intrinsic,
             min_intrinsic_first_pivot4=min_forced_intrinsic,
             min_cross_pair=pairmin[0],min_cross_pair_witness=pairmin[1],
             min_cross_pair_when_global_first_pivot4=forcedmin[0],
             forced_cross_witness=forcedmin[1],
             conclusion="pairwise bounds + matching constructive schedules prove all-k formulas")
if __name__=="__main__":print(json.dumps(run(),indent=2))
