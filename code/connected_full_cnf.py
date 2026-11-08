"""independent full-CNF crosscheck of connected-state clause-count rule.
Enumerates ALL 16^k eliminated-mask combinations for k=1,2,3.
No imports from the R21 or R22 code.
"""
from itertools import product
import json
BASE=((-4,-3),(-3,1),(-1,2),(3,5),(-4,-2,3),(-3,-2,-1),(-2,4,5))
def normalize(clauses):
 s={frozenset(c) for c in clauses if not any(-x in c for x in c)}
 return frozenset(c for c in s if not any(d<c for d in s))
def eliminate(f,v):
 pos=[c for c in f if v in c];neg=[c for c in f if -v in c]
 return normalize([c for c in f if v not in c and -v not in c]+
                  [(a-{v})|(b-{-v}) for a in pos for b in neg])
def local(mask):
 f=normalize(BASE)
 for v in range(1,5):
  if mask & (1<<(v-1)):f=eliminate(f,v)
 return f
L=[local(mask) for mask in range(16)]
C=[len(f) for f in L]
A=[sum(5 not in c for c in f) for f in L]
assert C==[7,6,6,2,6,4,4,1,5,3,3,2,3,2,2,1]
assert A==[5,4,4,1,2,1,1,0,3,2,2,1,1,0,0,0]
assert [m for m,f in enumerate(L) if frozenset({5}) in f]==[7,15]
def union_from_masks(masks):
 clauses=[]
 for i,m in enumerate(masks):
  for clause in L[m]:
   clauses.append(frozenset((x if abs(x)==5 else
                  (1 if x>0 else -1)*(10*i+abs(x))) for x in clause))
 return normalize(clauses)
def predicted(masks):
 if 7 in masks or 15 in masks:return 1+sum(A[m] for m in masks)
 return sum(C[m] for m in masks)
def run():
 rows=[]
 for k in (1,2,3):
  checked=0
  for masks in product(range(16),repeat=k):
   actual=len(union_from_masks(masks))
   expected=predicted(masks)
   assert actual==expected,(k,masks,actual,expected)
   checked+=1
  rows.append(dict(k=k,all_mask_combinations=checked,status="PASS"))
 return dict(status="PASS",rows=rows,combinations_total=sum(r['all_mask_combinations'] for r in rows),
  scope="Independent full-CNF normalization vs connected reduced state count; all masks for k<=3",
  limitation="Does not prove all-k optimal-cost closed forms or journal novelty")
if __name__=="__main__":print(json.dumps(run(),indent=2))
