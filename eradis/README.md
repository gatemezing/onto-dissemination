# ERADIS-KG query set

The SPARQL behind [era-eradis-explorer.html](../scripts/assets/era-eradis-explorer.html)
(deployed as `/eradis.html`). It searches two ERADIS registers, each laid out
like its ERADIS form, and links them to each other:

- the **EC declarations** of verification, conformity and suitability for use
  (`era:ECDeclaration`);
- the **NoBo certificates** they rest on (`era:CertificationLevelDocument`).
  `eradis.html#certificates` opens this register directly.

Endpoint: `https://graph.dev.data.test-era.europa.eu/repositories/ERADIS-KG`
(development server, open for anonymous reads; the production repository asks
for a login). Legal acts: `https://graph.dev.data.test-era.europa.eu/repositories/era-lex`.

| File | Runs against | What it does |
|---|---|---|
| `ecd-search.rq` | ERADIS-KG | one search from the form, with the field → property mapping in its header |
| `ecd-detail.rq` | ERADIS-KG | the full record of one declaration: versions, certificates, restrictions, derogations, signatories, technical file, published files |
| `cld-search.rq` | ERADIS-KG | one search from the certificate form, with the field → property mapping in its header |
| `cld-detail.rq` | ERADIS-KG | the full record of one certificate: versions, object of assessment, statements, conditions of use, published files, citing declarations |
| `snapshot-declarations.rq` | ERADIS-KG | snapshot part 1: one row per published declaration |
| `snapshot-links.rq` | ERADIS-KG | snapshot part 2: notified bodies, constituents, TSIs, directives, certificates |
| `snapshot-organisations.rq` | ERADIS-KG | snapshot part 3: organisation name, country, registration/VAT, NANDO code (declarations and certificates) |
| `snapshot-references.rq` | ERADIS-KG | snapshot part 4: the TSIs and directives declarations cite |
| `snapshot-versions.rq` | ERADIS-KG | snapshot part 5: versions per document |
| `snapshot-certificates.rq` | ERADIS-KG | certificate snapshot: one row per current certificate |
| `snapshot-certificate-links.rq` | ERADIS-KG | certificate snapshot: manufacturers, modules, recorded subsystem, the acts cited (four ways), constituents, earlier numbers, restrictions |
| `snapshot-certificate-versions.rq` | ERADIS-KG | certificate snapshot: every earlier version → its current version |
| `snapshot-lex.rq` | era-lex | ELI, English title, in-force status and `eli:changes` of every act cited |
| `snapshot-lex-ic.rq` | era-lex | name and TSI section of every interoperability constituent certificates cite |

`python3 scripts/build-eradis-snapshot.py` runs the snapshot queries (about a
minute) and writes two files:

- `scripts/assets/era-eradis-snapshot.json.gz`: 22,256 declarations plus the
  shared organisation, TSI and directive tables (~1.6 MB);
- `scripts/assets/era-eradis-certificates.json.gz`: 43,615 certificates and
  the 230 constituents they name (~3.3 MB), loaded only when the certificate
  tab is opened.

## Live and snapshot

The dev endpoint is open for anonymous reads and answers a page on any origin
(it returns the request's `Origin` in `Access-Control-Allow-Origin`; measured
2026-11-19). It was not always so: until October 2026 it sent no CORS headers,
and from 2026-10-12 it asked for a login. The page therefore searches a
snapshot built by the same queries, generates the **same search as SPARQL**
for every submission, and runs it live on request: "Run live on ERADIS-KG"
sends it, and the full record of a declaration or certificate is always read
live. "Open in GraphDB workbench" opens the query pre-filled in the workbench
(`/sparql?repositoryId=ERADIS-KG&query=…`). When the endpoint fails, the page
says why and the snapshot still works.

