---
theme: default
title: "A Semantic Backbone for European Rail Data Exchange"
info: |
  KGSWC 2026. Automating the telematics extension of the ERA Ontology with xsd2rdf:
  OWL for domain concepts, SHACL for constraints, SKOS for code lists.
  Ghislain Atemezing and Polymnia Vassilopoulou, European Union Agency for Railways.
author: Ghislain Atemezing, Polymnia Vassilopoulou
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

# A Semantic Backbone for European Rail Data Exchange

## Automating the telematics extension of the ERA Ontology

<div class="mt-8 text-base opacity-95">
<b>Ghislain Atemezing</b> · Polymnia Vassilopoulou<br>
<span class="opacity-75">European Union Agency for Railways</span>
</div>

<div class="mt-4 text-sm opacity-70">KGSWC 2026</div>

</div>

<div class="absolute top-0 bottom-0 right-0" style="left: 58%; padding: 40px 30px 40px 20px;">
  <CoverArt />
</div>

<!--
[0:00 → 0:30]
Good morning. I'm Ghislain Atemezing from the European Union Agency for Railways; this is joint work with Polymnia Vassilopoulou.
The talk is about how we turned the XML schemas that European railways use to exchange operational messages into a knowledge-graph vocabulary, without losing what those schemas say about validity and code lists.
-->

---
clicks: 5
---

# Agenda

<div class="mt-10">
<RailAgenda :reveal="$clicks" />
</div>

<div v-click="5" class="card mt-6 text-lg">One idea runs through the talk: <b>an XML Schema mixes three kinds of semantics, and each one belongs in its own W3C language</b>.</div>

<!--
[0:30 → 0:50]
Five stops on this line. Click through them:
1 Context: the ERA Ontology and why telematics matters now.
2 The objective: the problem of mixed semantics.
3 Our contributions: the converter, the generated extension, the method.
4 Results.
5 Where we go next: ERA Ontology version 4.
-->

---
layout: section
---

# ERA Ontology context

## From static registers to operational messages

<RailAgenda :current="0" on-dark class="mt-10" />

---

# The ERA Ontology at a glance

<div class="grid grid-cols-4 gap-3 mt-2">
<div class="hero"><div class="n">104</div><div class="l">classes</div></div>
<div class="hero"><div class="n">303</div><div class="l">object properties</div></div>
<div class="hero"><div class="n">442</div><div class="l">datatype properties</div></div>
<div class="hero"><div class="n" style="font-size:1.6rem; line-height:2.5rem">v3.3.2</div><div class="l">baseline · <code>era:</code> = data.europa.eu/949/</div></div>
</div>

<div class="grid grid-cols-5 gap-3 mt-5 text-sm">
<div v-click class="layer owl"><h3>Infrastructure</h3>operational points, sections of line, tracks, tunnels, platform edges… composed with <code>hasPart</code> / <code>isPartOf</code></div>
<div v-click class="layer owl"><h3>Technical</h3>contact line, ETCS, train detection, load capability; values as SKOS concepts</div>
<div v-click class="layer owl"><h3>Topology</h3>net elements and relations, linear positioning systems</div>
<div v-click class="layer owl"><h3>Organisations</h3><code>era:Body</code> plays roles typed by SKOS concepts, e.g. infrastructure manager</div>
<div v-click class="layer owl"><h3>Operational locations</h3>primary and subsidiary locations; <code>era:allocationCompany</code></div>
</div>

<div v-click class="card mt-5">It underpins <b>RINF</b> and the <b>vehicle registers</b>, whose data form the <b>ERA Knowledge Graph</b>, used e.g. for route-compatibility checks. Spatial, temporal and organisational semantics are reused from GeoSPARQL, OWL-Time, FOAF and ORG.</div>

<!--
[1:00 → 1:50]
The ERA Ontology is the reference vocabulary of the Agency. Version 3.3.2 is our baseline: about a hundred classes and seven hundred and fifty properties.
Its RINF part has five groups (click through them). Infrastructure, technical characteristics, topology, organisations, and operational locations: primary and subsidiary locations, which will matter a lot later.
Everything so far is static: registers that describe the network and the vehicles. That is what the earlier ISWC paper covered.
-->

---
clicks: 3
---

# A station in the ERA Knowledge Graph

<div class="text-sm muted -mt-3 flex gap-4 items-center">
<span>Valenciennes, home of the Agency · <code>era:operationalPoint/83728fa739</code> · live data from rinf-plus</span>
<span class="ml-auto"><span style="color: var(--c-skos)">●</span> coded value from a SKOS list</span>
</div>

<StationGraph :step="$clicks" class="mt-1" />

<!--
[1:50 → 2:50]
To make it concrete: a real resource, Valenciennes station, where the Agency is based. Live data from the rinf-plus graph, published by SNCF Réseau.
It is an operational point: RINF's word for any place where trains do something, a station, a junction, a border. It has an EU-wide identifier, a type and a country. The green dots mark coded values: "station" and "France" are concepts from controlled lists, SKOS concept schemes. Keep that in mind: the telematics code lists will work the same way.
(click) Where it is: a point on the map, and a position along each of the three national lines through the station.
(click) What it contains: era:hasPart leads to its tracks, eight running tracks and a siding. One of them, Voie A: standard gauge; a train radio with roaming agreements for nine networks (Belgium, Switzerland, Germany, Spain, France, Great Britain, Italy, Luxembourg, the Netherlands); part of the North Sea–Mediterranean freight corridor; managed by SNCF Réseau. Its platform, Quai 1: 464 metres usable, 58 centimetres high.
(click) And two primary locations: the codes that path requests and train-running messages use to say "Valenciennes". That is exactly where messages meet the register, which is the next slide.
Query used (rinf-plus): DESCRIBE-style SELECT on operationalPoint/83728fa739, track/669db3f795, platformEdge/1e0ce8c500; organisation name from OCR-KG (code 0087).
-->

