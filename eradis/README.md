# ERADIS-KG query set

The SPARQL behind [era-eradis-explorer.html](../scripts/assets/era-eradis-explorer.html)
(deployed as `/eradis.html`). It searches two ERADIS registers, each laid out
like its ERADIS form, and links them to each other:

- the **EC declarations** of verification, conformity and suitability for use
  (`era:ECDeclaration`);
- the **NoBo certificates** they rest on (`era:CertificationLevelDocument`).
  `eradis.html#certificates` opens this register directly.

Endpoint: `https://graph.dev.data.test-era.europa.eu/repositories/ERADIS-KG`
(development server; the production repository asks for a login).
Legal acts: `https://graph.dev.data.test-era.europa.eu/repositories/era-lex`.

| File | Runs against | What it does |
|---|---|---|
| `ecd-search.rq` | ERADIS-KG | one search from the form, with the field → property mapping in its header |
| `ecd-detail.rq` | ERADIS-KG | the full record of one declaration: versions, certificates, restrictions, signatories, technical file, published files |
| `cld-search.rq` | ERADIS-KG | one search from the certificate form, with the field → property mapping in its header |
| `cld-detail.rq` | ERADIS-KG | the full record of one certificate: versions, object of assessment, statements, conditions of use, citing declarations |
| `snapshot-declarations.rq` | ERADIS-KG | snapshot part 1: one row per published declaration |
| `snapshot-links.rq` | ERADIS-KG | snapshot part 2: notified bodies, constituents, TSIs, directives, certificates |
| `snapshot-organisations.rq` | ERADIS-KG | snapshot part 3: organisation name, country, registration/VAT, NANDO code (declarations and certificates) |
| `snapshot-references.rq` | ERADIS-KG | snapshot part 4: the TSIs and directives cited (declarations and certificates) |
| `snapshot-versions.rq` | ERADIS-KG | snapshot part 5: versions per document |
| `snapshot-certificates.rq` | ERADIS-KG | certificate snapshot: one row per current certificate |
| `snapshot-certificate-links.rq` | ERADIS-KG | certificate snapshot: manufacturers, modules, TSIs, directives, constituents, earlier numbers, restrictions |
| `snapshot-certificate-versions.rq` | ERADIS-KG | certificate snapshot: every earlier version → its current version |
| `snapshot-lex.rq` | era-lex | ELI, English title, in-force status and `eli:changes` of every act cited |

`python3 scripts/build-eradis-snapshot.py` runs the snapshot queries and writes two files:

- `scripts/assets/era-eradis-snapshot.json.gz`: 22,256 declarations plus the
  shared organisation, TSI and directive tables (~1.9 MB);
- `scripts/assets/era-eradis-certificates.json.gz`: 43,471 certificates
  (~3.7 MB), loaded only when the certificate tab is opened.

## Why a snapshot

The dev endpoint answers `curl`, but sends no `Access-Control-Allow-Origin` at all.
A page served from GitHub Pages therefore cannot read its answers: the request
reaches the server, and the browser then withholds the response. The page
searches the snapshot instead, and generates the **same search as SPARQL** for
every submission. "Run live on ERADIS-KG" sends it directly and reports the CORS
block when there is one; "Open in GraphDB workbench" opens the query pre-filled
in the workbench (`/sparql?repositoryId=ERADIS-KG&query=…`).

The snapshot and the SPARQL were checked against each other on 2026-09-30:
27 declaration searches and 14 certificate searches. They return identical sets
of Document IDs and certificates. Since 2026-10-01 "Run live" returns every
match, not the first 500: it sends the match alone (bare URIs; all 43,471
certificates in ~1.5 s), then the displayed fields for 1,000 documents at a
time, 6 in flight, as TSV. Each field is its own UNION branch, so multi-valued
fields never multiply before the GROUP BY - the cross product that made the old
single query take 88 s for 500 certificates and 112 s for all of them. Live and
snapshot rows were compared field by field on 7 searches (64,000+ rows) and
agree; organisation names are resolved through the snapshot's organisation
table, because some organisations carry several `foaf:name` or NANDO codes. The snapshot holds **no signatory names**
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
| Certificate of conformity ID | `dct:relation/rdfs:member` → an `era:CertificationLevelDocument`, `dct:identifier`. Not `rdfs:label`, which only 20,456 of the 47,908 certificates have. |
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

## NoBo certificates (`era:CertificationLevelDocument`)

The certificate form follows the ERADIS certificate page: general information,
TSIs and constituents, applicant, manufacturer, NoBo, dates. The field mapping
is in the header of `cld-search.rq`.

- **Scope.** The current version of each certificate in `graph/eradis`
  (43,471). Only unpublished drafts are dropped, i.e. certificates whose only
  state is "draft".
- **Validity is derived.** The recorded `era:state` says "amended" for 42,088
  current certificates and "inForce" for 12, so it can't answer "is this
  certificate valid?". The explorer uses:
  - withdrawn and suspended as recorded;
  - otherwise the `dct:valid` window (`time:hasBeginning` / `time:hasEnd`)
    against today's date.

  On 2026-09-30 this gives 24,998 valid today, 17,098 expired, 712 suspended,
  659 withdrawn and 4 not yet valid. The SPARQL computes the same value with
  `NOW()`.
- **Dates of issue.** 1,631 certificates carry several `dct:issued` values:
  - usually one of them equals the start of the validity window;
  - in 90 cases one equals its **end**, i.e. the validity end recorded as a
    date of issue;
  - a few are typos (3019 for 2019).

  The date shown is the latest one that is neither the validity end nor in the
  future. The date filter matches any recorded date, as the SPARQL's
  `FILTER EXISTS` does, and dates after the current year are kept out of the
  chart.
- **Versions and citations.** 5,681 of 82,082 declaration → certificate links
  point at an older version of the certificate. The replacement chains are not
  always closed: 3089 replaces 3091, yet 3091 has no `dct:isReplacedBy` and so
  also counts as current. A citation therefore counts for every current
  certificate whose `dct:replaces*` chain reaches the cited version, exactly as
  in the SPARQL. 1,530 citations reach two current certificates.

  16,076 certificates are cited by at least one published declaration. The two
  registers link both ways: a declaration's certificates, and a certificate's
  citing declarations.
- **Modules.** `dct:conformsTo` also points at Decision 2010/713 (the modules
  decision itself) on 5,337 certificates; it is not offered as a module.
- **Subsystem**, derived from the certificate's TSIs as for declarations: one
  subsystem for 27,359 certificates, several for 3,404, none for 12,708.

## Data observations

- `dct:type` (ECDoV / ECDoC / ECDoSU) and the `evidence-document-states`
  concepts carry **no `skos:prefLabel`** in ERADIS-KG; the labels are the explorer's.
- 11 declarations have a `dct:issued` date **after** 2026-09-30, e.g.
  `RO/J1992001591124/2026/000001` issued 2026-10-14.
- One NoBo certificate node, shared by 15 current declarations, is labelled
  `deleted`. It is a tombstone rather than a certificate ID, so the snapshot drops it.
- Country codes: one applicant address uses `…/country/BH`, which is not an
  ISO 3166 alpha-3 code.
