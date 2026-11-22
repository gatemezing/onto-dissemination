---
theme: default
title: "Build on the rail graph"
info: |
  FOSDEM 2027, Railways and Open Transport devroom, Brussels (30 January 2027). For open data developers. Carto RINF, an interactive map of European rail infrastructure built on live
  SPARQL over the ERA Knowledge Graph, and why the next app should be yours.
  Ghislain Atemezing, European Union Agency for Railways.
author: Ghislain Atemezing
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
routerMode: hash
layout: cover
class: era-cover
---

<div class="era-cover-panel">

<img src="/assets/era-ontology-logo-blue.png" class="w-52 mb-5 -ml-2" alt="ERA Ontology · Interoperable by Design" />

# Build on the rail graph

## Infrastructure, vehicle types, safety documents, telematics codes: Europe's rail registers are public, and joining one knowledge graph. Here is what one app built, and why the next one should be yours.

<div class="mt-8 text-base opacity-95">
<b>Ghislain Atemezing</b><br>
<span class="opacity-75">European Union Agency for Railways</span>
</div>

<div class="mt-4 text-sm opacity-70">FOSDEM 2027 · Railways and Open Transport devroom · Brussels</div>

</div>

<div class="absolute top-0 bottom-0 right-0" style="left: 58%; padding: 40px 30px 40px 20px;">
  <CoverArt />
</div>

<!--
[0:00 → 0:25]
Hello, Railways and Open Transport devroom. I'm Ghislain Atemezing from the European Union Agency for Railways.
This talk is an invitation. Europe's railway infrastructure data is public by law, and ERA publishes it as a knowledge graph you can query in one HTTP call.
I'll show what one small app built on it, what we learned the hard way, and why I think you should build the next one.
-->

---
clicks: 5
---

# Agenda

<div class="mt-10">
<RailAgenda :reveal="$clicks" />
</div>

<div v-click="5" class="card mt-6 text-lg">One idea runs through the talk: <b>the hard part, collecting authoritative data from 28 countries, is already done. What's missing is apps.</b></div>

<!--
[0:25 → 0:40]
Five stops. Click through them:
1 Why this data is open, and who publishes it.
2 What a knowledge graph gives you that a file doesn't.
3 Carto RINF, the proof.
4 The honest part: lessons from real-world data.
5 Your turn: a first query in five minutes, and app ideas.
-->

---
layout: section
---

# Open by law

## Not a pilot, not a hackathon dump: a legal obligation

<RailAgenda :current="0" on-dark class="mt-10" />

---

# Europe's open-data law, 2007 → 2024

<div class="grid grid-cols-5 gap-3 mt-4">
<div v-click class="layer owl"><span class="pill grey">2007</span><h3>INSPIRE</h3><b>Directive 2007/2/EC</b>, Annex I, theme 7 <i>Transport networks</i>: "road, <b>rail</b>, air and water transport networks and related infrastructure".</div>
<div v-click class="layer owl"><span class="pill grey">2019</span><h3>Open Data Directive</h3><b>Directive (EU) 2019/1024</b>: public-sector data re-usable by default, public transport operators included (Art. 1(1)(b)). Transposed by 17 July 2021.</div>
<div v-click class="layer skos"><span class="pill grey">2020 · 2023</span><h3>Data spaces</h3>The <b>European strategy for data</b>, COM(2020) 66, then the <b>common European mobility data space</b>, COM(2023) 751.</div>
<div v-click class="layer shacl"><span class="pill grey">2023</span><h3>High-value datasets</h3><b>Implementing Reg. (EU) 2023/138</b>, applying since 9 June 2024. Mobility is INSPIRE's transport networks: free, <b>API and bulk download</b>, CC BY 4.0 or less restrictive, structure and semantics documented.</div>
<div v-click class="layer xsd"><span class="pill grey">2024</span><h3>Interoperable Europe Act</h3><b>Regulation (EU) 2024/903</b>, applying since 12 July 2024: interoperability and the sharing of reusable solutions become legal duties.</div>
</div>

<div v-click class="card good mt-5">Read the requirements again: <b>APIs, documented semantics, open licences, reusable solutions</b>. That is a knowledge graph's job description, and it is now written into EU law.</div>

<!--
[0:40 → 1:40]
Rail data isn't open by goodwill. Five steps of EU law (click ×5).
INSPIRE, 2007: transport networks, rail named in the text, are spatial data every Member State must share.
The Open Data Directive, 2019: public-sector data is re-usable by default, public transport operators included.
The data strategy, then the common European mobility data space.
High-value datasets, since June 2024: transport-network data must be free, behind an API and a bulk download, under CC BY 4.0 or more open, with its structure and semantics documented.
And the Interoperable Europe Act, in two slides.
(click) Put those requirements together and you've described a knowledge graph.
Q&A: these bind Member States' public bodies (the Directive is addressed to the Member States, Art. 21). ERA's own duty comes from the rail law on the next slide.
-->

---

# Rail infrastructure data is public by law

<div class="grid grid-cols-3 gap-4 mt-3">
<div v-click class="contrib"><div class="num">1</div>

### Each Member State publishes

**Directive (EU) 2016/797, Art. 49**: every Member State publishes a register of infrastructure with the values of its network parameters.

</div>
<div v-click class="contrib"><div class="num">2</div>

### ERA makes it available

**Regulation (EU) 2016/796, Art. 37(3)(h)**: the Agency makes the registers of infrastructure publicly available, through the RINF application.

</div>
<div v-click class="contrib"><div class="num">3</div>

### One entry point, one model

**Implementing Regulation (EU) 2019/777**: RINF is the single entry point, with common specifications for every parameter.

</div>
</div>

<div v-click class="card mt-7">The rail law and the open-data law agree: rail networks are <b>high-value mobility data</b>. Annex 6.1 of <b>Implementing Regulation (EU) 2023/138</b> points to INSPIRE's <i>Transport networks</i>, which names rail.</div>

