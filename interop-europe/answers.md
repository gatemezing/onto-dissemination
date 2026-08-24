# ERA Ontology — reusability answers for the Interoperable Europe assessment

**Solution:** ERA Vocabulary (ERA Ontology), v3.3.4 (10 August 2026) · EUPL 1.2 ·
DOI [10.5281/zenodo.15089005](https://doi.org/10.5281/zenodo.15089005) ·
maintained by the European Union Agency for Railways
([public GitLab](https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/era-ontology)) ·
already listed on the [Interoperable Europe Portal](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology).

**Two sources, and where they disagree.** The published ontology v3.3.4 yields
**292** live RINF parameters; the catalogue built from the live endpoint yields
**294**. Both are correct — the deployed repository still runs an older ontology
version, as noted below. Figures are labelled by source throughout.

**A note on the figures below.** Every quantitative claim is either a legal
reference, a measurement of the **published artefacts** (ontology v3.3.4,
`era-shapes`, `era-skos`, `era-telem-skos`), or a measurement against the **live
knowledge graph** (`graph.data.era.europa.eu`) on **22 August 2026**. The two are
distinguished wherever they differ, because in places they do. Counts of
parameters **exclude `owl:deprecated` terms** unless stated — 100 terms in the
ontology are deprecated, and several still carry live data, so including them
overstates coverage. Where a number is uncertain or a limitation is known, it is
stated rather than smoothed over.

---

## 1. Would it make sense for public authorities to look at the reusability of this solution when implementing the assessed decision?

**Yes — and the strongest argument is that the ontology is not an
interpretation of the law, it is the law in machine-readable form.**

Commission Implementing Regulation (EU) 2019/777, as amended by (EU) 2023/1694,
lays down the common specification for the Register of Infrastructure as a
numbered parameter list. The ERA ontology annotates each property with the
matching legal index through `era:rinfIndex`: parameter **1.1.1.1.4.1 "Nominal
track gauge"** *is* `era:wheelSetGauge`. **292 live properties carry such an
index** (329 in total, of which 37 are `owl:deprecated`), so the trace from legal
text to data field is machine-checkable rather than a matter of documentation
discipline.

That matters for an interoperability assessment because it converts a recurring,
expensive problem into a solved one. The pattern is domain-neutral: *a legal act
mandates a register with numbered parameters and coded values; the register must
be comparable across 27 jurisdictions.* Whether the domain is rail, energy
metering or building permits, the reusable design is the same — annotate each
property with its legal index, ship the code lists as SKOS, ship SHACL shapes so
conformance is testable, and publish over open query standards.

Reuse here is demonstrated, not projected:

| Evidence | Measured value |
|---|---|
| Triples in the live knowledge graph | 47,413,498 |
| Countries publishing through it | 27 |
| Distinct national datasets (one per infrastructure manager) | 54 |
| Operational points | 60,562 |
| Sections of line | 69,448 |
| Running tracks | 725,637 |
| SKOS concepts / concept schemes published | 18,279 / 423 |
| SHACL node / property shapes / SPARQL constraints published | 147 / 882 / 323 |

### One vocabulary, four registers

An authority reusing this is not buying into a single-register design. The same
ontology carries the application guides for four distinct legal registers, each
with its own basis in EU law:

| Register | Covers | Legal basis |
|---|---|---|
| **RINF** | Infrastructure — lines, tracks, operational points | Reg. (EU) 2019/777, amended by (EU) 2023/1694 |
| **ERATV** | Authorised vehicle *types* | Decision 2011/665/EU; Reg. (EU) 2019/776; Decision (EU) 2021/701; Dir. (EU) 2016/797; Reg. (EU) 2018/545 |
| **EVR** | Individual registered *vehicles* | Reg. (EU) 2023/1695; Decision (EU) 2018/1614; Dir. (EU) 2016/797 |
| **ERADIS** | Safety and interoperability certification | Dir. (EU) 2016/798; Dir. (EU) 2016/797; Reg. (EU) 2016/796 |

The legal-index annotation is not RINF-only either. Counting live
(non-deprecated) properties in the published ontology: **292 carry
`era:rinfIndex`**, **174 carry `era:eratvIndex`** and **67 carry
`era:tsiOPEAppendixD2Index`**. The same design decision was applied across
registers rather than retrofitted to one.

### The legal trace goes further than an index string

ERA also publishes the legislation itself as linked data. A separate `era-lex`
dataset holds **208,517 triples** describing **7,317 legal resources** and
**7,198 work subdivisions** in the EU's own ELI (European Legislation
Identifier) vocabulary — and **420 ontology terms cite 79 legal acts directly**
through `dcterms:source`.

