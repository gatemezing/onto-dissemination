# CRD knowledge graph — review against the ERA ontology, ERA SHACL shapes and RINF

**Reviewed endpoint:** <https://rinf-ris-alignment.com/repositories/CRD>
(dataset `https://rinf-ris-alignment.com/graph/crd`, `dct:modified` 2026-11-03T13:14:58Z)
**Reference data:** <https://graph.data.era.europa.eu/repositories/rinf-plus> (RINF)
**Reference model:** ERA ontology v3.3.4 and ERA SHACL shapes, PROD (`ERA-Onto`, `graph/shacl`) and UAT
(`https://rinf.uat.data.test-era.europa.eu/era-vocabulary/era-shapes`)
**Measured:** 2026-11-03. Every number below comes from a query in [queries/](queries/) or from
[scripts/compare.py](scripts/compare.py) run over the extracts. Nothing is inferred from the ontology alone.

---

## 1. Summary

The CRD graph replicates RNE's Common Reference Data every day: TAF/TAP **primary locations**
(PLC) and **subsidiary locations** (SLC). It uses only ERA v3.3.4 terms, and every term it uses
exists, undeprecated, in the PROD ontology. Its PLC structure is cleaner than RINF's: one IRI per
code, every location named in English, flagged, dated and attributed to an IM, and a valid code
pattern throughout. On the 45,733 PLCs found in both sources, country and IM agree 100 %, the
four TAF/TAP flags ≥ 99 %, names 98 % and positions (≤ 1 km) 98 %. Against ERA's own SHACL shapes,
CRD conforms better than RINF: under PROD only two vocabulary-alignment constraints fire (§3.3).

What needs fixing before the graph can stand next to RINF:

| # | Severity | Finding | Affected |
|---|---|---|---|
| F1 | **MAJOR** | Allocation companies are all typed with the **IM** role, including UIC, freight RUs and others that OCR-KG does not list as IMs | 30,059 SLs (39.6 %) |
| F2 | **MAJOR** | All Great Britain PLCs sit at `POINT(0 0)` ("null island") rather than having no geometry | 7,312 PLs (+3 elsewhere) |
| F3 | **MAJOR** | SL type codes `01`, `02`, `03`, `10`, `15` and `27` exist only in the **UAT** SKOS scheme. CRD's own SKOS graph and PROD lack them, so PROD's `SubsidiaryLocationTypeSKOS` fails | 19,990 SLs (26 %) |
| F4 | **MAJOR** (UAT) | Every SL carries `era:inCountry`, `era:infrastructureManager` and `era:operatingLanguage`, which UAT's `sh:closed` `SubsidiaryLocationShape` does not allow | 75,917 SLs (100 %) |
| F5 | **MAJOR** (RINF side) | Danish codes identify **different places** in RINF and CRD. RINF/Banedanmark gives `DK00010` to Høje Taastrup, which CRD codes `DK00005` | 289 of 297 shared DK codes are > 10 km apart |
| F6 | MINOR | The data graphs re-declare 37 ERA ontology terms, including an `owl:Ontology` for `http://data.europa.eu/949/` | both data graphs |
| F7 | MINOR | `wgs84:lat`/`lon` are plain strings on `era:NetBasicReference`, which duplicates the WKT and puts the WGS84 vocabulary on a non-spatial-thing | 59,155 net references |
| F8 | MINOR | IRIs leak Python's `None` (`temporalFeature/20170701_None`, `parameterApplicability/…_None`) | 2,235 temporal features, 54,572 applicabilities |
| F9 | MINOR | 236 PL and 377 SL names carry fixed-width whitespace runs (`"Cottbus-Merzdorf                Süd-Nord"`) | 613 names |
| F10 | MINOR | `era:inNUTS3` IRIs differ by source. CRD uses `http://data.europa.eu/nuts/code/…`, as ERA's `graph/nuts` does. RINF (AT) uses `https://publications.europa.eu/resource/authority/nuts/…`, the scheme the ontology names, which has no `skos:inScheme` members in ERA-Onto | 9,425 PLs |
| F11 | SUGGESTION | IRIs are minted under ERA's own namespace `http://data.europa.eu/949/…` by a third-party publisher. The CRD SKOS graph also adds 293 UAT schemes to the PROD vocabulary | IRI governance |

What the comparison with RINF shows:

* **Coverage.** CRD holds 59,155 PLCs, RINF 50,172 (in 53,679 IRIs). 45,733 are in both.
  13,422 are in CRD only: GB 7,312, FR 962, PT 825, PL 685, RS 682, DE 550, …. 4,439 are in RINF only:
  DE 1,935, CH 922, IT 362, PL 271, NO 269, DK 221, EU 91, ….
* **4,413 PLCs that RINF operational points reference are absent from CRD**, mostly DB InfraGO (1,934) and
  the Swiss graphs 0085 + 3915 (905). [stats/rinf-op-pl-missing-from-crd.csv](stats/rinf-op-pl-missing-from-crd.csv) lists them.
* **RINF is already partly CRD-derived.** 9,166 of DB InfraGO's 11,104 RINF PLs and all 780 of ProRail's
  carry this pipeline's IRI fingerprints. Agreement there (100 % on every field) is not independent evidence,
  so §4.3 reports it separately.
* **Validity start dates disagree** on 59 % of the independent overlap. FR agrees on 30.8 %; HR, LT, LU and NO on
  0–3 %. Most likely the two sources date different events: CRD's start date often reaches back to the 19th century (e.g. `1874-01-01` in GR), while RINF's follows the RINF publication or the opening. This is an interpretation, not checked with the publishers.
* **Subsidiary locations do not overlap.** RINF has 3,899 SLs, all Bane NOR, all modelling *tracks*
  (`NO-S.n`, "Atna spor 1"). CRD has 75,917, the RNE SLC catalogue. Not one (PLC, SLC) pair is shared.

---

## 2. Inventory

| | CRD | RINF (rinf-plus) |
|---|---|---|
| Statements | 2,940,942 | — |
| Named graphs | `crd/primary-locations` 1,767,521 · `crd/subsidiary-locations` 1,067,261 · `era/skos` 91,169 · `era/ontology` 14,974 · `crd/metadata` 17 | one per IM (47 hold PLs) |
| `era:PrimaryLocation` | 59,155 IRIs = 59,155 codes | 53,679 IRIs → 50,172 codes (167 codes with > 1 IRI; 3,332 codes in > 1 IM graph) |
| `era:SubsidiaryLocation` | 75,917 | 3,899 (`graph/0076`, Bane NOR only) |
| PL IRI pattern | `http://data.europa.eu/949/primaryLocation/{PLC}` | same for 42,330; plus `…/functionalInfrastructure/primaryLocations/{PLC}`, `…/PrimaryLocation/57-PL-…`, `https://data.banenor.no/…` |
| Same IRI for the same code | 38,105 of the 45,733 shared codes | |
| Ontology | v3.3.4, identical to PROD (see §3.1) | v3.3.4 |

Metadata (`graph/crd/metadata`) describes the dataset in VoID/DCAT: `dct:title`, `dct:description`,
`dct:conformsTo <http://data.europa.eu/949/>`, `void:subset`, `void:triples`, `void:entities`,
`void:class`. It has no licence, publisher or `prov:wasDerivedFrom` pointing at RNE CRD (see F11).

### CRD primary locations per country (code prefix)

[stats/pl-by-country.csv](stats/pl-by-country.csv). Here `inCountry` always equals the code prefix.