<div v-click class="card good mt-3">For a developer this means: the data is <b>authoritative</b> (published by the infrastructure managers themselves), <b>maintained</b> (they must keep it up to date), and <b>not going away</b>.</div>

<!--
[1:40 → 2:25]
Now rail law, three steps (click ×3): each Member State must publish a register of infrastructure; ERA must make the registers publicly available; and RINF is the single entry point, with common specifications.
(click) The two bodies of law agree: the high-value-datasets annex points to INSPIRE's transport networks, which names rail.
(click) For you, this is not a one-off dump: it's maintained by the people who run the network, and backed by law.
Q&A: the other registers have their own bases. ERADIS: Directives (EU) 2016/797 and 2016/798 and Regulation (EU) 2016/796 (ERADIS home page). Telematics reference data: Implementing Regulation (EU) 2026/253, the Telematics TSI (teleref portal).
Sources: RINF terms of use (ERA, 2022) quote Art. 49 and Art. 37(3)(h); EUR-Lex for 2019/777, 2023/138 (Annex 6.1) and 2007/2/EC (Annex I, theme 7).
-->

---

# Interoperable Europe Act: interoperability by law

<div class="grid grid-cols-5 gap-6 mt-2">
<div class="col-span-3 rosetta text-sm">

| Regulation (EU) 2024/903 | What it asks |
|---|---|
| Art. 1(2), 2(5) | Applies to **Union entities, agencies included**, and to public sector bodies that run trans-European digital public services |
| Art. 3 | An **interoperability assessment** before new or changed binding requirements, applying since 12 Jan 2025 |
| Art. 4(1), 4(3) | **Share** interoperability solutions on request, with documentation and source code, for example on the **Interoperable Europe portal** |
| Art. 4(6) | Between equivalent solutions, **prefer those without restrictive licensing terms, such as open source** |
| Recital 28 | The **European Interoperability Framework** is the single point of reference |

</div>
<div class="col-span-2">

<div v-click class="card text-sm">An <b>interoperability solution</b> is "a reusable asset concerning legal, organisational, <b>semantic</b> or technical requirements" (Art. 2(4)). An ontology is one.</div>

<div v-click class="card good mt-3 text-sm">The <b>ERA Ontology</b> is listed on the Interoperable Europe portal, in the SEMIC collection, under <b>EUPL 1.2</b> (published 4 Aug 2026).</div>

<div v-click class="tk mt-3 text-sm">For this room: the EU's interoperability law tells public bodies to <b>favour open source</b>. Open apps on open models are what it asks for.</div>

</div>
</div>

<!--
[2:25 → 3:15]
The newest piece, and the one this room should know: the Interoperable Europe Act.
It covers EU institutions, bodies and agencies, and Member States' public bodies, where they regulate or run digital public services across borders. It asks for an interoperability assessment before new binding requirements, and for interoperability solutions to be shared, documentation and source code included, for example on the Interoperable Europe portal. Between equivalent solutions, it says to prefer those without restrictive licences, such as open source.
(click) In the Act's own words, an ontology is an interoperability solution. (click) ERA's is on that portal, under the EUPL. (click) So the law and FOSDEM want the same thing.
Q&A: Art. 3(1) to (4) apply from 12 January 2025, the rest from 12 July 2024 (Art. 23(2)).
-->

---

# Beyond RINF: ERA's public registers

<div class="rosetta text-sm mt-1">

| Register | What's in it | Open today | In the Knowledge Graph |
|---|---|---|---|
| **RINF** | the rail infrastructure of 28 countries | SPARQL · <a href="https://rinf.data.era.europa.eu/">rinf.data.era.europa.eu</a> | **live**: 52,677 operational points, 71 provider graphs, ≈ 42 M triples |
| **Telematics reference data** | organisation codes and primary location codes (TAF/TAP) | <a href="https://teleref.era.europa.eu/">teleref.era.europa.eu</a>: Excel download, location search | **ready**: 5,659 organisation codes (<code>OCR-KG</code>); location codes on RINF's primary locations |
| **ERADIS** | safety certificates, licences, ECM certificates, EC declarations, NoBo certificates | <a href="https://eradis.era.europa.eu/">eradis.era.europa.eu</a>: public, no account | migration ongoing |
| **ERATV** | authorised types of vehicles | <a href="https://eratv.era.europa.eu/Eratv">eratv.era.europa.eu</a>: public list and search | migration ongoing |
| **ERA-Lex** | references to EU rail law | SPARQL | **ready**: 7,317 legal resources |

</div>

<div class="grid grid-cols-2 gap-4 mt-3">
<div class="card text-sm">One model for all of them: the <b>ERA Ontology</b> v3.3.4, a Technical Document under Art. 4(8) of Directive (EU) 2016/797, with SKOS vocabularies and SHACL shapes.</div>
<div class="card good text-sm">Already built on them: <a href="https://gatemezing.github.io/onto-dissemination/eradis.html">ERADIS</a> and <a href="https://gatemezing.github.io/onto-dissemination/eratv.html">ERATV</a> explorers, a <a href="https://gatemezing.github.io/onto-dissemination/plc-extraction.html">primary-location extractor</a>, and a <a href="https://gatemezing.github.io/onto-dissemination/crd-rinf.html">check of RNE's locations against RINF</a>.</div>
</div>

<!--
[3:15 → 4:15]
RINF is only the start. ERA runs several registers whose data is public, and they're joining the same graph.
RINF is live: 52,677 operational points from 71 provider graphs, about 42 million triples (measured 20 November 2026).
Telematics reference data, under the Telematics TSI (Implementing Regulation (EU) 2026/253): the organisation codes, downloadable from teleref and already in the graph, 5,659 of them; and the primary location codes, which RINF's primary locations carry.
ERADIS, with safety certificates, licences and EC declarations, is public without an account. ERATV lists the authorised vehicle types. Both are being migrated into the graph, and so is the European Vehicle Register. ERA-Lex, the legal references, is ready.
One ontology for all of them. And people are already building: explorers for ERADIS and ERATV on ERA's preview graphs, and tools for the telematics location codes.
Status: ERA's Knowledge Graph page, updated 21 Sep 2026. Counts: live SPARQL on rinf-plus, OCR-KG and era-lex, 20 and 22 Nov 2026.
-->