So the chain is machine-followable end to end. `era:tsiMagneticFields` carries
RINF index `1.1.1.3.9.1` *and* points at
`http://data.europa.eu/eli/reg_impl/2023/1695/oj` — the act in the Official
Journal. A reuser can go from a data field to the numbered parameter to the
legal provision without a human in the loop. **This is the part we would most
encourage other domains to copy**, and it is entirely domain-neutral.

### One URI, reusable everywhere

This is the single idea that carries the most weight, and it is worth stating
plainly because it is what makes the rest work: **a thing gets one identifier,
and everyone points at it instead of describing it again.**

ERA applies that in both directions.

*Reusing what already exists, rather than minting alternatives.* Across the
legislation dataset alone there are **90,235** references to ELI legal-act URIs,
**6,688** to Publications Office corporate bodies, **1,863** to its language
authority, **1,092** to EuroVoc subject concepts, **186** to resource types and
**93** to treaties. Countries in RINF are Publications Office URIs, not ERA
codes. Nothing in that list was re-invented.

*Minting once, then reusing across registers.* The organisation register
(`OCR-KG`, **280,339** triples) holds **5,528** organisations, and **2,909 of
them — 53% — hold more than one role**. One URI,
`.../body/organisation/0080`, is DB InfraGO: it carries the roles Infrastructure
Manager, Railway Undertaking, Entity in Charge of Maintenance, Keeper, Owner and
ECM Certification Body at once. Those roles belong to *different registers* —
IM to RINF, Keeper/Owner/ECM to EVR, certification body to ERADIS — so the
single identifier is what joins them. Inside RINF, **665,487 infrastructure
elements** name that one URI as their manager. Register-wide there are 609
Infrastructure Managers, 2,096 Keepers, 2,593 Owners and 1,205 ECMs, all on the
same identifier space.

*And it reaches into the law.* `era-lex` holds **7,317 legal acts** plus
**7,198 individually addressable subdivisions** — down to the level of
`.../legislation/requirements/dec-2008-217/annex-C/section-3.1`, a numbered
section inside an annex. Each act carries machine-readable force status, its
treaty basis, its amendment chain and EuroVoc subjects, across **1,861 language
expressions in 24 languages**. A requirement can be cited by URI rather than
quoted, and the citation stays valid when the wording is translated or the act
is consolidated.

For a reusing authority the practical instruction is short: **reuse an
identifier before minting one, and where you must mint, mint once and publish
it so others can point at it.** That is the cheapest interoperability decision
available, and the most expensive one to retrofit.

### A working query library, not just a vocabulary

A reuser does not start at a blank query editor. ERA publishes **85 SPARQL
queries** against this graph — **38** in the visible Data Stories catalogue plus
**47** across three downloadable `.sparqlbook` notebooks — and the balance of
them says something about what a register is actually *for*:

| Theme | Visible queries |
|---|---|
| Completeness auditing, per element type and country | 18 |
| TEN-T corridor compliance | 9 |
| Inventory and scale per member state | 4 |
| Network topology quality | 3 |
| Cross-border and TSI compliance | 2 |
| Located property extraction | 2 |

Nearly half the catalogue exists to ask *how complete is this register* — which
is the honest centre of gravity for any public data programme.

The notebooks are literate rather than bare: `completeness.sparqlbook` (29
queries), `tentqueries.sparqlbook` (14) and `otherqueries.sparqlbook` (4) each
pair every query with a narrative markdown cell, so the artefact explains itself
as it runs.

I ran five of them unchanged against the live endpoint while drafting this:

| Query | Result |
|---|---|
| Operational points per member state | 23 rows, 4.5 s |
| Unreachable operational points | 5 |
| Sink operational points | 36 |
| Disconnected operational points | **2,244** |
| Gauging profiles in Ukraine's neighbours | 12 rows, 24.9 s |