| Prefix | CRD | RINF | Both | CRD only | RINF only | Share of CRD found in RINF |
|---|---:|---:|---:|---:|---:|---:|
| DE | 9,720 | 11,105 | 9,170 | 550 | 1,935 | 94.3 % |
| FR | 9,036 | 8,074 | 8,074 | 962 | 0 | 89.4 % |
| GB | 7,312 | 0 | 0 | 7,312 | 0 | — |
| PL | 4,625 | 4,211 | 3,940 | 685 | 271 | 85.2 % |
| CZ | 3,717 | 3,477 | 3,474 | 243 | 3 | 93.5 % |
| IT | 2,937 | 3,273 | 2,911 | 26 | 362 | 99.1 % |
| CH | 2,688 | 3,309 | 2,387 | 301 | 922 | 88.8 % |
| AT | 2,681 | 2,647 | 2,624 | 57 | 23 | 97.9 % |
| ES | 2,506 | 2,282 | 2,226 | 280 | 56 | 88.8 % |
| RO | 2,331 | 2,174 | 2,140 | 191 | 34 | 91.8 % |
| HU | 1,931 | 1,836 | 1,739 | 192 | 97 | 90.1 % |
| BE | 1,371 | 1,325 | 1,324 | 47 | 1 | 96.6 % |
| SE | 1,336 | 1,103 | 1,103 | 233 | 0 | 82.6 % |
| SK | 1,157 | 1,040 | 1,036 | 121 | 4 | 89.5 % |
| PT | 825 | 0 | 0 | 825 | 0 | — |
| NL | 780 | 780 | 780 | 0 | 0 | 100 % |
| RS | 682 | 0 | 0 | 682 | 0 | — |
| DK | 580 | 518 | 297 | 283 | 221 | 51.2 % |
| HR | 572 | 565 | 552 | 20 | 13 | 96.5 % |
| FI | 540 | 436 | 362 | 178 | 74 | 67.0 % |
| NO | 462 | 717 | 448 | 14 | 269 | 97.0 % |
| BG | 323 | 314 | 297 | 26 | 17 | 92.0 % |
| SI | 300 | 309 | 296 | 4 | 13 | 98.7 % |
| GR | 218 | 211 | 187 | 31 | 24 | 85.8 % |
| LT | 210 | 201 | 199 | 11 | 2 | 94.8 % |
| LU | 140 | 143 | 140 | 0 | 3 | 100 % |
| LV | 102 | 27 | 23 | 79 | 4 | 22.5 % |
| EE | 69 | 0 | 0 | 69 | 0 | — |
| EU | 0 | 91 | 0 | 0 | 91 | — |
| LI | 4 | 4 | 4 | 0 | 0 | 100 % |

GB and RS fall outside RINF's scope. **PT and EE are EU Member States whose RINF publishes no
`era:PrimaryLocation` at all**, so CRD is the only linked-data source of PLCs for them.

### CRD subsidiary locations

75,917 SLs in 28 countries: CZE 19,030, FRA 16,602, DEU 14,705, SVK 6,289, AUT 5,083, CHE 3,884, BEL 2,543, …
([stats/sl-by-country-type.csv](stats/sl-by-country-type.csv)). Every SL links to a PL present in CRD
(0 dangling), and 72,500 of those PLs are also in RINF. 12,267 (16 %) carry a geometry.

| Type (`subsidiary-location-types/…`) | SLs | In PROD scheme | In UAT scheme |
|---|---:|:---:|:---:|
| 37 Loading point | 20,768 | ✓ | ✓ |
| **01** | 19,051 | ✗ | ✓ |
| 41 Company specific identifier | 18,570 | ✓ | ✓ |
| 42 DIUM | 12,275 | ✓ | ✓ |
| 04 Sorting code | 1,969 | ✓ | ✓ |
| 36 Freight yard | 1,338 | ✓ | ✓ |
| **15** | 598 | ✗ | ✓ |
| 57 Intermodal terminal | 488 | ✓ | ✓ |
| 70 Network border | 414 | ✓ | ✓ |
| **03** | 327 | ✗ | ✓ |
| 06 Public loading places | 83 | ✓ | ✓ |
| **10**, **27**, **02** | 11 + 2 + 1 | ✗ | ✓ |
| 47, 60, 48, 54, 46, 99 | 22 | ✓ | ✓ |

