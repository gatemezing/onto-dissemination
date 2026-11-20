# CRD knowledge graph — review against the ERA ontology, ERA SHACL shapes and RINF

**Reviewed endpoint:** <https://rinf-ris-alignment.com/repositories/CRD>
(dataset `https://rinf-ris-alignment.com/graph/crd`, `dct:modified` 2026-11-20T01:01:52Z, generated from
the CRD snapshot of 2026-11-20T01:00:05Z)
**Reference data:** <https://graph.data.era.europa.eu/repositories/rinf-plus> (RINF)
**Reference model:** ERA ontology v3.3.4 and ERA SHACL shapes, PROD (`ERA-Onto`, `graph/shacl`) and UAT
(`https://rinf.uat.data.test-era.europa.eu/era-vocabulary/era-shapes`)
**Measured:** 2026-11-20, a re-run of the 2026-11-03 review. Every number below comes from a query in
[queries/](queries/) or from a script in [scripts/](scripts/) run over the extracts. Nothing is inferred
from the ontology alone.

---

## 1. Summary

The CRD graph replicates RNE's Common Reference Data every day: TAF/TAP **primary locations**
(PLC) and **subsidiary locations** (SLC). It uses only ERA v3.3.4 terms, and every term it uses
exists, undeprecated, in the PROD ontology. Its PLC structure is cleaner than RINF's: one IRI per
code, every location named in English, flagged, dated and attributed to an IM, and a valid code
pattern throughout. On the 44,443 PLCs found in both sources, country and IM agree 100 %, the
four TAF/TAP flags ≥ 99 %, names 98 % and positions (≤ 1 km) 98 %. Against ERA's own SHACL shapes,
CRD conforms better than RINF: under PROD only the NUTS vocabulary check (F10) fails, plus a geometry
Warning for the 7,315 PLs that have no coordinates (§3.3).

### What changed since 3 November

The publisher re-published the graph and acted on most of the review: five findings are resolved
(F1, F2, F4, F6, F9), one partly (F11), and F3 changed form.

| # | Finding (2026-11-03) | Status on 2026-11-20 |
|---|---|---|
| F1 | Allocation companies all typed with the IM role | **Resolved.** 33 of the 34 companies now carry a role OCR-KG lists for them. UIC is typed `SB` "Sector Organisation"; OCR-KG says `IRO`, a code ERA's role vocabulary does not define |
| F2 | Great Britain PLCs at `POINT(0 0)` | **Resolved.** The 7,315 PLs without coordinates now carry no geometry |
| F3 | SL types from the UAT scheme | **Changed, still MAJOR.** The six UAT-only codes are no longer typed at all: 20,020 SLs (26.1 %) have no `subsidiaryLocationType` |
| F4 | SL properties outside UAT's closed shape | **Resolved.** No SL carries `inCountry`, `infrastructureManager` or `operatingLanguage` |
| F5 | Danish codes identify different places (RINF side) | Unchanged: 294 of 302 shared DK codes are > 10 km apart |
| F6 | Ontology terms re-declared in the data graphs | **Resolved.** The data graphs hold none; a separate `graph/era/used-terms` lists the 37 terms used, as `rdf:type` statements only |
| F7 | `wgs84:lat`/`lon` as plain strings | Unchanged (51,942 net references) |
| F8 | Python `None` in IRIs | Unchanged (2,269 temporal features, 51,371 applicabilities) |
| F9 | Whitespace runs in names | **Resolved** (0 names) |
| F10 | NUTS IRIs differ by source | Unchanged in CRD; RINF itself now uses both forms |
| F11 | Suggestions: provenance, SKOS, IRI governance | **Partly resolved.** The metadata now names RailNetEurope as publisher and links the CRD snapshot with its generation time, and the SKOS graph is PROD's (70,705 triples). Still missing: a licence |

RINF changed too. **DB InfraGO's 9,618 PLs in RINF are now stubs** (type, label, country, code and
geometry only); on 3 November 9,166 of them carried names, flags, IMs and validity copied from CRD. Across
RINF, the share of PL codes with a name fell from 51.8 % to 40.5 %, with an IM from 43.3 % to 31.5 %, and
with the TAF/TAP flags from 42–44 % to 25–26 %. CRD is now the only linked-data source of names, flags and
IMs for German PLCs.

What still needs fixing before the graph can stand next to RINF:

| # | Severity | Finding | Affected |
|---|---|---|---|
| F3 | **MAJOR** | SL type codes `01`, `02`, `03`, `10`, `15` and `27` exist only in the **UAT** `SubsidiaryLocationTypes` scheme. CRD now drops the type instead of asserting it: the code survives only inside the SL's IRI (`…/subsidiaryLocation/CZ54100_5412_01_0054`). No SHACL shape notices: neither PROD nor UAT requires a type | 20,020 SLs (26.1 %), 99 % of them in CZ, SK and HR |
| F5 | **MAJOR** (RINF side) | Danish codes identify **different places** in RINF and CRD. RINF/Banedanmark gives `DK00010` to Høje Taastrup, which CRD codes `DK00005` | 294 of 302 shared DK codes are > 10 km apart |
| F7 | MINOR | `wgs84:lat`/`lon` are plain strings on `era:NetBasicReference`, which duplicates the WKT and puts the WGS84 vocabulary on a non-spatial-thing | 51,942 net references |
| F8 | MINOR | IRIs leak Python's `None` (`temporalFeature/20170701_None`, `parameterApplicability/…_None`) | 2,269 temporal features, 51,371 applicabilities |
| F10 | MINOR | `era:inNUTS3` IRIs differ by source. CRD uses `http://data.europa.eu/nuts/code/…`, as ERA's `graph/nuts` and now Greece's RINF do. Austria's RINF uses `https://publications.europa.eu/resource/authority/nuts/…`, the scheme the ontology names, which has no `skos:inScheme` members in ERA-Onto | 9,456 CRD PLs |
| F11 | SUGGESTION | IRIs are minted under ERA's own namespace `http://data.europa.eu/949/…` by a third-party publisher, and the metadata states no licence | IRI governance |
| F12 | SUGGESTION | UIC's allocation role: CRD says `SB` (in ERA's vocabulary), OCR-KG says `IRO` (not in it). One of the two registers should align | 18,435 SLs |

