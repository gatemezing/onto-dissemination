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

**✅ Verified directly over HTTP, not from screenshots (2026-08-16).** This section previously walked through Brussels Airport using nine user-supplied screenshots of `graph.data.era.europa.eu`, because that domain was blocked from the authoring session at the time. That block is no longer in effect: every fact below was fetched live during this session, either from Bane NOR's own Linked Data server (`https://data.banenor.no/data/...`, content-negotiated as JSON-LD) or from the ERA SPARQL endpoint (`graph.data.era.europa.eu/repositories/rinf-plus` and `/repositories/ERA-Onto`) for the shared `era:` URIs Bane NOR's data itself points to. The worked example below now centres on **Oslo S (Oslo Central Station)** — Norway's largest station, published by Bane NOR using the ERA ontology alongside railML3/RailTopoModel — rather than Brussels Airport, matching the dataset now shipped in `scripts/assets/era-graph-explorer-app.html`.

### The concept, in plain language

"Follow your nose" is one of the founding principles of Linked Data, first articulated by Tim Berners-Lee: give someone a URI, and looking it up should return not just data about that one thing, but **links to other URIs** — so a person (or a machine) can discover related information simply by clicking through, the same way you'd click from one Wikipedia article to another, without ever needing a pre-built map of "everything that connects to everything." ([W3C Design Issues: Linked Data](https://www.w3.org/DesignIssues/LinkedData.html))

The ERA graph browser at `graph.data.era.europa.eu/graphs-visualizations` is a literal, visual implementation of that idea for railway data: give it any ERA ontology URI, and it draws a **bubble graph** — the resource you asked about sits in the centre, and every RDF fact about it (its properties, and every other resource it links to) appears as a connected bubble around it. Click any linked bubble, and the browser re-centres on *that* resource, revealing its own links in turn. No query language, no integration code — just clicking.

**Tool note (confirmed from screenshot chrome):** the browser is Ontotext **GraphDB Workbench**'s "Visual graph" / class-relations explorer (footer reads "GraphDB · RDF4J · Workbench", left-hand icon rail has Import, Visual graph — the one used here, highlighted red — SPARQL, class hierarchy, Settings and Help icons). Worth knowing for the booth: it's an off-the-shelf triplestore UI feature pointed at the ERA data, not a bespoke ERA-built app — which is itself a nice aside on how little custom tooling is needed once data is published as standard RDF.

### Worked example: Oslo S, Norway's largest station (hop 1)

