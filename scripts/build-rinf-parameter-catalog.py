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
import concurrent.futures as futures

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
    # Check the header, not the first row: a query that legitimately matches
    # nothing still returns its header, and an empty result is not a fault.
    reader = csv.reader(io.StringIO(body))
    header = next(reader, None)
    if header is None:
        sys.exit(f"empty response where CSV was expected: {body.strip()[:300]}")
    missing = [c for c in expect if c not in header]
    if missing:
        sys.exit(f"unexpected response shape, missing column(s) {missing} "
                 f"(got {header}): {body.strip()[:300]}")
    return list(csv.DictReader(io.StringIO(body)))


# How a parameter's subject reaches a location. Resolved once, here, so the
# app never has to emit an unbound-predicate reverse join at query time — that
# is what times the endpoint out (a `?parent ?anyPred ?s` variant died at 120s
# server-side, while the bound-predicate lookups below run in ~2s over all 27
# countries). Each parameter stores the single pattern that applies to it.
#   self       subject is the section of line itself
#   part       ?parent era:hasPart ?subject
#   via:<pred> ?parent era:hasPart ?mid . ?mid era:<pred> ?subject
#   ''         no known path to a location
SUB_OBJECT_LINK = {
    "ETCS": "etcs",
    "TrainDetectionSystem": "trainDetectionSystem",
    "ContactLineSystem": "contactLineSystem",
    "HABD": "tracksideHabd",
}
PART_OF_PARENT = {"RunningTrack", "Track", "Siding", "Tunnel", "PlatformEdge",
                  "Signal", "OperationalPoint"}


def location_path(types):
    """Map a parameter's sampled subject types onto one location pattern."""
    if "SectionOfLine" in types:
        return "self"
    for t, pred in SUB_OBJECT_LINK.items():
        if t in types:
            return "via:" + pred
    if PART_OF_PARENT & set(types):
        return "part"
    return ""


def sample_subject_types(prop):
    """Types of a sample of this property's subjects, for location_path()."""
    rows = query(["type"], f"""PREFIX era: <http://data.europa.eu/949/>
SELECT DISTINCT ?type WHERE {{
  {{ SELECT ?s WHERE {{ ?s <{prop}> ?v }} LIMIT 120 }}
  ?s a ?type . FILTER(STRSTARTS(STR(?type), "http://data.europa.eu/949/"))
}}""", timeout=120)
    return prop, sorted({r["type"].rsplit("/", 1)[-1] for r in rows})


def const_of(block, name):
    """Pull one `const NAME = <json>;` line out of an existing data block."""
    head = f"const {name} = "
    for line in block.splitlines():
        if line.startswith(head):
            return json.loads(line[len(head):].rstrip().rstrip(";"))
    sys.exit(f"could not parse `const {name}` out of the existing data block")


def main():
    print("1/7  properties (excluding owl:deprecated) carrying an era:rinfIndex …")
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
  # Retired parameters are no longer permitted, so they must not be offered
  # for selection. They are still reported separately (step 6) because some
  # national datasets continue to publish them.
  FILTER NOT EXISTS { ?prop owl:deprecated true }
  OPTIONAL { ?prop rdfs:label ?lab FILTER(LANG(?lab)="en" || LANG(?lab)="") }
  OPTIONAL { ?prop rdfs:comment ?com FILTER(LANG(?com)="en" || LANG(?com)="") }
} GROUP BY ?prop ORDER BY ?prop""")
    props = [r["prop"] for r in base]
    print(f"     {len(props)} properties")

    print("2/7  statement / distinct-value counts (batched) …")
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

    print("3/7  which graphs hold rinfIndex data …")
    used = " ".join(f"<{p}>" for p in stats)
    datagraphs = {r["g"] for r in query(
        ["g"], f"SELECT ?g WHERE {{ VALUES ?p {{ {used} }} GRAPH ?g {{ ?s ?p ?v }} }} GROUP BY ?g")}

    print("4/7  how each populated parameter reaches a start/end operational point …")
    shapes = {}
    with futures.ThreadPoolExecutor(max_workers=6) as pool:
        for prop, types in pool.map(sample_subject_types, list(stats)):
            shapes[prop] = location_path(types)
    tally = collections.Counter(v or "(none)" for v in shapes.values())
    print("     " + ", ".join(f"{k}={n}" for k, n in tally.most_common()))

    print("5/7  retired parameters still being published …")
    depr_rows = query(["g", "p", "n"], """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX era: <http://data.europa.eu/949/>
SELECT ?g ?p (COUNT(*) AS ?n) WHERE {
  ?p owl:deprecated true ; era:rinfIndex ?i .
  GRAPH ?g { ?s ?p ?o }
} GROUP BY ?g ?p""")
    depr_total = query(["n"], """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX era: <http://data.europa.eu/949/>
SELECT (COUNT(*) AS ?n) WHERE {
  ?p owl:deprecated true ; era:rinfIndex ?i . ?s ?p ?o }""")
    print(f"     {len(depr_rows)} dataset/parameter pairs still carry retired parameters")

    print("6/7  graph -> country, from the countries the graph's resources declare …")
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

    print("7/7  writing the data block …")
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
                     lit=round(int(s["lit"]) / int(s["stmts"]), 3),
                     loc=shapes.get(u, ""))
        else:
            e.update(s=0, v=0, r=0, lit=None, loc="")
        catalog.append(e)
    catalog.sort(key=lambda e: ([int(p) if p.isdigit() else 0 for p in (e["i"][0] if e["i"] else "9").split(".")], e["n"]))

    # Which countries still publish parameters the specification has retired.
    by_country, by_prop = collections.defaultdict(
        lambda: {"stmts": 0, "props": set(), "datasets": set()}), collections.Counter()
    # invert the country -> datasets map built above
    ds2cc = {ds: c[len(COUNTRY_PREFIX):] for c, gs in bycountry.items() for ds in gs}
    for r in depr_rows:
        ds = r["g"][len(GRAPH_PREFIX):]
        cc = ds2cc.get(ds)
        if not cc:
            continue
        n = int(r["n"]); pn = r["p"].rsplit("/", 1)[-1]
        by_country[cc]["stmts"] += n
        by_country[cc]["props"].add(pn)
        by_country[cc]["datasets"].add(ds)
        by_prop[pn] += n
    deprecated = {
        "distinctStatements": int(depr_total[0]["n"]) if depr_total else 0,
        "datasetStatements": sum(by_prop.values()),
        "parameters": [{"n": n, "s": c} for n, c in by_prop.most_common()],
        "countries": sorted(
            ({"c": c, "l": labels.get(COUNTRY_PREFIX + c, c), "s": v["stmts"],
              "p": sorted(v["props"]), "g": sorted(v["datasets"])}
             for c, v in by_country.items()),
            key=lambda x: -x["s"]),
    }
    print(f"     {deprecated['distinctStatements']:,} statements still on retired parameters, "
          f"in {len(deprecated['countries'])} countries")

    meta = {"endpoint": EP, "snapshot": datetime.date.today().isoformat(),
            "graphPrefix": GRAPH_PREFIX, "countryPrefix": COUNTRY_PREFIX,
            "datasets": sum(len(c["g"]) for c in countries),
            "sharedExcluded": sorted(SHARED_GRAPHS)}
    block = ("const META = " + json.dumps(meta, separators=(",", ":")) + ";\n"
             "const COUNTRIES = " + json.dumps(countries, separators=(",", ":"), ensure_ascii=False) + ";\n"
             "const DEPRECATED = " + json.dumps(deprecated, separators=(",", ":"), ensure_ascii=False) + ";\n"
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
