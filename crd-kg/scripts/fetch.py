#!/usr/bin/env python3
"""Run every queries/*.rq against CRD and rinf-plus; write data/raw/<endpoint>/<query>.csv.
Usage: python3 -I scripts/fetch.py [query-name ...]"""
import sys, os, time, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sparql import run
root = pathlib.Path(__file__).resolve().parent.parent
names = sys.argv[1:] or sorted(p.stem for p in (root / "queries").glob("*.rq"))
for ep in ("crd", "rinf"):
    out = root / "data" / "raw" / ep; out.mkdir(parents=True, exist_ok=True)
    for n in names:
        if ep == "crd" and n == "pl-op":  # CRD has no operational points
            continue
        t = time.time()
        try:
            txt = run(ep, (root / "queries" / f"{n}.rq").read_text(), timeout=600)
            (out / f"{n}.csv").write_text(txt)
            print(f"{ep:5} {n:12} {txt.count(chr(10))-1:7} rows {time.time()-t:6.1f}s", flush=True)
        except Exception as e:
            print(f"{ep:5} {n:12} FAILED {e}", flush=True)