---
layout: section
---

# A graph, not a file

## What a developer gets that a CSV or a REST API can't give

<RailAgenda :current="1" on-dark class="mt-10" />

---

# What you get that a download can't give you

<div class="grid grid-cols-5 gap-3 mt-4 text-sm">
<div v-click class="layer owl"><h3>One query, 28 countries</h3>Every infrastructure manager publishes to the same model. A query written for France runs for Poland.</div>
<div v-click class="layer owl"><h3>Stable, linkable IDs</h3>Every station, track and tunnel has an IRI under <code>data.europa.eu/949/</code>. Link to it, store it, share it.</div>
<div v-click class="layer skos"><h3>Shared meaning</h3>Types, gauges, energy systems, ETCS levels are SKOS concepts: <b>125 concept schemes under CC BY 4.0</b>.</div>
<div v-click class="layer shacl"><h3>Links out</h3>EU country authority tables, NUTS, and keys that join Wikidata and OpenStreetMap.</div>
<div v-click class="layer xsd"><h3>Live, no ETL</h3>A provider republishes; your next query sees it. No mirror, no nightly import.</div>
</div>

<div v-click class="card mt-6">And it's <b>just HTTP</b>: one POST, results in JSON or CSV, no API key, and the endpoint answers browser requests from any origin, so a static web page can query it directly.</div>

<!--
[4:15 → 5:15]
Five things a file download doesn't give you (click ×5): one schema for every country; stable IRIs, so two apps showing the same station agree on which station it is; coded values as SKOS concepts, 125 schemes under CC BY 4.0; links out to country and NUTS tables, Wikidata and OSM; and live data, with no ETL.
(click) The entry cost is one HTTP POST. The endpoint takes anonymous queries and answers any origin, so a static page can call it.
-->

---

# Your first query, in five minutes

<div class="grid grid-cols-2 gap-6 mt-1">
<div class="smallcode">

```bash
curl -s https://graph.data.era.europa.eu/repositories/rinf-plus \
  -H 'Accept: text/csv' \
  --data-urlencode 'query=
PREFIX era: <http://data.europa.eu/949/>
SELECT ?op ?name ?uopid WHERE {
  ?op a era:OperationalPoint ;
      era:opName ?name ; era:uopid ?uopid .
  FILTER(CONTAINS(?name, "Valenciennes"))
} LIMIT 5'
```

<div class="rosetta mt-2">

| name | uopid |
|---|---|
| Valenciennes | FR0000002651 |
| CCVE de Valenciennes | FR0000007560 |
| ET Hainaut UPT Somain Résid T Valenciennes | FR0000007763 |

</div>
<div class="text-xs muted mt-1">answered in 0.8 s (20 Nov 2026)</div>

</div>
<div class="smallcode">

```sparql
# Every country in one query
SELECT ?country (COUNT(DISTINCT ?uopid) AS ?points)
WHERE {
  ?op a era:OperationalPoint ; era:uopid ?uopid .
  BIND(SUBSTR(?uopid, 1, 2) AS ?country)
} GROUP BY ?country ORDER BY DESC(?points)
```

<div class="text-sm mt-2"><code>FR 11,537 · DE 9,660 · PL 4,211 · CZ 3,581 · CH 3,308 · IT 3,199 · ES 2,343 …</code> <span class="muted">29 rows in 1.4 s</span></div>

```js
// the same from a web page
const res = await fetch(ENDPOINT, { method: "POST",
  headers: { Accept: "application/sparql-results+json" },
  body: new URLSearchParams({ query }) });
const { results } = await res.json();
```

</div>
</div>

<!--
[5:15 → 6:25]
This is the whole onboarding. Left: a curl command, a five-line query, and the answer: Valenciennes, where ERA is based, with its EU-wide identifier. 0.8 seconds.
Right: the same model across every country, in one aggregate query. 1.4 seconds; 29 rows because a few points carry the "EU" prefix.
And from JavaScript it's a plain fetch. No SDK, no key, no account.
Both queries were run live on 20 November 2026. Raw counts include every published version, so they're higher than what the map shows after the validity filter.
-->

---
layout: section
---

# Carto RINF

## One developer, one small stack, 28 countries

<RailAgenda :current="2" on-dark class="mt-10" />

---

# Carto RINF: a live map of the register

<div class="grid grid-cols-5 gap-5 mt-1">
<div class="col-span-3">
<img src="/assets/carto-rinf-switzerland.jpg" class="rounded-lg shot" alt="Carto RINF showing Switzerland's operational points and sections of line" />
<div class="text-xs muted mt-1">Switzerland, live from the ERA Knowledge Graph</div>
</div>
<div class="col-span-2 text-sm">

- operational points, sections of line, tunnels, primary locations
- level crossings, bridges, signals, switches where published
- colour by **max speed, electrification, gauge, ETCS level**
- **line profile** along a national line
- **Describe**: every triple of any resource, Turtle export
- CSV / GeoJSON export, shareable URLs, phone layout

<div class="card good mt-3"><b>16 Sep 2026</b>: France only.<br><b>18 Sep 2026</b>: all 28 countries.<br>The same model everywhere made that a two-day step.</div>

</div>
</div>

<style>
.shot { border: 1px solid var(--c-stroke); max-height: 360px; width: 100%; object-fit: cover; object-position: top left; }
</style>

<!--
[6:25 → 7:25]
Carto RINF. Pick a country: operational points coloured by type, sections of line, tunnels, primary locations; extra layers where a country publishes them; colouring by track parameters; a line profile; and a Describe tab with every triple RINF holds for what you click.
(point to the card) Version one covered France. Two days later, all 28 countries, because every manager publishes into the same model. That's my strongest argument for building on a knowledge graph.
And it's small on purpose: React and MapLibre, a thin Node server, no database, a 6-hour cache (architecture in backup). MIT, on GitHub: github.com/gatemezing/SemanticsCartoTchoo.
-->

