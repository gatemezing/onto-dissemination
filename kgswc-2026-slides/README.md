# A Semantic Backbone for European Rail Data Exchange · KGSWC 2026

Slidev deck for the KGSWC 2026 paper *A Semantic Backbone for European Rail Data Exchange:
Automating the Telematics Extension of the ERA Ontology* (Ghislain Atemezing, Polymnia Vassilopoulou,
European Union Agency for Railways). It is a 20-minute talk: 31 slides, including 5 section dividers, plus 2 backup slides after the questions.

The style follows [Dots and lines](https://matdata-eu.github.io/slides-railway-meso-macro-topology/)
(Slidev, a custom `style.css`, click-driven Vue/SVG components), restyled with the ERA Ontology logo
and its blue (`#004493`).

## Run

```bash
npm install
npm run dev      # presenter view: press "p", or open /presenter/
npm run build    # static SPA in dist/
npm run export   # PDF in dist/kgswc-2026-era-telematics.pdf (needs playwright-chromium)
```

The deck follows the system light/dark setting. Use the toggle in the navigation bar to switch.

## Structure and timing

Each slide's speaker notes start with its time window, for example `[8:10 → 9:30]`.

| Section | Slides | Time |
|---|---|---|
| Cover, agenda | 1–2 | 0:00–0:50 |
| 1 · ERA Ontology context (incl. the 1-minute app video) | 3–8 | 0:50–5:30 |
| 2 · Objective of the paper | 9–12 | 5:30–8:10 |
| 3 · Contributions | 13–20 | 8:10–13:50 |
| 4 · Results | 21–24 | 13:50–16:40 |
| 5 · Future work, lessons, questions | 25–31 | 16:40–20:00 |
| Backup: transformation rules, OOPS! | 32–33 | on demand |

The timing is tight. If you run long, shorten the video (click it to pause and move on) or skip slide 18 (the rules table).

## Components

| File | Used on | What it shows |
|---|---|---|
| `components/RailAgenda.vue` | agenda, section dividers | the agenda as a railway line; a train runs to the current section |
| `components/StationGraph.vue` | slide 5 | Valenciennes station from rinf-plus: identity, position, tracks and platform, primary locations, each property with a plain-English gloss |
| `components/AppMontage.vue` | slide 6 | plays `public/assets/one-graph-many-apps.mp4` when the slide opens, pauses on leave, click to pause; the poster stands in for it in the PDF |
| `components/ThreeLayers.vue` | slide 15 | one XSD split into OWL, SHACL and SKOS (Table 1), with the cross-links |
| `components/Pipeline.vue` | slide 16 | the 7-stage CI pipeline and the instance-data path (Fig. 1) |
| `components/PatternCheck.vue` | slide 20 | live check of `[0-9A-Z]{4}`: anchored XSD vs unanchored `sh:pattern` (Sect. 4.2 gap) |
| `components/ConflictBars.vue` | slide 23 | critical conflicts before vs after xsd2rdf 1.6.0 (Table 5) |
| `components/ModuleMap.vue` | slide 26 | v4.0.0 integration: core + TAF/TAP, NeTEx module, alignments, profiles |
| `components/CoverArt.vue` | cover | rails turning into a graph with OWL, SHACL and SKOS hubs |
| `slide-top.vue` | every slide | corner logo and footer. It is per-slide rather than `global-top`, so the PDF export gets them too. `hideLogo: true` in a slide's frontmatter removes the logo. |

## The app video (slide 6)

A 58-second live recording of the same station in two applications built on the ERA Knowledge Graph:
- **ERA's RINF unified search:** filter on Unique OP ID 1.2.0.0.0.2 (`era:uopid`), table view, generated SPARQL.
- **RINF Atlas:** search, fly to the station, same IRI and graph `0087`, Graph tab.

The clip ends on a split screen and a credits card.

To re-record it, for example after the data is republished, use `tools/montage/`:

```bash
npm install                                   # playwright-chromium comes with the deck
node tools/montage/record.mjs                 # drives both apps live; frames in tools/montage/frames/
cd tools/montage/frames && ffmpeg -f concat -safe 0 -i list.txt \
  -vf "fps=25,format=yuv420p" -c:v libx264 -preset slow -crf 22 -movflags +faststart \
  ../../../public/assets/one-graph-many-apps.mp4
```

`compose.html` holds both apps in iframes with the captions and a visible cursor; `record.mjs` holds the storyboard and timing.
The selectors follow the two apps as of 11 Nov 2026. A UI change in either app can break the script.

## Sources

- All figures come from the paper (Tables 2–7, Listings 1.1–1.5, Sects. 2–7), except slides 5, 6, 8, 17, 18, 27 and 28.
- Slide 5 shows live rinf-plus data queried on 2026-11-10: `operationalPoint/83728fa739` (Valenciennes,
  graph `0087`), `track/669db3f795` ("Voie A de Valenciennes") and `platformEdge/1e0ce8c500` ("Quai 1").
  The manager's name (SNCF Réseau, code 0087) comes from OCR-KG. Re-check it before the talk if the data is republished.
- Slides 17, 18 and 28 are adapted, with attribution on each slide, from slides 16, 17 and 19 of
  [What the telematics sources get wrong](https://matdata-eu.github.io/slides-telematics-xsd-source-issues/)
  by Mathias Vanden Auweele (ERA, Nov. 2026). Its slide content is CC BY 4.0. They show the pipeline status after the paper.
- Slide 8 summarises the TEL TSI technical documents v4.0 (TD B5 and its annexes, B10, B15, B16, B17, 105 and the
  Ontology TD) from [tsi_telematics/pdf](https://gitlab.com/era-europa-eu/public/era-telematics-tsi/tsi_telematics/-/tree/main/pdf).
  The quote is from TD B5 Annex A2, §1.1.4. The list of four input XSDs comes from the Ontology TD.
- Slide 27 ("xsd2rdf since the paper") summarises the xsd2rdf
  [CHANGELOG](https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/xsd2rdf/-/blob/main/CHANGELOG.md)
  for 2.0.0–2.1.0 (21–22 Oct 2026), checked against the 2.1.0 source on 2026-11-10. Update it when a new release comes out.
- `ex:` terms on slide 11 and the code `X7K2` on slide 20 are illustrative; the slides label them so.
- Logos: `public/assets/era-ontology-logo-{blue,white}.png` are the ERA Ontology "Interoperable by Design" logo.
