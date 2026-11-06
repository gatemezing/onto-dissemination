#!/usr/bin/env python3
"""Validate an RDF sample against ERA SHACL shapes with pyshacl and aggregate the report.
Usage: validate.py DATA.ttl SHAPES.ttl OUT.csv REFERENCE.ttl...
Data graph = sample + reference graphs (ERA ontology, ERA SKOS, countries, NUTS: needed for sh:class over
subclasses and for the SKOS-membership constraints). Only focus nodes described in the sample are reported."""
import sys, re, csv, collections, time, rdflib
from pyshacl import validate
from pyshacl.helper.sparql_query_helper import SPARQLQueryHelper
# ERA's SHACL-SPARQL constraints use VALUES / MINUS / nested SELECTs, which pyshacl rejects under the
# SHACL pre-binding rules (SHACL 1.0 section 5.3.1) and which GraphDB/RDF4J accept. Relax the check so the
# constraints run as ERA runs them; federated (SERVICE) constraints are dropped below instead.
SPARQLQueryHelper.check_invalid_sparql = lambda self, *a, **k: None
from rdflib.namespace import SH, RDF
data_f, shapes_f, out_f, refs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
t = time.time()
data = rdflib.Graph()
for f in [data_f] + refs:
    data.parse(f, format="turtle")
shapes = rdflib.Graph(); shapes.parse(shapes_f, format="turtle")
# ERA's sh:prefixes point at the ontology IRI; make sure every prefix the queries use is declared there,
# then drop (and log) any SHACL-SPARQL query that still does not parse, so one bad constraint
# cannot abort the whole validation.
from rdflib.plugins.sparql import prepareQuery
STD = {"era": "http://data.europa.eu/949/", "rdf": str(RDF), "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
       "skos": "http://www.w3.org/2004/02/skos/core#", "xsd": "http://www.w3.org/2001/XMLSchema#", "owl": "http://www.w3.org/2002/07/owl#",
       "sh": str(SH), "geo": "http://www.opengis.net/ont/geosparql#",
       "time": "http://www.w3.org/2006/time#", "dct": "http://purl.org/dc/terms/",
       "foaf": "http://xmlns.com/foaf/0.1/", "wgs": "http://www.w3.org/2003/01/geo/wgs84_pos#", "era-sh": "http://data.europa.eu/949/shapes/"}
ONTO = rdflib.URIRef("http://data.europa.eu/949/")
# rdflib binds one prefix per namespace: ERA declares both geo: and geosparql: for GeoSPARQL, so one of
# them silently stops resolving. Rewrite geosparql: to geo: in the queries and drop the alias.
for d in list(shapes.subjects(SH.prefix, rdflib.Literal("geosparql"))):
    for h in list(shapes.subjects(SH.declare, d)):
        shapes.remove((h, SH.declare, d))
for pred in (SH.select, SH.ask):
    for c, q in list(shapes.subject_objects(pred)):
        if "geosparql:" in str(q):
            shapes.set((c, pred, rdflib.Literal(str(q).replace("geosparql:", "geo:"))))
for c in set(shapes.subjects(SH.select, None)) | set(shapes.subjects(SH.ask, None)):
    if shapes.value(c, SH.prefixes) is None:
        shapes.add((c, SH.prefixes, ONTO))
for holder in set(shapes.objects(None, SH.prefixes)) | {ONTO}:
    have = {str(shapes.value(d, SH.prefix)) for d in shapes.objects(holder, SH.declare)}
    for pfx, ns in STD.items():
        if pfx not in have:
            d = rdflib.BNode(); shapes.add((holder, SH.declare, d)); shapes.add((d, SH.prefix, rdflib.Literal(pfx))); shapes.add((d, SH.namespace, rdflib.Literal(ns, datatype=rdflib.XSD.anyURI)))
# PROD's LangStringEnRequired / LangStringEnRequiredIfPresent project "SELECT $this $PATH", which is not
# valid SPARQL once $PATH is substituted by the path IRI; UAT already reads "SELECT $this". Apply UAT's fix.
patched = []
for c, q in list(shapes.subject_objects(SH.select)):
    if re.search(r"SELECT\s+\$this\s+\$PATH\b", str(q)):
        shapes.set((c, SH.select, rdflib.Literal(re.sub(r"(SELECT\s+\$this)\s+\$PATH\b", r"\1", str(q)))))
        patched.append(str(c))