---

# The query behind the map

<div class="grid grid-cols-5 gap-5">
<div class="col-span-3 smallcode">

```sparql
PREFIX era: <http://data.europa.eu/949/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?op ?uopid ?name ?wkt WHERE {
  ?op a era:OperationalPoint ; era:uopid ?uopid .
  FILTER(STRSTARTS(?uopid, "CH"))
  # RINF keeps past, current and future versions:
  # keep unversioned ones and those valid today
  FILTER(NOT EXISTS { ?op era:validity ?v } || EXISTS {
    ?op era:validity/time:hasBeginning/time:inXSDDate ?begin .
    FILTER(?begin <= xsd:date(NOW()))
    # (+ open-ended or not-yet-ended windows)
  })
  # geometry: on the net reference, else on the subject
  OPTIONAL { ?op era:netReference/geo:hasGeometry/geo:asWKT ?a }
  OPTIONAL { ?op geo:hasGeometry/geo:asWKT ?b }
  BIND(COALESCE(?a, ?b) AS ?wkt)
  OPTIONAL { ?op era:opName ?name }
}
```

<div class="text-xs muted">simplified from <code>backend/src/sparql/queries.ts</code></div>
</div>
<div class="col-span-2 text-sm">

<div class="card">One query per layer and country. The mapper turns bindings into GeoJSON.</div>

<div class="card mt-3">Every field is <b>a value</b>, <b>not applicable</b> (<code>era:notApplicable</code>), or <b>not available in RINF</b>. The UI never shows a blank as a fact.</div>

<div class="card warn mt-3">The comments are the real work: each line encodes something the data taught us. Next section.</div>

</div>
</div>

<!--
[7:25 → 8:15]
Here's the shape of the operational-points query, simplified. Scope by country through the uopid prefix; keep only the current version; read the geometry from either of the two places providers put it.
RINF distinguishes "not applicable" from "not provided": we keep that three-state distinction all the way to the screen.
(point to the yellow card) Every comment in this query is a lesson from real data. That's the next section.
-->

---
layout: section
---

# Real-world lessons

## The graph is real data from 71 publishers. Here is how to work with it.

<RailAgenda :current="3" on-dark class="mt-10" />

---

# Found and fixed in November 2026

<div class="grid grid-cols-3 gap-4 mt-2">
<div class="contrib"><div class="num">1</div>

### Primary locations without a position

None of their own in **CH 3,310 · HU 1,808 · SE 1,098 · ES 2,275 of 2,276**. Now placed at their operational point, and the popup says so.

</div>
<div class="contrib"><div class="num">2</div>

### 5,700+ tunnels without a country

**ES 3,152 · SE 560 · IE 549 · AT 458 · CH 251** lack `era:inCountry`. Scoped by provider graph: Spain **0 → 1,835** tunnels; Austria **0 → 219**, drawn portal to portal.

</div>
<div class="contrib"><div class="num">3</div>

### A cached failure

A transient Wikidata error was cached with the RINF layer for 6 h: France showed 0 matches. Now cached apart and **joined per request**.

</div>
</div>

<div class="card warn mt-6 text-sm">Still open, and worth reporting to the providers: Switzerland's tunnels and the 649 tunnels of graph <code>3915</code> carry <b>no position at all</b>.</div>

<!--
[8:15 → 9:25]
Three things found and fixed while preparing this talk, measured live on 20-21 November 2026.
One: several providers publish primary locations with no position of their own, so the map dropped them: zero for Switzerland, Hungary and Sweden. Now they sit at their operational point, flagged.
Two: tunnels were scoped by era:inCountry, which more than 5,700 lack. Scoped by provider graph, Spain went from 0 to 1,835; Austria's 219 are drawn portal to portal.
Three: a cached Wikidata error blanked France's enrichment for six hours. Now each source is cached separately.
(point to the yellow card) Some gaps only the provider can close. More patterns like these are on the provider-variance backup slide.
-->

---

# Linked data pays: 12% → 38% of stations enriched

<div class="grid grid-cols-5 gap-5">
<div class="col-span-3">
<MatchBars />
</div>
<div class="col-span-2 text-sm">

<div class="hero"><div class="n">5,671 → 17,791</div><div class="l">of 46,627 RINF primary locations matched to a Wikidata station</div></div>

<div class="card mt-3">Three keys, strongest first:<br>
① the primary location code (<code>P12783</code>), <b>any</b> station type<br>
② Wikidata's <b>ERA ID</b> (<code>P11631</code>) = the uopid<br>
③ the <b>UIC station code</b> (<code>P722</code>), accepted only <b>within 1 km</b> of RINF's position</div>

<div class="card good mt-3">Each match records how it was made. A heuristic is fine when it's labelled.</div>

</div>
</div>

<!--
[9:25 → 10:35]
What shared identifiers buy you. Carto RINF enriches stations from Wikidata: it used to match 5,671 of 46,627 primary locations, 12%.
Three changes took it to 17,791, 38%: accept any station type; use Wikidata's ERA ID, whose value is the uopid; and where the code is the country plus the UIC station number, derive it from the UIC code, accepting a match only within 1 km of RINF's position. That check rejected every false candidate in Germany and Denmark.
Czechia went from 1 to 2,832, Italy from 1 to 2,072, Switzerland from 3 to 1,846. What a match brings in, and tunnels: backup slide.
Measured live, 20-21 November 2026.
-->

---

# Your app is a data-quality sensor

<div class="grid grid-cols-2 gap-6 mt-3">
<div>

### What builders found, ERA and providers can act on

<div v-click class="card mt-2 text-sm"><b>Positions</b>: primary locations without geometry (CH, HU, SE, ES); tunnels without any position (CH, graph 3915).</div>
<div v-click class="card mt-2 text-sm"><b>Scoping</b>: <code>era:inCountry</code> missing on 5,700+ tunnels; named graphs work, but a property would be simpler.</div>
<div v-click class="card mt-2 text-sm"><b>Licence</b>: the data is public by law, but carries <b>no machine-readable licence</b> in the graph yet.</div>

