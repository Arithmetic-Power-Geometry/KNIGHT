"""exact connected-family DP using symmetry and shared positive visible literal.
Every clause of every local component has only local hidden variables and
possibly positive literal 5. Presence of unit {5} subsumes all other clauses
containing 5. The resulting global clause count is exact.
"""
from functools import lru_cache
import json
BASE=[(-4,-3),(-3,1),(-1,2),(3,5),(-4,-2,3),(-3,-2,-1),(-2,4,5)]
def norm(clauses):
 s={frozenset(c) for c in clauses if not any(-x in c for x in c)}
 return frozenset(c for c in s if not any(d<c for d in s))
def elim(f,v):
 pos=[x for x in f if v in x];neg=[x for x in f if -v in x]
 rest=[x for x in f if v not in x and -v not in x]
 return norm(rest+[(x-{v})|(y-{-v}) for x in pos for y in neg])
def table():
 f=norm(BASE);C=[];A=[]
 for mask in range(16):
  g=f
  for v in range(1,5):
   if mask&(1<<(v-1)):g=elim(g,v)
  C.append(len(g));A.append(sum(5 not in cl for cl in g))
 assert C==[7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1]
 assert A==[5,4,4,1,2,1,1,0,3,2,2,1,1,0,0,0]
 return C,A
C,A=table()
def solve(k,forced=False):
 start=[0]*16;start[0]=k-int(forced)
 if forced:start[8]=1
 start=tuple(start)
 @lru_cache(None)
 def W(s):
  if s[7]+s[15]:return 1+sum(s[i]*A[i] for i in range(16))
  return sum(s[i]*C[i] for i in range(16))
 @lru_cache(None)
 def dp(s):
  if s[15]==k:return 0
  best=10**30
  for m,count in enumerate(s):
   if not count:continue
   for v in range(4):
    bit=1<<v
    if m&bit:continue
    n=list(s);n[m]-=1;n[m|bit]+=1;n=tuple(n)
    best=min(best,W(n)+dp(n))
  return best
 return dp(start)+(W(start) if forced else 0),dp.cache_info().currsize
def run():
 rows=[]
 for k in range(1,9):
  opt,n=solve(k);forced,_=solve(k,True)
  rows.append(dict(k=k,optimum=opt,forced_first_pivot4=forced,gap=forced-opt,states=n))
 assert [(x['optimum'],x['forced_first_pivot4']) for x in rows]==[
 (10,11),(36,39),(73,79),(121,130),(180,192),(250,265),(331,349),(423,444)]
 return dict(status="PASS",rows=rows)
if __name__=="__main__":print(json.dumps(run(),indent=2))
