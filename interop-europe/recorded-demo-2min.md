# Two-Minute Recorded Demo: Reusing ERA Data Stories by Member State

## Purpose

Show how a Member State can reuse the 38 visible RINF Data Stories SPARQL queries and the 3 downloadable SPARQL notebooks as a practical interoperability assessment kit.

## Recording Setup

- Browser with the ERA endpoint open: https://rinf.data.era.europa.eu/endpoint
- Browser tab for RCC: https://rinf.data.era.europa.eu/route-compatibility
- Local file open: `interop-europe/data-stories-queries.md`
- Optional country to use in the demo: Belgium, France, Italy, Poland, or the Member State most relevant to the audience.

## 2-Minute Script

### 0:00-0:12 - Open The Reuse Kit

**On screen:** Open `data-stories-queries.md` and show the headings:

- Visible Query Catalogue
- SPARQL Notebooks
- Internal Computed Story Queries

**Narration:**

This demo shows how the ERA ontology and RINF Knowledge Graph can be reused by any Member State as an interoperability assessment kit. The file shown here extracts the public Data Stories queries: 38 visible SPARQL queries and 3 downloadable SPARQL notebooks.

### 0:12-0:30 - Run The Four Inventory Queries

**On screen:** Copy or point to the four inventory queries:

- `operational-points-per-member-state.sparql`
- `sections-of-line-per-member-state.sparql`
- `length-of-lines-per-member-state.sparql`
- `length-of-tunnels-per-member-state.sparql`

Open the ERA endpoint and run one inventory query, or show prepared results.

**Narration:**

The first reuse pattern is basic coverage. A Member State can immediately check how many operational points, sections of line, line kilometres and tunnel kilometres are represented in the European graph. This gives a shared baseline before discussing data quality or interoperability.

### 0:30-0:43 - Inspect One Member State

**On screen:** Filter the query result for one country, or highlight one country row.

**Narration:**

Here we focus on one Member State. The important point is that every country can run the same query, over the same public graph, using the same ERA definitions. The comparison is not hidden in a national spreadsheet or a proprietary report.

### 0:43-1:02 - Run Completeness And Investigator Queries

**On screen:** Show one general completeness query and one investigator query:

- `completeness-load-capability-1-v2.sparql`
- `track-completeness-investigator-v2.sparql`

Then show asset-specific alternatives for operational points, sections of line, tunnels, sidings, platforms, contact line systems and train detection systems.

**Narration:**

The second reuse pattern is completeness. These queries show which core parameters are present or missing by Member State. The investigator queries then let a data steward drill into one country and one property. This turns interoperability assessment into an operational data-quality workflow.

### 1:02-1:17 - Show SKOS Concept-Scheme Discipline

**On screen:** Search within the file or notes for `era:opType`. Show the expected concept scheme:

`http://data.europa.eu/949/concepts/op-types/OperationalPointTypes`

**Narration:**

Interoperability is not only about whether a value exists. It is also about whether the value uses the correct controlled vocabulary. For example, `era:opType` should use the Operational Point Types SKOS concept scheme. A similar-looking value from another scheme is a data-quality issue because applications can no longer compare operational points reliably.

### 1:17-1:28 - Show Deprecated-Term Warning Pattern

**On screen:** Show a note or query comment: filter out ontology properties marked `owl:deprecated true` for current conformance analysis.

**Narration:**

The same discipline applies to deprecated ontology terms. Live SPARQL may still contain legacy triples using deprecated properties. Those values are useful for migration audits, but they should not be counted as valid current conformance unless the analysis explicitly targets legacy data.

### 1:28-1:43 - Run TEN-T Or Track-Location Query

**On screen:** Show one route-relevant query:

- `ten-t-5-wheelSetGauge.sparql`
- `ten-t-6-energySupplySystem.sparql`
- `ten-t-11-etcsBaselineAndLevel.sparql`
- `track_rinf_properties_with_location.sparql`

**Narration:**

The third reuse pattern links data quality to services. TEN-T and track-location queries expose the infrastructure parameters needed for cross-border planning and route compatibility: gauge, energy system, ETCS level and baseline, and the location of track properties.

### 1:43-1:55 - Open RCC

**On screen:** Open https://rinf.data.era.europa.eu/route-compatibility.

Show origin, destination and optional via-point selection if available.

**Narration:**

The Route Compatibility Check app makes the value concrete. It combines RINF infrastructure data with ERATV vehicle-type data to ask whether a vehicle type can travel between operational points. The current page is a proof of concept, and it is clear about its limits: complete operational reliability requires better explicit track connectivity and navigability data.

### 1:55-2:08 - Conclude With Notebooks As Reuse Packages

**On screen:** Return to `data-stories-queries.md` and show:

- `completeness.sparqlbook`
- `otherqueries.sparqlbook`
- `tentqueries.sparqlbook`

**Narration:**

This is reusable because the assessment logic is not hidden in a national system. It is expressed as open SPARQL over a public ERA Knowledge Graph, grounded in ERA ontology terms, SKOS vocabularies and SHACL validation. Any Member State can rerun the same checks, compare results, improve its data, and contribute back to the shared European interoperability layer.

## Shorter Voiceover Version

This demo shows how any Member State can reuse the ERA Data Stories as an interoperability assessment kit. We start from a catalogue of 38 SPARQL queries and 3 notebooks extracted from the public RINF Data Stories app. First, we run the inventory queries to see operational points, sections of line, line length and tunnel length by Member State. Then we focus on one country and move from coverage to completeness, using the general completeness query and an investigator query to identify missing parameters.

The assessment is semantic, not just statistical. For `era:opType`, values must come from the Operational Point Types SKOS concept scheme. Similar-looking values from another scheme break interoperability. Current analysis should also filter deprecated ontology properties, because live SPARQL may still contain legacy data that should be handled as migration evidence, not current conformance.

Finally, we connect the queries to services. TEN-T and track-location queries provide the parameters needed for route planning and compatibility checks. The RCC app demonstrates the direction: RINF infrastructure data and ERATV vehicle-type data can support route compatibility, provided topology and navigability data are complete enough. The notebooks then package these checks so Member States can rerun, compare, improve and contribute back.