`https://data.banenor.no/data/_station_c0576848-8f76-4489-aa6e-ae95b98c1a1c` resolves to **"Oslo S"** — the `era:OperationalPoint` for Oslo Central Station, published by Bane NOR (Norway's national infrastructure manager), radiating out from the central "Oslo S" node:

| Bubble (as shown) | Edge label from the centre | What it is |
|---|---|---|
| Operational Point | type | Confirms the resource's own class. |
| Infrastructure element | type | The broader class `OperationalPoint` is a subclass of — both are asserted as RDF types. |
| `NOOSL` | Unique OP ID | The station's unique operational-point identifier (`era:uopid`). |
| `station` | Type of operational point | The exact same shared ERA vocabulary concept (`era:concepts/op-types/10`) that classified Brussels Airport in the original version of this walkthrough — see the bonus finding below. |
| Oslo S (primary location) | Primary location | A separate `era:PrimaryLocation` resource (code `NO00100`) for the point — see hop 4. |
| Norway | in country | The member state responsible for this record. |
| Validity from 2023-09-17 (no end known) | validity | The time window this version of the record is valid for — see the bonus finding below, it's a genuine reuse hub. |
| IM role of the body with organisation code 0076 | infrastructure manager | Which organisation is responsible for this station — see the bonus finding below, reused three times across this small worked example alone. |
| ØB2 (×2, "has part") | has part | One of **482** real tracks belonging to this station — only this one is individually explored (hop 2); the rest are honestly out of scope for a readable demo bubble graph. |
| OSLS_Nationaltheatret | is part of / has part (reciprocal) | A named subnetwork segment of the wider Oslo area rail network. |
| banenor.no/…/Oslo S | schematic overview | A link to Bane NOR's own human-readable schematic diagram for the station — real external documentation, not a placeholder. |
| OSL (SJN register) | has designator | An alternate, registry-specific code for the station (Norwegian "stedskoder" place-code system, register `SJN`, entry `OSL`). |
| station / passenger operation | operation type | Confirms Oslo S is modelled as a passenger station operation. |

This is a strong real example precisely because it's the country's largest station: every railway expert immediately understands "Oslo Central," which makes the abstraction land fast before the demo clicks deeper into the graph — and because it's Norwegian data using the *same* ontology as the original Belgian example, it doubles as proof the ontology travels across infrastructure managers, not just across borders within one.

### Worked example, hop 2: clicking through to a real track

Clicking the "ØB2" bubble from hop 1 re-centres the graph on that resource — a real secondary track at the station:

| Bubble (as shown) | Edge label from the centre | What it is |
|---|---|---|
| Track | type | Confirms the resource's own class (`era:Track`). |
| `KO-SPO-003462` | Track ID | The track's own identifier in Bane NOR's numbering. |
| `B` | Track direction | An ERA SKOS concept meaning "both directions defined by the Section of Line." |
| `40` | Maximum permitted speed | A real operational value, km/h. |
| `not_electrified` | Contact line system | A reference to Bane NOR's own controlled-vocabulary term for "not electrified" (not independently dereferenced in this curation — shown honestly as a reference, not invented). |
| `3` | has track type | A Bane NOR-specific track-type code. |
| IM role of the body with organisation code 0076 | infrastructure manager | **The same reuse-hub node as hop 1** — the graph really does converge, not just fan out. |
| Norway | in country | Same member state as hop 1. |
| Oslo S | is part of | Links straight back to hop 1 — the graph is genuinely bidirectional. |
| Bane NOR (railML organisational unit) | refers to infrastructure manager (railML) | **A second, independent description of the same real organisation** — this one from Bane NOR's own railML-based ontology instead of the shared ERA vocabulary. Two different modelling approaches, same real-world infrastructure manager. |

**This is the strongest single moment in the demo**: from a station to one of its 482 real tracks, with genuine operational facts (speed, electrification, direction) and two independent organisational descriptions converging on the same real entity — a concrete, visual proof that the graph connects real operational detail, not just relabelled copies of the station record.

### Bonus finding: the reuse "hub" (infrastructure manager role)

Clicking through to "IM role of the body with organisation code 0076" itself (the `infrastructure manager` bubble from both hops above, queried directly from the ERA SPARQL endpoint, not from Bane NOR) becomes the centre of a graph with **incoming** `infrastructure manager` links from every resource in this worked example that names an infrastructure manager: Oslo S itself, the ØB2 track, and the station's primary-location record — plus a `type → Organisation Role` edge and a `has organisation role → IM` edge, and a `role of` edge to the actual organisation, **Bane NOR** (`era:organisations/0076`, `rdfs:label "Bane NOR"`).

**Why this is worth its own beat in the pitch:** it's the clearest possible illustration of *reuse*, the other half of the interoperability story alongside Section 5's cross-border queries — and it's the exact same `era:OrganisationRole` modelling pattern the original Brussels/Infrabel version of this walkthrough used, now confirmed reused by a completely different infrastructure manager in a different country. One canonical "who's responsible for this" record is referenced by every resource that organisation manages, instead of each one re-stating the manager's details separately.

### Bonus finding: the validity-interval reuse hub

Following the "validity" link from Oslo S (or from its primary-location record) lands on the same **`Validity from 2023-09-17 (no end known)`** resource both times — a real, directly-observed reuse hub: this exact validity-interval URI is the `validity` target for both the station and its primary-location record simultaneously. It carries two `type` edges — **`Temporal Feature`** (the ERA class) and **`Interval`** (from the W3C Time Ontology) — and one outgoing `has beginning` edge to a `Time Instant` resource for the date itself, `2023-09-17`.

**Why this is worth mentioning:** two things stack up here, same as in the original Belgian example. First, it's the same *reuse* pattern as the infrastructure-manager hub above — one canonical validity record shared by multiple resources instead of re-typed on each one. Second, `Temporal Feature` / `Interval` / `Instant` are class names from the **W3C Time Ontology (OWL-Time)** — meaning ERA didn't invent its own way of modelling "when is this valid," it reused an existing W3C standard. That's a concrete, checkable example of the ontology practicing the interoperability it preaches: reusing established vocabularies, not just publishing railway-specific ones.

### Worked example, hop 4: the primary-location record, and the hubs again

Hop 1's "Oslo S (primary location)" bubble resolves to a separate `era:PrimaryLocation` resource, `NO00100`:

| Bubble (as shown) | Edge label from the centre | What it is |
|---|---|---|
| Primary Location | type | Confirms the resource's own class. |
| `NO00100` | primary location code | The location's own reference code, distinct from the station's `NOOSL` operational-point ID. |
| Oslo S | primary location name | The human-readable name, duplicated here as its own literal property. |
| Validity from 2023-09-17 (no end known) | validity | **The same validity-interval reuse hub as hop 1** — confirmed pointed to by two different resource types now. |
| Norway | in country | Same member state. |
| IM role of the body with organisation code 0076 | infrastructure manager | **The same infrastructure-manager reuse hub as hops 1 and 2** — now confirmed reused three times across this one small worked example. |

**Why it's worth the extra hop:** it's the cleanest, most concrete demonstration in the whole demo that "reuse" isn't a one-off — the same two canonical resources (one validity interval, one organisation role) get pointed to independently by a station, one of its tracks, and its own location record, exactly what you'd want from a well-modelled shared vocabulary instead of every record re-stating its own copy of the same facts.

### Suggested booth script (all hops fetched live from real endpoints)

> "Let's not talk about this abstractly — let's just click. Here's Oslo S, Norway's largest station, in Bane NOR's own register [open the URI in the browser]. See the bubbles around it? Each one is a fact Bane NOR entered — its country, its unique ID `NOOSL`, the fact it's a station. Now watch: I click *this* bubble, its infrastructure manager [click the 'infrastructure manager' bubble] — and we land on a shared 'who's responsible' record, queried straight from ERA's own European endpoint, not Bane NOR's. Now go back and click into one of the station's 482 real tracks [click 'has part' → ØB2] — real operational facts: maximum speed 40, not electrified, direction 'B'. And look — click its infrastructure manager too [click 'infrastructure manager' on the track] — same bubble as before. Same organisation, same canonical record, reused instead of re-typed, on a station on the other side of Europe from where this ontology was first demonstrated. That's 'follow your nose' — the same trick that makes clicking through Wikipedia effortless, except every link here is a verified railway fact, and the pattern holds whether the infrastructure manager is in Belgium or Norway."

### Why this belongs alongside Section 5

Section 5's SPARQL queries prove interoperability *analytically* (ask a question across borders, get one answer). This bubble browser proves it *experientially* — a non-technical visitor can feel the "same data model everywhere" point by clicking, without seeing a line of query syntax. Use Section 5 for visitors who want the "how," and this browser for visitors who just want to *see* it work. On a booth screen or tablet, this is likely the single most shareable 60-second moment.

### Explainer video mockup — now out of sync with the app, needs regenerating

`scripts/assets/era-follow-your-nose-demo.mp4` (source: `scripts/assets/era-follow-your-nose-scene.html`) is a ~42-second animated mockup, still depicting the **original Brussels Airport walkthrough** (Belgium → Y.Brucargo freight yard → the validity/date reuse hub → Y.Luchthaven), described accurately in the previous version of this section. That content is still true of the video file itself — nothing about the video changed — but as of this rewrite it **no longer matches the interactive app's default dataset**, which now opens on Oslo S. Before using the video and the app together at the booth, either regenerate the video from real Oslo S screen-recorded footage or clicks, or keep presenting them as two independent, self-consistent examples (Brussels for the video, Oslo for the live app) and say so explicitly rather than implying they're the same walkthrough.

### Interactive graph explorer app

`scripts/assets/era-graph-explorer-app.html` is a step further than the video: a real, **interactive** single-file web app — not a scripted animation — built to demonstrate "follow your nose" live at the booth. Paste (or click a quick-link to) any of the verified nodes above, and it draws the same 3D-look oriented bubble graph, now sized per bubble to its own label content and with edges trimmed to the visible gap between bubbles rather than running underneath them; **click any bubble and it actually navigates**, re-centring on that resource, updating a breadcrumb trail (tagged `LIVE` when the trail is live-fetched data, and reset — never mixed with offline nodes — whenever navigation crosses between the two data sources), with a Back button and an info panel showing the node's class and URI. It ships with:

- **An offline dataset**, rebuilt 2026-08-16 around Oslo S and covering every node documented in this section (both hops plus all three bonus finds) — genuinely clickable end-to-end, no network required, so it works even on flaky booth WiFi.
- **A live SPARQL mode** against `https://graph.data.era.europa.eu/repositories/rinf-plus`, the real GraphDB repository behind ERA's own graph browser — verified working end-to-end in a real browser (confirmed CORS headers, confirmed matching data, confirmed multi-hop click-through). An earlier candidate endpoint, `rinf.data.era.europa.eu/api/v1/sparql/rinf`, does not work from a browser: GET requests to it hang with no response, and its CORS policy only allows its own app's origin. Paste *any* ERA URI — including ones outside the curated dataset — switch "Data source" to "Try live ERA SPARQL," and it queries the resource's real outgoing/incoming triples plus best-effort `rdfs:label`/`skos:prefLabel` lookups (including the node's own label, not just its neighbours'), rendering them the same way as the offline nodes. Clicking a live-fetched bubble lazily fetches *that* resource in turn — real "follow your nose" against the live graph, not just the offline dataset. **Correction (2026-08-17):** this repository turns out to mirror non-ERA data too — pasting a Bane NOR URI directly (e.g. Oslo S's own primary-location resource) returns real matching data, though only the subset of properties that map onto the shared ERA vocabulary; Bane NOR's native railML3/`bno:` extension properties aren't mirrored and only show up when dereferencing the resource directly from `data.banenor.no`. For any URI in ERA's own namespace (`http://data.europa.eu/949/`), live mode also explicitly pulls in ERA's ontology graph (class definitions/comments/hierarchy) and SKOS graph (the ~14,700-concept controlled vocabulary), so following a `type` edge to a class, or a value edge to a controlled-vocabulary concept, surfaces real definitions rather than a bare label.
- Basic keyboard accessibility (every bubble and breadcrumb entry is a focusable, `Enter`-activatable control) and a responsive mobile layout.