"Run live" returns every match. It sends the match alone (bare URIs), then the
displayed fields for 1,000 documents at a time, 6 in flight, as TSV. Each
field is its own UNION branch, so multi-valued fields never multiply before
the GROUP BY - the cross product that made a single query take 88 s for 500
certificates. Organisation names are resolved through the snapshot's
organisation table, because some organisations carry several `foaf:name` or
NANDO codes; constituent names through its constituent table (they are in
era-lex, not ERADIS-KG). The snapshot holds **no signatory names** (personal
data) and no contact details, so the two signatory fields only work live.

**Checked 2026-11-19**, after ERA reloaded ERADIS-KG: 5 declaration searches
and 12 certificate searches return the same documents live and from the
snapshot, and the same values field by field - all 43,615 certificates
included (live in ~14 s).

## Scope

- **Published declarations only**: `GRAPH <http://data.europa.eu/949/graph/eradis>`.
  `…/eradis/ec-declaration/draft/graph` holds 979 unpublished submissions.
  `…/eradis/ec-declaration/confidential/graph` holds 5,844
  `era:ConfidentialInformation` documents (`…/ecd/confidential/N`); no
  declaration links to them, and nothing here reads that graph.
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
| Type of subsystem | **not recorded on declarations**, derived as described below |
| Certificate of conformity ID | `dct:relation/rdfs:member` → an `era:CertificationLevelDocument`, `dct:identifier`. Not `rdfs:label`, which most certificates lack. |
| To EC Directives / To TSIs | `dct:source` / `eli:id_local` |
| Signatories | `prov:wasAttributedTo` → `foaf:givenName` / `foaf:familyName`, leaving out the ERADIS account that submitted the declaration (see below) |
| Restrictions recorded | `vpa:checkedCompliance/vpa:withRestriction` → `era:nonCodedRestrictions` (directly `vpa:withRestriction` before the reload) |
| Date of issue | `dct:issued` (`xsd:date`) |

**Signatories and accounts.** Since the November 2026 reload every published
declaration is also attributed to the ERADIS account that submitted it
(`…/person/eradis-user/N`, 1,343 people, with `foaf:accountName`, `foaf:mbox`
and often `foaf:phone`). The signatories are separate resources
(`…/person/sig/…`, on 16,900 declarations), and only 3,854 of those carry the
submitter's name. The signatory search and the full record therefore leave out
any person with a `foaf:accountName`.

## "Type of subsystem" of a declaration, derived through era-lex

ERADIS shows the subsystem on its pages ("Control command and signalling"), but
ERADIS-KG records none for declarations. The explorer derives it from the TSIs a
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

Result (2026-11-19): 16,954 declarations with one subsystem, 1,073 with
several (mostly whole-train declarations of verification citing both
rolling-stock and CCS on-board TSIs), and 4,229 with none.

## NoBo certificates (`era:CertificationLevelDocument`)

The certificate form follows the ERADIS certificate page: general information,
TSIs and constituents, applicant, manufacturer, NoBo, dates. The field mapping
is in the header of `cld-search.rq`.

ERA reloaded the certificates in November 2026, and their model changed:

- **URIs**: `…/evidence/cld/N`, no longer `…/evidence/cld/cld-NoBoCert/N`. The
  number `N` is the same certificate (checked on 40 samples), and is still the
  ERADIS page id.
- **Subsystem is recorded**: `dct:subject` → `concepts/subsystems/…`
  (42,496 certificates), in a finer scheme than Annex II: on-board and
  trackside CCS, freight wagons and locomotives/passenger stock. The explorer
  maps it onto the Annex II subsystems; a certificate can record several (PRM
  certificates name infrastructure and rolling stock). It is no longer derived.
