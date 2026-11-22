# Build on the rail graph · Carto RINF for open data developers

Slidev deck for open data developers in the Railways and Open Transport devroom at FOSDEM 2027 (Brussels,
30 January 2027): why Europe's rail registers are open (EU open-data and interoperability law, rail law)
and which of ERA's registers you can use today (RINF, ERADIS, ERATV, telematics reference data, ERA-Lex),
what the ERA Knowledge Graph gives a developer, what [Carto RINF](https://github.com/gatemezing/SemanticsCartoTchoo)
built on it, what real-world data taught us, and why the next app should be theirs.
About 15 minutes, leaving 5 for questions in the devroom's 20-minute slot (Q&A included): 22 slides,
including 5 section dividers, plus 7 backup slides (four cut for time, three of sources). The submission
text is in [SUBMISSION.md](SUBMISSION.md).

It uses the template of the [KGSWC 2026 deck](../kgswc-2026-slides/): Slidev, the same `style.css`,
`slide-top.vue`, `RailAgenda.vue` and the ERA Ontology logo.

## Run

```bash
npm install
npm run dev      # presenter view: press "p", or open /presenter/
npm run build    # static SPA in dist/
npm run export   # PDF in dist/carto-rinf-open-data.pdf (needs playwright-chromium and its browser)
```

The deck follows the system light/dark setting. Use the toggle in the navigation bar to switch.

## Structure and timing

Each slide's speaker notes start with its time window, for example `[8:00 → 9:00]`.

| Section | Slides | Time |
|---|---|---|
| Cover, agenda | 1–2 | 0:00–0:40 |
| 1 · Open by law (EU law, rail law, Interoperable Europe Act, ERA's registers) | 3–7 | 0:40–4:15 |
| 2 · A graph, not a file (incl. the first query) | 8–10 | 4:15–6:25 |
| 3 · Carto RINF | 11–13 | 6:25–8:15 |
| 4 · Real-world lessons | 14–17 | 8:15–11:25 |
| 5 · Your turn, thank you | 18–22 | 11:25–14:50 |
| Backup: where ERA publishes it, small on purpose, provider variance, what a link brings in, three of sources | 23–29 | on demand |

## Components

| File | Used on | What it shows |
|---|---|---|
| `components/RailAgenda.vue` | agenda, section dividers | the agenda as a railway line (template component, new stations) |
| `components/CoverArt.vue` | cover | rails turning into a graph with RINF, Wikidata and "your app" hubs (template component, new labels) |
| `components/MatchBars.vue` | slide 16 | RINF primary locations matched to Wikidata, per country, before vs after (same encoding as the template's `ConflictBars.vue`) |
| `slide-top.vue` | every slide | corner logo and footer (template, new footer text) |

## Sources

Every number was measured live, or comes from a cited page. The backup slide lists them.

- **Legal basis**: Art. 49 of Directive (EU) 2016/797, Art. 37(3)(h) of Regulation (EU) 2016/796 and
  Implementing Regulation (EU) 2019/777, as quoted in the [RINF terms of use](https://www.era.europa.eu/system/files/2022-11/rinf_terms_of_use_en.pdf)
  (v1.0, 2022).
- **EU open-data and interoperability law**, read on EUR-Lex on 22 Nov 2026: Directive 2007/2/EC (INSPIRE,
  Annex I theme 7, which names rail), Directive (EU) 2019/1024 (Art. 1(1)(b), 14, 17(1), 21),
  Implementing Regulation (EU) 2023/138 (Art. 3(1), 4(3), 6; Annex 6.1, which sends mobility to INSPIRE's
  transport networks, and 6.2), Regulation (EU) 2024/903 (Art. 1(2), 2(4), 2(5), 3, 4(1), 4(3), 4(6), 23(2);
  recital 28). COM(2020) 66 and COM(2023) 751 are cited by reference.
- **Interoperable Europe portal**: the ERA Ontology's entry in the SEMIC collection (EUPL 1.2, published
  4 Aug 2026), read on 22 Nov 2026.
- **ERA's catalogue on data.europa.eu**: catalogue `era` via the portal's search API, 22 Nov 2026 (14 datasets;
  the Knowledge Graph record's licence, endpoint and landing page; the ontology record's version).
- **ERA's platform**: the routes of `rinf.data.era.europa.eu` (search, map explorer, dataset explorer, data
  stories, route compatibility, vocabulary), read from its web app on 22 Nov 2026.
- **ERA Knowledge Graph** (registers and their status, ontology v3.3.4, Art. 4(8), EUPL 1.2, service desk):
  [ERA's Knowledge Graph page](https://www.era.europa.eu/domains/registers/era-knowledge-graph), updated 21 Sep 2026.
- **Copyright**: [ERA disclaimer and copyright notice](https://www.era.europa.eu/content/disclaimer-and-copyright-notice).
- **Live SPARQL on `rinf-plus`, 20 Nov 2026**: 52,677 distinct uopids in 71 named graphs; 41,999,268 triples;
  licence statements (125 SKOS schemes CC BY 4.0, SHACL shapes EUPL, NUTS EUPL 1.1, none on RINF instance
  data); the two example queries (0.8 s and 1.4 s); CORS (the endpoint echoes the request's `Origin`).
- **Carto RINF**: provider variance from its `docs/ROADMAP.md` (measured 2026-10); the fixes, matching and
  enrichment numbers measured live on 20–21 Nov 2026 against `rinf-plus` and query.wikidata.org. The
  Wikidata property shares are over the 7,528 Wikidata items that carry a primary location code (`P12783`).
  The line join (`P1671`) was measured but is not in the app yet.
- **Screenshots**: `public/assets/carto-rinf-switzerland.jpg` and `carto-rinf-bern-wikidata.jpg` were taken
  from a local Carto RINF on 20–21 Nov 2026. Map data © OpenStreetMap contributors.
- **Logos**: `public/assets/era-ontology-logo-{blue,white}.png`, copied from the KGSWC 2026 deck.

Re-check the counts before the talk if the data has been republished.
