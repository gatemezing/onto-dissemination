#!/usr/bin/env python3
"""Rebuild the parameter catalogue embedded in era-rinf-value-explorer.html.

The app ships with a snapshot of every ERA property that carries an
era:rinfIndex, plus the country -> national-dataset map, so that it opens
instantly instead of spending ~40s discovering all of that on every load.
Re-run this when ERA publishes new parameters or a new IM starts reporting:

    python3 scripts/build-rinf-parameter-catalog.py

It rewrites the `const META/COUNTRIES/CATALOG` block in place and prints a
diff summary. Nothing else in the file is touched.
"""
import csv, io, json, re, subprocess, sys, collections, datetime, pathlib

EP = "https://graph.data.era.europa.eu/repositories/rinf-plus"
APP = pathlib.Path(__file__).resolve().parent / "assets" / "era-rinf-value-explorer.html"
GRAPH_PREFIX = "http://data.europa.eu/949/graph/"
COUNTRY_PREFIX = "http://publications.europa.eu/resource/authority/country/"
# Graphs that hold data for several countries at once and so cannot stand in
# for a national dataset. `borders` carries only border-point geometries.
SHARED_GRAPHS = {"borders"}


def query(expect, q, timeout=400):
    """Run a CSV SELECT (`expect` names the columns it must return) and fail
    loudly on anything that is not a clean 200.

    curl exits 0 for an HTTP 500 that carries a body, so without the explicit
    status check a failed batch would parse as zero rows and quietly mark
    every parameter in it as unpopulated. For an unattended job that silent
    mode of failure is the dangerous one, so every response is checked for
    its status and for the header columns the caller expects.
    """
    p = subprocess.run(
        ["curl", "-sS", "--max-time", str(timeout), "-w", "\n%{http_code}",
         "-X", "POST", EP,
         "-H", "Content-Type: application/sparql-query",
         "-H", "Accept: text/csv", "--data-binary", "@-"],
        input=q.encode(), capture_output=True)
    if p.returncode:
        sys.exit(f"curl failed (exit {p.returncode}): " + p.stderr.decode()[:400])
    body, _, code = p.stdout.decode("utf-8", "replace").rpartition("\n")
    if code.strip() != "200":
        sys.exit(f"endpoint returned HTTP {code.strip()}: {body.strip()[:300]}")
    rows = list(csv.DictReader(io.StringIO(body)))
    missing = [c for c in expect if not rows or c not in rows[0]]
    if missing:
        sys.exit(f"unexpected response shape, missing column(s) {missing}: {body.strip()[:300]}")
    return rows


def const_of(block, name):
    """Pull one `const NAME = <json>;` line out of an existing data block."""
    head = f"const {name} = "
    for line in block.splitlines():
        if line.startswith(head):
            return json.loads(line[len(head):].rstrip().rstrip(";"))
    sys.exit(f"could not parse `const {name}` out of the existing data block")