</div>
<div>

### The loop

<div class="loop mt-3">
<span>build</span><i>→</i><span>measure</span><i>→</i><span>report</span><i>→</i><span>provider fixes</span><i>→</i><span>every app improves</span><i>↺</i>
</div>

<div v-click class="tk mt-6">A fix in the graph reaches <b>every application at once</b>. A fix in your private copy reaches only you.</div>

</div>
</div>

<style>
.loop { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.loop span { background: var(--c-blue-bg); color: var(--c-blue-strong); font-weight: 700; padding: 6px 12px; border-radius: 18px; font-size: 14px; }
.loop i { font-style: normal; color: var(--c-ink-mod); font-size: 18px; }
</style>

<!--
[10:35 → 11:25]
Apps do more than consume. Every one of these findings came from building, and each is actionable (click ×3): positions, scoping, and the licence statement.
The loop: build, measure, report, the provider fixes it, and every app improves at once, because they all read the same graph. That's the argument against private copies.
ERA welcomes this feedback: through the ERA GitLab projects, or the Interoperable Data Programme service desk.
-->

---
layout: section
---

# Your turn

## Why now, what to build, where to start

<RailAgenda :current="4" on-dark class="mt-10" />

---

# Why build on it, and what to build

<div class="grid grid-cols-5 gap-5 mt-1">
<div class="col-span-2 text-sm">

### Why

<div class="card good"><b>⚖️ Authoritative</b>: required by EU rail law, published through ERA by the bodies that hold the data.</div>
<div class="card good mt-2"><b>🇪🇺 EU-wide</b>: 28 countries, several registers, one model. Your second country costs almost nothing.</div>
<div class="card good mt-2"><b>🔌 Zero onboarding</b>: no key, no account, CORS. One POST from a static page.</div>
<div class="card good mt-2"><b>🔗 Linkable</b>: stable IRIs join Wikidata, OSM and your own data.</div>
<div class="card good mt-2"><b>🪶 Cheap to run</b>: Carto RINF has no database, only a 6 h cache.</div>

</div>
<div class="col-span-3 text-sm">

### What

<div class="grid grid-cols-2 gap-3">
<div class="prob"><h3>♿ Accessible journeys</h3>RINF platforms, plus wheelchair access and free Wi-Fi from Wikidata.</div>
<div class="prob"><h3>🚚 Route checks</h3>RINF's gauge, energy, ETCS and speed against ERATV's vehicle types: "can this train run here?"</div>
<div class="prob"><h3>🗺️ An open rail atlas</h3>Tunnels, bridges, opening dates, photos, for education and heritage.</div>
<div class="prob"><h3>📊 Data-quality dashboards</h3>Missing positions, versions, scoping per provider. Send them back.</div>
<div class="prob"><h3>🤖 Grounded AI agents</h3>An LLM that answers by writing SPARQL and cites the IRIs it used.</div>
<div class="prob"><h3>🔎 Who runs what</h3>ERADIS licences and safety certificates, with the companies' telematics codes.</div>
</div>

</div>
</div>

<!--
[11:25 → 12:55]
Why build here? It's authoritative and backed by law. It's EU-wide by default, several registers under one model, so your second country costs almost nothing. No key, no account. It links to Wikidata, OSM and your own data. And it's cheap to run. You're not alone either: ERA's platform, RINF Atlas by Matdata, Carto RINF and the onto-dissemination tools all share the same identifiers.
What to build? Six ideas, and you'll have better ones: an accessibility layer for journey planners; route checks that put RINF's track parameters against ERATV's vehicle types, which is what ERA's own route compatibility check does; an open atlas for education and heritage; data-quality dashboards per provider; AI agents that answer by writing SPARQL and cite the IRIs they used; and "who runs what", from ERADIS licences and safety certificates and the companies' telematics codes.
-->
---

# Licence: what's clear, and what to ask

<div class="grid grid-cols-2 gap-6 mt-3">
<div>

<div class="card good text-sm"><b>Public by law</b>: Art. 49 of Directive (EU) 2016/797; ERA publishes it through RINF.</div>
<div class="card good mt-2 text-sm"><b>ERA's notice</b>: reproduction is authorised provided the source is acknowledged, save where otherwise stated.</div>
<div class="card good mt-2 text-sm"><b>Ontology</b>: EUPL 1.2. <b>SKOS schemes</b> in the graph: CC BY 4.0.</div>

</div>
<div>

<div class="card warn text-sm">The RINF <b>instance data</b> carries <b>no licence statement</b> in the graph (checked 20 Nov 2026). ERA's catalogue record on data.europa.eu says <b>CC BY-SA 4.0</b>, and RINF's terms of use say the published information stays the issuing entity's intellectual property.</div>

<div class="tk mt-4"><b>So:</b> acknowledge the source in your app (Carto RINF does), and ask for <b>one</b> explicit open licence, stated the same way in the graph (<code>dct:license</code>) and in the catalogue. The high-value-datasets benchmark is <b>CC BY 4.0 or less restrictive</b>.</div>

</div>
</div>

<!--
[12:55 → 13:45]
Developers ask this first. What's clear: public by law; ERA's notice authorises reproduction with acknowledgement; the ontology is EUPL 1.2, the SKOS schemes CC BY 4.0.
What's missing: no licence statement on the instance data in the graph (dct:license check, 20 November). The data.europa.eu record says CC BY-SA 4.0, share-alike, stricter than the CC BY 4.0 ceiling the high-value-datasets regulation sets for Member States. And RINF's terms of use leave intellectual property with the issuing entity.
So: acknowledge the source, and ask for one machine-readable open licence, the same in the graph and in the catalogue.
-->

---

# Start today

<div class="rosetta mt-2">

| | |
|---|---|
| SPARQL endpoint | `https://graph.data.era.europa.eu/repositories/rinf-plus` · also `OCR-KG`, `era-lex` |
| The registers | <a href="https://eradis.era.europa.eu/">ERADIS</a> · <a href="https://eratv.era.europa.eu/Eratv">ERATV</a> · <a href="https://teleref.era.europa.eu/">telematics reference data</a> · <a href="https://rinf.data.era.europa.eu/">RINF platform</a> and <a href="https://rinf.data.era.europa.eu/data-stories">data stories</a> |
| The model | <a href="https://rinf.data.era.europa.eu/era-vocabulary/">ERA Ontology</a> · <a href="https://rinf.data.era.europa.eu/era-vocabulary/rinf-appGuide/">RINF application guide</a> · <a href="https://data.europa.eu/data/catalogues/era?locale=en">ERA's catalogue</a> |
| ERA's public GitLab | <a href="https://gitlab.com/era-europa-eu/public">gitlab.com/era-europa-eu/public</a>: the ontology, KG mappings, data-quality scripts, and the <a href="https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/rail-data-forum-2025">Rail Data Forum 2025 masterclasses</a> (SPARQL, SHACL, RDF-isation, telematics) |
| Example apps | <a href="https://github.com/gatemezing/SemanticsCartoTchoo">Carto RINF</a> (MIT) · <a href="https://rinf-atlas.matdata.eu/">RINF Atlas</a> · <a href="https://gatemezing.github.io/onto-dissemination/">onto-dissemination tools</a> |
| Feedback to ERA | an issue on the relevant GitLab project · servicedesk@era.europa.eu |
| Meet us | <b>Rail Data Forum 2027</b> · Mulhouse · 8–10 June 2027 |

</div>

<div class="grid grid-cols-3 gap-4 mt-4 text-sm">
<div class="card"><b>1.</b> Run the curl from slide 10.</div>
<div class="card"><b>2.</b> Open any IRI in Carto RINF's Describe tab.</div>
<div class="card"><b>3.</b> Build one map, one table, one answer.</div>
</div>

<!--
[13:45 → 14:25]
Everything you need is on this slide: the endpoint and its sister repositories, the registers themselves, the ontology and ERA's catalogue, and ERA's public GitLab, where the ontology, the graph's mappings and data-quality scripts live, along with the hands-on masterclasses from the last Rail Data Forum. Then three example apps, and where to send feedback.
And come and meet us: the third Rail Data Forum is in Mulhouse, 8 to 10 June 2027.
Three steps: run the curl, open an IRI in the Describe tab, then build the smallest useful thing.
-->

---
layout: center
class: text-center
hideLogo: true
---

<img src="/assets/era-ontology-logo-white.png" class="h-20 mx-auto dark:hidden" alt="ERA Ontology · Interoperable by Design" />
<img src="/assets/era-ontology-logo-blue.png" class="h-20 mx-auto hidden dark:block rounded" alt="ERA Ontology · Interoperable by Design" />

# Thank you · let's build

<div class="text-left text-sm leading-relaxed mt-3 inline-block rosetta">

**Ghislain Atemezing** · European Union Agency for Railways

| | |
|---|---|
| Query the graph | <a href="https://graph.data.era.europa.eu/">graph.data.era.europa.eu</a> |
| ERA Knowledge Graph | <a href="https://www.era.europa.eu/domains/registers/era-knowledge-graph">era.europa.eu/…/era-knowledge-graph</a> |
| Carto RINF | <a href="https://github.com/gatemezing/SemanticsCartoTchoo">github.com/gatemezing/SemanticsCartoTchoo</a> · MIT |
| ERA Ontology | <a href="https://rinf.data.era.europa.eu/era-vocabulary/">rinf.data.era.europa.eu/era-vocabulary</a> · EUPL 1.2 |
| ERA on GitLab | <a href="https://gitlab.com/era-europa-eu/public">gitlab.com/era-europa-eu/public</a> |
| See you in Mulhouse | <b>Rail Data Forum 2027</b> · 8–10 June 2027 |

</div>

<!--
[14:25 → 14:50]
The registers are open, and they're becoming one graph. The hard part is done. Build something, tell us what you find, and come to Mulhouse in June. Thank you.
-->

---

# Backup · Where ERA publishes it

<div class="grid grid-cols-2 gap-6 mt-2">
<div>

### <a href="https://rinf.data.era.europa.eu/">rinf.data.era.europa.eu</a>

<div class="rosetta text-sm">

| | |
|---|---|
| Search, map explorer | look the register up by name or on a map |
| Dataset explorer | every manager's published RINF dataset, also as JSON |
| Data stories | ready-made questions over the register |
| Route compatibility | can this vehicle run this route? |
| ERA vocabulary | the ontology, its SKOS schemes and SHACL shapes |

</div>
</div>
<div>

### <a href="https://data.europa.eu/data/catalogues/era?locale=en">data.europa.eu</a> · ERA's catalogue

<div class="card text-sm"><b>14 datasets</b> from the European Union Agency for Railways: the <b>ERA Knowledge Graph</b> and <b>Ontology</b>, ERATV, the vehicle keeper markings, seven ERADIS databases, safety indicators, accident investigations and railway terminology.</div>

<div v-click class="card warn mt-3 text-sm">The records lag the platform (checked 22 Nov 2026). The Knowledge Graph record links to an older SPARQL endpoint and the retired <code>data-interop</code> host, and says <b>CC BY-SA 4.0</b>. The ontology record still says v3.0.0. Metadata is data too: report it like any other gap.</div>

</div>
</div>

<!--
[backup]
Where to find all this. ERA's own platform, rinf.data.era.europa.eu: search and a map explorer, a dataset explorer listing what each infrastructure manager published (with a JSON API behind it; Carto RINF's datasets dialog uses it), data stories, the route compatibility check, and the vocabulary.
And the EU's open data portal harvests ERA's catalogue: fourteen datasets, from the Knowledge Graph and the ontology to ERADIS and the safety indicators.
(click) Honest note: those catalogue records lag the platform. The Knowledge Graph record points to an older SPARQL endpoint and to data-interop.era.europa.eu, which no longer resolves, and gives CC BY-SA 4.0; the ontology record is still v3.0.0. Metadata is data: if you find a gap, say so.
Checked on 22 November 2026 with the data.europa.eu search API (catalogue "era").
-->