if patched:
    print(f"patched {len(patched)} constraints projecting $PATH:", *patched, sep="\n  ", flush=True)
dropped = []
for c, q in list(shapes.subject_objects(SH.select)) + list(shapes.subject_objects(SH.ask)):
    pre = dict(STD)
    for holder in shapes.objects(c, SH.prefixes):
        for d in shapes.objects(holder, SH.declare):
            px, nsv = shapes.value(d, SH.prefix), shapes.value(d, SH.namespace)
            if px is not None and nsv is not None and str(nsv).startswith("http"):
                pre[str(px)] = str(nsv)
    try:
        if re.search(r"\bSERVICE\b", str(q), re.I):
            raise ValueError("federated SERVICE query (needs a remote endpoint)")
        # prepend PREFIX lines as text (as pyshacl does); rdflib's initNs misses prefixed names in projections
        head = "".join(f"PREFIX {k}: <{v}>\n" for k, v in pre.items())
        prepareQuery(head + str(q).replace("$this", "?this").replace("$value", "?value").replace("$PATH", "?pathPlaceholder"))
    except Exception as e:
        dropped.append((str(c), str(e).splitlines()[0][:150]))
        for owner in list(shapes.subjects(SH.sparql, c)):
            shapes.remove((owner, SH.sparql, c))
if dropped:
    print(f"dropped {len(dropped)} unparseable SPARQL constraints:", *dropped, sep="\n  ", flush=True)
print(f"loaded data={len(data)} shapes={len(shapes)} in {time.time()-t:.0f}s", flush=True)
sample = rdflib.Graph(); sample.parse(data_f, format="turtle")
# The sample adds bare "?pl a era:PrimaryLocation" stubs so sh:class on linkedToPrimaryLocation resolves;
# do not report those stubs as focus nodes.
sample_nodes = {x for x in set(sample.subjects()) if any(p != RDF.type for p in sample.predicates(x))}
conforms, report, text = validate(data, shacl_graph=shapes, inference="none", advanced=True, allow_warnings=True, abort_on_first=False)
if not isinstance(report, rdflib.Graph):
    print("pyshacl failed:", text[:2000]); sys.exit(1)
print(f"validated in {time.time()-t:.0f}s conforms={conforms}", flush=True)
agg = collections.OrderedDict()
def short(x):
    if x is None: return ""
    s = str(x)
    for a, b in (("http://data.europa.eu/949/shapes/", "era-sh:"), ("http://data.europa.eu/949/", "era:"), (str(SH), "sh:")):
        s = s.replace(a, b)
    return s if not isinstance(x, rdflib.BNode) else "_:bnode"
described = set(data.subjects())
edge_dropped = 0
for r in report.subjects(RDF.type, SH.ValidationResult):
    focus = report.value(r, SH.focusNode)
    if focus not in sample_nodes:      # ignore results on the ontology / SKOS scaffolding
        continue
    # sh:class on a value the sample does not describe (its rdf:type lies beyond the sample's hop
    # limit) cannot be judged from the sample: drop it rather than report a false violation.
    if report.value(r, SH.sourceConstraintComponent) == SH.ClassConstraintComponent and report.value(r, SH.value) not in described:
        edge_dropped += 1
        continue
    ftypes = sorted(short(t) for t in data.objects(focus, RDF.type))
    shape = report.value(r, SH.sourceShape)
    path = report.value(r, SH.resultPath)
    key = (short(report.value(r, SH.resultSeverity)), short(shape), short(report.value(r, SH.sourceConstraintComponent)), short(path) if not isinstance(path, rdflib.BNode) else "_:path", "+".join(ftypes))
    a = agg.setdefault(key, {"n": 0, "focus": set(), "example": str(focus), "message": str(report.value(r, SH.resultMessage) or "")[:300], "value": str(report.value(r, SH.value) or "")[:120]})
    a["n"] += 1; a["focus"].add(focus)
with open(out_f, "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["severity", "shape", "component", "path", "focus_types", "results", "focus_nodes", "example_focus", "example_value", "message"])
    for k, a in sorted(agg.items(), key=lambda kv: -kv[1]["n"]):
        w.writerow(list(k) + [a["n"], len(a["focus"]), a["example"], a["value"], a["message"]])
print(f"{len(agg)} result groups -> {out_f}; dropped {edge_dropped} sh:class results on values outside the sample")