Those topology queries are worth dwelling on: ERA publishes, openly, the queries
that expose **2,244 operational points not connected to the network** in its own
register. A programme confident enough to ship its own audit tooling is a
programme whose data can be trusted to be checkable.

**One limitation, stated plainly.** The vocabulary spans four registers, but at
the public endpoint only **RINF data** is currently published as open linked
data. The five readable repositories are `rinf`, `rinf-plus`, `ERA-Onto`,
`era-lex` and `OCR-KG`; there is no open ERATV, EVR or ERADIS *data* repository
today. The `rinf-plus` repository also still describes itself as built on the
"ERA Ontology 3.1.x model" while the vocabulary is at v3.3.4 — a version lag a
reuser should know about.

---

## 2. What was the main challenge, and what were the main lessons learnt?

**The main challenge was not building the vocabulary. It was that a shared
vocabulary does not by itself produce comparable data.** Publication and
convergence are different problems, and the second is much harder.

This is best shown with real defects still observable in the production graph
today — deliberately included here, because an assessment is worth more when it
is honest:

#### A conformance check that the data can talk its way past

`era:opType` (RINF index 1.2.0.0.0.4) is bound to one concept scheme,
**Operational Point Types** (`.../concepts/op-types/OperationalPointTypes`),
issued 2020-09-01 under CC-BY 4.0 and actively maintained — the 28 May 2026
revision added types 20, 110 and 150. In the **published** SKOS artefact that
scheme has exactly **15 members**, `.../concepts/op-types/{notation}`, each with
a `skos:notation` and a lower-case English label.

The published shapes do constrain it. `shapes/OpTypeSKOS` is a SHACL
`SPARQLConstraint` whose test is, in essence:

```sparql
$this era:opType ?concept .
era:opType era:inSkosConceptScheme ?conceptScheme .
FILTER NOT EXISTS { ?concept skos:inScheme ?conceptScheme }
```

Yet the **deployed** graph contains 8 further concepts,
`.../op-types/OperationalPointTypes/{n}` — the scheme IRI mistaken for a path
prefix — with no `skos:notation`, Title-Case labels, the typos "Shuting yard"
and "Tehnical change", and a trailing newline inside "Switch". One publisher
uses them, on 582 operational points.

**Why the check does not catch them, and this is the transferable part.** Those
8 concepts assert `skos:inScheme` the real scheme. The constraint asks whether a
value is in the scheme *as the graph reports it* — so data that declares its own
membership extends the very vocabulary it is being validated against, and passes.
The published vocabulary is clean; the working graph is not.

> **The lesson generalises well beyond rail.** A value-set check must resolve the
> value set from a *trusted, published* source — a protected named graph, a
> versioned artefact — never from the same graph the data under test can write
> into. Otherwise conformance is self-certified.

Two related observations, both checkable:

- **Nothing validates the vocabulary itself.** The suite has shapes targeting
  `skos:Concept`, but none targeting `skos:ConceptScheme`. Constraints such as
  "every member carries a `skos:notation`", "no two members share a notation" or
  "member IRIs match the scheme's pattern" would have caught this at load time.
- **The deployed validation lags the published specification.** The published
  `era-shapes` carries **147 node shapes, 882 property shapes and 323 SPARQL
  constraints**; the repository serving the live data carries **76, 393 and
  211** — roughly half. `rinf-plus` still describes itself as the
  "ERA Ontology 3.1.x model" against a v3.3.4 vocabulary. Shipping a rule and
  enforcing it are different acts.

#### Retired parameters that still carry data

Of the **329** properties carrying a `rinfIndex`, **37 are `owl:deprecated`**,
leaving **292 live** parameters. Deprecation has not reached the data: **17 of
those deprecated properties still carry 237,781 statements** in the live
endpoint, published by **nine countries**.

| Country | Datasets | Statements | Retired parameters |
|---|---|---|---|
| Germany | `1080` | 156,064 | 9 |
| Switzerland | `0085`, `3915` | 63,159 | 3 |
| Czechia | `0054` | 6,538 | 2 |
| Netherlands | `0084` | 3,409 | 3 |
| Sweden | `0074`, `3779`, `3872`, `LQB6` | 3,095 | 10 |
| Spain | `0071` | 2,607 | 4 |
| Hungary | `0055` | 2,250 | 1 |
| Ireland | `0060` | 1,670 | 7 |
| France | `3430` | 592 | 14 |

