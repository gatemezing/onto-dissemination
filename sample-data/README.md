# sample-data

Sample SPARQL query + result pairs fetched live from real ERA endpoints, kept
as reference examples (e.g. for testing tools, sharing with colleagues, or
comparing against future endpoint behaviour).

## operationalPoint-f317d4ae4b

- **Query:** [`operationalPoint-f317d4ae4b-query.rq`](operationalPoint-f317d4ae4b-query.rq) — a `CONSTRUCT` that
  exports every triple where `http://data.europa.eu/949/operationalPoint/f317d4ae4b`
  appears as either subject or object, so the result includes both what the
  resource asserts and what points back to it (e.g. each track's reciprocal
  `isPartOf`).
- **Result:** [`operationalPoint-f317d4ae4b.rdf`](operationalPoint-f317d4ae4b.rdf) — RDF/XML, fetched
  2026-08-19 from `https://graph.data.era.europa.eu/repositories/rinf-plus`
  (confirmed byte-identical to the same query run against
  `https://rinf.data.era.europa.eu/api/v1/sparql/rinf`, ERA's other public
  RINF SPARQL endpoint — see the root [README](../README.md) for the CORS/GET-vs-POST
  differences between the two).
- **What it resolves to:** Paris-Gare-de-Lyon (`era:OperationalPoint`), a
  real major French station — 22 real `hasPart` tracks, 2 `primaryLocation`
  references, a `canonicalURI`, `opType`, and one incoming `sectionOfLine`
  link via `opStart`.

To re-run or adapt this query against a different resource, swap the URI in
`operationalPoint-f317d4ae4b-query.rq` and POST/GET it to either endpoint,
e.g.:

```bash
curl -sS -G "https://graph.data.era.europa.eu/repositories/rinf-plus" \
  --data-urlencode "query@operationalPoint-f317d4ae4b-query.rq" \
  -H "Accept: application/rdf+xml" -o result.rdf
```

## operationalPoint-f317d4ae4b-recursive

A deeper export of the same resource: not just its 1-hop neighbourhood, but
everything transitively reachable down to real leaf values (literals),
bounded to 5 hops.

- **Query:** [`operationalPoint-f317d4ae4b-recursive-query.rq`](operationalPoint-f317d4ae4b-recursive-query.rq)
- **Result:** [`operationalPoint-f317d4ae4b-recursive.rdf`](operationalPoint-f317d4ae4b-recursive.rdf) — RDF/XML,
  fetched 2026-08-19 from `graph.data.era.europa.eu/repositories/rinf-plus`,
  475 `rdf:Description` blocks / ~2,700 triples, runs in ~6s.

A plain "follow every edge, arbitrarily deep" recursive query doesn't work on
this graph — two real problems were found and fixed while building this one
(full rationale is in the query file's header comment, since it's the kind
of thing a future re-run needs to know about, not just this README):

1. **Cycles.** `era:hasPart`/`era:isPartOf` is bidirectional — operational
   point → track → back to the operational point — so an unguarded
   traversal regenerates the entire starting node's properties at every
   subsequent hop and never settles. Fixed with "don't revisit a node
   already seen on this path" guards.
2. **Ontology/vocabulary bleed.** The moment traversal lands on a class,
   property, or SHACL shape (reached via `rdf:type`, `rdfs:isDefinedBy`,
   `skos:inScheme`, or even a legitimate `era:notApplicable` value that
   happens to *be* a property URI), continuing to follow its properties
   pulls in thousands of unrelated ontology/SHACL/legal-citation triples.
   Fixed by blocking recursion through the standard vocabulary namespaces
   plus a few era:-specific administrative predicates, **and** a
   structural guard that never recurses into a node asserted
   `a owl:Class`/`rdf:Property`/`sh:NodeShape`/`sh:PropertyShape`,
   regardless of which predicate led there.

Depth 5 was chosen empirically — tested at depths 2 through 5 against this
exact URI; deep enough to reach genuine literal leaves on every real branch,
without ballooning (an earlier *unguarded* attempt at depth 5 didn't finish
in 90 seconds and was still pulling in SHACL/ELI ontology metadata when
killed). Reverse (incoming) edges are only followed one hop, at the root —
recursing backwards would reintroduce the same explosion problem, since some
resources in this graph have tens of thousands of incoming edges (see the
`era-graph-explorer-app.html` dataset's own reuse-hub notes for concrete
examples).