---

# Telematics meets the core

<div class="grid grid-cols-2 gap-8 mt-2">
<div>

### TEL TSI · Reg. (EU) 2026/253

- in force since **2 March 2026**
- merges **TAF** (freight) and **TAP** (passenger)
- relies on the **ERA Ontology** as the common semantic model for telematics data
- in line with the **EU Data Act**

<div v-click class="card warn mt-4 text-sm">Meanwhile every actor migrates from legacy numeric company codes to the alphanumeric <b>Organization Code</b> assigned by ERA.</div>

</div>
<div>

### Three anchor points

<div v-click class="card mt-2"><b>📍 Locations</b> · <code>era:PrimaryLocation</code>, <code>era:SubsidiaryLocation</code>, identified by location codes</div>
<div v-click class="card mt-3"><b>🏢 Organisations</b> · company and Organization Codes, roles such as <code>era:allocationCompany</code></div>
<div v-click class="card mt-3"><b>🚃 Vehicles</b> · wagons and rolling-stock datasets</div>

<div v-click class="mt-4 text-sm muted">Here the generated vocabulary must <b>reuse, not duplicate</b> ERA terms. It is also where the integration conflicts appear.</div>

</div>
</div>

<!--
[2:50 → 4:00]
What changed this year: the new Telematics TSI. It merges the freight and passenger specifications and names the ERA Ontology as the common semantic model.
(click) And at the same time everybody is migrating company codes to the new alphanumeric Organization Code.
Messages, path requests, train running information, consignments, touch the core at three anchor points (click ×3): locations, organisations, vehicles.
(click) Keep these anchors in mind: this is where the generated terms must reuse the core, and where we found most conflicts.
-->

---

# What the technical documents contain

<div class="grid grid-cols-3 gap-4 mt-1 tdc">
<div class="layer xsd">
<span class="pill xsd">TAP · TD B5 + annexes A1, A2, B1, B2</span>

### Booking seats and issuing tickets

- **Who**: a distributor (RU or ticket vendor) and the **attributor**, the RU that holds seat inventory and fares
- **Messages**: availability, reservation, partial and full cancellation
- **Formats**: fixed-length binary (A1) and **XML** (A2)
- ticket layout in TD B11, security barcodes in TD B12

<div class="xs">XSD: B.5 XML schema files</div>
</div>
<div class="layer xsd">
<span class="pill xsd">TAP · TD B10</span>

### Booking assistance for passengers with reduced mobility

- **Who**: an RU requests assistance at a station run by another RU, IM or station manager
- **Messages**: availability of assistance, booking; automatic or partly manual allocation
- **Model**: booking, customer, assistance, station, platform, train, train stop…

<div class="xs">XSD: <code>tap_tsi_b.10.xsd</code></div>
</div>
<div class="layer xsd">
<span class="pill xsd">CEN/TS 16614 · TDs B15, B16, B17</span>

### Timetables, fares and stations: NeTEx

- **What**: the CEN Network and Timetable Exchange standard, built on Transmodel (EN 12896)
- **B17**: timetables (`ServiceFrame`) and station data (`SiteFrame`)
- **B16**: European Fare Information Profile for Rail
- **B15**: station accessibility profile

<div class="xs">XSD: <code>NeTEx_publication.xsd</code> (full schema)</div>
</div>
</div>

<div class="grid grid-cols-5 gap-4 mt-3 text-sm">
<div v-click class="card col-span-3">📜 <i>"The relevant master documents for implementing an interface based on this specification are the <b>schema files only</b>."</i> <span class="muted">TD B5 Annex A2, §1.1.4</span><br>The XSD <b>is</b> the specification, so a schema-driven converter works at the right level.</div>
<div class="card col-span-2" style="border-left-color: var(--c-grey)"><b>TAF</b> (freight): TD 105 <i>XSD data and message model</i>, <code>taf_cat_complete.xsd</code> and its code lists. The <b>Ontology TD</b> lists these four XSDs as the conversion input.</div>
</div>

<div class="text-xs muted mt-2">Technical documents v4.0, published with Reg. (EU) 2026/253 · gitlab.com/era-europa-eu/public/era-telematics-tsi/tsi_telematics</div>

<style>
.tdc .layer { font-size: .8rem; }
.tdc .layer h3 { font-size: 1rem; margin: 6px 0 4px; }
.tdc .layer ul { padding-left: 1rem; }
.tdc .layer li { margin: .15rem 0; line-height: 1.3; }
.tdc .xs { margin-top: 6px; padding-top: 5px; border-top: 1px dashed var(--c-stroke); font-size: .72rem; color: var(--c-xsd); font-weight: 700; }
.tdc .xs code { font-size: .7rem; }
</style>

