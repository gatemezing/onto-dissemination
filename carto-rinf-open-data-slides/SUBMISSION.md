# FOSDEM 2027 submission · Railways and Open Transport devroom

Submit at <https://fosdem.org/submit>, track **Railways and Open Transport**, by **27 November 2026,
23:59 Brussels time**. Selected talks are announced on 7 December; the devroom runs on the morning of
Saturday 30 January 2027, on site only.

## Title

Build on the rail graph: Europe's railway infrastructure as open linked data

## Abstract

Europe's rail registers are public: the infrastructure of 28 countries (RINF), authorised vehicle types
(ERATV), safety certificates, licences and EC declarations (ERADIS), and the telematics reference codes
for companies and locations. The European Union Agency for Railways (ERA) is bringing them into one
knowledge graph, starting with RINF: about 42 million triples behind a public SPARQL endpoint, with no key
or account. Few developers know it's there.

This talk shows what you can build on it, through Carto RINF, an MIT-licensed map of stations, lines,
tunnels, bridges and track parameters that queries the graph live, with no database of its own. You'll
see a first query in five minutes, the quirks of data from 71 publishers and how to handle them, and how
linking to Wikidata took station enrichment from 12% to 38%. We'll also look at what EU open-data and
interoperability law, which now tells public bodies to prefer open-source solutions, means for people
building on public data.

## Description

What you'll take away:

- **Where the data comes from.** RINF is public by law (Directive (EU) 2016/797, Art. 49). ERA's other
  registers are set up under EU law too, and ERADIS, ERATV and the telematics reference data can be
  searched publicly today. Organisation codes and legal references are already in the graph; ERADIS and
  ERATV are being migrated. The high-value-datasets
  regulation and the Interoperable Europe Act point the same way.
- **How to query it.** One HTTP POST, from curl or from a static web page. The ERA Ontology (EUPL 1.2) and
  its SKOS vocabularies give every country the same model.
- **How a small app is built on it.** Carto RINF is React and MapLibre plus a thin Node server with a
  6-hour cache. Going from France to all 28 countries took two days, because every manager publishes into
  the same model.
- **What real data looks like.** Versioned records, missing country links, geometry in two places, and
  the fixes, each measured and covered by a regression test.
- **Why identifiers matter.** Matching RINF to Wikidata on three keys: the primary location code, the ERA
  ID, and the UIC station code, accepted only within 1 km.
- **How builders feed back.** A fix in the graph reaches every app at once. And there's an open question
  we'd like help with: a machine-readable licence for the data.

Links:

- SPARQL endpoint: <https://graph.data.era.europa.eu/repositories/rinf-plus>
- ERA's RINF platform: <https://rinf.data.era.europa.eu/>
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