The allocation companies number 34 ([§5 F1](#f1--allocation-companies-typed-as-infrastructure-managers)).
UIC (3011) has allocated 17,559 SLs. For 35,285 SLs the allocation company is not the PL's IM.

---

## 3. Conformance with the ERA ontology and SHACL shapes

### 3.1 Ontology

* **Vocabulary.** All 8 classes and 29 properties the data uses are declared in ERA PROD v3.3.4,
  none deprecated, with the expected domains and ranges: `era:PrimaryLocation`, `era:SubsidiaryLocation`,
  `primaryLocationCode/Name`, `subsidiaryLocationCode/Name/Type`, `linkedToPrimaryLocation`,
  `allocationCompany`, the four flags, `inNUTS3`, `ParameterApplicability`, and so on.
  The CRD data uses no `era:tafTAPCode`, deprecated or otherwise.
* **CRD's copy of the ontology** (`graph/era/ontology`, 14,974 triples) is graph-isomorphic to PROD's
  `graph/ontology` once CRLF line endings are normalised. 296 multi-line literals use `\r\n` where PROD
  uses `\n`. This is harmless, but it makes a naive diff report 296 changes.
* **`ParameterApplicability`** is modelled correctly. The class is `rdfs:subClassOf era:TemporalFeature`,
  so `time:hasBeginning` directly on it is right. Of 54,572 applicabilities, none contradicts the flag it
  qualifies, and no PL holds two conflicting applicabilities for the same flag. RINF's CRD-derived graphs
  model it identically.
* **Re-declared terms (F6).** `graph/crd/primary-locations` and `graph/crd/subsidiary-locations` carry
  the full ERA descriptions of the classes and properties they use, `owl:Ontology <http://data.europa.eu/949/>`
  included: 37 terms, with labels, comments, `rdfs:subClassOf` and `owl:disjointWith`. A query that
  counts classes or properties per graph therefore picks up schema rows, and a reasoner sees two copies of
  the ontology. Keep the schema in `graph/era/ontology` only.

### 3.2 SHACL — what the location shapes require

| Shape | PROD | UAT |
|---|---|---|
| `PrimaryLocationShape` | open; code `^[A-Z]{2}[0-9]{5}$` 1..1; name `rdf:langString` uniqueLang + `@en` if present; flags `xsd:boolean` ≤ 1; `inNUTS3` ≤ 1 (Warning); `primaryLocation` forbidden | **`sh:closed`**; adds name ≥ 1, `validity` ≥ 1 (`TemporalFeature`), `isPrimaryLocationOf` and at most one OP, geometry via `netReference/hasGeometry` ≥ 1 (Warning) |
| `SubsidiaryLocationShape` | open; code `xsd:string` 1–10 chars ≤ 1; name langString uniqueLang + `@en`; `linkedToPrimaryLocation` `sh:class PrimaryLocation`; `allocationCompany` `sh:class OrganisationRole`; type IRI + `SubsidiaryLocationTypeSKOS` | **`sh:closed`**, allowing only: allocationCompany, linkedToPrimaryLocation, subsidiaryLocationCode/Name/Type, validity, notApplicable, notYetAvailable, `geo:hasGeometry`, `rdf:type`, `rdfs:label` |

### 3.3 SHACL — results

pyshacl 0.40.2 ran over a deterministic sample from each source and reported only the sampled resources and
the nodes they reach. The data graph was the sample plus ERA PROD's ontology, its SKOS vocabulary, its NUTS
concepts and rinf-plus `graph/rinf/countries`. The CRD sample held 3,000 PLs and 3,000 SLs; the RINF
sample held 3,000 PLs and all 3,899 SLs. The aggregated reports are in [data/shacl/](data/shacl/).

**CRD, PROD shapes: two constraints fire, nothing else.**

| Constraint | Resources in sample | Full dataset (§3.5) |
|---|---:|---:|
| `SubsidiaryLocationTypeSKOS`: type not in the scheme (F3) | 772 / 3,000 SLs (25.7 %) | 19,990 (26.3 %) |
| `InNUTS3SKOS`: NUTS concept not in `inSkosConceptScheme` (F10) | 486 / 3,000 PLs (16.2 %) | every PL with `inNUTS3`: 9,425 (15.9 %) |

Every other PROD constraint that targets these resources passes on the sample: codes, names, flags,
`allocationCompany`, `linkedToPrimaryLocation`, validity, the `TemporalFeature`/`Instant` chain, IM roles
and countries. `InNUTS3SKOS` is meant as a Warning, but ERA puts `sh:severity` on the
`sh:SPARQLConstraint` node, which SHACL ignores, so it reports as a Violation (§3.4).

**CRD, UAT shapes: the closed-shape failure dominates.**

| Constraint | Resources in sample | Full dataset |
|---|---:|---:|
| `SubsidiaryLocationShape` `sh:closed`: `era:inCountry` / `era:infrastructureManager` / `era:operatingLanguage` (F4) | 3,000 / 2,999 / 3,000 SLs (100 %) | 75,917 / 75,838 / 75,913 |
| `InSkosConceptScheme`: SL type (F3) | 772 SLs | 19,990 |
| `InSkosConceptScheme`: NUTS (F10) | 486 PLs | 9,425 |
| `HasSite`: `era:Body` without `org:hasSite` | 65 bodies | all 97 bodies |

CRD's PLs pass UAT's closed `PrimaryLocationShape`, its new `validity` and `primaryLocationName`
minimums and its geometry warning. Apart from the 7,315 `POINT(0 0)` PLs, CRD is UAT-ready for primary
locations. The `HasSite` finding comes from CRD minting bodies that carry only `organisationCode` and `role`.
OCR-KG holds the sites, so either link to OCR-KG's body IRIs or omit the `era:Body` typing.

**RINF sample, for comparison.** The same shapes fire far more on RINF. The main groups, with their
`focus_nodes` counts:

| | PROD | UAT |
|---|---|---|
| PL with no geometry reachable via `netReference` (Warning) | 852 / 3,000 | 852 / 3,000 |
| PL without `primaryLocationName` and `validity` (new UAT minimum) | — | 1,322 / 3,000 (44 %) |
| `NetPointReference` with `wgs84:lat`/`long` (outside UAT closed shape) | — | 1,290 |
| `NetPointReference` with no `hasTopoCoordinate`, or one of the wrong class | 280 | 1,577 |
| NUTS3 not in scheme / wrong class | 18 PLs | 18 PLs |
| Bane NOR `kmPost` of the wrong class | 95 | 95 |
| Bodies: `role`/`roleOf`/`rdfs:label`/`hasSite` (results) | 10 | 29 |
| RINF subsidiary locations (Bane NOR) | 0 | 0 |

So, measured with ERA's own shapes, **CRD's location data is more conformant than RINF's PL data**.
Under PROD it has 2 failing constraints, both vocabulary-alignment problems; RINF has 15 groups,
including structural gaps.

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
* **Severity on SPARQL constraints is ignored.** Several constraints (`InNUTS3SKOS` among them) carry
  `sh:severity sh:Warning` on the `sh:SPARQLConstraint` node. SHACL defines `sh:severity` on shapes, so
  conforming engines report these as Violations. Move the severity to a dedicated shape.

### 3.5 Exact full-dataset checks

[queries/crd-checks.rq](queries/crd-checks.rq), result in [stats/crd-checks.csv](stats/crd-checks.csv).
Each check counts distinct resources over the whole CRD graph.

| Check | Resources |
|---|---:|
| PL code not matching `^[A-Z]{2}[0-9]{5}$` | 0 |
| PL or SL with two names in one language (`sh:uniqueLang`) | 0 |
| PL without an `@en` name | 0 |
| PL flag not `xsd:boolean`, or > 1 value | 0 |
| SL code not a 1–10-character `xsd:string` | 0 |
| SL `linkedToPrimaryLocation` not resolving to a PL in CRD | 0 |
| SL country ≠ its PL's country | 0 |
| ParameterApplicability contradicting its flag | 0 |
| validity without `time:hasBeginning` | 0 |
| PL geometry `POINT(0 0)` | **7,315** |
| SL type not in the `SubsidiaryLocationTypes` scheme (CRD's own SKOS graph = PROD) | **19,990** |
| SL with `inCountry`, `infrastructureManager` or `operatingLanguage` (outside UAT closed shape) | **75,917** |
| SL without geometry (allowed: no `minCount`) | 63,650 |
| SL without `infrastructureManager` / `operatingLanguage` | 79 / 4 |
| `NetBasicReference` with `wgs84:lat` as a plain string | 59,155 |
| `TemporalFeature` IRI containing `None` | 2,235 |
| ERA ontology terms re-declared in the data graphs | 37 |

---

## 4. Comparison with RINF

### 4.1 Property completeness (per code)

[stats/pl-completeness.csv](stats/pl-completeness.csv)

| Property | CRD | RINF | RINF, on shared codes |
|---|---:|---:|---:|
| `inCountry` | 100 % | 98.4 % | 98.4 % |
| `infrastructureManager` | 100 % | 43.3 % | 46.8 % |
| `primaryLocationName` | 100 % (all with `@en`) | 51.8 % | 56.0 % |
| passenger / freight / container / handover flags | 100 % | 42–44 % | 46–47 % |
| position (non-zero WKT) | 87.6 % | 82.6 % | 83.3 % |
| `validity` | 100 % | 51.8 % | 56.0 % |
| validity end | 12.7 % | 23.0 % | 25.1 % |
| `inNUTS3` | 15.9 % | 0.6 % | 0.6 % |

Here CRD is the richer source. Many RINF IMs publish the PL as a stub: code, label and geometry only.
CRD can fill the IM, the names and the TAF/TAP flags for those PLs.

### 4.2 Which RINF graphs are CRD-derived

[stats/rinf-pl-provenance-by-graph.csv](stats/rinf-pl-provenance-by-graph.csv). In two RINF graphs the
PLs carry this pipeline's IRIs: `temporalFeature/YYYYMMDD_None` and
`parameterApplicability/{PLC}_{flag}_{date}_None`.

| RINF graph | PLs | CRD-style validity | With ParameterApplicability |
|---|---:|---:|---:|
| `0080` DB InfraGO | 11,104 | 9,166 | 9,003 |
| `0084` ProRail | 780 | 780 | 636 |
| all other 45 graphs | 41,795 | 0 | 0 |

### 4.3 Value agreement on the 45,733 shared codes

Multi-valued RINF fields count as agreeing when CRD's value is among them. The "independent" column
excludes codes published only in `0080`/`0084`.
[stats/pl-agreement-by-prefix.csv](stats/pl-agreement-by-prefix.csv) breaks this down per country, and
[stats/pl-value-differences.csv](stats/pl-value-differences.csv) lists the disagreeing values.

| Field | Comparable (all) | Agree (all) | Comparable (independent) | Agree (independent) |
|---|---:|---:|---:|---:|
| country | 44,982 | 100 % | 35,032 | 100 % |
| IM organisation code | 21,385 | 100 % | 11,439 | 100 % |
| passengerFlag | 21,623 | 99.4 % | 11,677 | 99.0 % (73 true→false, 48 false→true) |
| freightFlag | 21,201 | 99.9 % | 11,255 | 99.8 % |
| containerHandlingFlag | 21,196 | 100 % | 11,250 | 99.9 % |
| handoverPointFlag | 21,200 | 100 % | 11,254 | 99.9 % |
| name (accent/case/punctuation-insensitive) | 25,610 | 98.2 % | 15,664 | 97.1 % |
| position within 1 km | 38,076 | 97.9 % | 28,127 | 97.2 % |
| validity begin | 21,891 | 67.9 % | 11,945 | **41.2 %** |
| NUTS3 code | 13 | 100 % | 13 | 100 %, but under different IRIs (F10) |

* **Names.** Most mismatches are in GR (7.5 % agree), where RINF prefixes the name with the code number
  (`954-DILOFO`). That is a RINF naming convention, not a different place.
* **Positions.** Median distance 0 m, p90 137 m, p99 3.2 km. 802 codes are > 1 km apart, 301 > 10 km and
  179 > 100 km ([stats/pl-distance-outliers.csv](stats/pl-distance-outliers.csv)). 289 of the 301 > 10 km
  are Danish (F5). The rest look like single-record typos on one side: DK00459 Hirtshals in CRD at
  `POINT(9.96 7.59)` (apparently 57.59 typed as 7.59), GR00757, PL08950 and FR08334, among others.
* **Validity.** Agreement is 100 % in the derived DE/NL graphs and 95.6 % in AT, but 30.8 % in FR and
  0–3 % in HR, LT, LU and NO. The likely reading is that the two sources date different events. CRD's
  start dates reach back to `1874-01-01`, while RINF's follow the RINF record or the opening. This was not
  checked with the publishers. Either way, anyone merging the two must keep both windows apart rather
  than overwrite one with the other.

### 4.4 Operational points → primary locations

RINF links operational points to PLs with `era:primaryLocation`. 46,899 PL IRIs (46,897 codes) are
referenced this way, and 6,844 of them by more than one OP.

* **42,484 referenced codes exist in CRD.** CRD can enrich those OPs with names, flags and IMs by code.
* **4,413 referenced codes are missing from CRD**: DB InfraGO (0080) 1,934; SBB Infrastructure +
  Schweizerische Trassenvergabestelle (0085 + 3915) 905; PKP PLK (0051) 306; Bane NOR (0076) 269;
  Banedanmark (0086) 223; FER (3525) 123; …. They are either retired from CRD after RINF was loaded or never
  allocated. Each row of [stats/rinf-op-pl-missing-from-crd.csv](stats/rinf-op-pl-missing-from-crd.csv)
  gives its uopid, so the IMs can check.
* **Denmark (F5)** is a different case: the codes match, but not what they identify.

### 4.5 Subsidiary locations

| | CRD | RINF |
|---|---|---|
| SLs | 75,917 in 28 countries | 3,899, NOR only |
| Code | RNE SLC (`53414`, `BMZD`, `0076700001`) | Bane NOR track id (`NO-S.1`) |
| `subsidiaryLocationType` | 100 % | 0 % |
| Geometry | 16 % (`POINT`) | 99 % (`LINESTRING`: the track) |
| `allocationCompany` | 34 companies, all typed IM (F1) | 0076 |
| Shared (PLC, SLC) pairs | 0 | 0 |

Bane NOR uses `era:SubsidiaryLocation` for **tracks within a station**, while the class is defined
for the TAF/TAP SLC catalogue (loading points, DIUM codes and so on). For Norway the two sources cannot
be reconciled by code.

---

## 5. Findings in detail

### F1 — Allocation companies typed as infrastructure managers

**MAJOR · verified.** Every `era:allocationCompany` points at an IRI of the form
`…/organisationRole/{code}_IM`, which `era:hasOrganisationRole` `organisation-roles/IM`. Checked in
OCR-KG, 11 of the 34 companies hold no IM role there, and between them they cover **30,059 SLs**:
UIC (3011, 17,559 SLs, role IRO), Rail Cargo Austria (2181), DB Cargo (2180), ČD Cargo (2154),
SBB Cargo (2185), Rail Cargo Hungaria (2155), UIRR (3620), CFL Cargo, Gysev Cargo, DB Cargo Hungária
and Rail&Sea. The graph thus asserts that UIC is an infrastructure manager.
*Fix:* point `allocationCompany` at an `era:OrganisationRole` with the role the company actually holds
in OCR-KG (or a dedicated "allocation company" role if ERA adds one). Keep the IM role for
`era:infrastructureManager` only.

### F2 — Great Britain at null island

**MAJOR · verified.** All 7,312 GB PLs, plus DE, FR and CZ one each, have
`geo:asWKT "POINT(0 0)"` and `wgs84:lat "0.0"`. A map draws them in the Gulf of Guinea, and any nearest-
neighbour or bounding-box query is skewed. *Fix:* omit `netReference`/`hasGeometry` when CRD has no
coordinates. Under UAT that yields the intended `PrimaryLocationNetReferenceGeometry` warning instead of a
fake point.

### F3 — Subsidiary-location types from UAT

**MAJOR · verified.** 19,990 SLs use type codes 01 (19,051), 15 (598), 03 (327), 10 (11), 27 (2) and 02 (1).
These exist in the UAT `SubsidiaryLocationTypes` scheme (50 codes) but not in PROD's (37 codes). CRD's
own `graph/era/skos` is PROD's scheme plus 293 UAT schemes, so CRD fails its own vocabulary as well.
*Fix:* pin one release, either loading the UAT `SubsidiaryLocationTypes` or validating against UAT
throughout, and state the choice in the dataset metadata.

### F4 — SL properties outside the UAT closed shape

**MAJOR for UAT, no issue under PROD.** UAT closes `SubsidiaryLocationShape`, so `era:inCountry`
(75,917), `era:infrastructureManager` (75,838) and `era:operatingLanguage` (75,913) each raise a
`sh:ClosedConstraintComponent` violation on every SL. They are useful properties. Either ERA adds them
to the closed shape or CRD derives them from the linked PL and stops asserting them on the SL. This is
worth raising with ERA before UAT is promoted.

### F5 — Danish codes identify different places

**MAJOR, on the RINF side · verified for samples.** For 289 of the 297 shared DK codes the CRD and RINF
positions are > 10 km apart. In 256 cases the CRD position of code X equals the RINF position of some
other code Y exactly. Example: RINF's OP `uopid DK00010` "Høje Taastrup" sits at
`POINT(12.269823 55.648536)`, which is CRD's `DK00005` Høje Taastrup. CRD's `DK00010` is Borup,
25 km away. RINF's Danish PLs have no names, so name matching cannot catch this. The uopids Banedanmark
uses in RINF are not the RNE PLCs, yet RINF links them as `era:primaryLocation`. Report this to
Banedanmark and ERA, and do not join DK on code until it is fixed.

### F6 – F9 — minor

* **F6** Ontology re-declared in the data graphs (§3.1).
* **F7** `era:NetBasicReference` carries `wgs84:lat`/`lon` as untyped strings next to a typed
  `geo:wktLiteral`, and the geometry node is typed `wgs84:Point` with no lat/long of its own. Drop the
  WGS84 triples; ERA reads positions through `netReference/geo:hasGeometry/geo:asWKT`.
* **F8** `None` in IRIs (`temporalFeature/20170701_None`, `…_freight_19800101_None`): apparently a Python
  `None` serialised into the IRI. Stable but unattractive, and it makes "no end date" look like a value.
  The same IRIs already exist in RINF's DE/NL graphs, so renaming them breaks alignment. Change them
  only together with ERA.
* **F9** Whitespace runs in 236 PL and 377 SL names, probably from a fixed-width CRD export. Normalise
  internal whitespace.

### F10 — NUTS IRIs

**MINOR, partly on the ERA side · verified.** The ontology says `era:inNUTS3 era:inSkosConceptScheme
<https://publications.europa.eu/resource/authority/nuts>`. ERA-Onto holds no concept `skos:inScheme`
that scheme, and its `graph/nuts` (910,907 triples) uses `http://data.europa.eu/nuts/code/{code}`.
CRD follows `graph/nuts`, while RINF's Austrian publishers use the Publications Office IRIs. On the 13
PLs where both sources carry a value, the codes agree but the IRIs do not, so a join on the IRI returns
nothing. As written, PROD's `InNUTS3SKOS` (Warning) fires for every value in either form, unless the
scheme memberships are loaded. ERA should pick one IRI form; CRD should follow it.

### F11 — suggestions

* **IRI governance.** All CRD resources are minted under `http://data.europa.eu/949/` (ERA's namespace)
  by a publisher at `rinf-ris-alignment.com`. For PLs this is deliberate and useful: 38,105 shared codes
  have the same IRI in RINF, so the two graphs join without `owl:sameAs`. It also means CRD triples
  merge silently with ERA's own. Agree the pattern with ERA, or mint under a CRD namespace and link
  with `owl:sameAs`/`skos:exactMatch`.
* **Provenance.** Add `dct:publisher`, `dct:license`, `prov:wasDerivedFrom` (RNE CRD) and the replication
  timestamp per run to `graph/crd/metadata`. `dct:modified` alone does not say which CRD snapshot this is.
* **SKOS.** `graph/era/skos` mixes PROD with 293 UAT-only schemes (booking, accommodation, OSDM-like
  vocabularies). Either load PROD as-is or label the graph as UAT.
* **Validity.** CRD shows only currently valid codes: no end date before 2026-11-03 and no future start.
  The 1,935 DE codes in RINF but not in CRD suggest CRD drops retired codes. If so, keep them with a
  closed validity window, so RINF's references to retired codes stay resolvable.

---

## 6. Method, reproducibility and limits

```text
crd-kg/
├── README.md               this report
├── queries/                every SPARQL query used (run against both endpoints unless noted)
│   ├── pl-*.rq             one field per query, joined locally (avoids RINF's 120 s limit)
│   ├── sl.rq               subsidiary locations
│   ├── crd-checks.rq       exact full-dataset data-quality checks
│   └── sample-*.rq         deterministic SHACL samples (ORDER BY MD5(IRI))
├── scripts/
│   ├── sparql.py           minimal SPARQL client (stdlib only)
│   ├── fetch.py            runs queries/*.rq → data/raw/{crd,rinf}/*.csv (git-ignored, ~80 MB)
│   ├── compare.py          joins on primaryLocationCode → stats/
│   └── validate.py         pyshacl over a sample + ERA ontology + ERA SKOS → data/shacl/
├── stats/                  every table in this report, as CSV, plus summary.json
└── data/shacl/             aggregated SHACL results per dataset × shape set
```

```bash
python3 -I scripts/fetch.py                # ~1 min, both endpoints
python3 -I scripts/compare.py 2026-11-03   # as-of date for validity checks
python3 -I scripts/sparql.py crd queries/crd-checks.rq
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
  yearly, hence the 167 codes with several IRIs and the 3,332 codes in several IM graphs. Fields count as
  agreeing when CRD matches any RINF variant, which flatters RINF slightly.
* **SHACL scope.** Validation ran on a 3,000 + 3,000 sample, extrapolated with the exact full-dataset
  counts in §3.5 wherever a constraint fired. Constraints that need a remote endpoint (`SERVICE`) were
  skipped, and pyshacl's SHACL 1.0 pre-binding restrictions were relaxed so ERA's `VALUES`/`MINUS`
  queries run as GraphDB runs them.
* **OCR-KG.** F1 relies on OCR-KG's role list as of 2026-11-03.
