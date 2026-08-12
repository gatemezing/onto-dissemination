# Dissemination Script — "What is an Ontology, and Why Does Railway Data Need One?"

**Event:** InnoTrans 2026, Berlin ExpoCenter City, 22–25 September 2026
**Audience:** Railway experts (infrastructure managers, railway undertakings, National Safety Authorities, rolling stock manufacturers, signalling engineers) — technical but **not** semantic-web/IT specialists
**Speaker role:** Booth staff / dissemination officer for the ERA ontology (railway semantic interoperability)
**Formats included:** 30-second elevator pitch · 3-minute booth talk · 7–8 minute workshop/theatre talk · FAQ · audience-satisfaction review · production checklist

---

## 0. How to use this file

This is a **working script**, not a finished slide deck. Use it to:

1. Brief booth staff so everyone tells the same story, in the same order, with the same examples.
2. Draft the poster / roll-up / one-pager copy (Section 6 gives you the checklist).
3. Rehearse against the audience-satisfaction review in Section 4 before printing anything.

Anything in `[brackets]` is a placeholder to fill in with your booth number, QR code, or contact details closer to the event.

---

## 1. The core idea in one sentence

> **An ontology is a shared technical dictionary and rulebook for data — the ERA ontology is that dictionary for railway infrastructure and rolling stock data, so that every country's systems mean the same thing by "track," "electrification," or "loading gauge."**

Keep this sentence as the anchor. Every version of the script below is a longer or shorter unpacking of it.

---

## 2. Elevator pitch (~30 seconds)

Use when someone glances at the booth and you have one sentence to earn their attention.

> "Quick question — when your infrastructure register says 'track gauge 1435mm,' and a train manufacturer's system says the same thing, are you 100% sure a computer would know those are the same fact? That's the interoperability problem the ERA ontology solves. It's the agreed data dictionary behind the EU's railway infrastructure register, RINF, so that data from 27 member states can be combined and queried automatically instead of reconciled by hand. Got 3 minutes? I'll show you."

---

## 3. Booth talk (~3 minutes)

### Opening — the pain point, not the technology (30s)

> "Let me start with a problem, not a tool. A train running from France to Germany crosses infrastructure managed by different organisations, in different languages, historically described in different national data formats. Track parameters, electrification systems, ETCS levels, loading gauges — the *facts* are comparable, but the *data* often isn't, because each system was built to describe its own network, not to talk to its neighbour's system."

### What is an ontology (60s)

> "An ontology is nothing exotic — think of it the way you'd think of a signalling rulebook. ETCS doesn't just move information between trackside and cabin; it defines what a 'movement authority' or a 'balise' *means*, so that any compliant train and any compliant trackside system interpret it the same way, regardless of manufacturer or country.
>
> An ontology does the same job for *data*: it defines, with a precise and machine-readable structure, what a 'Track,' an 'Operational Point,' or a 'Contact Line' *is*, what properties it can have, and how those things relate to each other. Once everyone publishes data against that same definition, software — not people — can combine it correctly."

### The ERA ontology, concretely (60s)

> "The EU Agency for Railways maintains exactly this: the **ERA vocabulary**, published at `data.europa.eu/949`. It's a formal technical document under the Fourth Railway Package [Directive (EU) 2016/797, Article 4(8)], built in RDF/OWL and aligned with RailTopoModel and railML3.
>
> It underpins the **Register of Infrastructure (RINF)**, which since 2021 has been published as a queryable knowledge graph. In practice: every 'Track' in every member state's register uses the same class definition — `data.europa.eu/949/Track` — so a query like 'show me all interoperable lines between Germany and France certified for ETCS Level 2' can be answered by machine, across national borders, without a single spreadsheet reconciliation."

### Why it matters to you (30s)

> "For an infrastructure manager, it means your register data becomes reusable beyond your own systems — by manufacturers checking vehicle authorisation, by RUs planning cross-border paths, by ERA itself for TSI conformity checks. For a manufacturer, it means one integration effort instead of 27 national ones. That's what 'interoperability' means at the data layer, and it's the same goal the Single European Railway Area has at the operational layer."