The heaviest are `tsiCompliantMaxDistConsecutiveAxles` (55,045),
`TSITractionHarmonics` (29,421) and `maxDistEndTrainFirstAxle` (23,493).

Worse for a consumer, only **one of the 17 declares a replacement** via
`dcterms:isReplacedBy` — and in that one case both spellings are populated:
`TSITractionHarmonics` (deprecated) holds 27,818 statements while its successor
`tsiTractionHarmonics` holds 31,387. Query only the live property and you miss
47% of the parameter. The other 16 offer no machine-readable route to their
successor at all.

There is a second-order trap here: the retired and current terms differ only by
capitalisation (`TSIMagneticFields` / `tsiMagneticFields`), which is easy to read
past in a mapping table.

And a third, which caught us while measuring it. `TSITractionHarmonics` carries
**two** `rinfIndex` values, so counting retired statements with
`?p era:rinfIndex ?i . ?s ?p ?o` multiplies that property's statements by two and
inflates the total by its own 27,818. Resolving the property set in a subquery
first gives the correct 237,781. A parameter that legitimately appears at more
than one index is easy to double-count, and 146 of the properties in this
ontology have more than one.

**These findings are now enforced, not just recorded.** The three tools in this
repository exclude `owl:deprecated` parameters: the catalogue behind the value
explorer omits them (294 properties rather than 331), so one cannot be selected
by accident, and the RDF exporter drops them at every level of its recursion. The
value explorer still *reports* the table above, because silently omitting the
data would repeat the very failure this section is about.

#### Published queries that name graphs the deployment does not have

The three downloadable notebooks wrap their patterns in named graphs —
`graph/rinf`, `graph/eratv`, `graph/ontology`, `graph/skos`, `graph/shacl` —
referenced 47 times for `graph/rinf` alone. **All five are empty in the
repository that serves the data**, which holds it in per-infrastructure-manager
graphs instead (`graph/0080` with 15.5 M triples, `graph/1080` with 10.8 M, and
so on).

Run a notebook query exactly as published, against the endpoint named in its own
header comment, and it returns **HTTP 200 with a column header and no rows**.
The same patterns without the `GRAPH` wrapper return data immediately. The 38
visible catalogue queries are unaffected — they query the default union graph,
and all five I tested returned real results.

This is the same failure mode as the concept-scheme case and the dangling
organisation URIs: **a silent, well-formed zero**. Nothing errors, nothing warns,
and a reuser evaluating the register through its own published notebooks would
conclude the data is absent. A published query is an interface, and interfaces
need a test that runs them.

#### The same organisation under two identifiers

The "one URI" principle in the previous answer is right, and this is what it
costs when it is not held. RINF names **180** distinct organisations as
infrastructure managers. Only **93 of those URIs resolve** in the authoritative
organisation register — **87, or 48%, do not**.

The instructive case is Belgium. RINF calls its infrastructure manager
`.../body/organisation/0088`; the register knows the same body as
`.../body/organisation/1976`. Nothing links the two — no `owl:sameAs`, no
mapped code. And the two records are not equivalent:

| | RINF's `0088` | The register's `1976` |
|---|---|---|
| Name | *(none)* | INFRABEL S.A./N.V. |
| Legal / VAT number | *(none)* | BE0869.763.267 |
| Roles | 1 (IM) | 7 (IM, ECM, Keeper, Owner, RC, CI, CONS) |
| Site, homepage, change history | *(none)* | present, last modified 2026-08-13 |

So the richer record exists, and is unreachable from the place that needs it.
Anyone joining RINF infrastructure to organisational identity gets a complete
answer for 93 managers and a bare code for the other 87. The same stub also
carries its role under two different URI patterns
(`body/organisationRole/0088_IM` and `body/organisation/organisationRole/0088_IM`),
which is the same shape of defect as the concept-scheme problem above:
identifiers constructed by string assembly rather than looked up.



**Lessons learnt**

1. **Annotate the ontology with the legal index.** `era:rinfIndex` is the single
   highest-leverage design decision: it makes legal-to-technical traceability
   queryable, and it is what lets tools be built generically over *any*
   parameter rather than hard-coded per parameter.