<!--
[4:00 → 5:10]
Which schemas are we talking about? The TSI comes with technical documents, version 4.0, published with the regulation in February.
TAP B5 is about booking seats and issuing tickets between railways: a distributor, an RU or a ticket vendor, asks the attributor, the RU that owns the seat inventory and the fares, for availability, a reservation or a cancellation. There is an old fixed-length binary format and an XML format; we lift the XML one. Ticket layout and barcodes are in B11 and B12.
TAP B10 books assistance for persons with reduced mobility: an RU asks for help at a station run by someone else. Its model has bookings, customers, assistance, stations, platforms, trains, train stops.
NeTEx is not an ERA schema: it is the CEN standard for public-transport networks, timetables and fares, built on Transmodel. Three technical documents profile it for rail: timetables and station data (B17), fares (B16) and station accessibility (B15). We convert the full NeTEx publication schema, which is why NeTEx is so large in our results.
(click) And the key sentence for this paper: the technical documents say the schema files are the master documents. The XSD is the specification. That is why we lift schemas, not message examples.
TAF, freight, is TD 105. The Ontology technical document lists exactly these four XSDs as the input of the conversion.
-->

---
layout: section
---

# Objective of the paper

## One schema, three kinds of semantics

<RailAgenda :current="1" on-dark class="mt-10" />

---

# XML is well formed, not shared meaning

<div class="text-lg mt-1">RUs and IMs exchange path requests, train compositions, running information and consignment notes as <b>XML messages fixed by XSDs</b>.</div>

<div class="grid grid-cols-2 gap-4 mt-4">
<div class="prob"><h3>🔀 Same thing, different identifiers</h3>The same location or company is identified differently in freight and passenger messages.</div>
<div class="prob"><h3>🔗 No link to the registers</h3>Nothing links a message to the registers that describe the infrastructure the train runs on.</div>
</div>

<div v-click class="mt-6 font-bold text-lg">And each XSD mixes three kinds of semantics:</div>

<div class="grid grid-cols-3 gap-4 mt-3">
<div v-click class="layer owl"><span class="pill owl">domain concepts</span><h3>What it is about</h3>a path request, a planned journey location</div>
<div v-click class="layer shacl"><span class="pill shacl">validation constraints</span><h3>What is valid</h3>a company is 4 characters matching <code>[0-9A-Z]{4}</code></div>
<div v-click class="layer skos"><span class="pill skos">code lists</span><h3>Which values exist</h3>the 4-digit border-point codes, list B.1.3: <code>1001</code> Sarkiai</div>
</div>

<!--
[5:20 → 6:30]
XML guarantees that a message is well formed. It does not guarantee that two systems read it the same way.
(click) And the schemas mix three things that a knowledge graph should keep apart.
(click) Domain concepts: what the message is about.
(click) Validation constraints: four characters, uppercase or digits. This one is the running example, because it accepts both the old numeric codes and the new Organization Codes.
(click) And code lists, like border points, with their own release cycle.
-->

---

# Why not put everything in OWL?

<div class="grid grid-cols-2 gap-6 mt-3">
<div class="layer owl">
<span class="pill owl">OWL · open world</span>

### "exactly one sender" as an axiom

```turtle
ex:Message rdfs:subClassOf [ a owl:Restriction ;
    owl:onProperty ex:sender ; owl:cardinality 1 ] .
ex:msg42 a ex:Message .        # no sender
```

<div v-click class="mt-2">🤔 Consistent. A reasoner <b>infers</b> an unnamed sender. Nothing is reported.</div>
</div>
<div class="layer shacl">
<span class="pill shacl">SHACL · closed world</span>

### "exactly one sender" as a shape

```turtle
ex:MessageShape a sh:NodeShape ;
    sh:targetClass ex:Message ;
    sh:property [ sh:path ex:sender ;
        sh:minCount 1 ; sh:maxCount 1 ] .
```

<div v-click class="mt-2">🚫 <b>Violation</b>: fewer than 1 value for <code>ex:sender</code>. The message is <b>rejected</b>.</div>
</div>
</div>

<div v-click class="card mt-5 text-lg">Lifting everything to OWL either <b>drops the constraints</b> or turns them into open-world axioms that <b>infer</b> facts instead of <b>rejecting</b> invalid messages.</div>

<div class="text-xs muted mt-2">Illustrative <code>ex:</code> terms, not ERA vocabulary.</div>

<!--
[6:30 → 7:20]
Why does this matter? Take "exactly one sender".
As an OWL cardinality restriction, a message without a sender is perfectly consistent (click): the reasoner concludes that some sender exists that we don't know.
As a SHACL shape (click), the same message is a violation. An XSD behaves like the right-hand side: it rejects the document.
(click) So mapping all of an XSD to OWL is a semantic mistake, not just a loss of detail.
-->

---

# The gap, and our objective

<div class="rosetta mt-1">

| Approach | Level | Output | Mapping | Constraints | Code lists | TSI |
|---|---|---|---|---|---|---|
| RML · SPARQL-Generate · YARRRML | data | RDF data | manual | partial | – | manual |
| X3ML · ShExML | data | RDF data | manual / declarative | partial | – | – |
| XMLSchema2ShEx | schema | ShEx | automatic | ✓ | – | – |
| <b>ERA xsd2rdf</b> | <b>schema</b> | <b>OWL + SHACL + SKOS</b> | <b>automatic</b> | <b>✓</b> | <b>✓</b> | <b>✓</b> |

</div>

<div class="grid grid-cols-2 gap-4 mt-3 text-sm">
<div class="card">Mapping languages lift <b>instances</b>, with a hand-written mapping per message type: this does not scale to <b>hundreds of TAF/TAP structures</b>.</div>
<div class="card">Schema-lifting tools give an ontology <b>or</b> shapes, never both <b>with managed code lists</b>.</div>
</div>

<div v-click class="tk mt-5 text-lg">🎯 <b>Objective</b>: lift each kind of XSD semantics to the W3C language designed for it, <b>automatically, in one schema-driven run</b>, with the three layers <b>linked</b>, and deliver the result as the telematics extension of the ERA Ontology.</div>