What the comparison with RINF shows:

* **Coverage.** CRD holds 59,257 PLCs, RINF 48,824 (in 52,331 IRIs). 44,443 are in both.
  14,814 are in CRD only: GB 7,312, DE 2,036, FR 962, PT 825, PL 685, RS 682, …. 4,381 are in RINF only:
  DE 1,935, CH 922, IT 307, PL 271, NO 269, DK 216, EU 91, ….
* **4,356 PLCs that RINF operational points reference are absent from CRD**, mostly DB InfraGO (1,934) and
  the Swiss graphs 0085 + 3915 (905). [stats/rinf-op-pl-missing-from-crd.csv](stats/rinf-op-pl-missing-from-crd.csv) lists them.
* **RINF is partly CRD-derived.** ProRail's 780 PLs carry this pipeline's IRI fingerprints, so §4.3 reports
  them apart. Italy's RFI (2,845 shared codes) and Luxembourg's CFL (141) now agree with CRD on every field,
  validity dates included, with their own IRIs: most likely loaded from CRD as well, but counted as
  independent here because they carry no fingerprint.
* **Validity start dates disagree** on 47 % of the independent overlap. FR agrees on 30.8 %; HR, LT and NO
  on 0–3 %. Most likely the two sources date different events: CRD's start date often reaches back to the
  19th century (e.g. `1874-01-01` in GR), while RINF's follows the RINF publication or the opening. This is
  an interpretation, not checked with the publishers.
* **Subsidiary locations do not overlap.** RINF has 3,899 SLs, all Bane NOR, all modelling *tracks*
  (`NO-S.n`, "Atna spor 1"). CRD has 76,786, the RNE SLC catalogue. Not one (PLC, SLC) pair is shared.

---

## 2. Inventory

| | CRD | RINF (rinf-plus) |
|---|---|---|
| Statements | 2,593,035 | — |
| Named graphs | `crd/primary-locations` 1,689,525 · `crd/subsidiary-locations` 817,760 · `era/skos` 70,705 · `era/ontology` 14,974 · `era/used-terms` 46 · `crd/metadata` 25 | one per IM (63 hold PLs) |
| `era:PrimaryLocation` | 59,257 IRIs = 59,257 codes | 52,331 IRIs → 48,824 codes (167 codes with > 1 IRI; 3,400 codes in > 1 IM graph) |
| `era:SubsidiaryLocation` | 76,786 | 3,899 (`graph/0076`, Bane NOR only) |
| PL IRI pattern | `http://data.europa.eu/949/primaryLocation/{PLC}` | same for 40,700; plus `…/functionalInfrastructure/primaryLocations/[AT/{IM}/]{PLC}` (6,317), `https://data.banenor.no/…` (717), `…/PrimaryLocation_{PLC}` (582), hashed IRIs (143) |
| Same IRI for the same code | 36,676 of the 44,443 shared codes | |
| Ontology | v3.3.4, identical to PROD (see §3.1) | v3.3.4 |

Metadata (`graph/crd/metadata`) describes the dataset in VoID/DCAT: `dct:title`, `dct:description`,
`dct:conformsTo` (`http://data.europa.eu/949/` and the v3.3.4 release), `dct:publisher` RailNetEurope,
`void:subset`, `void:triples`, `void:entities` and `void:class`. Since 2026-11-20 it also links a
`prov:Entity` "Snapshot of the RNE Common Reference Data (CRD)" through `prov:wasDerivedFrom`, with its
`prov:generatedAtTime`. It has no licence (see F11).

### CRD primary locations per country (code prefix)

[stats/pl-by-country.csv](stats/pl-by-country.csv). Here `inCountry` always equals the code prefix.

| Prefix | CRD | RINF | Both | CRD only | RINF only | Share of CRD found in RINF |
|---|---:|---:|---:|---:|---:|---:|
| DE | 9,720 | 9,619 | 7,684 | 2,036 | 1,935 | 79.1 % |
| FR | 9,036 | 8,074 | 8,074 | 962 | 0 | 89.4 % |
| GB | 7,312 | 0 | 0 | 7,312 | 0 | — |
| PL | 4,625 | 4,211 | 3,940 | 685 | 271 | 85.2 % |
| CZ | 3,717 | 3,616 | 3,612 | 105 | 4 | 97.2 % |
| IT | 2,993 | 3,272 | 2,965 | 28 | 307 | 99.1 % |
| AT | 2,712 | 2,647 | 2,624 | 88 | 23 | 96.8 % |
| CH | 2,688 | 3,309 | 2,387 | 301 | 922 | 88.8 % |
| ES | 2,506 | 2,282 | 2,226 | 280 | 56 | 88.8 % |
| RO | 2,331 | 2,174 | 2,140 | 191 | 34 | 91.8 % |
| HU | 1,930 | 1,836 | 1,738 | 192 | 98 | 90.1 % |
| BE | 1,371 | 1,325 | 1,324 | 47 | 1 | 96.6 % |
| SE | 1,337 | 1,103 | 1,102 | 235 | 1 | 82.4 % |
| SK | 1,157 | 1,040 | 1,036 | 121 | 4 | 89.5 % |
| PT | 825 | 0 | 0 | 825 | 0 | — |
| NL | 780 | 780 | 780 | 0 | 0 | 100 % |
| RS | 682 | 0 | 0 | 682 | 0 | — |
| DK | 594 | 518 | 302 | 292 | 216 | 50.8 % |
| HR | 572 | 565 | 552 | 20 | 13 | 96.5 % |
| FI | 540 | 436 | 362 | 178 | 74 | 67.0 % |
| NO | 462 | 717 | 448 | 14 | 269 | 97.0 % |
| BG | 323 | 314 | 297 | 26 | 17 | 92.0 % |
| SI | 300 | 309 | 296 | 4 | 13 | 98.7 % |
| GR | 218 | 211 | 187 | 31 | 24 | 85.8 % |
| LT | 210 | 201 | 199 | 11 | 2 | 94.8 % |
| LU | 141 | 143 | 141 | 0 | 2 | 100 % |
| LV | 102 | 27 | 23 | 79 | 4 | 22.5 % |
| EE | 69 | 0 | 0 | 69 | 0 | — |
| EU | 0 | 91 | 0 | 0 | 91 | — |
| LI | 4 | 4 | 4 | 0 | 0 | 100 % |

