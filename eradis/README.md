# ERADIS-KG query set

The SPARQL behind [era-eradis-explorer.html](../scripts/assets/era-eradis-explorer.html)
(deployed as `/eradis.html`): a search over the EC declarations of verification,
conformity and suitability for use, laid out like the ERADIS search form.

Endpoint: `https://graph.dev.data.test-era.europa.eu/repositories/ERADIS-KG`
(development server; the production repository asks for a login).
Legal acts: `https://graph.dev.data.test-era.europa.eu/repositories/era-lex`.

| File | Runs against | What it does |
|---|---|---|
| `ecd-search.rq` | ERADIS-KG | one search from the form, with the field → property mapping in its header |
| `ecd-detail.rq` | ERADIS-KG | the full record of one declaration: versions, certificates, restrictions, signatories, technical file, published files |
| `snapshot-declarations.rq` | ERADIS-KG | snapshot part 1: one row per published declaration |
| `snapshot-links.rq` | ERADIS-KG | snapshot part 2: notified bodies, constituents, TSIs, directives, certificates |
| `snapshot-organisations.rq` | ERADIS-KG | snapshot part 3: organisation name, country, registration/VAT, NANDO code |
| `snapshot-references.rq` | ERADIS-KG | snapshot part 4: the TSIs and directives cited |
| `snapshot-versions.rq` | ERADIS-KG | snapshot part 5: versions per document |
| `snapshot-lex.rq` | era-lex | ELI, English title, in-force status and `eli:changes` of every act cited |

`python3 scripts/build-eradis-snapshot.py` runs the snapshot queries and writes
`scripts/assets/era-eradis-snapshot.json.gz` (22,256 declarations, ~2 MB).

## Why a snapshot

The dev endpoint answers `curl`, but sends no `Access-Control-Allow-Origin` at all.
A page served from GitHub Pages therefore cannot read its answers: the request
reaches the server, and the browser then withholds the response. The page
searches the snapshot instead, and generates the **same search as SPARQL** for
every submission. "Run live on ERADIS-KG" sends it directly and reports the CORS
block when there is one; "Open in GraphDB workbench" opens the query pre-filled
in the workbench (`/sparql?repositoryId=ERADIS-KG&query=…`).

The snapshot and the SPARQL were checked against each other on 2026-09-30 for 27
form combinations. They return identical sets of Document IDs wherever the live
query stays under its 500-row limit. The snapshot holds **no signatory names**
(personal data) and no contact details, so the two signatory fields only work live.

## Scope

- **Published declarations only**: `GRAPH <http://data.europa.eu/949/graph/eradis>`.
  `…/eradis/ec-declaration/draft/graph` holds 979 unpublished submissions.
- **Current version of each document**: `FILTER NOT EXISTS { ?d dct:isReplacedBy ?newer }`.
  Every amendment is a new resource sharing `dct:identifier`.
- **Published states**: in force, amended, revoked and suspended. Rejected
  declarations (9,841 current versions) are not part of the public register.
- **Organisation data lives in a separate graph**
  (`…/eradis/organisation/graph`). Pinning the whole query to the declaration
  graph silently returns no names and no countries. Only the declaration triple
  is pinned.

## Mapping the ERADIS form onto the graph

| Form field | ERADIS-KG |
|---|---|
| Document ID number | `dct:identifier` (`CC/registration/year/sequence`) |
| Applicant | `dct:creator` → `era:roleOf` |
| Applicant country | `org:hasSite/org:siteAddress/locn:adminUnitL1` of that organisation |
| Applicant national registration no. | embedded in the Document ID (zero-padded); `gr:legalNumber`/`gr:vatID` is recorded for only 383 of 903 applicants |
| Authorised representative | `dct:contributor` whose role is `organisation-roles/Manufacturer`, checked against ERADIS pages 13438 and 15513 |
| Type of subsystem | **not in ERADIS-KG**, derived as described below |
| Certificate of conformity ID | `dct:relation/rdfs:member` in `…/evidence/cld/cld-NoBoCert/`, `rdfs:label` |
| To EC Directives / To TSIs | `dct:source` / `eli:id_local` |
| Signatories | `prov:wasAttributedTo` → `foaf:givenName` / `foaf:familyName` |
| Date of issue | `dct:issued` (`xsd:date`) |

## "Type of subsystem", derived through era-lex

ERADIS shows the subsystem on its pages ("Control command and signalling"), but
ERADIS-KG has no property for it. The explorer derives it from the TSIs a
declaration cites (`eli:id_local`), resolving each act in **era-lex**:

1. **Find the ELI.** ERADIS-KG names acts `…/949/legislation/requirements/reg_impl-2019-776`.
   For 15 of the 71 acts it records an `owl:sameAs` ELI; the rest are built from
   the key. The key's type is not always right: `dir-402-2013` is Implementing
   Regulation 402/2013, and `dir-2015-1136` is Implementing Regulation 2015/1136.
   All 71 resolve.
2. **Pick the right one of a numbered pair.** 2006/66, 2007/153, 2009/107, 2010/79
   and 2012/88 exist in era-lex only as `…/dec/YYYY/N(1)/oj` and `(2)/oj`.
   The `(2)` is an EEA Joint Committee decision (`eli:based_on` treaty/EEA),
   so the `(1)` is used. ERADIS-KG's `owl:sameAs` points at the unsuffixed URI,
   which does not exist in era-lex.
3. **Base TSI: read the subsystem from its title.** The English title is on
   `eli:is_realized_by` → the ENG expression → `eli:title`. The titles contain
   non-breaking spaces, which are normalised before matching.
4. **Amending or correcting act: follow `eli:changes`.** The act takes the
   subsystem of the acts it changes, when they all belong to one subsystem.
   - 2012/696 → 2012/88 → CCS;
   - 2019/774 → 1304/2014 → rolling stock;
   - 2020/420 (a German-language correction of 2016/919) → CCS.

   An act that amends several subsystems gets none (2019/776, 2020/387,
   2023/1694, 2018/868). When the acts changed are not TSIs, the act's own title
   decides: 2012/757 is the OPE TSI and also amends Decision 2007/756.
5. **Map onto Directive (EU) 2016/797 Annex II.** The locomotive, wagon and noise
   TSIs are all rolling stock. The PRM and tunnel-safety TSIs span several
   subsystems and name none; they stay searchable through "To TSIs".

Result: 16,985 declarations with one subsystem, 1,099 with several (mostly
whole-train declarations of verification citing both rolling-stock and CCS
on-board TSIs), and 4,172 with none.

## Data observations

- `dct:type` (ECDoV / ECDoC / ECDoSU) and the `evidence-document-states`
  concepts carry **no `skos:prefLabel`** in ERADIS-KG; the labels are the explorer's.
- 11 declarations have a `dct:issued` date **after** 2026-09-30, e.g.
  `RO/J1992001591124/2026/000001` issued 2026-10-14.
- One NoBo certificate node, shared by 15 current declarations, is labelled
  `deleted`. It is a tombstone rather than a certificate ID, so the snapshot drops it.
- Country codes: one applicant address uses `…/country/BH`, which is not an
  ISO 3166 alpha-3 code.