<!--
[7:20 → 8:10]
Related work splits in two. Declarative mapping languages are expressive but need a mapping per message type. Schema-lifting tools like XMLSchema2ShEx keep constraints but produce no ontology and no code lists.
The two lines are complementary: in our pipeline the schemas are lifted by xsd2rdf, and the messages by declarative mappings.
(click) So the objective: one run, three languages, linked.
-->

---
layout: section
---

# Contributions

## xsd2rdf and the telematics extension

<RailAgenda :current="2" on-dark class="mt-10" />

---

# Three contributions

<div class="grid grid-cols-3 gap-5 mt-8">
<div v-click class="contrib"><div class="num">1</div>

### xsd2rdf

An open-source, **schema-driven converter**: OWL for classes and properties, SHACL for constraints, SKOS for code lists, with **shapes linked to the concept schemes**.

<div class="mt-2"><span class="pill grey">EUPL 1.2</span> <span class="pill grey">PyPI</span> <span class="pill grey">GitLab</span></div>
</div>
<div v-click class="contrib"><div class="num">2</div>

### The telematics extension

Generated from the **TAF, TAP and NeTEx** schemas and published as **2,630 Turtle artifacts**, documented on the ERA vocabulary portal.

</div>
<div v-click class="contrib"><div class="num">3</div>

### Evaluation and integration

Coverage, syntax, **OOPS!**, **conflict analysis** against ERA Ontology v3.3.2 and **92 expert competency questions**, plus the integration strategy for **v4.0.0**.

</div>
</div>

<div v-click class="card mt-8">New compared with the ERA KG paper (ISWC 2021): a <b>schema-driven</b> method that carries <b>constraints and code lists</b> alongside the ontology, applied to <b>dynamic, message-based operations</b>.</div>

<!--
[8:20 → 9:00]
Three contributions. The converter. The vocabulary it generated: 2,630 files. And an evaluation from five angles, with the integration strategy for the next major release.
(click) What is new compared with our earlier KG work: that was hand-built and static. This is generated, and it is about operations.
-->

---
clicks: 4
---

# Three semantics, three languages

<ThreeLayers :step="$clicks" />

<div class="grid grid-cols-2 gap-4 -mt-1 text-sm" :class="$clicks >= 4 ? '' : 'invisible'">
<div class="card"><b>①</b> each OWL property → <code>era:shaclShapeValidationRule</code> → its SHACL shape</div>
<div class="card"><b>②</b> each code-list property → <code>era:inSkosConceptScheme</code> → its concept scheme</div>
</div>

<!--
[9:00 → 10:10]
This is the core design, Table 1 of the paper. Same fragment of the TAF schema.
1 Complex types, elements, attributes and type extension go to OWL: reusable domain meaning, where the open-world reading is right.
2 Occurrences, choices, patterns, length and value facets go to SHACL: closed-world validation.
3 Enumerations go to SKOS, because code lists evolve independently and are reused across messages. A SHACL constraint checks membership in the scheme (dashed line).
4 And the layers stay navigable: from a property you can reach its shape and its concept scheme.
-->

---

# Transformation rules

<div class="rosetta mt-2">

| XSD construct | <span class="pill owl">OWL</span> | <span class="pill shacl">SHACL</span> | <span class="pill skos">SKOS</span> |
|---|---|---|---|
| `complexType` | `owl:Class` | `sh:NodeShape` | – |
| element / attribute of simple type | `owl:DatatypeProperty`, `rdfs:range xsd:*` | `sh:PropertyShape`, `sh:datatype` | – |
| element of complex type | `owl:ObjectProperty`, `rdfs:range` class | `sh:class` / `sh:node` | – |
| `extension` | `rdfs:subClassOf` | shape reuses base properties | – |
| `minOccurs` / `maxOccurs` | (existence only) | `sh:minCount` / `sh:maxCount` | – |
| `choice` | (approximated) | `sh:xone` | – |
| `pattern`, `min/maxLength`, `min/maxInclusive` | – | `sh:pattern`, `sh:min/maxLength`, `sh:min/maxInclusive` | – |
| `enumeration` | `owl:ObjectProperty`, `rdfs:range skos:Concept` | `sh:class skos:Concept` + SPARQL `skos:inScheme` check | `skos:ConceptScheme`, `skos:Concept`, `skos:notation` |
| `documentation` | `rdfs:comment` | `sh:description` | `skos:prefLabel` |

</div>

<div class="text-sm muted mt-3"><code>xsd:all</code> and <code>xsd:choice</code> are enforced in SHACL but only approximated in OWL, which expresses neither ordering nor exclusivity.</div>

<!--
[10:10 → 10:30]
The rules in one table; I won't read it. Two things to notice: cardinalities never become OWL restrictions, only existence; and every enumeration produces something in all three languages.
-->

---
clicks: 3
---

# The pipeline

<Pipeline :step="$clicks" />

<!--
[10:30 → 11:30]
It runs as a continuous-integration workflow in seven stages. Four schema families: TAF, two TAP families (B5 and B10) and NeTEx, each with its imports and includes.
1 Generation emits one OWL file, one SHACL file and one SKOS file per code list. Post-processing places terms in the era: namespace and derives readable labels. It is deterministic: the same XSD release gives the same artifacts, so every term traces back to its normative source.
2 Merge builds one graph per family and a combined one without NeTEx; publication goes to the vocabulary portal.
3 On the instance side, messages are lifted with RML and validated against the generated shapes; competency questions run on top.
-->

---

# Worked example · from XSD to three layers

<div class="smallcode">