GB and RS fall outside RINF's scope. **PT and EE are EU Member States whose RINF publishes no
`era:PrimaryLocation` at all**, so CRD is the only linked-data source of PLCs for them. Germany's overlap
fell from 9,170 to 7,684 codes: DB InfraGO's RINF graph now holds 9,619 PLCs, against 11,105 on 3 November.

### CRD subsidiary locations

76,786 SLs in 28 countries, counted by the country of the linked PL (since 2026-11-20 SLs carry no
`era:inCountry` of their own, F4): CZE 18,669, FRA 16,609, DEU 14,747, SVK 6,278, AUT 5,197, CHE 4,915,
BEL 2,568, … ([stats/sl-by-country-type.csv](stats/sl-by-country-type.csv)). Every SL links to a PL
present in CRD (0 dangling), and 71,934 of those PLs are also in RINF. 12,819 (16.7 %) carry a geometry.
Since 3 November, 2,150 SLs were added and 1,281 removed.

| Type (`subsidiary-location-types/…`) | SLs | In PROD scheme | In UAT scheme |
|---|---:|:---:|:---:|
| 37 Loading point | 21,783 | ✓ | ✓ |
| **no type** (was 01, 15, 03, 10, 27, 02 — F3) | 20,020 | | |
| 41 Company specific identifier | 18,570 | ✓ | ✓ |
| 42 DIUM | 12,101 | ✓ | ✓ |
| 04 Sorting code | 1,969 | ✓ | ✓ |
| 36 Freight yard | 1,336 | ✓ | ✓ |
| 57 Intermodal terminal | 488 | ✓ | ✓ |
| 70 Network border | 414 | ✓ | ✓ |
| 06 Public loading places | 83 | ✓ | ✓ |
| 47, 60, 48, 54, 46, 99 | 22 | ✓ | ✓ |

