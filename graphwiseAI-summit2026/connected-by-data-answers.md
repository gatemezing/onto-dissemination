# Connected by data — ERA's answers, questions 1 to 5

**Graphwise AI Summit 2026 · panel "Connected by data: how knowledge graphs drive
interoperability and ROI in complex, regulated ecosystems" · 7 October 2026**
Speaker: Ghislain Atemezing (ERA). These are ERA's answers only.

**How to read the evidence.** Every figure is one of three kinds, labelled in
each table:

- **Live**: measured against the public knowledge graph
  (`graph.data.era.europa.eu`) on the date given. Anyone can rerun it.
- **Published**: counted in ERA's published artefacts (ontology v3.3.4, SHACL
  shapes, SKOS schemes) or stated in EU law.
- **Repo**: measured while building the tools in this repository, with the
  commit that holds the details.

No figure here is a euro amount. ERA has not published cost figures for the
knowledge graph, so ROI is shown as time, effort and risk removed. A cost
figure should come from ERA's own records before it is quoted.

---

## 1. The "interoperability tax"

**Key message:** the tax is the cost of every party re-describing the same
thing in its own terms. It is paid in bilateral requests, manual
reconciliation, and answers that look complete but are not.

- **Before:** comparing a single parameter across Europe meant collecting it
  country by country, from 27 different national setups.
- **The hidden part of the tax is risk, not effort.** Data that does not share
  identifiers fails silently: a query returns an empty or partial answer,
  with no error.
- **What the knowledge graph changes:** one vocabulary, one identifier per
  thing, and the legal parameter number on every property. A Europe-wide
  question becomes one query.

| Evidence | Figure | Kind |
|---|---|---|
| The gauge landscape of the whole European network: 8 nominal gauges, from 1435 mm (383,474 tracks) to 750 mm (4) | **1 query, 3.8 s**, instead of one request per country | Live, 7 Oct 2026 |
| Infrastructure managers named in RINF whose organisation URI does not resolve in ERA's organisation register (e.g. Infrabel is `0088` in RINF, `1976` in the register) | **87 of 180 (48%)** | Live, 22 Aug 2026 |
| Statements still published on 17 retired RINF parameters, in 9 countries; only 1 of the 17 names its successor | **237,781** | Live, 22 Aug 2026 |
| Operational-point positions in the Eurostat export, when read through the old WGS84 property instead of the shared geometry model | **187 of 62,117 points**: filled for Lithuania only | Live / Repo `06d2042` |

**On stage:** "The tax isn't the integration project you can see. It's the
answer that comes back complete-looking and wrong. Shared identifiers are how
you stop paying it."

---

## 2. Ontologies versus one-off integrations

**Key message:** the deciding factor was that the ontology can carry the
**law itself**. Each property is tied to the numbered parameter of the
regulation that requires it, so the model stays correct as the law changes.

- **The old way:** each register and each national system kept its own
  format, exchanged as files and reconciled bilaterally. Every new question
  meant a new extraction; every partner pair meant a new mapping.
- **Its limits:** effort grows with the number of partner pairs (27 countries
  give 351 pairs). Meaning lives in documents, not in the data. And nothing
  shows when two partners drift apart.
- **The critical factor:** `era:rinfIndex`. Parameter 1.1.1.1.4.1, "Nominal
  track gauge", *is* the property `era:wheelSetGauge`, so tools can be
  written once over *any* parameter instead of being hard-coded parameter by
  parameter.
- **Confirmation from outside the mandate:** Bane NOR (Norway) publishes on
  its own server with the ERA ontology, and railML.org aligned its model with
  ERA under a Memorandum of Intent (30 May 2023).

| Evidence | Figure | Kind |
|---|---|---|
| Live RINF parameters carrying their legal index in the ontology | **292** (329 indexed, 37 retired) | Published, v3.3.4 |
| The same design on other registers: vehicle-type index; route-book (TSI OPE Appendix D2) index | **174**; **46** indices | Published / Live, 7 Oct 2026 |
| Properties flagged for route-compatibility checks (`era:usedInRCCCalculations`) | **89** | Live, 7 Oct 2026 |
| Partner pairs needing a mapping: point-to-point versus one shared model, for 27 countries | **351 pairs** versus **27 mappings** | Arithmetic: n(n−1)/2 versus n |
| Tools in this repository built once over the legal annotations rather than per parameter: RINF value explorer (`rinfIndex`), route compatibility (`usedInRCCCalculations`), route book (D2 index) | **3** | Repo |

**On stage:** "We didn't choose graphs because they were fashionable. We chose
them because a regulation is already a structured model, and an ontology lets
the data carry the legal reference with it."

---

## 3. Regulation and compliance

**Key message:** when the regulation is part of the data model, a compliance
question becomes a query, and an audit becomes something anyone can rerun.

- **The ontology is itself a regulatory instrument.** It is a Technical
  Document issued by ERA under Article 4(8) of Directive (EU) 2016/797.
- **The law is in the graph too.** `era-lex` publishes EU rail law with ELI
  identifiers, so a data field links to the parameter number and the
  parameter to the provision in the Official Journal. No human is needed in
  the loop.
