# Dissemination Script — "What is an Ontology, and Why Does Railway Data Need One?"

**Event:** InnoTrans 2026, Berlin ExpoCenter City, 22–25 September 2026
**Audience:** Railway experts (infrastructure managers, railway undertakings, National Safety Authorities, rolling stock manufacturers, signalling engineers) — technical but **not** semantic-web/IT specialists
**Speaker role:** Booth staff / dissemination officer for the ERA ontology (railway semantic interoperability)
**Formats included:** 30-second elevator pitch · 3-minute booth talk · 7–8 minute workshop/theatre talk · FAQ · audience-satisfaction review · production checklist

---

## 0. How to use this file

This is a **working script**, not a finished slide deck. Use it to:

1. Brief booth staff so everyone tells the same story, in the same order, with the same examples.
2. Draft the poster / roll-up / one-pager copy (Section 10 gives you the checklist).
3. Rehearse against the audience-satisfaction review in Section 8 before printing anything.

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

## 5. Top 5 interoperability queries for the live demo (from the ERA "Data stories")

**⚠️ Access note:** `data-interop.era.europa.eu` (and `era.europa.eu`) could not be fetched directly from this session — both domains are blocked by this environment's network egress policy (a 403-class organisational block, not a transient error). The table below is **reconstructed from the closest available public secondary source**: Vladimir Alexiev's *RailDataForum2025-SPARQL* tutorial, which explicitly states it works from **"RINF data stories represented as competency questions"** against the same `data-interop.era.europa.eu` SPARQL endpoint (ontology v3.0.1, presented at the 2025 Rail Data Forum). It is a strong proxy, not a verified transcript of the live "Data stories" page.

**Before InnoTrans, someone with access must:**
1. Open `data-interop.era.europa.eu` → **Data stories** section directly.
2. Confirm whether these 5 are indeed featured there (titles may differ) or swap in the site's actual top stories.
3. Copy the *exact* SPARQL text and run it live against the endpoint at least once before the booth demo — do not present the illustrative queries below as verified.

With that caveat, here are 5 stories that best "showcase interoperability using the ontology" for a railway-expert audience — chosen because together they span the five different *kinds* of interoperability payoff the ontology delivers (cross-country comparison, national filtering reuse, cross-country aggregation, temporal/versioning consistency, and network topology construction):

| # | Data story | Competency question (plain English) | What it demonstrates about interoperability | Illustrative SPARQL sketch *(verify before use)* |
|---|---|---|---|---|
| 1 | **Longest tunnel in Europe** | "What is the single longest railway tunnel, and where is it?" | The same `Tunnel` class and `length` property are populated identically by every member state's infrastructure manager, so a single query can rank assets across 27 countries — something no single national register could answer on its own. | `SELECT ?tunnel ?country ?length WHERE { ?tunnel a era:Tunnel ; era:length ?length ; era:inCountry/skos:prefLabel ?country . FILTER(lang(?country)="en") } ORDER BY DESC(?length) LIMIT 1` |
| 2 | **Tunnels in a given country (e.g. Romania), ranked** | "What are the top 3 longest tunnels in Romania?" | Shows the *same* query pattern from Story 1 works unmodified for any country just by changing one filter value — proof that the data model, not a bespoke per-country integration, is doing the work. | `SELECT ?tunnel ?length WHERE { ?tunnel a era:Tunnel ; era:length ?length ; era:inCountry/skos:prefLabel "Romania"@en . } ORDER BY DESC(?length) LIMIT 3` |
| 3 | **Tunnel counts and average length, by country** | "How many tunnels does each country have, and how long are they on average?" | A cross-border aggregate/analytics query — the kind of question a planner or manufacturer would ask when comparing network characteristics across the EU, only possible because every country's tunnels share one class and one unit of measurement. | `SELECT ?country (COUNT(?tunnel) AS ?n) (SUM(?length) AS ?total) (AVG(?length) AS ?avg) WHERE { ?tunnel a era:Tunnel ; era:length ?length ; era:inCountry/skos:prefLabel ?country . FILTER(lang(?country)="en") } GROUP BY ?country ORDER BY DESC(?n)` |
| 4 | **Same asset, tracked over time (canonical URIs)** | "This infrastructure element has been updated many times — how do I know it's still the same real-world asset?" | Directly demonstrates *temporal* interoperability: infrastructure changes (electrification upgrades, gauge changes) are versioned, but a stable "canonical" URI lets any consuming system recognise that record N and record N+1 describe the same physical track or structure. Good story for audiences worried about "which version is authoritative." | `SELECT ?canonical (COUNT(?version) AS ?nVersions) WHERE { ?version era:canonicalURI ?canonical . } GROUP BY ?canonical HAVING (COUNT(?version) > 1) ORDER BY DESC(?nVersions)` |
| 5 | **Operational points connected by sections of line (network graph, e.g. Bulgaria)** | "Which stations/operational points are directly connected, and how does the network fit together?" | A `CONSTRUCT` query that turns individually-published `SectionOfLine` and `OperationalPoint` records into a connected network graph — the clearest visual proof that independently-maintained national records combine into one usable topology, which is exactly what cross-border path planning needs. Strongest **visual** demo for a booth screen. | `CONSTRUCT { ?op1 era:connectedTo ?op2 } WHERE { ?sol a era:SectionOfLine ; era:opStart ?op1 ; era:opEnd ?op2 ; era:inCountry/skos:prefLabel "Bulgaria"@en . }` |