```xml
<xs:simpleType name="CompanyCode">
  <xs:restriction base="String4-4"><xs:pattern value="[0-9A-Z]{4}"/></xs:restriction>
</xs:simpleType>
<xs:simpleType name="BorderPointTypeCodeList"> <!-- code list B.1.3 -->
  <xs:restriction base="xs:nonNegativeInteger">
    <xs:enumeration value="1001"> ... Sarkiai(Gr) ... </xs:enumeration> ...
```

</div>

<div class="text-center muted -my-1">↓ xsd2rdf + post-processing</div>

<div class="smallcode">

```turtle {1-4|5-12|13-15|all}
# OWL
era:PathConfirmedMessage a owl:Class ; rdfs:label "Path confirmed message"@en .
era:borderPointTypeCodeList a owl:ObjectProperty ; rdfs:range skos:Concept ;
    era:inSkosConceptScheme b13:BorderPointTypeCodeList .
# SHACL
nsh:CompositIdentifierPlannedType a sh:NodeShape ;
    sh:targetClass era:CompositIdentifierPlannedType ; sh:property shp:Company .
shp:Company a sh:PropertyShape ; sh:path era:company ; sh:pattern "[0-9A-Z]{4}" .
shp:BorderPointTypeCodeList a sh:PropertyShape ; sh:path era:borderPointTypeCodeList ;
    sh:class skos:Concept ; sh:nodeKind sh:IRI ;
    sh:sparql [ sh:select """ ... FILTER NOT EXISTS {
        ?concept skos:inScheme b13:BorderPointTypeCodeList } ... """ ] .
# SKOS
b13:1001 a skos:Concept ; skos:inScheme b13:BorderPointTypeCodeList ;
    skos:notation "1001"^^xsd:token ; skos:prefLabel "Sarkiai(Gr)"@en .
```

</div>

<!--
[11:30 → 12:10]
The running example end to end. Two XSD fragments: the CompanyCode pattern and the border-point code list.
(click) OWL: the message class, and the code-list property pointing to its scheme.
(click) SHACL: the pattern on era:company, and the membership check for border points: a SPARQL constraint that the concept is in scheme B.1.3.
(click) SKOS: the concept 1001, with its notation and label.
-->

---

# Worked example · a real message

<div class="grid grid-cols-2 gap-5 smallcode">
<div>

```xml
<PlannedTransportIdentifiers>
  <ObjectType>TR</ObjectType>
  <Company>2171</Company>
  <Core>----80803003</Core>
  <Variant>00</Variant>
  <TimetableYear>2024</TimetableYear>
</PlannedTransportIdentifiers>
```

<div class="text-xs muted text-center">fragment of a real <code>PathConfirmedMessage</code></div>
</div>
<div>

```turtle
:id2 a era:CompositIdentifierPlannedType ;
    era:objectType ot:TR ;
    era:company "2171" ;
    era:core "----80803003" ;
    era:variant "00" ;
    era:timetableYear 2024 .
```

<div class="text-xs muted text-center">lifted by a declarative mapping that uses the generated vocabulary</div>
</div>
</div>

<div class="mt-4">

**Validate `era:company`.** One shape accepts legacy and new codes during the Organization Code migration:

<PatternCheck class="mt-2" />

</div>

<!--
[12:10 → 13:10]
A fragment of a real path-confirmed message, and its RDF form. Note the division of labour: xsd2rdf produced the vocabulary and the shapes; the message is lifted by a mapping.
Live demo: 2171 and 0071, legacy codes: valid. An alphanumeric code: valid. 07A: rejected.
-->

---
layout: section
---

# Results

## Coverage, validity, quality, conflicts, competency questions

<RailAgenda :current="3" on-dark class="mt-10" />

---

# Coverage and syntactic validity

<div class="grid grid-cols-4 gap-3 mt-1">
<div class="hero"><div class="n">57 / 57</div><div class="l">XSD constructs supported</div></div>
<div class="hero"><div class="n">2,630</div><div class="l">Turtle artifacts</div></div>
<div class="hero"><div class="n">0</div><div class="l">parse failures (independent parser)</div></div>
<div class="hero"><div class="n">53.9 MB</div><div class="l">uncompressed RDF</div></div>
</div>

<div class="grid grid-cols-2 gap-8 mt-5">
<div>

**Constructs used per schema** (of 57)

<div class="bars mt-2">
<div v-for="b in [['TAF', 55], ['TAP B5', 40], ['TAP B10', 41], ['NeTEx', 43]]" :key="b[0]" class="bar-row">
  <span class="bl">{{ b[0] }}</span>
  <span class="track"><span class="fill" :style="{ width: (b[1] / 57 * 100) + '%' }"></span></span>
  <span class="bv">{{ b[1] }}</span>
</div>
</div>

<div class="text-xs muted mt-2">Only <code>xsd:all</code> is used by none of the schemas; the converter supports it anyway. Full matrix in the paper's appendix.</div>

</div>
<div>

**Published artifacts**

<div class="rosetta">

| | TAF/TAP | NeTEx | Total |
|---|---:|---:|---:|
| Turtle files | 519 | 2,111 | 2,630 |
| OWL / SHACL / OWL-constraint | 6 / 6 / 3 | 2 / 2 / 1 | 8 / 8 / 4 |
| SKOS concept-scheme files | 500 | 2,106 | 2,606 |
| Merged graphs | 4 | 0 | 4 |
| Uncompressed RDF (MB) | 12.9 | 41.0 | 53.9 |

</div>

<div v-click class="card mt-3 text-sm">NeTEx: <b>80 %</b> of the files and over <b>¾</b> of the content, a first argument for keeping it a <b>separate module</b>.</div>