---

# Backup · Small on purpose

<div class="flow mt-4">
<div class="box"><b>Browser</b><br>React · MapLibre GL<br><span class="muted">≈ 9k lines of TypeScript in all</span></div>
<i>→</i>
<div class="box"><b>Node · Fastify</b><br>6 h cache · shared in-flight fetches<br>rate limits · input checks</div>
<i>→</i>
<div class="col">
<div class="box era"><b>ERA SPARQL</b> · <code>rinf-plus</code><br>infrastructure, live</div>
<div class="box wd"><b>Wikidata</b> query service<br>enrichment, cached separately</div>
</div>
</div>

<div class="grid grid-cols-3 gap-4 mt-7">
<div class="hero"><div class="n">0</div><div class="l">databases, mirrors or ETL jobs</div></div>
<div class="hero"><div class="n">6 h</div><div class="l">cache: RINF changes on a weeks/months cadence</div></div>
<div class="hero"><div class="n">≈ 10–60 s</div><div class="l">a large country's layer, cold; instant after</div></div>
</div>

<style>
.flow { display: flex; align-items: center; gap: 14px; }
.flow i { font-style: normal; font-size: 26px; color: var(--c-ink-mod); }
.flow .col { display: flex; flex-direction: column; gap: 10px; }
.box { background: var(--c-surface); border: 1px solid var(--c-stroke); border-top: 4px solid var(--c-grey); border-radius: 10px; padding: 10px 14px; font-size: .88rem; line-height: 1.35; }
.box.era { border-top-color: var(--c-blue); }
.box.wd { border-top-color: var(--c-shacl); }
</style>