**Booth delivery tip:** run Story 1 first (universally relatable — "the longest tunnel in Europe" is a good hook), then Story 2 live-edited in front of the visitor to change the country filter to *their* country (makes the "same query, any country" point land physically, not just verbally), then close on Story 5's graph visualisation if the booth has a screen — it's the most visually convincing proof of interoperability.

---

## 6. The "follow your nose" demo — ERA graph browser (bubble visualization)

**✅ Verified against real screenshots (hop 1 and hop 2 of the click-through, plus three bonus finds).** `graph.data.era.europa.eu` is still blocked from this session's own network access (same policy as the other `*.era.europa.eu` subdomains), so this section can't be independently re-browsed — but the user supplied seven screenshots of the live bubble view (Brussels Airport – Zaventem; the Section of Line reached from it; a Track/Running-track node; an infrastructure-manager reuse "hub"; and a validity-period / end-date reuse pair), so the content below is confirmed, not illustrative, for two full hops plus three extra finds. Several bubble labels are still cut off on a phone-width screen (`...`) — those are marked below and should be read in full on a wider screen before the event.

### The concept, in plain language

"Follow your nose" is one of the founding principles of Linked Data, first articulated by Tim Berners-Lee: give someone a URI, and looking it up should return not just data about that one thing, but **links to other URIs** — so a person (or a machine) can discover related information simply by clicking through, the same way you'd click from one Wikipedia article to another, without ever needing a pre-built map of "everything that connects to everything." ([W3C Design Issues: Linked Data](https://www.w3.org/DesignIssues/LinkedData.html))

The ERA graph browser at `graph.data.era.europa.eu/graphs-visualizations` is a literal, visual implementation of that idea for railway data: give it any ERA ontology URI, and it draws a **bubble graph** — the resource you asked about sits in the centre, and every RDF fact about it (its properties, and every other resource it links to) appears as a connected bubble around it. Click any linked bubble, and the browser re-centres on *that* resource, revealing its own links in turn. No query language, no integration code — just clicking.

**Tool note (confirmed from screenshot chrome):** the browser is Ontotext **GraphDB Workbench**'s "Visual graph" / class-relations explorer (footer reads "GraphDB · RDF4J · Workbench", left-hand icon rail has Import, Visual graph — the one used here, highlighted red — SPARQL, class hierarchy, Settings and Help icons). Worth knowing for the booth: it's an off-the-shelf triplestore UI feature pointed at the ERA data, not a bespoke ERA-built app — which is itself a nice aside on how little custom tooling is needed once data is published as standard RDF.

### Worked example: the operational point in the URL you gave (confirmed, hop 1)

`http://data.europa.eu/949/operationalPoint/a8e453be0d` resolves to **"Brussels Airport – Zaventem"** — the `era:OperationalPoint` for Brussels Airport station in Belgium. The live bubble view shows, radiating out from the central "Brussels Airport – Zav…" node:

| Bubble (as shown) | Edge label from the centre | What it is |
|---|---|---|
| `BEFBNL` | Canonical URI | The stable, canonical identifier for this operational point (survives across versioned/temporal updates — the same mechanism Section 5, Story 4 describes). |
| `BE00219` | Primary location | A national/reference location code for the point. |
| Operational Point | type | Confirms the resource's own class. |
| Infrastructure element | type | The broader class `OperationalPoint` is a subclass of — both are asserted as RDF types. |
| `station` | Type of operational point | The operational-point category (as opposed to e.g. a junction or border point). |
| Belgium | in country | The member state responsible for this record. |
| Validity period from 20… | validity | The time window this version of the record is valid for (truncated in the screenshot — confirm exact date on a full screen). |
| Railway location of OP… | net reference | Links to the point's location on the rail network model. |
| Section of Line Brusse… | Operational point at **start** of section of line | The section of line that begins here — **this is the "next hop" to click for the cross-border/cross-station story.** |
| Section of Line Y.Luch… | Operational point at **end** of section of line | The section of line that ends here, coming from the other direction. |
| 3× "…Nat. Luchthav…" bubbles | is part of / has part (reciprocal pairs) | Likely alternate-language name variants or related sub-records (e.g. Dutch "Brussel Nationaal Luchthaven") — text is truncated in the screenshot; confirm the full labels before using this specific detail in the script. |

This is a strong real example precisely because it's an airport station: every railway expert immediately understands "Brussels Airport," which makes the abstraction land fast before the demo clicks deeper into the graph.

### Worked example, hop 2 (confirmed): clicking through to the Section of Line

Clicking the "Section of Line Brusse…" bubble from hop 1 re-centres the graph on that resource. The live bubble view shows:

| Bubble (as shown) | Edge label from the centre | What it is |
|---|---|---|
| `0364_BEFBNL_BEYBR…` | Canonical URI | The stable identifier for this section of line. |
| `0364` | National line identification | The official national line number. |
| Section Of Line | type | Confirms the resource's own class. |
| Infrastructure element | type | The broader superclass, same pattern as hop 1. |
| Validity period from 20… | validity | Same versioning mechanism as hop 1 (truncated — confirm full date on a wide screen). |
| Belgium | in country | Same member state as hop 1 — the line doesn't cross a border here, but the mechanism is identical wherever it does. |
| Regular SoL | Nature of Section of Line | The section's category. |
| Brussels Airport – Zav… | Operational point at **start** of section of line | Links straight back to hop 1 — the graph is genuinely bidirectional. |
| **Y.Brucargo (from 2019…)** | Operational point at **end** of section of line | **The payoff of the click:** a completely different real place — Brussels' rail **freight yard** (Brucargo), reached from the airport passenger station with zero integration code, just by following one link. |
| IM role of the body wit… | infrastructure manager | Which organisation is responsible for this section (see the bonus finding below — this single record is reused across dozens of other elements). |
| 1238-1 / 1238-2 (from 2017-09…) | is part of / has part (reciprocal) | The physical track segments that make up this section of line. |

**This is the strongest single moment in the demo**: two clicks, zero code, and you've gone from an airport passenger terminal to a freight yard — a concrete, visual proof that the graph really does connect *different kinds* of real infrastructure, not just relabelled copies of the same thing.

### Bonus finding: the reuse "hub" (infrastructure manager role)

A separate screenshot shows what happens when you click through to "IM role of the body wit…" itself (the `infrastructure manager` bubble from both hops above): it becomes the centre of a graph with **dozens** of incoming links — numbered line/section identifiers like `1296-1 (from 2026-0…)`, `334-1 (from 2026-06-…)`, `1877-2 (from 2025-06-…)`, each pointing *in* via the same `infrastructure manager` predicate — plus a `type → Organisation Role` edge and a `has organisation role → Infrastructure Manage[r]` edge to the actual organisation (Infrabel).

**Why this is worth its own beat in the pitch:** it's the clearest possible illustration of *reuse*, the other half of the interoperability story alongside Section 5's cross-border queries. One canonical "who's responsible for this" record is referenced by every line segment that organisation manages, instead of every infrastructure element re-stating the manager's details separately. Consider it for a second demo screen or a follow-up slide if a technical visitor wants to go deeper than the two-hop airport → freight-yard story.

### Bonus finding: real-world data completeness, honestly

