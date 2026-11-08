"""Recreate the technical illustrations using the recorded manuscript data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
TABLES=json.loads((ROOT/"data"/"manuscript_tables.json").read_text())
OUT=ROOT/"figures"/"generated"
OUT.mkdir(exist_ok=True)

fig, ax=plt.subplots(figsize=(9.4,2.5))
ax.set_xlim(0,10);ax.set_ylim(0,2);ax.axis("off")
boxes=[(0.1,"Normalized\nCNF + pivots"),(2.6,"Background\nlower bounds"),(5.1,"Lazy / indexed\nupper bound"),(7.6,"Strict gap?\ncertify or abstain")]
for x,s in boxes:
    ax.text(x+.9,1,s,ha="center",va="center",fontsize=11,bbox={"boxstyle":"round,pad=.55","facecolor":"white","edgecolor":"black"})
for x in (2.08,4.58,7.08):
    ax.annotate("",xy=(x+.48,1),xytext=(x,1),arrowprops={"arrowstyle":"->","lw":1.3})
fig.savefig(OUT/"workflow.pdf",bbox_inches="tight");plt.close(fig)

rows=TABLES["timing"]; xs=[r["m"] for r in rows]
fig,ax=plt.subplots(figsize=(7,3.6))
for key,marker,label in (("incremental_ms","o-","Incremental certificate"),("indexed_ms","s-","Indexed batch"),("exact_ms","^-","Exact lookahead")):
    ax.plot(xs,[r[key] for r in rows],marker,label=label)
ax.set_yscale("log");ax.set_xlabel("Family parameter m");ax.set_ylabel("Median call time (ms; log scale)");ax.grid(alpha=.25);ax.legend()
fig.tight_layout();fig.savefig(OUT/"timing.pdf");plt.close(fig)

d=TABLES["coverage"];n=d["favorable"]
fig,ax=plt.subplots(figsize=(7,3.2))
ax.barh(["Incremental certificate","Indexed batch","Exact-a / lower-b","Exact lookahead"],[d["incremental"]/n*100,d["indexed"]/n*100,d["one_sided"]/n*100,100])
ax.set_xlim(0,105);ax.set_xlabel("Favorable comparisons certified (%)")
fig.tight_layout();fig.savefig(OUT/"coverage.pdf");plt.close(fig)
print("Created",*(str(p) for p in sorted(OUT.glob("*.pdf"))),sep="\n")