### Call to action (10–20s)

> "We have a live demo at `[booth number]` where you can run a real cross-border query against the RINF knowledge graph in under a minute. Here's a QR code to the vocabulary browser and our contact for anyone exploring a pilot: `[QR code / contact placeholder]`."

---

## 4. Extended workshop talk (~7–8 minutes)

Use this version for a seminar slot, side-event, or when someone at the booth wants the fuller picture. It follows the same arc as the booth talk but adds structure suitable for slides.

**Slide 1 — Hook:** "Same fact, different data. Why cross-border rail data still needs manual reconciliation in 2026."

**Slide 2 — What is an ontology:**
- Analogy: ETCS is a shared rulebook for signals; an ontology is a shared rulebook for data.
- Formal definition (for the technically curious, in a footnote): a machine-readable specification of the concepts, properties and relationships in a domain, typically expressed in RDF/OWL.
- The key promise: *same meaning, every time, for every system that adopts it.*

**Slide 3 — The interoperability problem in railways:**
- Cross-border operations require exchanging infrastructure, rolling stock and operational data across ~27 national systems.
- Historically: different formats, different terminology, different granularity → manual reconciliation, delay, risk of error.
- Legal driver: Fourth Railway Package pushes toward common, machine-readable data definitions (Directive (EU) 2016/797, Art. 4(8)).

**Slide 4 — The ERA ontology / vocabulary:**
- Published at `http://data.europa.eu/949/`, versioned (current major line ~3.x), maintained by the EU Agency for Railways.
- Aligned with RailTopoModel and railML3, and with INSPIRE where relevant.
- Every class and property has a dereferenceable URI — `http://data.europa.eu/949/Track`, `.../OperationalPoint`, `.../ContactLineSystem`, etc. — meaning you can look each one up like a dictionary entry, and software can too.

**Slide 5 — It's not just a document, it's a live knowledge graph:**
- RINF (Register of Infrastructure) has been published as RDF Linked Data / a knowledge graph since 2021.
- Queryable via SPARQL — federated queries across national datasets become possible in principle, not just in theory.
- Live demo moment: run one real query on screen (e.g., list operational points with a given ETCS level on a named cross-border corridor).

**Slide 6 — Concrete benefits:**
1. One shared definition instead of 27 national ones → lower integration cost for manufacturers and IT vendors.
2. Machine-checkable TSI conformity instead of manual document review.
3. Reusable infrastructure data for vehicle authorisation, capacity planning, and future digital-twin / AI applications.
4. A stable foundation as ERTMS deployment and Europe's Rail Joint Undertaking initiatives increase the volume of cross-system data exchange.

**Slide 7 — What we're asking of the audience:**
- Try the live query at the booth.
- Take the one-pager / QR code home to your IT and data teams.
- Tell us where your current data pain points are — pilots and feedback shape the next ontology release.

**Closing line:**
> "The rulebook that lets an ETCS-fitted train cross a border safely already exists. We're building the equivalent rulebook so the *data* about that border crossing can move just as smoothly. Come see it work."

---

## 5. Anticipated questions (FAQ)

| Question a railway expert is likely to ask | Short answer to give at the booth |
|---|---|
| "Is this just another data format / schema?" | No — a schema defines structure (fields, types); an ontology also defines *meaning* and *relationships*, and is designed to be linked and queried across independently-published datasets, not just parsed by one application. |
| "Do I need to know RDF/OWL/SPARQL to use this?" | No. Most users interact with RINF through the standard web interface. RDF/SPARQL matters to the systems and integrators behind the scenes — the same way you don't need to know ETCS message formats to benefit from ETCS. |
| "Is this mandatory?" | The ERA vocabulary is a technical document issued under Directive (EU) 2016/797, underpinning mandatory registers like RINF. Ask `[insert current legal/compliance answer confirmed with ERA before the event]` for the precise compliance scope relevant to the visitor's role. |
| "How is this different from railML?" | The ERA ontology is aligned with railML3 and RailTopoModel rather than competing with them — it reuses their concepts as the semantic backbone for the EU's official infrastructure register. |
| "What do I actually get if my organisation adopts it?" | Reduced one-off integration cost per partner/country, machine-checkable conformity, and infrastructure data that's reusable beyond its original purpose (e.g., by manufacturers, planners, or future AI/digital-twin tools). |
| "Where can I see it / try it myself?" | Point to the live demo, the vocabulary browser QR code, and `[GitLab/GitHub repository link placeholder]` for anyone technical who wants to inspect it directly. |

