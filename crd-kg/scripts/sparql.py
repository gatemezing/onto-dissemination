#!/usr/bin/env python3
"""Tiny SPARQL client: sparql.py ENDPOINT (QUERYFILE|-) [accept]  -> prints CSV/TSV/Turtle."""
import sys, urllib.request, urllib.parse
ENDPOINTS = {
    "crd": "https://rinf-ris-alignment.com/repositories/CRD",
    "rinf": "https://graph.data.era.europa.eu/repositories/rinf-plus",
    "onto": "https://graph.data.era.europa.eu/repositories/ERA-Onto",
}
def run(endpoint, query, accept="text/csv", timeout=300):
    url = ENDPOINTS.get(endpoint, endpoint)
    data = urllib.parse.urlencode({"query": query}).encode()
    req = urllib.request.Request(url, data=data, headers={"Accept": accept, "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")
if __name__ == "__main__":
    ep, qf = sys.argv[1], sys.argv[2]
    q = sys.stdin.read() if qf == "-" else open(qf).read()
    print(run(ep, q, sys.argv[3] if len(sys.argv) > 3 else "text/csv"), end="")