<!--
[backup]
The architecture is deliberately small: a React and MapLibre front end, a thin Node server, and the two SPARQL endpoints.
The server caches each country layer for six hours, because RINF changes on a weeks-to-months cadence, and concurrent requests for the same layer share one upstream query. Wikidata has its own cache.
No database, no mirror, no ETL. The trade-off: a cold load of a big country takes time (measured 20 Nov 2026: France's points 13 s, its sections 19 s, Germany's primary locations 29 to 60 s), then it's instant from the cache.
For an index of the whole register, RINF Atlas took the opposite path, mirroring into PostGIS: both are valid, and both exist because the data is open.
-->

---

# Backup · Provider variance

<div class="rosetta mt-1">

| What we met | Measured | What the app does |
|---|---|---|
| Past, current and future **versions** of the same entity | Germany: 2025, 2026, 2027 versions of one uopid | keep unversioned + valid-today; open-ended windows count |
| **Open-ended** validity windows | Switzerland: 3,308 of 3,310 points | treated as still running, not as expired |
| **Geometry in two places** | all 713 Norwegian sections on the subject itself | net reference first, else the subject |
| **Country codes** | Greece: registry `EL`, uopids `GR` | per-country uopid prefix |
| **Provider-minted concepts** | Croatia: own op-type concepts and spellings | map the code to ERA's concept, show a note |
| Missing **`era:inCountry`** | about half of the infrastructure elements surveyed | scope by the provider's **named graph** |

</div>

<div class="card good mt-4">None of these is a reason not to build. Each is a <b>pattern you write once</b>, and a <b>finding you can send back</b> to the publisher.</div>

<!--
[backup]
Developers trust honesty, so here's what real-world data looks like. 71 publishers, one model, but each with its habits.
Versions: RINF keeps several dated versions of the same entity; Germany publishes one per calendar year. Open-ended windows: for Switzerland nearly every point has a start date and no end date, and treating that as expired emptied the map at first. Geometry in two places. Greece's EL versus GR. Croatia minting its own operational point types. And era:inCountry, missing on about half of non-OP elements: scope by the provider's named graph instead.
Each of these was measured live and is covered by a regression test in the repo (docs/ROADMAP.md, "Data issues found and fixed").
-->

---

# Backup · What a link brings in

<div class="grid grid-cols-5 gap-5">
<div class="col-span-2">
<img src="/assets/carto-rinf-bern-wikidata.jpg" class="rounded-lg shot2" alt="Carto RINF popup for Bern: RINF record plus Wikidata accessibility, free Wi-Fi, 12 platforms, matched on UIC station code 8507000" />
<div class="text-xs muted mt-1 text-center">Bern in Carto RINF: matched on UIC code 8507000</div>
</div>
<div class="col-span-3 text-sm">

<div class="rosetta">

| On Wikidata stations with a PLC | Share | Adds |
|---|---|---|
| `P5817` state of use | 96% | in use or disused |
| `P137` operator | 93% | station operator (RINF has the IM) |
| `P18` image | 80% | a photo |
| `P1192` connecting service | 74% | trains that call there |
| `P1619` opening date | 50% | history |
| `P2044` elevation | 37% | points for a line profile |

</div>

<div class="card mt-3">Beyond stations: Wikidata <b>tunnels</b> paired by position (300 m) and length: DE 775 · AT 172 · FR 107 · NO 86 · IT 76 · ES 18, median 9–21 m. <b>Lines</b>: route number <code>P1671</code> joins DE 745 of 1,490, FR 315 of 892.</div>

</div>
</div>

<style>
.shot2 { border: 1px solid var(--c-stroke); max-height: 375px; width: auto; margin: 0 auto; display: block; }
</style>

<!--
[backup]
What does the link bring? Bern, from RINF: its uopid, type, 384 sub-elements. From Wikidata: wheelchair accessible, free Wi-Fi, 12 platforms. And the popup says exactly how the match was made.
The table: how often these properties appear on the 7,528 Wikidata items carrying a primary location code (measured 20 Nov 2026). State of use, operator, photo, the train services that call there, opening date, elevation. RINF doesn't have most of these; Wikidata doesn't have the infrastructure parameters. Together they're a much richer app.
Same for tunnels, paired by position and length (Wikidata railway tunnels and bridges; bridges NO 36, EL 4), and for lines, where Wikidata's route number joins RINF's national line for 745 German and 315 French lines (measured; lines are not yet in the app).
Free Wi-Fi is now shown explicitly: for example 70 French stations.
-->