Tested end-to-end in a real browser (Playwright + system Chrome, not just a headless mock): every offline hop, the breadcrumb/back behaviour and its live/offline separation, the unknown-URI fallback message, live-mode click-through against the real ERA endpoint, and bubble/edge sizing under a real 24-edge live node. Deployed and confirmed live at https://gatemezing.github.io/onto-dissemination/.

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
- [x] Section 6's Oslo S worked example (hops 1–4 plus all three bonus finds) is now fetched and confirmed directly over HTTP from Bane NOR's Linked Data server and the ERA SPARQL endpoint, not from screenshots — done 2026-08-16.
- [ ] `scripts/assets/era-follow-your-nose-demo.mp4` still depicts the *original* Brussels Airport walkthrough and has not been regenerated to match Oslo S — see the "Explainer video mockup" note in Section 6. Before using it publicly: either regenerate it against Oslo S (real screen-recorded footage or clicks), or present it explicitly as a separate Brussels-based example rather than implying it matches the app.
- [x] `scripts/assets/era-graph-explorer-app.html`'s live SPARQL mode now points at `https://graph.data.era.europa.eu/repositories/rinf-plus`, verified end-to-end in a real browser (real data returned, CORS headers confirmed, multi-hop click-through tested) — done 2026-08-16. The offline demo mode (now Oslo S) is also tested end-to-end.
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
- ERA graph browser (bubble visualization tool, built on **Ontotext GraphDB Workbench**'s Visual graph feature) — `graph.data.era.europa.eu/graphs-visualizations`, backed by the SPARQL endpoint `graph.data.era.europa.eu/repositories/rinf-plus`. Reachable and queried directly as of 2026-08-16 — **all of Section 6's worked examples and bonus findings are confirmed by live HTTP requests during this session**, not from screenshots.
- Bane NOR Linked Data — `https://data.banenor.no/data/`, a Fuseki-backed Linked Data server publishing Norwegian railway infrastructure (including Oslo S, Section 6's current worked example) using the ERA ontology alongside railML3/RailTopoModel. Supports standard content negotiation (`Accept: application/ld+json` / `text/turtle` / `application/rdf+xml`) and open CORS.
- W3C Time Ontology (OWL-Time) — [W3C Recommendation](https://www.w3.org/TR/owl-time/), referenced for the `Temporal Feature` / `Time instant` classes seen in Section 6's validity-period bonus finding.

**All version numbers, legal-status wording, endpoint URLs, the Section 5 "Top 5" data stories, and the Section 6 bubble-view walkthrough above should be re-verified close to the event date (see Section 9) — ontology versions, legal framing, and the site's content can change.**
