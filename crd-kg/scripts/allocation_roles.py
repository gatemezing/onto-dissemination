#!/usr/bin/env python3
"""Finding F1: is each CRD allocation company typed with a role it holds in OCR-KG?

Reads every era:allocationCompany role of the CRD subsidiary locations (organisation code, role
concept, SLs), looks the organisation codes up in ERA's OCR-KG, and writes
stats/allocation-company-roles.csv. Usage: python3 -I scripts/allocation_roles.py"""
import csv, io, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sparql import run

ROOT = pathlib.Path(__file__).resolve().parent.parent
OCR = "https://graph.data.era.europa.eu/repositories/OCR-KG"
CRD_Q = """PREFIX era: <http://data.europa.eu/949/>
SELECT ?code ?crdRole (COUNT(DISTINCT ?sl) AS ?sls) WHERE {
  ?sl era:allocationCompany ?ac . ?ac era:hasOrganisationRole ?r
  BIND(REPLACE(STR(?ac), "^.*/([^/_]+)_.*$", "$1") AS ?code)
  BIND(STRAFTER(STR(?r), "organisation-roles/") AS ?crdRole)
} GROUP BY ?code ?crdRole ORDER BY DESC(?sls)"""
OCR_Q = """PREFIX era: <http://data.europa.eu/949/> PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?code (GROUP_CONCAT(DISTINCT STRAFTER(STR(?r), "organisation-roles/"); separator="|") AS ?ocrRoles) (SAMPLE(?nm) AS ?name)
WHERE { VALUES ?code { %s } ?b era:organisationCode ?code .
  OPTIONAL { ?b foaf:name ?nm } OPTIONAL { ?role era:roleOf ?b ; era:hasOrganisationRole ?r } } GROUP BY ?code"""

crd = list(csv.DictReader(io.StringIO(run("crd", CRD_Q))))
codes = " ".join(f'"{c}"' for c in sorted({r["code"] for r in crd}))
ocr = {r["code"]: r for r in csv.DictReader(io.StringIO(run(OCR, OCR_Q % codes)))}
with open(ROOT / "stats" / "allocation-company-roles.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["organisation_code", "name_in_ocr_kg", "crd_role", "ocr_kg_roles", "crd_role_held_in_ocr_kg", "sls"])
    for r in crd:
        o = ocr.get(r["code"], {})
        roles = sorted(set((o.get("ocrRoles") or "").split("|")) - {""})
        w.writerow([r["code"], o.get("name", ""), r["crdRole"], "|".join(roles), "yes" if r["crdRole"] in roles else "no", r["sls"]])
bad = [r for r in crd if r["crdRole"] not in set((ocr.get(r["code"], {}).get("ocrRoles") or "").split("|"))]
print(f"{len(crd)} companies; {len(bad)} typed with a role OCR-KG does not list, covering "
      f"{sum(int(r['sls']) for r in bad):,} of {sum(int(r['sls']) for r in crd):,} SLs")