- **Compliance questions become queries:** route compatibility, the
  route-book obligations an infrastructure manager owes a railway
  undertaking, and TEN-T corridor membership.
- **Legacy registers get the same treatment:** migrating ERADIS into the
  graph exposes, for instance, how many certificates are really still valid.
- **Stated honestly:** the rules live online lag the published ones, so
  compliance tooling must name which version it checks against.

| Evidence | Figure | Kind |
|---|---|---|
| Legal acts and individually addressable provisions in `era-lex`, in 24 languages | **7,317** acts, **7,198** subdivisions | Live, 22 Aug 2026 |
| Validation rules shipped with the ontology: node shapes / property shapes / SPARQL constraints | **147 / 882 / 323** (the deployed repository holds **76 / 393 / 211**) | Published / Live |
| ERADIS migrated into the graph: EC declarations and notified-body certificates, each TSI resolved to its ELI | **22,256** and **43,471** | Repo, 30 Sep 2026 |
| Certificates whose recorded state says "amended" although they are the current version, so validity has to be derived from the validity window | **42,088** of 43,471 | Repo `48db48b` |
| Route-book elements (TSI OPE Appendix D2) that *no* manager can fill today, because their class (`SpecialArea`, `RadioBlockCenter`) has no instance | **5** of 46 | Live, 7 Oct 2026 |

**On stage:** "Regulation stops being a blocker once it is in the model. The
auditor no longer asks for a report; they rerun the query."

---

## 4. Proving trust and ROI

**Key message:** trust is not claimed, it is made checkable. Publish the
query next to the number, publish your own defect findings, and test every
derived figure against an independent source.

**Showing trust to regulators and safety bodies**

- **Every figure comes with its query.** Each tool shows the exact SPARQL
  before it runs, and the endpoint is open, so a regulator can rerun it.
- **Gaps are shown, not hidden.** Missing values read "no data", and coverage
  statistics come with every export.
- **ERA publishes its own audit queries,** including those that expose its
  defects (2,244 operational points not connected to the network).
- **Figures are cross-checked before release.** Live answers were compared
  field by field against independent snapshots; country totals were checked
  against known traps such as Germany's yearly republication.

**Before and after: three moments, measured**

| Moment | Before | After | Kind |
|---|---|---|---|
| A Europe-wide parameter question (e.g. track gauge) | One request per country, then reconciliation | **1 query, 3.8 s** | Live, 7 Oct 2026 |
| Searching all current notified-body certificates in ERADIS | **88 s** for the first 500 only | **all 43,471 in ~10 s** | Repo `b50217e` |
| The Eurostat sections-of-line export for the whole EU | **79 s**, positions empty outside Lithuania | **51 s**, all 62,117 point positions filled | Repo `06d2042` |

| Trust evidence | Figure | Kind |
|---|---|---|
| ERADIS live answers compared with the snapshot, field by field, on 7 searches | **64,000+ rows**, identical documents and fields | Repo `b50217e` |
| A plausible-looking deduplication rule (newest date per line) on France's line 830000‑1 | **67,281 → 132 rows: 99.6% data loss.** Caught by a test, not by eye | Repo (RCC tool) |
| German sections counted twice without the validity rule | **36,648** rows instead of **18,313** | Repo `06d2042` |
| Operational points flagged as disconnected by ERA's own published audit query | **2,244** | Live, 22 Aug 2026 |

**On stage:** "A regulator doesn't need to understand a graph. They need to
rerun the number and get the same answer, and to see that we publish what's
wrong as readily as what's right."

---

## 5. The single lesson for any regulated industry

**Key message:** govern the identifiers and the meaning centrally. Publish
openly, so anyone can verify. And treat a quiet, plausible answer as the
main risk.

1. **Identifiers first.** Reuse an existing one before minting your own, and
   mint once. In rail, 48% of infrastructure-manager references fail to join
   the organisation register for lack of exactly this rule. Healthcare and
   finance have the same problem with patients, products and legal entities.
2. **Put the regulation in the model.** A legal index on each field turns
   "are we compliant?" from a report into a query.
3. **Test for the silent failure.** The costly errors never raise an
   exception: an empty result, a doubled count, a 99.6% loss that looks like
   tidy deduplication. Make "no data" explicit, and check every derived total
   against an independent source.

**On stage:** "Agree on what things are called and who owns the name, put
the rulebook in the data, and never trust an answer just because it came
back without an error."

---

### Sources

- ERA Ontology v3.3.4 — <https://rinf.data.era.europa.eu/era-vocabulary/>
- ERA knowledge graph (SPARQL) — <https://graph.data.era.europa.eu/> (repositories `rinf-plus`, `OCR-KG`, `era-lex`)
- Directive (EU) 2016/797, Art. 4(8); Implementing Regulation (EU) 2019/777, as amended by (EU) 2023/1694 (RINF)
- [interop-europe/answers.md](../interop-europe/answers.md): ERA reusability answers, measured 22 Aug 2026
- Tools and measurements in this repository: [README](../README.md); commits `06d2042`, `b50217e`, `48db48b`
- ERA / railML.org Memorandum of Intent, 30 May 2023
