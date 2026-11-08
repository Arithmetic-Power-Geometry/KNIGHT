"""exact, independent switch invariants for shared-positive-visible CNF.
Checks all 16 local masks, all 16^3 global states, and all legal transitions
for k=1,2,3; tests monotonicity and exact clause-count switch.
"""
from itertools import product
import json
BASE=((-4,-3),(-3,1),(-1,2),(3,5),(-4,-2,3),(-3,-2,-1),(-2,4,5))
def norm(clauses):
 s={frozenset(c) for c in clauses if not any(-v in c for v in c)}
 return frozenset(c for c in s if not any(d<c for d in s))
def elim(f,v):
 pos=[c for c in f if v in c];neg=[c for c in f if -v in c]
 return norm([c for c in f if v not in c and -v not in c]+[(a-{v})|(b-{-v}) for a in pos for b in neg])
def local(m):
 f=norm(BASE)
 for v in range(1,5):
  if m&(1<<(v-1)):f=elim(f,v)
 return f
T=[local(m) for m in range(16)]
unit=frozenset({5})
U={m for m,f in enumerate(T) if unit in f}
assert U=={7,15}
assert all((m|1<<v) in U for m in U for v in range(4) if not(m&(1<<v)))
C=[len(f) for f in T]
A=[sum(5 not in cl for cl in f) for f in T]
def full(ms):
 clauses=[]
 for i,m in enumerate(ms):
  for cl in T[m]:
   clauses.append(frozenset(x if abs(x)==5 else (1 if x>0 else -1)*(10*i+abs(x)) for x in cl))
 return norm(clauses)
def formula(ms):
 return (1+sum(A[m] for m in ms)) if any(m in U for m in ms) else sum(C[m] for m in ms)
def run():
 rows=[]
 for k in (1,2,3):
  states=0;edges=0;switches=0
  for ms in product(range(16),repeat=k):
   states+=1
   actual=full(ms)
   assert len(actual)==formula(ms)
   assert (unit in actual)==any(m in U for m in ms)
   for i,m in enumerate(ms):
    for v in range(4):
     if m&(1<<v):continue
     n=list(ms);n[i]=m|1<<v;n=tuple(n)
     before=any(t in U for t in ms)
     after=any(t in U for t in n)
     assert not before or after
     if not before and after:
      switches+=1
      assert n[i] in (7,15)
     edges+=1
  rows.append(dict(k=k,states=states,legal_edges=edges,first_switch_edges=switches))
 return dict(status="PASS",unit_masks=sorted(U),rows=rows,
  theorem="Once shared visible unit appears it persists; first appearance enters mask 7 or 15 (third or fourth elimination within that copy).")
if __name__=="__main__":print(json.dumps(run(),indent=2))