The allocation companies number 34 ([§5 F1](#f1--allocation-company-roles)), checked against OCR-KG in
[stats/allocation-company-roles.csv](stats/allocation-company-roles.csv). UIC (3011) has allocated
18,435 SLs. For 36,154 SLs the allocation company is not the PL's IM.

---

## 3. Conformance with the ERA ontology and SHACL shapes

### 3.1 Ontology

* **Vocabulary.** All the classes and properties the data uses are declared in ERA PROD v3.3.4,
  none deprecated, with the expected domains and ranges: `era:PrimaryLocation`, `era:SubsidiaryLocation`,
  `primaryLocationCode/Name`, `subsidiaryLocationCode/Name/Type`, `linkedToPrimaryLocation`,
  `allocationCompany`, the four flags, `inNUTS3`, `ParameterApplicability`, and so on.
  The CRD data uses no `era:tafTAPCode`, deprecated or otherwise.
* **CRD's copy of the ontology** (`graph/era/ontology`, 14,974 triples) is graph-isomorphic to PROD's
  `graph/ontology` once CRLF line endings are normalised. 296 multi-line literals use `\r\n` where PROD
  uses `\n`. This is harmless, but it makes a naive diff report 296 changes.
* **`ParameterApplicability`** is modelled correctly. The class is `rdfs:subClassOf era:TemporalFeature`,
  so `time:hasBeginning` directly on it is right. Of 54,532 applicabilities, none contradicts the flag it
  qualifies, and no PL holds two conflicting applicabilities for the same flag. RINF's CRD-derived graph
  (ProRail) models it identically.
* **Used terms (F6, resolved).** On 3 November the two data graphs re-declared 37 ERA terms with their
  labels, comments, `rdfs:subClassOf` and `owl:disjointWith`, and an `owl:Ontology` for
  `http://data.europa.eu/949/`. They now hold data only. The new `graph/era/used-terms` (46 triples) lists
  the 37 terms the data uses (7 classes, 14 object, 10 datatype and 5 annotation properties, and the
  ontology), typed and nothing else, so it adds no second copy of the axioms.

### 3.2 SHACL — what the location shapes require

| Shape | PROD | UAT |
|---|---|---|
| `PrimaryLocationShape` | open; code `^[A-Z]{2}[0-9]{5}$` 1..1; name `rdf:langString` uniqueLang + `@en` if present; flags `xsd:boolean` ≤ 1; `inNUTS3` ≤ 1 (Warning); `primaryLocation` forbidden | **`sh:closed`**; adds name ≥ 1, `validity` ≥ 1 (`TemporalFeature`), `isPrimaryLocationOf` and at most one OP, geometry via `netReference/hasGeometry` ≥ 1 (Warning) |
| `SubsidiaryLocationShape` | open; code `xsd:string` 1–10 chars ≤ 1; name langString uniqueLang + `@en`; `linkedToPrimaryLocation` `sh:class PrimaryLocation`; `allocationCompany` `sh:class OrganisationRole`; type IRI + `SubsidiaryLocationTypeSKOS`, **optional** (no `sh:minCount`) | **`sh:closed`**, allowing only: allocationCompany, linkedToPrimaryLocation, subsidiaryLocationCode/Name/Type, validity, notApplicable, notYetAvailable, `geo:hasGeometry`, `rdf:type`, `rdfs:label` |

Shapes as downloaded on 2026-11-20: PROD 7,569 triples, 76 node shapes (unchanged since 2026-10-20);
UAT 15,200 triples, 161 node shapes (156 on 2026-10-20). One UAT change matters below: `HasTopoCoordinate`
no longer requires exactly one `era:hasTopoCoordinate` on a `NetPointReference`; it now only checks its class.

### 3.3 SHACL — results

pyshacl 0.40.2 (rdflib 7.6.0) ran over a deterministic sample from each source and reported only the
sampled resources and the nodes they reach. The data graph was the sample plus ERA PROD's ontology, its
SKOS vocabulary, its NUTS concepts and rinf-plus `graph/rinf/countries`. The CRD sample held 3,000 PLs,
3,000 SLs and the 62 bodies they reach; the RINF sample held 3,000 PLs and all 3,899 SLs. Each run took
10–14 minutes. The aggregated reports are in [data/shacl/](data/shacl/). Figures in brackets are
those of 3 November.

**CRD, PROD shapes: one constraint fails, one Warning is new.**

| Constraint | Resources in sample | Full dataset (§3.5) |
|---|---:|---:|
| `InNUTS3SKOS`: NUTS concept not in `inSkosConceptScheme` (F10) | 485 / 3,000 PLs (486) | every PL with `inNUTS3`: 9,456 (16.0 %) |
| `NetReferenceGeometryAsWKT` (Warning): no WKT via `netReference/hasGeometry` | 375 / 3,000 PLs (0) | 7,315: GBR 7,312, DEU, FRA, CZE 1 each (F2) |
| `SubsidiaryLocationTypeSKOS`: type not in the scheme (F3) | 0 (772 / 3,000 SLs) | 0 (19,990) |

Every other PROD constraint that targets these resources passes on the sample: codes, names, flags,
`allocationCompany`, `linkedToPrimaryLocation`, validity, the `TemporalFeature`/`Instant` chain, IM roles
and countries. `InNUTS3SKOS` is meant as a Warning, but ERA puts `sh:severity` on the
`sh:SPARQLConstraint` node, which SHACL ignores, so it reports as a Violation (§3.4). **The 20,020 SLs
without a type (F3) pass every shape**: `subsidiaryLocationType` has no `sh:minCount` in PROD or UAT, so
dropping the types cleared F3's violations without a single new one.

**CRD, UAT shapes: the closed-shape failure is gone.**

| Constraint | Resources in sample | Full dataset |
|---|---:|---:|
| `InSkosConceptScheme`: NUTS (F10) | 485 PLs (486) | 9,456 |
| `HasSite`: `era:Body` without `org:hasSite` | 62 bodies (65) | all 98 bodies (97) |
| `PrimaryLocationNetReferenceGeometry` (Warning) | 375 PLs (0) | 7,315 |
| `NetReferenceGeometryAsWKT` (Warning) | 375 PLs (0) | 7,315 |
| `SubsidiaryLocationShape` `sh:closed`: `inCountry` / `infrastructureManager` / `operatingLanguage` (F4) | 0 (3,000 / 2,999 / 3,000 SLs) | 0 (75,917 / 75,838 / 75,913) |
| `InSkosConceptScheme`: SL type (F3) | 0 (772 SLs) | 0 (19,990) |

CRD's PLs pass UAT's closed `PrimaryLocationShape` and its new `validity` and `primaryLocationName`
minimums. The only PL results are the two geometry Warnings on the 7,315 PLs without coordinates, which is
exactly what fixing F2 was meant to produce: a Warning instead of a fake point. The `HasSite` finding comes
from CRD minting bodies that carry only `organisationCode` and `role`. OCR-KG holds the sites, so either
link to OCR-KG's body IRIs or omit the `era:Body` typing.

**RINF sample, for comparison.** The same shapes fire far more on RINF. The main groups, with their
`focus_nodes` counts (3 November in brackets):

| | PROD | UAT |
|---|---|---|
| PL with no geometry reachable via `netReference` (Warning) | 872 / 3,000 (852) | 872 / 3,000 (852) |
| PL without `primaryLocationName` and `validity` (new UAT minimum) | — | **1,666 / 3,000, 55 %** (1,322) |
| `NetPointReference` with `wgs84:lat`/`long` (outside UAT closed shape) | — | **2,001** (1,290) |
| `GeometryShape` closed: `wgs84:lat`/`lon` | — | 153 (151) |
| `NetPointReference` without `hasTopoCoordinate` | — | 0 (1,297): UAT dropped the minimum (§3.2); live, 175,794 of 324,968 RINF `NetPointReference`s still have none |
| NUTS3 not in the declared scheme (F10) | 19 PLs (18) | 19 PLs (18) |
| Bodies: `roleOf` max 1, `rdfs:label` uniqueLang, `hasSite` | 3 + 1 | 24 (22, counted slightly differently) |
| RINF subsidiary locations (Bane NOR) | 0 | 0 |

So, measured with ERA's own shapes, **CRD's location data remains more conformant than RINF's PL data**.
Under PROD it fails one vocabulary-alignment constraint, plus a Warning for PLs without coordinates. RINF
has 8 result groups, and more PLs without name and validity than on 3 November, mostly since DB InfraGO's
PLs became stubs (§4.2).

> **Sampling artifacts, filtered since 2026-11-06.** `sh:class` results whose value sits at the last hop
> of the sample are false positives, because `queries/sample-rinf.rq` does not copy that value's
> `rdf:type`. `scripts/validate.py` drops them: 0 on CRD, and 409 (PROD) / 410 (UAT) on RINF, all for
> `era:kmPost`, `era:hasTopoCoordinate`, a body's `era:role` and `era:inNUTS3`. Checked live over all of
> rinf-plus on 2026-11-20, **no such value lacks its expected type**. The CSVs in `data/shacl/` were
> regenerated with this filter (those of 3 November still contained the artifacts).
>
> What Bane NOR does differently with km posts is a modelling choice the shapes do not check. All 732
> of its `era:KilometricPost`s hang on one nationwide LPS (`_lps02`, "Landsomfattende LPS", no
> `era:lineId`) as an integer grid from km −2 to 729. None of its 35 line LPSs carries a post. Its
> 24,045 coordinates reference the *nearest* post, with offsets from −500 to +500 m (49.7 % negative).
> Every other large publisher references the preceding post on a line LPS.

### 3.4 Notes for ERA's shape maintainers (found while running the shapes)

These are defects or portability problems in ERA's shapes, independent of CRD:

* **PROD `LangStringEnRequired` and `LangStringEnRequiredIfPresent` are invalid SPARQL** once `$PATH` is
  substituted: `SELECT $this $PATH` projects an IRI. UAT already reads `SELECT $this`. Any engine that
  substitutes `$PATH` textually (as SHACL-SPARQL specifies) fails on every `primaryLocationName`,
  `subsidiaryLocationName`, `opName`, ….
* **The ontology header declares both `geo:` and `geosparql:`** for the GeoSPARQL namespace. rdflib-based
  validators (pyshacl) bind one prefix per namespace, so queries using the other prefix stop resolving.
  Keep one.
* **ERA's constraints use `VALUES`, `MINUS` and nested `SELECT`.** SHACL 1.0's pre-binding rules (§5.3.1)
  forbid these, and pyshacl rejects them by default. They run on ERA's own engine, but third parties
  must relax their validator to reproduce ERA's results.
* **17 UAT constraints use `SERVICE`** (federated ERADIS/CLD checks) and cannot run on a local copy.
* **`era:inNUTS3` points at a scheme with no members** (F10). ERA's own `graph/nuts` concepts would
  fail `InNUTS3SKOS` too.
* **`subsidiaryLocationType` is optional in both PROD and UAT.** A publisher can drop every type, as CRD
  did for 20,020 SLs (F3), without a single result. If the type is meant to be there, add `sh:minCount 1`.
* **UAT relaxed `HasTopoCoordinate`** between 3 and 20 November: it no longer requires one
  `era:hasTopoCoordinate` per `NetPointReference`. 175,794 of RINF's 324,968 `NetPointReference`s have
  none, so the relaxation removes ~1,300 results from the RINF sample without any data change. If the
  minimum is meant for the release, restore it; if not, say so in the release notes.
* **Severity on SPARQL constraints is ignored.** Several constraints (`InNUTS3SKOS` among them) carry
  `sh:severity sh:Warning` on the `sh:SPARQLConstraint` node. SHACL defines `sh:severity` on shapes, so
  conforming engines report these as Violations. Move the severity to a dedicated shape.

### 3.5 Exact full-dataset checks

[queries/crd-checks.rq](queries/crd-checks.rq), result in [stats/crd-checks.csv](stats/crd-checks.csv).
Each check counts distinct resources over the whole CRD graph; a check that matches nothing returns no
row, shown here as 0.

| Check | 2026-11-03 | 2026-11-20 |
|---|---:|---:|
| PL code not matching `^[A-Z]{2}[0-9]{5}$` | 0 | 0 |
| PL or SL with two names in one language (`sh:uniqueLang`) | 0 | 0 |
| PL without an `@en` name | 0 | 0 |
| PL flag not `xsd:boolean`, or > 1 value | 0 | 0 |
| SL code not a 1–10-character `xsd:string` | 0 | 0 |
| SL `linkedToPrimaryLocation` not resolving to a PL in CRD | 0 | 0 |
| ParameterApplicability contradicting its flag | 0 | 0 |
| validity without `time:hasBeginning` | 0 | 0 |
| PL geometry `POINT(0 0)` (F2) | **7,315** | 0 |
| SL type not in the `SubsidiaryLocationTypes` scheme (F3) | **19,990** | 0 |
| SL without any `subsidiaryLocationType` (F3) | 0 | **20,020** |
| SL with `inCountry`, `infrastructureManager` or `operatingLanguage` (F4) | **75,917** | 0 |
| SL without geometry (allowed: no `minCount`) | 63,650 | 63,967 |
| `NetBasicReference` with `wgs84:lat` as a plain string (F7) | 59,155 | 51,942 |
| `TemporalFeature` IRI containing `None` (F8) | 2,235 | 2,269 |
| ERA ontology terms re-declared in the data graphs (F6) | 37 | 0 |

The "without any type" count comes from [stats/summary.json](stats/summary.json)
(`sl.crd_type_distribution`); the query's "no infrastructureManager / operatingLanguage" rows now match
every SL by design (F4).

---

## 4. Comparison with RINF

### 4.1 Property completeness (per code)

[stats/pl-completeness.csv](stats/pl-completeness.csv)

| Property | CRD | RINF | RINF, on shared codes | RINF on 2026-11-03 |
|---|---:|---:|---:|---:|
| `inCountry` | 100 % | 98.4 % | 98.3 % | 98.4 % |
| `infrastructureManager` | 100 % | 31.5 % | 33.9 % | 43.3 % |
| `primaryLocationName` | 100 % (all with `@en`) | 40.5 % | 43.7 % | 51.8 % |
| passenger / freight / container / handover flags | 100 % | 25–26 % | 27–28 % | 42–44 % |
| position (non-zero WKT) | 87.7 % | 82.1 % | 82.8 % | 82.6 % |
| `validity` | 100 % | 40.5 % | 43.7 % | 51.8 % |
| validity end | 12.7 % | 23.7 % | 25.9 % | 23.0 % |
| `inNUTS3` | 16.0 % | 0.6 % | 0.6 % | 0.6 % |

Here CRD is the richer source, and more so since DB InfraGO's PLs became stubs. Many RINF IMs publish the
PL as a stub: code, label and geometry only. CRD can fill the IM, the names and the TAF/TAP flags for
those PLs.

### 4.2 Which RINF graphs are CRD-derived

[queries/pl-provenance.rq](queries/pl-provenance.rq) →
[stats/rinf-pl-provenance-by-graph.csv](stats/rinf-pl-provenance-by-graph.csv). A RINF graph counts as
CRD-derived when its PLs carry this pipeline's IRIs: `temporalFeature/YYYYMMDD_None` and
`parameterApplicability/{PLC}_{flag}_{date}_None`. [scripts/compare.py](scripts/compare.py) reads the
list from that query rather than hard-coding it.

| RINF graph | PLs | CRD-style validity | With ParameterApplicability | 2026-11-03 |
|---|---:|---:|---:|---|
| `0084` ProRail | 780 | 780 | 636 | 780 / 780 / 636 |
| `0080` DB InfraGO | 9,618 | 0 | 0 | 11,104 / 9,166 / 9,003 |
| all other 61 graphs | 45,326 | 0 | 0 | |

DB InfraGO's PLs now carry `rdf:type`, `rdfs:label`, `era:inCountry`, `era:primaryLocationCode` and
`era:netReference`, and nothing else. **Italy (`0083` RFI, 2,845 shared codes) and Luxembourg (`0082` CFL,
141)** agree with CRD on every field, validity start included (Luxembourg agreed on 0 % of validity starts on
3 November), with validity IRIs of their own (`temporalFeature/0b326374d1`). They are most likely loaded
from CRD too, but they carry no fingerprint, so they stay in the "independent" column below.

### 4.3 Value agreement on the 44,443 shared codes

Multi-valued RINF fields count as agreeing when CRD's value is among them. The "independent" column
excludes the 780 codes published only in the CRD-derived graph (`0084`).
[stats/pl-agreement-by-prefix.csv](stats/pl-agreement-by-prefix.csv) breaks this down per country, and
[stats/pl-value-differences.csv](stats/pl-value-differences.csv) lists the disagreeing values.

| Field | Comparable (all) | Agree (all) | Comparable (independent) | Agree (independent) |
|---|---:|---:|---:|---:|
| country | 43,692 | 100 % | 42,912 | 100 % |
| IM organisation code | 15,062 | 100 % | 14,282 | 100 % (1 differs: `3487` → `0081`) |
| passengerFlag | 12,512 | 99.0 % | 11,732 | 99.0 % (73 true→false, 48 false→true) |
| freightFlag | 12,090 | 99.8 % | 11,310 | 99.8 % |
| containerHandlingFlag | 12,085 | 100 % | 11,305 | 99.9 % |
| handoverPointFlag | 12,089 | 99.9 % | 11,309 | 99.9 % |
| name (accent/case/punctuation-insensitive) | 19,428 | 97.6 % | 18,648 | 97.5 % |
| position within 1 km | 36,789 | 97.6 % | 36,009 | 97.6 % |
| validity begin | 15,588 | 55.7 % | 14,808 | **53.3 %** |
| NUTS3 code | 13 | 100 % | 13 | 100 %, but under different IRIs (F10) |

* **Names.** Most mismatches are in GR (7.5 % agree), where RINF prefixes the name with the code number
  (`954-DILOFO`). That is a RINF naming convention, not a different place.
* **Positions.** Median distance 2 m, p90 178 m, p99 3.7 km. 871 codes are > 1 km apart, 307 > 10 km and
  183 > 100 km ([stats/pl-distance-outliers.csv](stats/pl-distance-outliers.csv)). 294 of the 307 > 10 km
  are Danish (F5). The rest look like single-record typos on one side, still uncorrected: DK00459 Hirtshals
  in CRD at `POINT(9.96 7.59)` (apparently 57.59 typed as 7.59), GR00757, PL08950 and FR08334, among others.
* **Validity.** Agreement is 100 % in the derived NL graph and in IT and LU, and 95.3 % in AT, but 30.8 % in
  FR and 0–3 % in HR, LT and NO. The likely reading is that the two sources date different events. CRD's
  start dates reach back to `1874-01-01`, while RINF's follow the RINF record or the opening. This was not
  checked with the publishers. Either way, anyone merging the two must keep both windows apart rather
  than overwrite one with the other.

### 4.4 Operational points → primary locations

RINF links operational points to PLs with `era:primaryLocation`. 47,031 PL IRIs (47,029 codes) are
referenced this way, and 6,844 of them by more than one OP. Every referenced IRI is typed
`era:PrimaryLocation` and has a code.

* **42,673 referenced codes exist in CRD.** CRD can enrich those OPs with names, flags and IMs by code.
* **4,356 referenced codes are missing from CRD**: DB InfraGO (0080) 1,934; SBB Infrastructure +
  Schweizerische Trassenvergabestelle (0085 + 3915) 905; PKP PLK (0051) 306; Bane NOR (0076) 269;
  Banedanmark (0086) 218; FER (3525) 123; …. They are either retired from CRD after RINF was loaded or never
  allocated. Each row of [stats/rinf-op-pl-missing-from-crd.csv](stats/rinf-op-pl-missing-from-crd.csv)
  gives its uopid, so the IMs can check.
* **Denmark (F5)** is a different case: the codes match, but not what they identify.

### 4.5 Subsidiary locations

| | CRD | RINF |
|---|---|---|
| SLs | 76,786 in 28 countries | 3,899, NOR only |
| Code | RNE SLC (`53414`, `BMZD`, `0076700001`) | Bane NOR track id (`NO-S.1`) |
| `subsidiaryLocationType` | 73.9 % (F3) | 0 % |
| Geometry | 16.7 % (`POINT`) | 99 % (`LINESTRING`: the track) |
| `allocationCompany` | 34 companies, roles as in OCR-KG but one (F1) | 0076 |
| Shared (PLC, SLC) pairs | 0 | 0 |

Bane NOR uses `era:SubsidiaryLocation` for **tracks within a station**, while the class is defined
for the TAF/TAP SLC catalogue (loading points, DIUM codes and so on). For Norway the two sources cannot
be reconciled by code.

---

## 5. Findings in detail

### F1 — Allocation company roles

**Resolved on 2026-11-20 · verified.** On 3 November every `era:allocationCompany` pointed at an
`…/organisationRole/{code}_IM` role, so the graph asserted that UIC, DB Cargo and nine other non-IMs were
infrastructure managers (30,059 SLs). The role now follows the company: 23 companies are `IM`, 9 are
`RU-3` (freight railway undertaking: Rail Cargo Austria, DB Cargo, ČD Cargo, SBB Cargo, UIRR, …), Rail&Sea
is `Keeper` and UIC is `SB`. [scripts/allocation_roles.py](scripts/allocation_roles.py) checks each against
OCR-KG ([stats/allocation-company-roles.csv](stats/allocation-company-roles.csv)): 33 of the 34 hold that
role there. The exception is UIC (18,435 SLs), which OCR-KG lists only as `IRO`. ERA's
`organisation-roles` vocabulary has no `IRO` concept, while `SB` ("Sector Organisation") is in it, so
CRD's choice is the one ERA's vocabulary supports. The mismatch is OCR-KG's (F12).

### F2 — Great Britain at null island

**Resolved on 2026-11-20 · verified.** On 3 November all 7,312 GB PLs, plus DE, FR and CZ one each, had
`geo:asWKT "POINT(0 0)"`. They now have no `netReference` geometry at all, which UAT reports as the intended
`PrimaryLocationNetReferenceGeometry` warning rather than drawing them in the Gulf of Guinea.

### F3 — Subsidiary-location types from UAT

**MAJOR · verified, changed on 2026-11-20.** On 3 November 19,990 SLs used type codes 01, 15, 03, 10, 27
and 02, which exist in the UAT `SubsidiaryLocationTypes` scheme (50 codes) but not in PROD's (37 codes).
CRD now loads PROD's SKOS as-is, and **drops the type** for those SLs instead: every one of the 19,965
still present lost its `era:subsidiaryLocationType`, and the 55 new SLs with those codes arrived untyped.
20,020 SLs (26.1 %) now have no type: CZ 12,926, SK 5,155, HR 1,633, others 306. The RNE code still
shows in the IRI (`…/subsidiaryLocation/{PLC}_{SLC}_01_{company}`), so the information exists but is no
longer data. PROD's vocabulary check passes, at the price of a quarter of the types.
*Fix:* assert the type and load the UAT `SubsidiaryLocationTypes` scheme (or the six concepts) with it,
or validate against UAT throughout, and state the choice in the dataset metadata. Dropping data to pass a
shape is the wrong trade.

### F4 — SL properties outside the UAT closed shape

**Resolved on 2026-11-20 · verified.** UAT closes `SubsidiaryLocationShape`. On 3 November every SL
carried `era:inCountry`, `era:infrastructureManager` and `era:operatingLanguage`, which it does not allow.
None does now. The country, the IM and the language can be read from the linked PL; this review now derives
an SL's country that way.

### F5 — Danish codes identify different places

**MAJOR, on the RINF side · verified for samples, unchanged.** For 294 of the 302 shared DK codes the CRD
and RINF positions are > 10 km apart. For 236 of them, CRD's position of code X lies within 100 m of
RINF's position of another Danish code Y (235 on 3 November, counted the same way). Example: RINF's OP
`uopid DK00010` "Høje Taastrup" sits at `POINT(12.269823 55.648536)`, which is CRD's `DK00005` Høje
Taastrup. CRD's `DK00010` is Borup, 25 km away. RINF's Danish PLs have no names, so name matching cannot
catch this. The uopids Banedanmark uses in RINF are not the RNE PLCs, yet RINF links them as
`era:primaryLocation`. Report this to Banedanmark and ERA, and do not join DK on code until it is fixed.

### F6 – F9

* **F6 resolved** — the data graphs no longer re-declare ontology terms (§3.1).
* **F7 unchanged** — `era:NetBasicReference` carries `wgs84:lat`/`lon` as untyped strings next to a typed
  `geo:wktLiteral` (51,942 references), and the geometry node is typed `wgs84:Point` with no lat/long of its
  own. Drop the WGS84 triples; ERA reads positions through `netReference/geo:hasGeometry/geo:asWKT`.
* **F8 unchanged** — `None` in IRIs (`temporalFeature/20170701_None`, `…_freight_19800101_None`): 2,269
  temporal features and 51,371 of the 54,532 applicabilities. Apparently a Python `None` serialised into
  the IRI. Stable but unattractive, and it makes "no end date" look like a value. The same IRIs exist in
  RINF's ProRail graph, so renaming them breaks alignment. Change them only together with ERA.
* **F9 resolved** — no PL or SL name carries a whitespace run any more (236 + 377 on 3 November).

### F10 — NUTS IRIs

**MINOR, partly on the ERA side · verified.** The ontology says `era:inNUTS3 era:inSkosConceptScheme
<https://publications.europa.eu/resource/authority/nuts>`. ERA-Onto holds no concept `skos:inScheme`
that scheme, and its `graph/nuts` (910,907 triples) uses `http://data.europa.eu/nuts/code/{code}`.
CRD follows `graph/nuts` (9,456 PLs). RINF now uses both forms: Greece's OSE (`0073`, 212 PLs) the same
form as CRD, and the Austrian publishers (88 PLs) the Publications Office IRIs. On the 13 PLs where CRD
and RINF both carry a value, the codes agree but the IRIs do not, so a join on the IRI returns nothing.
As written, PROD's `InNUTS3SKOS` (Warning) fires for every value in either form, unless the scheme
memberships are loaded. ERA should pick one IRI form; CRD and RINF should follow it.

### F11 — suggestions

* **IRI governance.** All CRD resources are minted under `http://data.europa.eu/949/` (ERA's namespace)
  by a publisher at `rinf-ris-alignment.com`. For PLs this is deliberate and useful: 36,676 shared codes
  have the same IRI in RINF, so the two graphs join without `owl:sameAs`. It also means CRD triples
  merge silently with ERA's own. Agree the pattern with ERA, or mint under a CRD namespace and link
  with `owl:sameAs`/`skos:exactMatch`.
* **Provenance — mostly done.** The metadata now has `dct:publisher` (RailNetEurope) and a
  `prov:wasDerivedFrom` snapshot with its `prov:generatedAtTime`, so each run says which CRD snapshot it is.
  Add `dct:license`.
* **SKOS — done.** `graph/era/skos` is now PROD's vocabulary (70,705 triples, the size of ERA-Onto's
  `graph/skos`), without the 293 UAT schemes it carried on 3 November. That is what turned F3 into dropped
  types.
* **Validity.** CRD shows only currently valid codes: no end date before 2026-11-20 and no future start.
  The 1,935 DE codes in RINF but not in CRD suggest CRD drops retired codes. If so, keep them with a
  closed validity window, so RINF's references to retired codes stay resolvable.

### F12 — UIC's role differs between CRD and OCR-KG

**SUGGESTION.** CRD types UIC's allocation role `SB` ("Sector Organisation"); OCR-KG gives UIC the role
`IRO`, which ERA's `organisation-roles` vocabulary does not define. Either OCR-KG should use a defined
concept or ERA should add `IRO`; CRD should then follow OCR-KG. 18,435 SLs are affected.

---

## 6. Method, reproducibility and limits

```text
crd-kg/
├── README.md               this report
├── queries/                every SPARQL query used (run against both endpoints unless noted)
│   ├── pl-*.rq             one field per query, joined locally (avoids RINF's 120 s limit)
│   ├── pl-provenance.rq    which graphs carry this pipeline's IRIs (§4.2)
│   ├── sl.rq               subsidiary locations
│   ├── crd-checks.rq       exact full-dataset data-quality checks
│   └── sample-*.rq         deterministic SHACL samples (ORDER BY MD5(IRI))
├── scripts/
│   ├── sparql.py           minimal SPARQL client (stdlib only)
│   ├── fetch.py            runs queries/*.rq → data/raw/{crd,rinf}/*.csv (git-ignored, ~80 MB)
│   ├── compare.py          joins on primaryLocationCode → stats/
│   ├── allocation_roles.py F1: CRD allocation roles against OCR-KG → stats/allocation-company-roles.csv
│   └── validate.py         pyshacl over a sample + ERA ontology + ERA SKOS → data/shacl/
├── stats/                  every table in this report, as CSV, plus summary.json
└── data/shacl/             aggregated SHACL results per dataset × shape set
```

```bash
python3 -I scripts/fetch.py                # ~1 min, both endpoints (the two sample-*.rq need Turtle: see SHACL)
python3 -I scripts/compare.py 2026-11-20   # as-of date for validity checks
python3 -I scripts/allocation_roles.py     # F1, CRD against OCR-KG
cp data/raw/crd/crd-checks.csv stats/      # §3.5
# SHACL (needs: pip install pyshacl). Inputs, all CONSTRUCTed or downloaded as described in §3.3:
#   SAMPLE   = queries/sample-crd.rq | queries/sample-rinf.rq        (Accept: text/turtle)
#   SHAPES   = ERA-Onto graph/shacl (PROD) | UAT era-shapes file
#   REFS     = ERA-Onto graph/ontology, graph/skos, graph/nuts (concepts only), rinf-plus graph/rinf/countries
python -I scripts/validate.py SAMPLE.ttl SHAPES.ttl OUT.csv REF1.ttl REF2.ttl …
```

Limits:

* **Join key.** The comparison joins on `era:primaryLocationCode`. Where a code means different things on
  each side (F5), agreement statistics are meaningless for that country.
* **RINF validity.** RINF is taken as published, without per-place validity deduplication. DE republishes
  yearly, hence the 167 codes with several IRIs and the 3,400 codes in several IM graphs. Fields count as
  agreeing when CRD matches any RINF variant, which flatters RINF slightly.
* **Independence.** Only IRI fingerprints mark a RINF graph as CRD-derived. IT and LU agree on every field
  without them (§4.2), so the "independent" figures may still include copies of CRD.
* **SHACL scope.** Validation (pyshacl 0.40.2, rdflib 7.6.0) ran on a 3,000 + 3,000 sample, extrapolated with the exact full-dataset
  counts in §3.5 wherever a constraint fired. Constraints that need a remote endpoint (`SERVICE`) were
  skipped, and pyshacl's SHACL 1.0 pre-binding restrictions were relaxed so ERA's `VALUES`/`MINUS`
  queries run as GraphDB runs them.
* **OCR-KG.** F1 and F12 rely on OCR-KG's role list as of 2026-11-20.
* **History.** The 3 November figures quoted for comparison are those of the first review (git history of
  this file and of `stats/`).
