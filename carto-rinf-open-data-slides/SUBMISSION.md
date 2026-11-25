# FOSDEM 2027 submission · Railways and Open Transport devroom

Submit at <https://fosdem.org/submit>, track **Railways and Open Transport**, by **27 November 2026,
23:59 Brussels time**. Selected talks are announced on 7 December; the devroom runs on the morning of
Saturday 30 January 2027, on site only.

## Title

Build on the rail graph: Europe's rail registers as open linked data

## Abstract

Europe's rail registers are public: the infrastructure of 28 countries (RINF: the 25 EU Member States
with a railway, plus Norway, Switzerland and Liechtenstein), authorised vehicle types (ERATV), safety
certificates, licences and EC declarations (ERADIS), the telematics codes for companies and locations,
and references to EU rail law (ERA-Lex). The European Union Agency for Railways (ERA) is bringing them
into one knowledge graph, linked by shared identifiers. RINF is live, with about 42 million triples
behind a public SPARQL endpoint and no key or account; organisation codes and legal references are
already in, and ERADIS and ERATV are joining. Few developers know it's there.

This talk shows what you can build on it, through Carto RINF, an MIT-licensed map that queries the graph
live with no database of its own: a first query in five minutes, the quirks of data from 71 publishers,
how linking to Wikidata took station enrichment from 12% to 38%, and app ideas that join the registers.

## Description

What you'll take away:

- **Where the data comes from.** RINF is public by law (Directive (EU) 2016/797, Art. 49). ERADIS rests
  on Directives (EU) 2016/797 and 2016/798 and Regulation (EU) 2016/796, the telematics reference data on
  the Telematics TSI. EU open-data and interoperability law points the same way: the high-value-datasets
  regulation asks for APIs, documented semantics and open licences, and the Interoperable Europe Act tells
  public bodies to prefer open-source solutions.
- **Which registers you can use today.** RINF is in the graph, and so are 5,659 organisation codes and
  7,317 legal resources from ERA-Lex. ERADIS, public without an account, and ERATV, with a public list and
  search, are being migrated, as is the European Vehicle Register. ERADIS and ERATV explorers on ERA's
  preview graphs, a primary-location extractor and a check of RNE's locations against RINF are already
  built on them. ERSAD, the European Railway Station Accessibility Database, is public as a web
  application, outside the graph.
- **How to query it.** One HTTP POST, from curl or from a static web page, to `rinf-plus` or its sister
  repositories `OCR-KG` and `era-lex`. The ERA Ontology (EUPL 1.2), with its SKOS vocabularies and SHACL
  shapes, gives every country the same model, and the registers joining the graph share its identifiers.
- **How a small app is built on it.** Carto RINF is React and MapLibre plus a thin Node server with a
  6-hour cache. Going from France to all 28 countries took two days, because every manager publishes into
  the same model.
- **What real data looks like.** Versioned records, missing country links, geometry in two places, and
  the fixes, each measured and covered by a regression test.
- **Why identifiers matter.** Matching RINF to Wikidata on three keys: the primary location code, the ERA
  ID, and the UIC station code, accepted only within 1 km. The same codes join the registers: RINF's
  primary locations carry the telematics location codes.
- **What to build next.** Apps that join registers: route checks that put RINF's gauge, energy, ETCS and
  speed against ERATV's vehicle types; accessible journeys from ERSAD's station accessibility data (PRM
  TSI) and RINF's platforms; or "who runs what", from ERADIS licences and safety certificates with the
  companies' telematics codes.
- **How builders feed back.** A fix in the graph reaches every app at once. And there's an open question
  we'd like help with: a machine-readable licence for the data.

Links:

- SPARQL endpoint: <https://graph.data.era.europa.eu/repositories/rinf-plus>
- ERA Knowledge Graph: <https://www.era.europa.eu/domains/registers/era-knowledge-graph>
- ERA's RINF platform: <https://rinf.data.era.europa.eu/>
- ERADIS, ERATV, ERSAD and the telematics reference data: <https://eradis.era.europa.eu/>,
  <https://eratv.era.europa.eu/Eratv>, <https://ersad.data.era.europa.eu/>, <https://teleref.era.europa.eu/>
- ERA's public GitLab: <https://gitlab.com/era-europa-eu/public>
- Carto RINF (MIT): <https://github.com/gatemezing/SemanticsCartoTchoo>

## Notes for the organisers

20 minutes including Q&A: about 15 minutes of talk and 5 of questions. Presented on site. No live demo,
so nothing depends on the venue's network: screenshots and recorded query timings are in the slides.

## Speaker biography

Ghislain Atemezing is a Project Officer in the ICT & Operational Data Systems Unit of the European Union
Agency for Railways (ERA), where since 2023 he has worked on the ERA Knowledge Graph and the open tools
built on it. Before ERA he was Research & Development Director at Mondeca, and he holds a PhD in Computer
Science from Télécom Paris (2015) on publishing and consuming geospatial and government data on the
Semantic Web. He has maintained Linked Open Vocabularies (LOV) since 2012, co-edited the W3C note "Best
Practices for Publishing Linked Data", and chaired the 2nd Rail Data Forum in 2025.

Homepage: <https://perso.linkedvocabs.org/>

<!-- Source: perso.linkedvocabs.org, last updated 19 August 2026. Other links it lists: ORCID
0000-0003-1562-6922, github.com/gatemezing, linkedin.com/in/gatemezing. -->