2. **Resolve a value set from a trusted source, not from the graph under test.**
   18,279 concepts in 423 published schemes exist precisely so that "station" is
   not spelled eleven ways — and the published vocabulary is clean. The defect
   arose because conformance was evaluated against the working graph, which the
   data itself can extend. Validate against the versioned artefact.
3. **Validate the vocabulary, not only the data.** The suite has shapes for
   `skos:Concept` but none for `skos:ConceptScheme`. Three constraints —
   every member has a `skos:notation`, notations are unique within a scheme,
   member IRIs match the scheme's pattern — would have caught this at load time.
   Coverage is uneven more generally: **116 of the 300 live object properties**
   are guarded by a scheme-membership check, so the suite needs its own
   completeness report.
4. **Deprecation is a data migration, not an annotation.** Marking 37 RINF
   parameters `owl:deprecated` did not move the data: 17 of them still carry
   237,781 statements, and only one names its successor. Retiring a term should
   ship with `dcterms:isReplacedBy` on every retired term, and a published
   count of what still sits on it.
5. **Model the publication dimension explicitly, not just the geographic one.**
   A hard-won lesson: filtering by the per-resource `era:inCountry` property
   returns **zero** values for `era:maximumPermittedSpeed` in Austria — the real
   answer is 43 — because many parameters sit on sub-objects (contact line
   systems, ETCS equipment) that carry no country of their own. Scoping by the
   publisher's dataset is reliable where the geographic property is not. Any
   register federating national contributions will meet this.
6. **Cross-border objects are shared, not duplicated.** Two operational points
   are registered by two states at once — the Sweden–Finland border at Tornio and
   the France–Italy border at Menton/Ventimiglia — each in the neighbour's
   language. Naive de-duplication destroys real information; naive summing
   double-counts. Cross-border identity needs an explicit, stated rule.
7. **An identifier is only reusable if it resolves.** Publishing URIs is not the
   same as governing them. The gap above is not a modelling error — both systems
   use the right namespace and the right shape — it is the absence of a single
   authority deciding which identifier denotes a given organisation. Any
   federation should stand up its identifier register *before* the datasets that
   reference it, and should monitor dangling references as a standing metric,
   the same way it monitors parameter completeness.
8. **Ship the caveat with the query.** The catalogue does this well and it is
   worth copying. The tunnel-length query documents its own deduplication
   rationale — the same tunnel is reported once per track inside it, sometimes
   with differing lengths, so `MAX` is used and the comment concedes it "might
   not be the correct value, but it's deterministic and consistent". Others warn
   "this query will LIKELY time out" and point at an optimised variant, or
   explain why explicit hierarchy beats a property path. Publishing the
   reasoning alongside the SPARQL is what makes a query library reusable rather
   than merely available.
9. **Reuse hubs are powerful and fragile.** A single temporal-validity record is
   referenced by **347,989 resources**, and the most-shared contact line system by
   **3,953 tracks**. Excellent for consistency and storage, but a change to one
   such node propagates instantly across a national network, so change management
   has to account for the blast radius.

---

## 3. Do you envisage collaboration with other Member States or Union entities?

**Collaboration is already the operating model, not an aspiration.**

- **With standardisation bodies.** A Memorandum of Intent with **railML.org was
  signed on 30 May 2023**, under which ERA and railML jointly published their
  ontologies and developed use cases transforming railML data into RINF
  provisions. Alignment continues through regular working meetings.
- **With the Publications Office.** ERA does not mint its own country codes: the
  graph points directly at the EU authority tables
  (`http://publications.europa.eu/resource/authority/country/...`). Reusing
  existing EU semantic assets rather than duplicating them is a deliberate choice
  and one we would recommend to any reuser.
- **With W3C and OGC.** The ontology imports GeoSPARQL, SKOS, PROV, ORG and
  OWL-Time rather than reinventing geometry, provenance or organisational
  modelling.
- **With Member States and infrastructure managers**, through the National
  Registration Entities that the RINF Regulation requires, and through a public
  GitLab issue tracker where change requests are visible to everyone.