---

## 6. Audience-satisfaction review (self-review pass)

Before this script is used live, it was reviewed against a **railway-expert persona** (infrastructure engineer / planner, technically strong but not a semantic-web specialist) to check it lands with the intended audience rather than a knowledge-engineering audience. Findings and the revisions already folded into Sections 2–4 above:

| Criterion | v1 draft issue found | Revision applied | Resulting confidence |
|---|---|---|---|
| **Opens with relevance, not definitions** | v1 opened with "an ontology is a formal specification of concepts..." — too abstract, loses a booth visitor in the first sentence. | Rewritten to open with the cross-border data-mismatch pain point before naming the concept (Section 3, "Opening"). | High |
| **Jargon level** | v1 led with RDF/OWL/SPARQL terminology up front. | Technical vocabulary (RDF, OWL, SPARQL, dereferenceable URI) moved to secondary sentences or footnotes, always after a plain-language analogy has landed first. | High |
| **Analogy fits the audience's world** | Generic analogies ("like a shared library catalogue") tested poorly — librarians resonate, engineers don't. | Replaced with an ETCS/signalling-rulebook analogy, since it maps a familiar interoperability concept (shared meaning across systems) onto the new one. | High |
| **Concreteness** | v1 stayed abstract about "combining data across systems." | Added a specific, checkable example: cross-border query for ETCS Level 2 lines between two named countries, and named URI examples (`.../Track`, `.../OperationalPoint`). | Medium–High — needs a real, tested query confirmed against the live RINF SPARQL endpoint before the event (see Section 7, item 4). |
| **Length for a trade-fair booth** | v1 was a single ~6-minute block — too long for someone standing at a booth. | Split into a 30-second hook, a 3-minute booth version, and a separate 7–8 minute workshop version, so staff can match length to visitor engagement. | High |
| **Clear "so what" for the visitor's own job** | v1 ended on a mission-style statement about "European interoperability" with no visitor-specific payoff. | Added role-specific payoffs (infrastructure manager vs. manufacturer) before the call to action (Section 3, "Why it matters to you"). | High |
| **Actionable close** | v1 had no explicit next step. | Added a concrete call to action (live demo, QR code, contact) at the end of every format. | High — pending real booth number / QR code / contact being filled in. |

**Overall assessment:** the script now leads with the visitor's problem, uses a railway-native analogy, defers jargon, and closes with a specific action — the profile most likely to satisfy a non-specialist railway-expert audience at a trade fair. The remaining open risk is factual/legal precision (see Section 7) rather than framing or tone.

---

## 7. Before this goes into production — checklist

- [ ] Confirm current ERA vocabulary/ontology **version number** and **legal status wording** directly with ERA's Interoperable Data Programme team before printing any material (versions and legal framing can change between now and September 2026).
- [ ] Confirm and rehearse a **real, working SPARQL query** against the live RINF knowledge graph endpoint for the booth demo (don't rely on this script's example query without testing it).
- [ ] Fill in `[booth number]`, `[QR code]`, and `[contact]` placeholders once InnoTrans 2026 booth logistics are confirmed.
- [ ] Confirm the exact GitLab/GitHub repository link to share with technical visitors (e.g., the ERA Ontology group repository).
- [ ] Have a compliance-aware colleague sign off on the FAQ answer to "Is this mandatory?" — this is the question most likely to be pressed on by regulators/NSAs.
- [ ] Pilot the 3-minute booth talk and the FAQ live with 2–3 colleagues playing the "railway expert" role, and update Section 6 with real feedback once available.
- [ ] Translate the elevator pitch (Section 2) into German for the Berlin venue, if booth staff will engage German-speaking visitors directly.