def main():
    print("1/5  properties carrying an era:rinfIndex …")
    base = query(["prop", "indexes", "kinds", "label", "comment"], """
PREFIX era: <http://data.europa.eu/949/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?prop (GROUP_CONCAT(DISTINCT ?idx; separator=" | ") AS ?indexes)
       (GROUP_CONCAT(DISTINCT ?kind; separator=" | ") AS ?kinds)
       (SAMPLE(?lab) AS ?label) (SAMPLE(?com) AS ?comment)
WHERE {
  ?prop era:rinfIndex ?idx ; a ?kind .
  FILTER(?kind IN (owl:DatatypeProperty, owl:ObjectProperty, rdf:Property))
  OPTIONAL { ?prop rdfs:label ?lab FILTER(LANG(?lab)="en" || LANG(?lab)="") }
  OPTIONAL { ?prop rdfs:comment ?com FILTER(LANG(?com)="en" || LANG(?com)="") }
} GROUP BY ?prop ORDER BY ?prop""")
    props = [r["prop"] for r in base]
    print(f"     {len(props)} properties")

    print("2/5  statement / distinct-value counts (batched) …")
    stats = {}
    for i in range(0, len(props), 25):
        chunk = props[i:i + 25]
        vals = " ".join(f"<{p}>" for p in chunk)
        rows = query(["p", "stmts", "dv", "ds", "lit"], f"""SELECT ?p (COUNT(*) AS ?stmts) (COUNT(DISTINCT ?v) AS ?dv)
(COUNT(DISTINCT ?s) AS ?ds) (SUM(IF(isLiteral(?v),1,0)) AS ?lit)
WHERE {{ VALUES ?p {{ {vals} }} ?s ?p ?v }} GROUP BY ?p""")
        for r in rows:
            stats[r["p"]] = r
        print(f"     batch {i//25 + 1}: {len(stats)} populated so far", flush=True)

    print("3/5  which graphs hold rinfIndex data …")
    used = " ".join(f"<{p}>" for p in stats)
    datagraphs = {r["g"] for r in query(
        ["g"], f"SELECT ?g WHERE {{ VALUES ?p {{ {used} }} GRAPH ?g {{ ?s ?p ?v }} }} GROUP BY ?g")}

    print("4/5  graph -> country, from the countries the graph's resources declare …")
    dist = collections.defaultdict(dict)
    for r in query(["g", "country", "n"], """PREFIX era: <http://data.europa.eu/949/>
SELECT ?g ?country (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s era:inCountry ?country } }
GROUP BY ?g ?country"""):
        dist[r["g"]][r["country"]] = int(r["n"])
    labels = {r["c"]: r["label"] for r in query(["c", "label"], """PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?c ?label WHERE {
  GRAPH <http://data.europa.eu/949/graph/rinf/countries> { ?c skos:prefLabel ?label }
  FILTER(LANG(?label)="en")
  FILTER EXISTS { ?x <http://data.europa.eu/949/inCountry> ?c } }""")}

    bycountry, impure = collections.defaultdict(list), []
    for g in sorted(datagraphs):
        code = g[len(GRAPH_PREFIX):]
        if code in SHARED_GRAPHS or g not in dist:
            continue
        d = dist[g]
        top, n = max(d.items(), key=lambda kv: kv[1])
        bycountry[top].append(code)
        if n < sum(d.values()):
            impure.append((code, top[len(COUNTRY_PREFIX):], n, sum(d.values())))
    countries = sorted(
        ({"c": c[len(COUNTRY_PREFIX):], "l": labels.get(c, c[len(COUNTRY_PREFIX):]), "g": sorted(gs)}
         for c, gs in bycountry.items()),
        key=lambda x: x["l"])
    for code, cc, n, tot in impure:
        print(f"     NOTE dataset {code} -> {cc} is {n/tot*100:.2f}% single-country "
              f"({tot - n} of {tot} resources are elsewhere)")

    print("5/5  writing the data block …")
    catalog = []
    for r in base:
        u = r["prop"]
        s = stats.get(u)
        e = {"u": u, "n": re.split(r"[/#]", u)[-1],
             "i": sorted(x.strip() for x in r["indexes"].split("|") if x.strip()),
             "l": (r["label"] or "").strip(),
             "k": "O" if "ObjectProperty" in r["kinds"] else ("D" if "DatatypeProperty" in r["kinds"] else "P")}
        com = re.sub(r"\s+", " ", (r["comment"] or "")).strip()
        if com:
            e["d"] = com[:400]
        if s:
            e.update(s=int(s["stmts"]), v=int(s["dv"]), r=int(s["ds"]),
                     lit=round(int(s["lit"]) / int(s["stmts"]), 3))
        else:
            e.update(s=0, v=0, r=0, lit=None)
        catalog.append(e)
    catalog.sort(key=lambda e: ([int(p) if p.isdigit() else 0 for p in (e["i"][0] if e["i"] else "9").split(".")], e["n"]))

    meta = {"endpoint": EP, "snapshot": datetime.date.today().isoformat(),
            "graphPrefix": GRAPH_PREFIX, "countryPrefix": COUNTRY_PREFIX,
            "datasets": sum(len(c["g"]) for c in countries),
            "sharedExcluded": sorted(SHARED_GRAPHS)}
    block = ("const META = " + json.dumps(meta, separators=(",", ":")) + ";\n"
             "const COUNTRIES = " + json.dumps(countries, separators=(",", ":"), ensure_ascii=False) + ";\n"
             "const CATALOG = " + json.dumps(catalog, separators=(",", ":"), ensure_ascii=False) + ";\n")

    html = APP.read_text()
    pattern = re.compile(r"const META = .*?\nconst CATALOG = .*?;\n", re.S)
    m = pattern.search(html)
    if not m:
        sys.exit("could not find the data block in " + str(APP))
    prev = m.group(0)

    # A daily unattended run must never quietly replace a good snapshot with a
    # gutted one — a half-answered endpoint would otherwise look like "most
    # parameters are suddenly unpopulated". Refuse any material shrink.
    allow_shrink = "--allow-shrink" in sys.argv
    for name, now, before in (
            ("properties", len(catalog), len(const_of(prev, "CATALOG"))),
            ("populated properties", sum(1 for e in catalog if e["s"]),
             sum(1 for e in const_of(prev, "CATALOG") if e["s"])),
            ("countries", len(countries), len(const_of(prev, "COUNTRIES")))):
        if before and now < before * 0.8 and not allow_shrink:
            sys.exit(f"refusing to write: {name} fell from {before} to {now} (>20% drop).\n"
                     f"Re-run when the endpoint is healthy, or pass --allow-shrink "
                     f"if the drop is real.")

    APP.write_text(pattern.sub(lambda _: block, html, count=1))
    before_cat = const_of(prev, "CATALOG")
    added = {e["n"] for e in catalog} - {e["n"] for e in before_cat}
    removed = {e["n"] for e in before_cat} - {e["n"] for e in catalog}
    print(f"\nwrote {APP.name}: {len(catalog)} properties "
          f"({sum(1 for e in catalog if e['s'])} populated), {len(countries)} countries, "
          f"{meta['datasets']} datasets")
    print(f"     was {len(before_cat)} properties "
          f"({sum(1 for e in before_cat if e['s'])} populated), "
          f"{len(const_of(prev, 'COUNTRIES'))} countries")
    if added:
        print("     new parameters: " + ", ".join(sorted(added)[:12]))
    if removed:
        print("     gone: " + ", ".join(sorted(removed)[:12]))
    if not added and not removed:
        print("     no parameters added or removed")
    print("Re-run the Playwright checks before committing.")


if __name__ == "__main__":
    main()