</div>
</div>

<style>
.bar-row { display: grid; grid-template-columns: 70px 1fr 34px; align-items: center; gap: 8px; margin: 7px 0; font-size: 14px; }
.bl { text-align: right; color: var(--c-ink); }
.track { height: 12px; background: var(--c-surface); border-radius: 0 4px 4px 0; border-left: 1.5px solid var(--c-ink-subtle); }
.fill { display: block; height: 100%; background: var(--c-blue); border-radius: 0 4px 4px 0; }
.bv { font-weight: 700; font-variant-numeric: tabular-nums; }
</style>

<!--
[13:20 → 14:10]
All 57 XSD constructs found in the TEL TSI schemas are supported. TAF is the richest, using 55.
Every one of the 2,630 files parses with a parser independent of the pipeline.
(click) NeTEx is 80 % of the files: code lists, mostly. Remember that for the integration strategy.
-->

---

# Ontology pitfalls with OOPS!

<div class="text-sm muted">Post-processed TAP B10 module; no parsing failure. On NeTEx the OOPS! web service timed out after 60 s, so NeTEx relies on parser validation.</div>

<div class="grid grid-cols-3 gap-4 mt-4">
<div class="layer" style="border-top-color: var(--c-bad)">
<span class="pill" style="background: var(--c-bad-bg); color: var(--c-bad)">genuine defects · fix in generator</span>

- **P08** 102 missing annotations · minor
- **P34** 1 untyped class · important
- P04 1 unconnected element · minor
- P20 10 annotation issues · minor
- P22 1 naming inconsistency · minor

</div>
<div class="layer" style="border-top-color: var(--c-good)">
<span class="pill" style="background: var(--c-good-bg); color: var(--c-good)">expected by design</span>

- **P10** missing disjointness · important
- **P13** 43 undeclared inverses · minor

<div class="text-sm mt-2">The XSDs state neither. Adding them automatically would add <b>commitments absent from the regulation</b>.</div>
</div>
<div class="layer" style="border-top-color: var(--c-yellow)">
<span class="pill" style="background: var(--c-warn-bg); color: var(--c-warn-ink)">to review</span>

- **P11** 54 properties without domain or range · important

</div>
</div>

<div v-click class="tk mt-5 text-lg">For schema-derived ontologies, OOPS! is a <b>review queue</b>, not a pass/fail criterion.</div>

<!--
[14:10 → 14:50]
OOPS! on the TAP B10 module. Some pitfalls are real defects the generator can fix: missing annotations, the untyped class.
Others are expected: the XSDs say nothing about disjointness or inverses, and inventing them would put commitments in the ontology that the regulation does not make.
(click) So we treat the report as a review queue.
-->

---

# Conflicts with ERA Ontology v3.3.2

<div class="text-sm muted -mt-2 mb-1">Critical conflicts block a merge: the same IRI with a different type, label or range, or a property declared both as object and as datatype property.</div>

<ConflictBars />

<div class="grid grid-cols-3 gap-3 mt-2 text-sm">
<div v-click class="card"><code>era:primaryLocationCode</code><br>range <code>xsd:string</code> vs <code>xsd:positiveInteger</code><br>→ keep <code>xsd:string</code>, the code as exchanged</div>
<div v-click class="card"><code>era:PrimaryLocation</code><br>"Primary Location" vs "Location ident"<br>→ keep the core label; XSD name as <code>skos:altLabel</code></div>
<div v-click class="card"><code>era:startLocation</code> / <code>endLocation</code><br>end of a tunnel vs journey location<br>→ a homonym: needs a <b>curated decision</b></div>
</div>

<div v-click class="card warn mt-3 text-sm">📍 Most remaining conflicts sit at the <b>location anchor</b>. These are <b>proposals</b>; the decisions rest with the <b>ERA Ontology CCM board</b>.</div>

<!--
[14:50 → 16:00]
Because TAF and TAP terms are destined for the core, the pipeline compares every module with the ERA Ontology.
In the June release, TAF had 13 URI collisions and 8 property type conflicts. A preliminary re-run with xsd2rdf 1.6.0, which separates datatype and object properties that share a name (era:length versus era:lengthReference), brings these down to 6 and 1. Hover for each pair. NeTEx, 38 and 20, was not re-run yet.
(click ×3) Three of the remaining ones: the code as a string or an integer; the label; and a real homonym: start and end location mean the ends of a tunnel in the core, journey locations in TAF. Only a curated decision can resolve that.
(click) Most sit at the location anchor. The generator does not resolve them silently: they go to the change control board.
If asked about review-level findings: 40 / 28 / 28 inverse-property candidates (10,148 for NeTEx) come from lexical matching, with obvious false positives such as era:customer paired with prov:wasDerivedFrom. A review queue, not a defect count.
-->

---

# 92 competency questions

<div class="grid grid-cols-2 gap-6 mt-1">
<div>

Drafted with **railway domain experts**; each records an expected answer, the message types and an **executable SPARQL query**. **26 message types** covered.

<div class="bars mt-3">
<div v-for="b in [['PathRequest', 15], ['PathDetails', 15], ['delay reporting', 10], ['path unavailability', 8], ['train running info', 7]]" :key="b[0]" class="bar-row">
  <span class="bl">{{ b[0] }}</span>
  <span class="track"><span class="fill" :style="{ width: (b[1] / 15 * 100) + '%' }"></span></span>
  <span class="bv">{{ b[1] }}</span>
</div>
</div>
<div class="text-xs muted">CQs on the best-covered message types (a CQ may cover several).</div>

