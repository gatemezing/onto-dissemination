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
