# onto-dissemination

This repository collects materials and demo assets used to disseminate the ERA ontology (ERA vocabulary) and demonstrate "follow your nose" Linked Data navigation for railway infrastructure data.

Contents
- `scripts/innotrans2026-era-ontology-script.md`: booth/demo script, elevator pitch, demo queries, and checklist for InnoTrans 2026.
- `scripts/assets/era-follow-your-nose-scene.html`: demo scene / explainer mockup (video/animation source).
- `scripts/assets/era-graph-explorer-app.html`: interactive offline demo app (single-file HTML) for the bubble-graph explorer.

Live demo
- **https://gatemezing.github.io/onto-dissemination/** — the GitHub Pages deployment of `era-graph-explorer-app.html`, rebuilt automatically by [.github/workflows/pages.yml](.github/workflows/pages.yml) on every push to `main` that touches the app file.

Quick start
- To view the offline interactive demo, open [scripts/assets/era-graph-explorer-app.html](scripts/assets/era-graph-explorer-app.html) in a modern browser. For best results run a local HTTP server from the repository root and open the file URL in your browser:

```bash
python3 -m http.server 8000
# then open http://localhost:8000/scripts/assets/era-graph-explorer-app.html
```

- The `era-follow-your-nose-scene.html` file is a stylised demo/scene used to create a short explainer video. Open it the same way or use the `era-graph-explorer-app.html` for interactive navigation.

What this repo is for
- Provide a rehearsable booth script and demo assets to explain the ERA ontology (see `scripts/innotrans2026-era-ontology-script.md`).
- Ship an offline, clickable graph demo so the booth can run without relying on external network or CORS — plus an experimental live SPARQL mode for visitors who want to query the real graph.

Notes & checklist
- **Offline demo rebuilt around Oslo S (2026-08-16):** the curated offline dataset now centres on `https://data.banenor.no/data/_station_c0576848-8f76-4489-aa6e-ae95b98c1a1c` (Oslo Central Station, published by Bane NOR using the ERA ontology), replacing the original Brussels Airport walkthrough. Every node/edge was fetched live over HTTP during this session — Bane NOR's own Linked Data server plus the ERA SPARQL endpoint for shared `era:` URIs — not screenshots or invented data. See Section 6 of `scripts/innotrans2026-era-ontology-script.md` for the full worked example and reuse-hub findings.
- **Live SPARQL mode fixed and verified (2026-08-16):** the app's "Try live SPARQL" data source points at `https://graph.data.era.europa.eu/repositories/rinf-plus`, the GraphDB repository behind ERA's own graph browser. Confirmed reachable with a real browser-shaped request (GET, with an `Origin` header) — it returns correct data and sends back an `Access-Control-Allow-Origin` header that allows cross-origin `fetch()`, so it works from the GitHub Pages deployment. The previously-configured endpoint (`rinf.data.era.europa.eu/api/v1/sparql/rinf`) does not work from a browser: GET requests to it hang with no response, and its CORS policy only allows its own app's origin. Note this endpoint is ERA-specific — it won't resolve non-ERA Linked Data URIs like Bane NOR's, even though the offline Oslo S dataset above was partly sourced from there.
- Bubbles now size themselves to their label content and connecting edges trim to the visible gap between bubbles instead of running underneath them; the breadcrumb tags live-fetched nodes and never mixes a live trail with an offline one.
- Verify remaining live queries (Section 5 of the script) and legal/version wording before publishing or printing — see the checklist inside `scripts/innotrans2026-era-ontology-script.md`.