<div class="text-sm mt-3">
<b>Q9</b> train compositions between two locations · <b>Q15</b> delays along a path · <b>Q56</b> most frequent RID classes between two countries · <b>Q63</b> ECM certificates expiring
</div>

</div>
<div>

**Q2** · How many hand-over points on the path of a given train?

<div class="smallcode">

```sparql {all|7-8|all}
PREFIX era:  <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT (COUNT(?loc) AS ?handoverCount) WHERE {
  ?msg a era:PathDetailsMessage ; era:pathInformation ?pi .
  ?pi  era:plannedJourneyLocation ?loc .
  ?loc era:operationalTrainNumber "75853" ;
       era:journeyLocationTypeCode/skos:notation ?code .
  FILTER (str(?code) = "03") }
```

</div>

<div v-click class="card good mt-3 text-sm">✅ The CQs are a <b>regression suite</b>: re-run on every schema release, they catch breaking changes in classes and properties <b>before publication</b>.</div>

</div>
</div>

<style>
.bar-row { display: grid; grid-template-columns: 130px 1fr 30px; align-items: center; gap: 8px; margin: 6px 0; font-size: 13.5px; }
.bl { text-align: right; color: var(--c-ink); }
.track { height: 12px; background: var(--c-surface); border-radius: 0 4px 4px 0; border-left: 1.5px solid var(--c-ink-subtle); }
.fill { display: block; height: 100%; background: var(--c-blue); border-radius: 0 4px 4px 0; }
.bv { font-weight: 700; font-variant-numeric: tabular-nums; }
</style>

<!--
[16:00 → 16:50]
The functional test: 92 competency questions written with domain experts, published on the pipeline wiki. Strongest coverage on the path life-cycle.
Q2 counts the hand-over points on a train path. The location type code is a SKOS concept (click), matched through its notation, so the query works whatever label the code list carries.
(click) And because each CQ is executable, the catalogue protects every later release.
-->

---
layout: section
---

# Future work

## Towards ERA Ontology v4.0.0

<RailAgenda :current="4" on-dark class="mt-10" />

---
clicks: 3
---

# Integration strategy for v4.0.0

<ModuleMap :step="$clicks" />

<!--
[17:00 → 17:50]
The integration strategy.
1 TAF and TAP go into the core: they are railway-operational notions from the same regulatory source, of moderate size.
2 NeTEx stays the only separate module, in its own namespace. It imports the core where it needs to; the core never imports NeTEx. Links between generated and existing terms live in curated alignment modules with weak relations (closeMatch, subClassOf), not equivalence. Code lists remain separate modules because they change at a different rhythm.
3 Application profiles assemble what a use case needs: capacity management needs only the enlarged core; passenger information also imports NeTEx.
-->

---

# xsd2rdf since the paper · 1.6 → 2.1

<div class="rel mt-1">
<span class="r old">1.6.0 · Aug 2026<small>the paper's re-run</small></span><i>→</i>
<span class="r">2.0.0 · 21 Oct 2026<small>shape model, new IRIs</small></span><i>→</i>
<span class="r">2.0.1 · 21 Oct<small>repeated elements</small></span><i>→</i>
<span class="r">2.1.0 · 22 Oct 2026<small>provenance, w3id</small></span>
<span class="src">source: <code>CHANGELOG.md</code>,<br>checked against the 2.1.0 code</span>
</div>

<div class="grid grid-cols-3 gap-4 mt-4">
<div v-click class="layer" style="border-top-color: var(--c-good)">
<span class="pill" style="background: var(--c-good-bg); color: var(--c-good)">paper gaps closed in 2.0</span>

- ✅ `sh:pattern` anchored as `^(…)$`; several patterns ORed
- ✅ facet bounds typed with the base datatype
- ✅ `totalDigits`, `fractionDigits` → SPARQL constraints
- ✅ `xs:choice` → `sh:xone` over the shapes it creates
- ⬜ `whiteSpace`: still ignored

</div>
<div v-click class="layer owl">
<span class="pill owl">new capabilities</span>

- `xs:key` / `unique` / `keyref` → SPARQL constraints
- `--source-provenance`: each term → its XSD component, as `dct:source` <span class="pill grey">2.1</span>
- identical output on every run
- persistent namespace `w3id.org/xsd2rdf#` <span class="pill grey">2.1</span>
- OWL from a shape model: **~20× faster** on TAF

</div>
<div v-click class="layer" style="border-top-color: var(--c-yellow)">
<span class="pill" style="background: var(--c-warn-bg); color: var(--c-warn-ink)">breaking → regenerate</span>

- generated **IRIs and OWL output change**: re-convert, compare with 1.x
- a named `simpleType` is no longer an OWL property → re-run the **conflict report**
- unused imported components pruned by default → **artifact counts change**
- Python ≥ 3.12; 1.x CLI flags removed
- the counts on earlier slides are **1.x output**

</div>
</div>