---

# Backup · Sources

<div class="rosetta text-xs">

| Claim | Source |
|---|---|
| Art. 49 Dir. 2016/797, Art. 37(3)(h) Reg. 2016/796, Reg. 2019/777 | RINF terms of use (ERA, v1.0, 2022), §1 and §5 · <a href="http://data.europa.eu/eli/reg_impl/2019/777/oj">ELI 2019/777</a> |
| EU open-data and interoperability law | See the next slide |
| Registers, ontology v3.3.4, Art. 4(8), EUPL 1.2 | <a href="https://www.era.europa.eu/domains/registers/era-knowledge-graph">ERA Knowledge Graph page</a> (updated 21 Sep 2026) |
| Copyright notice | <a href="https://www.era.europa.eu/content/disclaimer-and-copyright-notice">ERA disclaimer and copyright notice</a> |
| 52,677 uopids, 71 graphs, ≈ 42 M triples, licences, query timings, CORS | live SPARQL on <code>rinf-plus</code>, 20 Nov 2026 |
| Provider variance | Carto RINF <code>docs/ROADMAP.md</code>, "Data issues found and fixed" (measured 2026-10) |
| Fixes, matching, enrichment | Carto RINF, measured live 20–21 Nov 2026 against <code>rinf-plus</code> and query.wikidata.org |
| Wikidata property shares | 7,528 Wikidata items with <code>P12783</code>, 20 Nov 2026 |

</div>

<!--
[backup]
Where every number comes from.
-->

---

# Backup · Sources: EU law and catalogues

<div class="rosetta text-xs">

| Claim | Source |
|---|---|
| INSPIRE, Annex I theme 7 "Transport networks" names rail | <a href="http://data.europa.eu/eli/dir/2007/2/oj">Directive 2007/2/EC</a> |
| Public undertakings and public service operators in scope (Art. 1(1)(b)); high-value datasets (Art. 14); transposition by 17 July 2021 (Art. 17(1)); addressed to the Member States (Art. 21) | <a href="http://data.europa.eu/eli/dir/2019/1024/oj">Directive (EU) 2019/1024</a> |
| APIs and bulk download (Art. 3(1)); CC0, CC BY 4.0 or less restrictive (Art. 4(3)); applies 16 months after entry into force, i.e. 9 June 2024 (Art. 6); mobility = INSPIRE transport networks, documented structure and semantics (Annex 6.1, 6.2) | <a href="http://data.europa.eu/eli/reg_impl/2023/138/oj">Implementing Regulation (EU) 2023/138</a> |
| Data strategy; common European mobility data space (29 Nov 2023) | COM(2020) 66 · <a href="https://transport.ec.europa.eu/transport-themes/smart-mobility/creating-common-european-mobility-data-space_en">COM(2023) 751</a> |
| Scope and Union entities (Art. 1(2), 2(5)); interoperability solution (Art. 2(4)); assessment (Art. 3); sharing (Art. 4(1), (3)); licensing preference (Art. 4(6)); EIF (recital 28); application dates (Art. 23(2)) | <a href="http://data.europa.eu/eli/reg/2024/903/oj">Regulation (EU) 2024/903</a> |
| ERA Ontology on the Interoperable Europe portal, EUPL 1.2, published 4 Aug 2026 | <a href="https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology">SEMIC collection entry</a> |
| ERA's catalogue: 14 datasets; Knowledge Graph record (CC BY-SA 4.0, older endpoint); ontology record v3.0.0 | data.europa.eu search API, catalogue “era”, 22 Nov 2026 |
| ERA's platform: search, map explorer, dataset explorer, data stories, route compatibility, vocabulary | <a href="https://rinf.data.era.europa.eu/">rinf.data.era.europa.eu</a>, 22 Nov 2026 |

</div>

<!--
[backup]
The legal and catalogue sources behind the "Open by law" section.
-->

---

# Backup · Sources: ERA's registers

<div class="rosetta text-xs">

| Claim | Source |
|---|---|
| Each register's status in the Knowledge Graph: RINF live; OCR and ERA-Lex ready; ERADIS, ERATV and EVR migration ongoing | <a href="https://www.era.europa.eu/domains/registers/era-knowledge-graph">ERA Knowledge Graph page</a>, updated 21 Sep 2026 |
| ERADIS contents; "All data submitted to ERADIS is public and accessible without user credentials"; legal basis Directives (EU) 2016/797 and 2016/798, Regulation (EU) 2016/796 | <a href="https://eradis.era.europa.eu/">eradis.era.europa.eu</a> (v5.0.1), read 22 Nov 2026 |
| ERATV: types of vehicle authorised by the Member States; public list of registered authorisations | <a href="https://eratv.era.europa.eu/Eratv">eratv.era.europa.eu</a> (v3.2.2), read 22 Nov 2026 |
| Telematics reference data: organisation codes (Excel download) and primary location codes; Implementing Regulation (EU) 2026/253 | <a href="https://teleref.era.europa.eu/">teleref.era.europa.eu</a> (v2.1), read 22 Nov 2026 |
| 5,659 organisation codes in <code>OCR-KG</code>; 7,317 legal resources in <code>era-lex</code> | live SPARQL on graph.data.era.europa.eu, 22 Nov 2026 |
| ERA's public GitLab: 26 projects, including the Rail Data Forum 2025 masterclasses | GitLab API, group <code>era-europa-eu/public</code>, 22 Nov 2026 |
| Rail Data Forum 2027: third edition, Mulhouse, 8–10 June 2027 | <a href="https://www.railwaygazette.com/agenda/3rd-rail-data-forum/">Railway Gazette agenda</a> · ERA's event listing |
| ERADIS and ERATV explorers, primary-location extractor, RNE locations vs RINF | <a href="https://gatemezing.github.io/onto-dissemination/">onto-dissemination</a>; the explorers read ERA's preview graphs |

</div>

<!--
[backup]
Where the register facts come from.
-->
