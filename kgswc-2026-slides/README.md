# A Semantic Backbone for European Rail Data Exchange · KGSWC 2026

Slidev deck for the KGSWC 2026 paper *A Semantic Backbone for European Rail Data Exchange:
Automating the Telematics Extension of the ERA Ontology* (Ghislain Atemezing, Polymnia Vassilopoulou,
European Union Agency for Railways). It is a 20-minute talk: 29 slides, including 5 section dividers.

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
| Cover, agenda | 1–2 | 0:00–1:00 |
| 1 · ERA Ontology context | 3–7 | 0:50–5:10 |
| 2 · Objective of the paper | 8–11 | 5:10–8:10 |
| 3 · Contributions | 12–18 | 8:10–13:10 |
| 4 · Results | 19–23 | 13:10–16:50 |
| 5 · Future work, lessons, questions | 24–29 | 16:50–20:00 |

The timing is tight. If you run long, skip slide 15 (the transformation-rules table, 20 s) and slide 21 (OOPS!).

## Components

| File | Used on | What it shows |
|---|---|---|
| `components/RailAgenda.vue` | agenda, section dividers | the agenda as a railway line; a train runs to the current section |
| `components/StationGraph.vue` | slide 5 | Valenciennes station from rinf-plus: identity, position, tracks and platform, primary locations, each property with a plain-English gloss |
| `components/ThreeLayers.vue` | slide 14 | one XSD split into OWL, SHACL and SKOS (Table 1), with the cross-links |
| `components/Pipeline.vue` | slide 16 | the 7-stage CI pipeline and the instance-data path (Fig. 1) |
| `components/PatternCheck.vue` | slide 18 | live check of `[0-9A-Z]{4}`: anchored XSD vs unanchored `sh:pattern` (Sect. 4.2 gap) |
| `components/ConflictBars.vue` | slide 22 | critical conflicts before vs after xsd2rdf 1.6.0 (Table 5) |
| `components/ModuleMap.vue` | slide 25 | v4.0.0 integration: core + TAF/TAP, NeTEx module, alignments, profiles |
| `components/CoverArt.vue` | cover | rails turning into a graph with OWL, SHACL and SKOS hubs |
| `slide-top.vue` | every slide | corner logo and footer. It is per-slide rather than `global-top`, so the PDF export gets them too. `hideLogo: true` in a slide's frontmatter removes the logo. |

## Sources

- All figures come from the paper (Tables 2–7, Listings 1.1–1.5, Sects. 2–7), except slides 5, 7 and 26.
- Slide 5 shows live rinf-plus data queried on 2026-11-10: `operationalPoint/83728fa739` (Valenciennes,
  graph `0087`), `track/669db3f795` ("Voie A de Valenciennes") and `platformEdge/1e0ce8c500` ("Quai 1").
  The manager's name (SNCF Réseau, code 0087) comes from OCR-KG. Re-check it before the talk if the data is republished.
- Slide 7 summarises the TEL TSI technical documents v4.0 (TD B5 and its annexes, B10, B15, B16, B17, 105 and the
  Ontology TD) from [tsi_telematics/pdf](https://gitlab.com/era-europa-eu/public/era-telematics-tsi/tsi_telematics/-/tree/main/pdf).
  The quote is from TD B5 Annex A2, §1.1.4. The list of four input XSDs comes from the Ontology TD.
- Slide 26 ("xsd2rdf since the paper") summarises the xsd2rdf
  [CHANGELOG](https://gitlab.com/era-europa-eu/public/interoperable-data-programme/era-ontology/xsd2rdf/-/blob/main/CHANGELOG.md)
  for 2.0.0–2.1.0 (21–22 Oct 2026), checked against the 2.1.0 source on 2026-11-10. Update it when a new release comes out.
- `ex:` terms on slide 10 and the code `X7K2` on slide 18 are illustrative; the slides label them so.
- Logos: `public/assets/era-ontology-logo-{blue,white}.png` are the ERA Ontology "Interoperable by Design" logo.