<style>
.rel { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.rel .r { background: var(--c-blue-bg); color: var(--c-blue-strong); font-weight: 700; font-size: 14px; padding: 4px 12px; border-radius: 10px; line-height: 1.15; }
.rel .r small { display: block; font-weight: 400; font-size: 11px; color: var(--c-ink-mod); }
.rel .r.old { background: var(--c-surface); color: var(--c-ink-mod); }
.rel i { font-style: normal; color: var(--c-ink-mod); }
.rel .src { margin-left: auto; font-size: 11px; color: var(--c-ink-mod); text-align: right; line-height: 1.3; }
.rel .src code { font-size: 10.5px; padding: 0 3px; }
.slidev-layout .layer code { font-size: .72rem; padding: 0 3px; }
.slidev-layout .layer { font-size: .94rem; }
.slidev-layout .layer li { line-height: 1.4; margin: .25rem 0; }
.slidev-layout .layer code { font-size: .82rem; }
</style>

<!--
[17:50 → 18:40]
The converter did not stand still after the paper. Our conflict numbers came from 1.6.0, in August. Since then: 2.0 and 2.1, in October.
(click) Three of the fidelity gaps from the paper are closed: patterns are anchored, which is exactly the case on slide 18; facet bounds are typed; digit facets become SPARQL constraints. whiteSpace is still ignored.
(click) New: keys and key references become constraints, and with --source-provenance every generated term points to the XSD component it came from, as a W3C component designator. That makes the traceability we claim machine-readable.
(click) The price: IRIs and OWL output change. So the extension has to be regenerated and the conflict report and the competency questions re-run before v4.0.0. Which is exactly the release loop on the next slide.
If asked about determinism: 2.0 lists "the output is the same on every run" under Fixed (#27), so 1.x runs were not always identical. Check with the developers what differed before answering.
-->

---

# Next steps

<div class="grid grid-cols-3 gap-5 mt-4">
<div class="contrib"><div class="num">1</div>

### Regenerate, then resolve

Re-convert with **xsd2rdf 2.1** and re-run the conflict report; resolve with the **CCM ontology board**, then integrate TAF/TAP into the **v4.0.0** core.

</div>
<div class="contrib"><div class="num">2</div>

### Close the fidelity gaps

- ✅ anchored patterns <span class="pill grey">2.0</span>
- ✅ typed facet bounds <span class="pill grey">2.0</span>
- ✅ `totalDigits`, `fractionDigits` <span class="pill grey">2.0</span>
- ⬜ `whiteSpace`
- ⬜ propagate concept-scheme renaming (post-processing)

</div>
<div class="contrib"><div class="num">3</div>

### Reference query sets

Publish **SPARQL query sets** for cross-border operational analytics.

</div>
</div>

<div class="mt-7 text-sm font-bold muted">EVERY TEL TSI RELEASE, TWICE A YEAR</div>
<div class="loop mt-2">
<span>regenerate</span><i>→</i><span>conflict report</span><i>→</i><span>92 CQs</span><i>→</i><span>CCM board</span><i>→</i><span>release</span><i>↺</i>
</div>

<style>
.loop { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.loop span { background: var(--c-blue-bg); color: var(--c-blue-strong); font-weight: 700; padding: 6px 14px; border-radius: 18px; font-size: 15px; }
.loop i { font-style: normal; color: var(--c-ink-mod); font-size: 18px; }
</style>

<!--
[18:40 → 19:20]
Three next steps. Regenerate with 2.1, then the conflict decisions with the board, then integration. Of the fidelity gaps, three are closed in the converter; whiteSpace and the concept-scheme renaming in post-processing remain. And reference query sets for cross-border analytics.
Because the schemas change twice a year, each release follows the same loop; these reports are the evidence base for the board.
-->

---
layout: center
class: text-center
---

# Lessons learned

<div class="grid grid-cols-4 gap-4 mt-8 text-left">
<div class="tk">🧩<br><b>Separate the three semantics from the start.</b><br>Most XSD-lifting problems come from forcing constraints and code lists into OWL.</div>
<div class="tk">📋<br><b>Quality reports are review queues.</b><br>Pitfalls and conflict counts mean something only against the source schemas.</div>
<div class="tk">📦<br><b>Keep code lists modular.</b><br>They change most often and are reused most widely.</div>
<div class="tk">✅<br><b>Competency questions are regression tests.</b><br>Written once with experts, they protect every release.</div>
</div>

<!--
[19:20 → 19:45]
Four lessons, if you remember only one: give each kind of semantics its own language.
-->

---
layout: center
class: text-center
hideLogo: true
---

<img src="/assets/era-ontology-logo-white.png" class="h-20 mx-auto dark:hidden" alt="ERA Ontology · Interoperable by Design" />
<img src="/assets/era-ontology-logo-blue.png" class="h-20 mx-auto hidden dark:block rounded" alt="ERA Ontology · Interoperable by Design" />

# Thank you · questions?

<div class="text-left text-sm leading-relaxed mt-3 inline-block rosetta">

**Ghislain Atemezing** · Polymnia Vassilopoulou · <a href="mailto:ghislain.atemezing@era.europa.eu">ghislain.atemezing@era.europa.eu</a>

| | |
|---|---|
| Converter | <a href="https://pypi.org/project/xsd2rdf/">pypi.org/project/xsd2rdf</a> · EUPL 1.2 |
| Pipeline and CQ catalogue | <a href="https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/era-telematics-ontology-pipeline">gitlab.com/era-europa-eu/…/era-telematics-ontology-pipeline</a> |
| Documentation | <a href="https://rinf.uat.data.test-era.europa.eu/era-vocabulary/telematics-appGuide/">telematics-appGuide</a> · <a href="https://rinf.uat.data.test-era.europa.eu/era-vocabulary/netex-appGuide/">netex-appGuide</a> |
| v4.0.0 release candidate | <a href="https://rinf.uat.data.test-era.europa.eu/era-vocabulary/ontology.ttl">era-vocabulary/ontology.ttl</a> |
| ERA Ontology releases | <a href="https://doi.org/10.5281/zenodo.21046698">doi.org/10.5281/zenodo.21046698</a> |

</div>

<!--
[19:45 → 20:00]
Everything is open, under the EUPL. Thank you; happy to take questions.
-->