---

## 8. From this script to dissemination materials — production checklist

Use each script section as the source text for a specific deliverable:

| Deliverable | Source section | Notes |
|---|---|---|
| Roll-up banner / poster headline + subhead | Section 1 (core sentence) | Keep to the one-sentence anchor plus a single visual (e.g., the ETCS-rulebook analogy or a "before/after" data diagram). |
| One-pager / leave-behind | Sections 1, 3, 5 | Front: elevator pitch + "why it matters to you." Back: 2–3 FAQ entries + QR code. |
| Booth staff briefing sheet | Sections 2, 3, 5, 6 | Print full booth talk + FAQ for rehearsal; the satisfaction review explains *why* the script is phrased this way, useful for staff who improvise. |
| Workshop / side-event slide deck | Section 4 | One slide per bullet block; keep the live-demo moment on its own slide with nothing else on it. |
| Social media teaser (LinkedIn/X) | Section 2 | Trim the elevator pitch to ~280 characters, keep the question-opening hook, link to the vocabulary browser. |
| Live demo script | Section 4, Slide 5 + Section 7 checklist | Must be tested against the real SPARQL endpoint before the event — do not present an untested query live. |

---

## 9. Glossary (plain language, for booth staff who need a quick refresher)

- **Ontology** — a machine-readable definition of the concepts in a domain (e.g., "Track," "Operational Point") and how they relate, so different systems interpret the same data the same way.
- **ERA vocabulary / ERA ontology** — the EU Agency for Railways' ontology for railway infrastructure and rolling stock data, published at `data.europa.eu/949`.
- **RINF** — Register of Infrastructure, the EU's register of railway network characteristics, published as Linked Data / a knowledge graph since 2021.
- **RDF / OWL** — the technical languages the ontology is written in (Resource Description Framework / Web Ontology Language). Not needed by most end users.
- **SPARQL** — the query language used to ask questions of RDF data (e.g., "list all tracks with ETCS Level 2 between two countries").
- **Dereferenceable URI** — a web address that, when opened, returns the definition of that concept (e.g., `http://data.europa.eu/949/Track`).
- **RailTopoModel / railML3** — existing railway data standards the ERA ontology is deliberately aligned with, not competing against.
- **Interoperability (data layer)** — the ability of independently-built systems to exchange and correctly interpret each other's data without manual reconciliation.

---

## 10. Sources used to fact-check this script

- ERA Vocabulary (ERA Ontology) — [Interoperable Europe Portal](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology)
- ERA Knowledge Graph — [European Union Agency for Railways](https://www.era.europa.eu/domains/registers/era-knowlege-graph_en)
- ERA Ontology (versioned browsable vocabulary) — [rinf.data.era.europa.eu/era-vocabulary](https://rinf.data.era.europa.eu/era-vocabulary/)
- ERA Ontology group repository — [GitLab: era-europa-eu/public/interoperable-data-programme/era-ontology](https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/era-ontology)
- Community mirror/docs — [GitHub: Interoperable-data/ERA_vocabulary](https://github.com/Interoperable-data/ERA_vocabulary)
- "Leveraging semantic technologies for digital interoperability in the European Railway domain" (ISWC 2021 In-Use) — [julianrojas.org](https://julianrojas.org/papers/iswc2021-in-use/)
- InnoTrans 2026 dates and venue — [InnoTrans official site](https://www.innotrans.de/en) (22–25 September 2026, Berlin ExpoCenter City)

**All version numbers, legal-status wording, and endpoint URLs above should be re-verified close to the event date (see Section 7) — ontology versions and legal framing can change.**