A third screenshot (clicking one of hop 1's "…Nat. Luchthav…" bubbles) shows it resolves to a **Running Track** — `era:InfrastructureElement`, nominal track gauge `1435` (mm, standard gauge) — sitting alongside several properties explicitly valued **"Not provided"** or **"Not applicable"** (e.g. `Category of line`, `Gauging`, `Document with the tra…`, `EC declaration of verifi…`). This is a useful, honest talking point if a visitor pushes on "is the data actually complete?": the ontology defines the field for every TSI-required parameter; population is ongoing and visibly incomplete in places, which is exactly what a real, evolving EU-wide register looks like — not a marketing claim of perfection.

### Bonus finding: the validity-period reuse hub (and a W3C standards tie-in)

Two more screenshots follow the "validity" link from a "Validity period from 20…" bubble itself. The first shows that a **single** validity-period resource is the `validity` target for a whole cluster of unrelated infrastructure elements at once — real Belgian track/line-section names like `Anvers - Central-2…`, `Kontich - Voie V - Secti…`, `Diest - Voie II - Section`, `Malines - Voie V - Sect…`, `Antwerpen - Berchem…` (repeated several times — clearly many distinct track segments through that station), and even `Brussel Nat. Luchthav…` from hop 1 — all pointing **in** to the same validity-period node via `validity`. It also carries two `type` edges: **`Temporal Feature`** and **`Temporal entity`**.

Clicking through to that validity period's own `has end` link (second screenshot) lands on **`date_2078-12-31`** — and *that* node turns out to be an even bigger hub: dozens of *different* "Validity period from 20…" resources across the dataset all share this exact same end date, typed as a **`Time instant`**.

**Why this is worth mentioning:** two things stack up here. First, it's the same *reuse* pattern as the infrastructure-manager hub above, but even more relatable — `2078-12-31` is doing the job of "valid indefinitely / no known expiry," shared as one canonical value instead of being re-typed on every record. Second, `Temporal Feature` / `Temporal entity` / `Time instant` are the class names from the **W3C Time Ontology (OWL-Time)** — meaning ERA didn't invent its own way of modelling "when is this valid," it reused an existing W3C standard. That's a concrete, checkable example of the ontology practicing the interoperability it preaches: reusing established vocabularies, not just publishing railway-specific ones.

### Suggested booth script (hop 1 and hop 2 both confirmed)

> "Let's not talk about this abstractly — let's just click. Here's Brussels Airport station in the register [open the URI in the browser]. See the bubbles around it? Each one is a fact Belgium's infrastructure manager entered — its country, its canonical ID `BEFBNL`, the fact it's a station. Now watch: I click *this* bubble, 'Section of Line' [click the 'Operational point at start of section of line' bubble] — and we jump, with zero integration code, to the section of track leaving this station. See its national line number, `0364`? Now one more click [click 'Operational point at end of section of line'] — and we land on `Y.Brucargo`. That's not another passenger station — that's Brussels' **freight yard**. Two clicks, zero integration code, from an airport to a cargo terminal. That's 'follow your nose' — the same trick that makes clicking through Wikipedia effortless, except every link here is a verified railway fact, maintained by the responsible infrastructure manager, not a hyperlink someone typed by hand."

### Why this belongs alongside Section 5

Section 5's SPARQL queries prove interoperability *analytically* (ask a question across borders, get one answer). This bubble browser proves it *experientially* — a non-technical visitor can feel the "same data model everywhere" point by clicking, without seeing a line of query syntax. Use Section 5 for visitors who want the "how," and this browser for visitors who just want to *see* it work. On a booth screen or tablet, this is likely the single most shareable 60-second moment.

### Explainer video mockup

`scripts/assets/era-follow-your-nose-demo.mp4` (source: `scripts/assets/era-follow-your-nose-scene.html`) is a ~35-second animated mockup built to pitch this booth moment before the event: a stylized, 3D-look bubble graph with **oriented links** (directional arrowheads matching the live tool — single-headed for one-way facts, double-headed for reciprocal `is part of` / `has part` pairs), auto-clicking through the confirmed hop-1 data (Canonical URI, in country, type of operational point), then the "start of section of line" hop, then landing on the confirmed hop-2 payoff — Y.Brucargo — before a closing card.

**This is a concept mockup, not a screen recording of the live tool** — it was generated from the HTML/CSS/JS scene file with a headless browser. As of this version, every bubble and edge label it shows for both hops is drawn from the verified screenshots in this section (no more generic placeholders) — the remaining gap is that it's a stylized re-creation, not pixel-accurate footage of the real UI's chrome, fonts, or exact positions. Use it to brief booth staff and storyboard the real click-through, and swap it for actual screen-recorded footage of `graph.data.era.europa.eu` once that's captured (see the Section 9 checklist).

---

## 7. Anticipated questions (FAQ)

| Question a railway expert is likely to ask | Short answer to give at the booth |
|---|---|
| "Is this just another data format / schema?" | No — a schema defines structure (fields, types); an ontology also defines *meaning* and *relationships*, and is designed to be linked and queried across independently-published datasets, not just parsed by one application. |
| "Do I need to know RDF/OWL/SPARQL to use this?" | No. Most users interact with RINF through the standard web interface. RDF/SPARQL matters to the systems and integrators behind the scenes — the same way you don't need to know ETCS message formats to benefit from ETCS. |
| "Is this mandatory?" | The ERA vocabulary is a technical document issued under Directive (EU) 2016/797, underpinning mandatory registers like RINF. Ask `[insert current legal/compliance answer confirmed with ERA before the event]` for the precise compliance scope relevant to the visitor's role. |
| "How is this different from railML?" | The ERA ontology is aligned with railML3 and RailTopoModel rather than competing with them — it reuses their concepts as the semantic backbone for the EU's official infrastructure register. |
| "What do I actually get if my organisation adopts it?" | Reduced one-off integration cost per partner/country, machine-checkable conformity, and infrastructure data that's reusable beyond its original purpose (e.g., by manufacturers, planners, or future AI/digital-twin tools). |
| "Where can I see it / try it myself?" | Point to the live demo, the vocabulary browser QR code, and `[GitLab/GitHub repository link placeholder]` for anyone technical who wants to inspect it directly. |
| "This all sounds abstract — can I actually see how one piece of data connects to another?" | Yes — open the ERA graph browser (`graph.data.era.europa.eu`), paste in any ERA URI, and click through the bubbles it draws. That's the Section 6 demo: no query language needed, just clicking from one linked fact to the next. |
| "Did ERA invent all of this from scratch, or reuse existing standards?" | Reuse where it made sense: alongside RailTopoModel/railML3 for the railway concepts, the "validity period" mechanism reuses the **W3C Time Ontology** (`Temporal Feature`, `Time instant`) — see Section 6's validity-period bonus finding. |

---

## 8. Audience-satisfaction review (self-review pass)

Before this script is used live, it was reviewed against a **railway-expert persona** (infrastructure engineer / planner, technically strong but not a semantic-web specialist) to check it lands with the intended audience rather than a knowledge-engineering audience. Findings and the revisions already folded into Sections 2–4 above:

| Criterion | v1 draft issue found | Revision applied | Resulting confidence |
|---|---|---|---|
| **Opens with relevance, not definitions** | v1 opened with "an ontology is a formal specification of concepts..." — too abstract, loses a booth visitor in the first sentence. | Rewritten to open with the cross-border data-mismatch pain point before naming the concept (Section 3, "Opening"). | High |
| **Jargon level** | v1 led with RDF/OWL/SPARQL terminology up front. | Technical vocabulary (RDF, OWL, SPARQL, dereferenceable URI) moved to secondary sentences or footnotes, always after a plain-language analogy has landed first. | High |
| **Analogy fits the audience's world** | Generic analogies ("like a shared library catalogue") tested poorly — librarians resonate, engineers don't. | Replaced with an ETCS/signalling-rulebook analogy, since it maps a familiar interoperability concept (shared meaning across systems) onto the new one. | High |
| **Concreteness** | v1 stayed abstract about "combining data across systems." | Added a specific, checkable example: cross-border query for ETCS Level 2 lines between two named countries, and named URI examples (`.../Track`, `.../OperationalPoint`). Section 5 now adds 5 fuller demo-ready queries, and Section 6 adds a click-through visual demo. | Medium–High — Section 5's queries and Section 6's bubble-view walkthrough are both reconstructed from secondary sources, not the live ERA site (blocked in this session); need verification against the real endpoint/tool before the event (see Section 9). |
| **Length for a trade-fair booth** | v1 was a single ~6-minute block — too long for someone standing at a booth. | Split into a 30-second hook, a 3-minute booth version, and a separate 7–8 minute workshop version, so staff can match length to visitor engagement. | High |
| **Clear "so what" for the visitor's own job** | v1 ended on a mission-style statement about "European interoperability" with no visitor-specific payoff. | Added role-specific payoffs (infrastructure manager vs. manufacturer) before the call to action (Section 3, "Why it matters to you"). | High |
| **Actionable close** | v1 had no explicit next step. | Added a concrete call to action (live demo, QR code, contact) at the end of every format. | High — pending real booth number / QR code / contact being filled in. |

**Overall assessment:** the script now leads with the visitor's problem, uses a railway-native analogy, defers jargon, and closes with a specific action — the profile most likely to satisfy a non-specialist railway-expert audience at a trade fair. The remaining open risk is factual/legal precision (see Section 9) rather than framing or tone.

---

## 9. Before this goes into production — checklist

- [ ] Confirm current ERA vocabulary/ontology **version number** and **legal status wording** directly with ERA's Interoperable Data Programme team before printing any material (versions and legal framing can change between now and September 2026).
- [ ] Confirm and rehearse a **real, working SPARQL query** against the live RINF knowledge graph endpoint for the booth demo (don't rely on this script's example query without testing it).
- [ ] Fill in `[booth number]`, `[QR code]`, and `[contact]` placeholders once InnoTrans 2026 booth logistics are confirmed.
- [ ] Confirm the exact GitLab/GitHub repository link to share with technical visitors (e.g., the ERA Ontology group repository).
- [ ] Have a compliance-aware colleague sign off on the FAQ answer to "Is this mandatory?" — this is the question most likely to be pressed on by regulators/NSAs.
- [ ] Verify the Section 5 "Top 5" data stories and SPARQL text directly against `data-interop.era.europa.eu` → Data stories (this session's network egress policy blocked that domain, so Section 5 is currently a secondary-source reconstruction, not a verified transcript).
- [ ] Hop 1 and hop 2 of the Section 6 bubble view (Brussels Airport – Zaventem → Section of Line → Y.Brucargo) are confirmed from screenshots, plus two bonus finds (the infrastructure-manager reuse hub; a Track node with real/missing TSI parameters). Still needed: the full, untruncated text of a few labels cut off on a phone screen (e.g. "Validity period from 20…", the exact date), confirmed on a wider screen.
- [ ] `scripts/assets/era-follow-your-nose-demo.mp4` is a generated mockup, not real screen-capture footage — all bubble content is now drawn from verified screenshots, but it's still a stylized re-creation, not pixel-accurate footage of the real UI. Before using it publicly: replace (or supplement) it with an actual screen recording of `graph.data.era.europa.eu`.
- [ ] Pilot the 3-minute booth talk and the FAQ live with 2–3 colleagues playing the "railway expert" role, and update Section 8 with real feedback once available.
- [ ] Translate the elevator pitch (Section 2) into German for the Berlin venue, if booth staff will engage German-speaking visitors directly.

---

## 10. From this script to dissemination materials — production checklist

Use each script section as the source text for a specific deliverable:

| Deliverable | Source section | Notes |
|---|---|---|
| Roll-up banner / poster headline + subhead | Section 1 (core sentence) | Keep to the one-sentence anchor plus a single visual (e.g., the ETCS-rulebook analogy or a "before/after" data diagram). |
| One-pager / leave-behind | Sections 1, 3, 5 | Front: elevator pitch + "why it matters to you." Back: 2–3 FAQ entries + QR code. |
| Booth staff briefing sheet | Sections 2, 3, 5, 6 | Print full booth talk + FAQ for rehearsal; the satisfaction review explains *why* the script is phrased this way, useful for staff who improvise. |
| Workshop / side-event slide deck | Section 4 | One slide per bullet block; keep the live-demo moment on its own slide with nothing else on it. |
| Social media teaser (LinkedIn/X) | Section 2 | Trim the elevator pitch to ~280 characters, keep the question-opening hook, link to the vocabulary browser. |
| Live demo script | Section 4, Slide 5 + Section 5 (query catalogue) + Section 6 (bubble browser walkthrough) + Section 9 checklist | Must be tested against the real SPARQL endpoint and graph browser before the event — do not present an untested query or click-path live. |
| Social media / booth-screen teaser video | Section 6, "Explainer video mockup" (`scripts/assets/era-follow-your-nose-demo.mp4`) | Storyboard/pitch only — replace with real screen-recorded footage before publishing externally (see Section 9 checklist). |

---

## 11. Glossary (plain language, for booth staff who need a quick refresher)

- **Ontology** — a machine-readable definition of the concepts in a domain (e.g., "Track," "Operational Point") and how they relate, so different systems interpret the same data the same way.
- **ERA vocabulary / ERA ontology** — the EU Agency for Railways' ontology for railway infrastructure and rolling stock data, published at `data.europa.eu/949`.
- **RINF** — Register of Infrastructure, the EU's register of railway network characteristics, published as Linked Data / a knowledge graph since 2021.
- **RDF / OWL** — the technical languages the ontology is written in (Resource Description Framework / Web Ontology Language). Not needed by most end users.
- **SPARQL** — the query language used to ask questions of RDF data (e.g., "list all tracks with ETCS Level 2 between two countries").
- **Dereferenceable URI** — a web address that, when opened, returns the definition of that concept (e.g., `http://data.europa.eu/949/Track`).
- **RailTopoModel / railML3** — existing railway data standards the ERA ontology is deliberately aligned with, not competing against.
- **Interoperability (data layer)** — the ability of independently-built systems to exchange and correctly interpret each other's data without manual reconciliation.

---

## 12. Sources used to fact-check this script

- ERA Vocabulary (ERA Ontology) — [Interoperable Europe Portal](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology)
- ERA Knowledge Graph — [European Union Agency for Railways](https://www.era.europa.eu/domains/registers/era-knowlege-graph_en)
- ERA Ontology (versioned browsable vocabulary) — [rinf.data.era.europa.eu/era-vocabulary](https://rinf.data.era.europa.eu/era-vocabulary/)
- ERA Ontology group repository — [GitLab: era-europa-eu/public/interoperable-data-programme/era-ontology](https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/era-ontology)
- Community mirror/docs — [GitHub: Interoperable-data/ERA_vocabulary](https://github.com/Interoperable-data/ERA_vocabulary)
- "Leveraging semantic technologies for digital interoperability in the European Railway domain" (ISWC 2021 In-Use) — [julianrojas.org](https://julianrojas.org/papers/iswc2021-in-use/)
- InnoTrans 2026 dates and venue — [InnoTrans official site](https://www.innotrans.de/en) (22–25 September 2026, Berlin ExpoCenter City)
- Section 5 query catalogue reconstructed from — [GitHub: VladimirAlexiev/RailDataForum2025-SPARQL](https://github.com/VladimirAlexiev/RailDataForum2025-SPARQL) (Rail Data Forum 2025 SPARQL tutorial against `data-interop.era.europa.eu`, ERA ontology v3.0.1). **`data-interop.era.europa.eu` itself was not reachable from this session (blocked by network egress policy) — its actual "Data stories" section must be checked directly before the event.**
- "Follow your nose" Linked Data principle — [W3C Design Issues: Linked Data, Tim Berners-Lee](https://www.w3.org/DesignIssues/LinkedData.html)
- ERA graph browser (bubble visualization tool, built on **Ontotext GraphDB Workbench**'s Visual graph feature) — `graph.data.era.europa.eu/graphs-visualizations`. Not reachable from this session's own network access (blocked by network egress policy, same as the other `*.era.europa.eu` subdomains). **All of Section 6's worked examples and bonus findings (hop 1, hop 2, and the infrastructure-manager / Track / validity-period finds) are confirmed from user-supplied screenshots**, not independently re-browsed by this session.
- W3C Time Ontology (OWL-Time) — [W3C Recommendation](https://www.w3.org/TR/owl-time/), referenced for the `Temporal Feature` / `Time instant` classes seen in Section 6's validity-period bonus finding.

**All version numbers, legal-status wording, endpoint URLs, the Section 5 "Top 5" data stories, and the Section 6 bubble-view walkthrough above should be re-verified close to the event date (see Section 9) — ontology versions, legal framing, and the site's content can change.**