- **Acts are no longer `eli:id_local`.** A certificate cites an act four ways,
  and the explorer reduces each to the act's year and number:
  - the TSI part checked: `vpa:checkedCompliance/vpa:checkedRequirement` →
    `…/requirements/reg/2013/321/WAG`, or a consolidated version
    `…/reg/2014/1302/2019-06-16/LOCPAS` (42,496 certificates);
  - `dct:source` → `…/requirements/dir/2016/797`, the directive, and on some
    certificates TSI regulations too (`reg/2014/1304`, `reg_impl/2023/1694`);
  - `dct:references` → `…/celex/32019R0776`, the amending acts (25,197);
  - **a note**, when the act is not in era-lex: `skos:note "Legislation
    reference not in era-lex: '2008/57/EC' (32008L0057)"` (12,398
    certificates). Directive 2008/57/EC (7,539 certificates), 2019/774 and
    Directive 2020/700 are only recorded this way, so the explorer reads the
    CELEX number out of the note.

  Every certificate keeps the TSIs it had before the reload; 10,048 gain one,
  the TSI of the constituent they name. 2025/675 and 2025/2064 are cited but
  not in era-lex.
- **Constituents are TSI subdivisions**: `dct:subject` →
  `…/requirements/reg/2013/321/WAG/3`. ERADIS-KG has no name for it; era-lex
  does (`eli:title "Wheel"`, `eli:number "5.3.3"`), and all 230 cited resolve.
  Where the loader could not place a constituent in a TSI it left a blank node
  with `eli:title` (885 certificates). 10,119 certificates name a constituent.
- **Restrictions**: `vpa:checkedCompliance/vpa:withRestriction/era:nonCodedRestrictions`
  (24,605 certificates; `rdfs:comment` before).
- **Numbers**: ~1,600 certificates now carry two or three spellings in
  `dct:identifier` - the number as typed (`N°3017/6/SD/…`, `1960_1_SB_…`,
  three numbers run together) plus a cleaned copy. The explorer shows one: a
  spelling that contains another whole goes, then plain ASCII without spaces,
  the NoBo/type/module/year structure, most slashes, shortest. All spellings
  stay searchable.
- **Published files**: `era:hasDocumentFile/era:documentUrl` (the certificate
  PDF on ERADIS), shown in the full record.
- 7 current certificates have no number and 50 no version number; 8,581
  record version 0.

Unchanged rules:

- **Scope.** The current version of each certificate in `graph/eradis`
  (43,615). Only unpublished drafts are dropped, i.e. certificates whose only
  state is "draft". 297 certificates are "submitted".
- **Validity is derived.** The recorded state is no guide: on 2026-11-19,
  17,081 of the 41,101 current certificates recorded as "inForce" were past the
  end of their validity window (before the reload, 42,088 said "amended"). The
  explorer uses withdrawn and suspended as recorded, and otherwise the
  `dct:valid` window (`time:hasBeginning` / `time:hasEnd`) against today's
  date. On 2026-11-19 this gives 24,518 valid today, 17,724 expired, 713
  suspended, 656 withdrawn and 4 not yet valid. The SPARQL computes the same
  value with `NOW()`.
- **Dates of issue.** Each certificate records one `dct:issued` since the
  reload (1,631 recorded several before, sometimes the validity end). The
  explorer still picks the latest that is neither the validity end nor in the
  future, and the date filter matches any recorded date.
- **Versions and citations.** 1,833 of 34,034 declaration → certificate links
  point at an older version of the certificate. The replacement chains are not
  always closed, so a citation counts for every current certificate whose
  `dct:replaces*` chain reaches the cited version, exactly as in the SPARQL;
  1,710 citations reach two current certificates. 17,097 certificates are cited
  by at least one published declaration. The two registers link both ways.
- **Modules.** `dct:conformsTo` also points at Decision 2010/713 (the modules
  decision itself) on 4,844 certificates; it is not offered as a module.

## Data observations

- `dct:type` (ECDoV / ECDoC / ECDoSU) and the `evidence-document-states`
  concepts carry `skos:prefLabel`s since the reload ("EC declarations of
  verification of subsystems", "In force"); the explorer keeps its own shorter
  labels.
- Two acts certificates cite, 2025/675 and 2025/2064, are not in era-lex, so
  they have no title.
- Country codes: one applicant address uses `…/country/BH`, which is not an
  ISO 3166 alpha-3 code.