- **Beyond the compliance perimeter.** Bane NOR, the Norwegian infrastructure
  manager, publishes its own station data using the ERA ontology on its own
  Linked Data server (`data.banenor.no`) — its resources are visible in the
  shared graph — for instance contact line systems referenced by 2,873 and 1,641
  Norwegian tracks. Voluntary adoption by a publisher outside the EU mandate is
  the clearest available evidence that the model is reusable on its merits.

Natural next steps we would welcome partners on: deeper alignment with the
European Mobility Data Space and National Access Points; publishing ERATV, EVR
and ERADIS **data** as openly as RINF already is, since today the vocabulary
covers all four registers but only RINF data is openly queryable; closing the
value-set validation gaps identified in §2; and contributing the pattern back to
SEMIC as a reusable design rather than a rail-specific artefact.

---

## 4. Is the solution suitable for local, regional, or national public administrations?

**Yes, at every level — because the unit of publication is the dataset, not the
country.**

The graph today holds **54 distinct national datasets across 27 countries**, one
per publishing infrastructure manager. The distribution shows this is not a
national-champions-only model:

- **Italy: 9** publishing organisations · **Austria: 8** · **France: 7** ·
  **Sweden: 4** · **Germany, Finland, Switzerland: 2 each**
- **Belgium, Poland, Portugal, Ireland and others: 1 each**

Small regional and private infrastructure managers already publish alongside
national incumbents, using the same vocabulary and appearing in the same
cross-border queries. No entity has to be large to participate.

The granularity supports local asset management as well as strategic planning:
the ontology models platforms, sidings, level crossings, tunnels, bridges,
signals and kilometric posts, not only strategic corridors. A regional authority
can therefore adopt it for its own network and get immediate internal value —
consistent asset descriptions, validated against shipped SHACL shapes — without
waiting for anyone else.

---

## 5. Does it need central governance, or does it bring value if deployed in just some entities?

**Two things must be separated, and the honest answer differs for each.**

**The vocabulary needs central governance. The deployment does not.**

*Central, and non-negotiable:* a shared meaning must have exactly one owner. ERA
maintains the ontology under a single version line (v3.3.4), one licence (EUPL
1.2), a public repository and an archival DOI. Without that you do not get one
vocabulary used 27 times; you get 27 dialects. §2 shows why the *published*
artefact is not the whole job: the governed vocabulary is clean, yet the
deployed graph carries concepts that were never in it. **Central governance of
the code lists is the part that cannot be devolved — and it has to extend to
what is loaded, not stop at what is published.**

*Decentralised, and valuable immediately:* deployment accrues benefit
incrementally, per publisher. Each entity that adopts the vocabulary gets value
before anyone else joins — its own data becomes queryable, comparable
year-on-year, and testable against the SHACL shapes. Bane NOR demonstrates this:
it derives value publishing essentially alone, outside the EU mandate.

The realistic caveat: **cross-border value requires both critical mass and
conformance.** Partial deployment *with* local variation is the worst of both
worlds — it produces the appearance of interoperability without the substance,
because queries return plausible but incomplete answers. Partial deployment
*with* conformance is genuinely useful from the first publisher onward.

---

## 6. How does the solution support cross-border data exchange and EU sovereignty?

### Cross-border exchange

The canonical use case is **route compatibility**: checking a vehicle against
the infrastructure it is to run on, across borders, without bilateral agreements
or point-to-point integrations. That check spans three registers at once — the
individual vehicle in **EVR**, its authorised type in **ERATV**, and the line in
**RINF** — and the ontology models the joins that connect them: an EVR
`Vehicle` references its `VehicleType`, which carries the gauge, ETCS level and
braking characteristics that RINF's track parameters must be compared against.
Because all three sides share one vocabulary and one set of code lists, this is
a query rather than an integration project. It is the clearest argument for
modelling a *family* of registers together rather than one at a time.

Borders are modelled as first-class objects, not edge cases: **288
`era:ReferenceBorderPoint` resources**, plus operational points typed "border
point" (427 under the canonical concept, plus 17 under one of the duplicate
concepts described in §2) and "domestic border point" (433), and the
jointly-registered cross-border stations described in §2.

A single query illustrates what cross-border comparability buys. Asking the graph
for legal parameter **1.1.1.1.4.1** returns the gauge landscape of the entire
European network:

| Nominal track gauge (mm) | Running tracks |
|---|---|
| 1435 (standard) | 697,901 |
| 1668 (Iberian) | 13,275 |
| 1524 (Finnish/Baltic) | 2,813 |
| 1000 (metre) | 2,746 |
| 1520 (former Soviet) | 1,826 |
| 1600 (Irish) | 274 |
| 760 | 131 |
| 750 | 4 |

That is the classic break-of-gauge interoperability barrier — Iberian, Baltic and
Irish networks — quantified across 27 countries from one question, in seconds.
Before a shared vocabulary, assembling that meant 27 bilateral data requests.

The published catalogue already turns this into standing instruments. One query
returns the gauging profiles of tracks in **Ukraine's neighbouring countries** —
a live question for interoperability with a non-member network, answerable
because Hungary, Poland, Slovakia and Romania describe their gauges in the same
terms. Three more audit the network as a *graph* rather than a table, finding
operational points that are unreachable (5), sinks (36) or wholly disconnected
(**2,244**). Cross-border operation depends on the topology actually joining up,
and that is only checkable once everyone's topology is expressed the same way.

### EU sovereignty

- **Custody stays national.** Each Member State publishes into its own dataset,
  through its own National Registration Entity and infrastructure managers. What
  is shared is the *meaning*, not the ownership. There is no central database
  that takes possession of national data.
- **EU-controlled identifiers — the sovereignty argument proper.** Resources are
  named under `http://data.europa.eu/949/`, and where an EU authority already
  names something, ERA points at it rather than minting a rival: Publications
  Office country, language, treaty, resource-type and corporate-body tables,
  EuroVoc subjects, ELI legal acts. Whoever controls the identifiers controls
  who can join the data. Here that authority is European, the URIs are
  persistent and publicly governed, and the vocabulary binding them is EUPL 1.2
  with an archival DOI. **A shared identifier space is the most durable form of
  digital sovereignty on offer** — it cannot be withdrawn by a supplier, and it
  does not depend on where anything is hosted.
- **No vendor lock-in anywhere in the stack.** RDF, SPARQL, SKOS, SHACL (W3C) and
  GeoSPARQL (OGC) are open standards with multiple independent implementations.
  The vocabulary is EUPL 1.2 and archived on Zenodo with a DOI, so it survives
  any single supplier, contract or hosting decision.
- **EU-hosted infrastructure.** The knowledge graph is served from EU ERA  infrastructure (`graph.data.era.europa.eu`), with no
  dependency on non-EU cloud services for the semantic layer.
- **Open access enables scrutiny.** The endpoint is publicly queryable with
  permissive CORS, so any Member State, researcher or citizen can verify a claim
  about the register directly rather than trusting a report. The data-quality
  findings in §2 were found exactly that way.

---

## 7. What is the first step to reuse the solution?

**Query it before committing to anything.** No account, no licence negotiation,
no data pipeline. The following runs as-is and returns the table in §6:

```bash
curl -sS -X POST "https://graph.data.era.europa.eu/repositories/rinf-plus" \
  -H "Content-Type: application/sparql-query" -H "Accept: text/csv" \
  --data-binary '
PREFIX era:  <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?rinfIndex ?property ?value ?label (COUNT(DISTINCT ?track) AS ?tracks)
WHERE {
  ?property era:rinfIndex ?rinfIndex .
  FILTER(?rinfIndex = "1.1.1.1.4.1")          # Nominal track gauge
  ?track ?property ?value .
  OPTIONAL { ?value skos:prefLabel ?label FILTER(LANG(?label)="en") }
}
GROUP BY ?rinfIndex ?property ?value ?label
ORDER BY DESC(?tracks)'
```

Then, in order:

1. **Run the published queries first.** The
   [Data Stories catalogue](https://rinf.data.era.europa.eu/data-stories) holds
   38 ready-made queries and three downloadable notebooks; the commonest
   questions about a rail register are already written, annotated and tested.
   Start there rather than at a blank editor — but note the notebook caveat in
   §2 and drop the `GRAPH` wrapper if a notebook query returns nothing.
2. **Read the vocabulary** — <https://rinf.data.era.europa.eu/era-vocabulary/>
   (v3.3.4; RDF/XML, Turtle, JSON-LD, N-Triples, CSV, plus SHACL and SKOS
   artefacts) — and the
   [RINF application guide](https://rinf.data.era.europa.eu/era-vocabulary/rinf-appGuide/),
   which explains how each numbered parameter maps to a property.
3. **Locate your own parameters.** If you already hold a register, map your
   fields to the ERA properties via their `rinfIndex`. Anything that does not map
   is either genuinely national or a gap worth raising upstream.
4. **Adopt the identifiers before anything else.** Before modelling, look up
   what already has a URI — countries and languages in the Publications Office
   tables, legal acts in ELI, subjects in EuroVoc, railway organisations in
   ERA's register. Pointing at an existing identifier is the cheapest
   interoperability you will ever buy; minting a parallel one is the most
   expensive thing to undo later, as the Belgian case in §2 shows.
5. **Adopt the code lists before the classes.** Reusing the SKOS concept schemes
   is where most of the remaining comparability is won — take them from the
   published `era-skos` artefact, and pin the version you validated against.
6. **Validate early with the shipped SHACL shapes**, in your own pipeline, before
   first publication — this is the step whose absence produced the defects in §2.
   Check specifically that each *coded* parameter you publish has a value-set
   shape, and treat a coded parameter without one as unvalidated. Add one check
   of your own: that every external URI you reference actually resolves.
7. **Publish into your own dataset**, keeping custody.
8. **Engage the maintainers** through the public GitLab issue tracker for
   extensions or clarifications. The vocabulary is versioned and the change
   process is open.

For an authority whose domain is *not* rail, the reusable asset is step 1's
design rather than the rail classes themselves: a legal annex expressed as
indexed properties, governed code lists, shipped validation shapes, and open
query access. That pattern is what we would encourage assessors to consider
transferable.

---

### Sources

- ERA Ontology v3.3.4 — <https://rinf.data.era.europa.eu/era-vocabulary/>
- RINF application guide (technical annex) — <https://rinf.data.era.europa.eu/era-vocabulary/rinf-appGuide/>
- ERATV application guide — <https://rinf.data.era.europa.eu/era-vocabulary/eratv-appGuide/>
- EVR application guide — <https://rinf.data.era.europa.eu/era-vocabulary/evr-appGuide/>
- ERADIS application guide — <https://rinf.data.era.europa.eu/era-vocabulary/eradis-appGuide/>
- Commission Implementing Regulation (EU) 2019/777 (16 May 2019), as amended by (EU) 2023/1694 (10 August 2023)
- Commission Recommendation 2014/881/EU
- ERATV: Decision 2011/665/EU; Reg. (EU) 2019/776; Decision (EU) 2021/701; Dir. (EU) 2016/797; Reg. (EU) 2018/545
- EVR: Reg. (EU) 2023/1695; Decision (EU) 2018/1614
- ERADIS: Dir. (EU) 2016/798; Dir. (EU) 2016/797; Reg. (EU) 2016/796
- ERA Knowledge Graph — <https://www.era.europa.eu/domains/registers/era-knowlege-graph_en>
- RINF Data Stories (38 queries, 3 SPARQL notebooks) — <https://rinf.data.era.europa.eu/data-stories>
- Organisation register (`OCR-KG`) — <https://graph.data.era.europa.eu/repositories/OCR-KG>
- Legislation dataset (`era-lex`) — <https://graph.data.era.europa.eu/repositories/era-lex>
- Published SHACL shapes — <https://rinf.data.era.europa.eu/era-vocabulary/era-shapes>
- Published SKOS vocabularies — <https://rinf.data.era.europa.eu/era-vocabulary/era-skos> and <https://rinf.data.era.europa.eu/era-vocabulary/era-telem-skos>
- Published ontology (OWL / N-Triples / CSV) — <https://rinf.data.era.europa.eu/era-vocabulary/ontology.nt>
- ELI (European Legislation Identifier) and EuroVoc, Publications Office of the EU
- Interoperable Europe Portal, ERA Vocabulary solution — <https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology>
- ERA / railML.org Memorandum of Intent, 30 May 2023 — <https://www.railml.org/en/news/a-year-of-transformative-collaboration-era-and-railml-org-enhance-railway-data-standards>
- ERA Ontology repository — <https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/era-ontology>
- Live measurements taken 22 August 2026 against <https://graph.data.era.europa.eu/repositories/rinf-plus>
