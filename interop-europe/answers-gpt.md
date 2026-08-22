## Labelled solutions have to be assessed for their reusability in interoperability assessments

### 1. Would it make sense for public authorities to look in this context at the reusability of your solution for the implementation of the assessed decision?

Yes. Public authorities should assess the reusability of the ERA ontology solution because it addresses a core interoperability problem in public-sector data exchange: different authorities can comply with the same legal obligation while still using different terms, code lists, identifiers and data structures. The ERA ontology reduces that gap by providing a common, machine-readable semantic model for railway infrastructure, authorised vehicle types, vehicle-register information and interoperability/safety evidence, governed by the European Union Agency for Railways and aligned with the relevant application guides: RINF, ERATV, EVR and ERADIS.

The case for reuse is strong because this is not a theoretical model. The ERA ontology is published as RDF, with dedicated SKOS controlled vocabulary and SHACL validation artefacts, and RINF data has been published as an RDF Knowledge Graph queryable through SPARQL since 2021. The same semantic framework is also used to document ERATV vehicle-type parameters, ERADIS certification and compliance concepts, and EVR-related vehicle registration concepts. This means the solution can be reused both by policy and data teams: policy teams get a traceable link from legal parameters to data elements, while technical teams get stable URIs, graph data, validation rules and endpoint access.

For an interoperability assessment, this is exactly the type of solution that should be examined: it turns regulation-driven registers into reusable data infrastructure. It supports semantic interoperability, data quality checks, reuse across Member States, and practical services such as route compatibility analysis, parameter completeness monitoring, vehicle/infrastructure compatibility, certification evidence reuse and cross-border comparison of infrastructure and vehicle characteristics.

The Route Compatibility Check (RCC) application is a particularly convincing example of this value. It brings together RINF infrastructure data and ERATV vehicle-type data around a concrete public-service question: can a given railway vehicle type travel between selected operational points? Even where the current RCC page is presented as a proof of concept rather than an operationally complete RCC report generator, it demonstrates the practical policy value of the ontology: once infrastructure elements, tracks, operational points, vehicle types and compatibility parameters share the same semantic model, they can be combined in applications instead of being manually reconciled case by case.

### 2. What was your main challenge to implement this solution, and which were the main lessons learnt following the implementation?

The main challenge was not only to publish an ontology, but to make it operational for real public-sector data across several connected registers and legal processes. RINF contains detailed infrastructure parameters, national practices, infrastructure-manager datasets, controlled lists, topology relationships and legal references. ERATV adds authorised vehicle-type characteristics and authorisation cases. EVR adds vehicle registration concepts. ERADIS adds interoperability and safety evidence, certification-level documents, compliance checks and restrictions. The difficult part was aligning all of these into a model that is precise enough for railway experts, stable enough for implementers, and usable enough for public authorities and application developers.

Several practical lessons followed.

First, governance is as important as modelling. The RINF Technical Annex records versioned changes, SHACL corrections, parameter refinements and domain/range adjustments. That shows that a public ontology must be maintained as a living asset, with transparent releases and issue handling, not treated as a one-off documentation exercise.

Second, validation must be part of the solution. The published ERA SHACL shapes make it possible to check whether data follows the intended structure, controlled vocabularies, cardinalities and parameter-specific constraints. This is essential when many national entities publish data into a shared European knowledge graph.

Third, linked data exposes both value and data-quality differences. The data stories and SPARQL examples show how the Knowledge Graph can answer concrete questions, such as the number of operational points or sections of line per Member State, total infrastructure length, and completeness of core parameters. That makes quality gaps visible and actionable.

Fourth, controlled vocabularies need strict concept-scheme discipline. A SKOS concept is not valid only because its local code looks familiar. For example, `era:opType` is the RINF parameter "Type of operational point" and its values are expected to come from the specific Operational Point Types concept scheme: `http://data.europa.eu/949/concepts/op-types/OperationalPointTypes`. If a dataset uses a similarly coded concept from another scheme, such as a national or legacy operational-point-type scheme, the value may look understandable to a person but it breaks semantic comparability and should be treated as a conformance/data-quality issue. This is exactly why SHACL checks against the expected SKOS scheme are needed.

Fifth, deprecated ontology terms must be excluded from current interoperability analysis. Live SPARQL data may still carry values on properties marked `owl:deprecated` or with an archaic/deprecated term status, because legacy data and migration processes do not disappear immediately. That data can be useful for audit or migration, but it should not be counted as valid current conformance without an explicit exception. Queries and validation reports should therefore filter out deprecated properties and follow the replacement term when one is provided.

Sixth, usability matters. Public authorities need more than RDF files. They need browsable documentation, application guides, examples, queries, APIs, and simple tools that allow non-ontology specialists to inspect values, compare countries and export data.

Seventh, demonstrators should be honest about data readiness. The RCC application explicitly warns that the current RINF dataset does not yet contain the full explicit connectivity and navigability relationships between tracks needed to calculate complete, operationally reliable routes. This is a useful lesson for public-sector interoperability: the ontology enables reuse, but operational services also depend on coverage, topology quality, validation, expert-agreed business rules and clear liability boundaries.

### 3. Do you envisage collaboration with other Member States or Union entities, e.g. around future developments of the solutions, and how?

Yes. Collaboration is both necessary and already built into the nature of the solution. The ERA ontology is governed at EU level and the RINF Technical Annex states that applicability and data format are discussed and agreed within RINF Topical Working Groups. The same principle applies across ERATV, EVR and ERADIS: infrastructure data, vehicle-type data, vehicle registration data and certification evidence must remain consistent enough to support EU-wide railway interoperability. This is the right model for future development: a central semantic core governed by ERA, with structured input from Member States, infrastructure managers, National Registration Entities, vehicle authorisation actors, conformity assessment bodies and Union bodies.

Future collaboration should focus on four areas.

First, Member States should continue to contribute implementation feedback: ambiguous parameters, missing controlled-list values, national modelling cases, validation issues and cross-border edge cases.

Second, Union entities should support convergence around shared artefacts: stable URIs, the ERA SKOS file, the ERA SHACL shapes, application-guide updates and reference SPARQL queries.

The `era:opType` case is a concrete example of where collaboration matters. If one publisher uses values from the required Operational Point Types scheme and another uses values from a different but similarly named scheme, downstream applications cannot reliably compare operational points across borders. The fix is not only technical; it requires shared governance of code lists, migration guidance, validation reports and agreement on whether divergent concepts should be mapped, deprecated or corrected at source. The same discipline applies to deprecated ontology properties: if a property is marked as deprecated, administrations need a coordinated migration path so live data can be corrected rather than silently perpetuating obsolete semantics.

Third, administrations and infrastructure managers should share reusable tools and data stories. Queries for completeness reports, route-compatibility checks and parameter comparison should not be rebuilt separately in each country.

The RCC app also shows where collaboration should go next: infrastructure managers and RCC experts need to converge on the detailed connectivity, navigability and compatibility data required for production-grade route compatibility. The proof-of-concept app assumes simplified connectivity inside operational points; moving from demonstration to operational use requires agreed topology modelling, complete track-to-track relationships and shared interpretation of the parameters used in compatibility checks.

Fourth, collaboration should include extension governance. Local or national extensions may be needed, but they should remain interoperable with the ERA core through documented mappings, clear namespaces and validation rules.

### 4. Is your solution suitable for local, regional, or national public administrations?

Yes. The solution is suitable at all three levels, provided the administration has a need to publish, validate, exchange or consume structured infrastructure data.

At national level, the fit is direct: RINF is a national-register and European-scale obligation, and National Registration Entities need a common model for collecting and submitting data about their Member State network. The same reuse logic applies to national actors involved in vehicle registration, vehicle type authorisation, safety certification and interoperability evidence.

At regional level, the ontology can support infrastructure planning, investment coordination, accessibility analysis, safety-related reporting and integration with geographic or transport datasets. The ontology already represents infrastructure elements such as operational points, sections of line, tracks, platforms, signals, tunnels and related topology, and also links infrastructure characteristics to vehicle and authorisation concepts that matter for compatibility and operational planning.

At local level, the value is more selective but still real. Local authorities operating stations, multimodal hubs or public transport interfaces can benefit when railway infrastructure data is linked to local mobility, accessibility, asset-management or emergency-planning datasets. The benefit increases when local data uses the same identifiers, country vocabularies, geospatial standards and controlled lists as national and EU systems.

The solution is therefore not limited to central railway authorities. It is most powerful nationally and cross-border, but it also gives local and regional administrations a clean way to connect their own data to authoritative European infrastructure, vehicle, registration and certification data.

The RCC use case also makes the value understandable for administrations that are not ontology specialists. A user selects origin, destination and optional via operational points, and the system can use the shared data model to plan a route and screen compatibility against vehicle-type data. That is the difference between publishing data and making data interoperable enough to support a service.

### 5. Does it need central governance, or does it also bring value, if deployed in just some entities?

It needs central governance for the shared semantic core, but it also brings value when reused by only some entities.

Central governance is needed because semantic interoperability depends on common meaning. If each authority changes parameter definitions, URI patterns, code lists, concept schemes or validation rules independently, the shared European graph loses comparability. ERA governance, versioned releases, SHACL shapes and SKOS concept schemes provide the trust framework that makes data reusable across borders. Governance also has to manage deprecation: live data can contain obsolete terms, but assessment and reuse should be based on the current non-deprecated ontology terms unless a migration/audit use case explicitly requires otherwise.

However, partial deployment is still valuable. A single infrastructure manager or administration can reuse the ontology to structure its own data, publish linked data, validate quality, export machine-readable RINF/ERATV/EVR/ERADIS-aligned information and prepare for later integration. Even before every Member State adopts the same level of maturity, early adopters gain better documentation, clearer internal data ownership, automated validation and easier connection to EU-level services.

At the same time, the RCC example shows why central governance cannot be skipped. Route compatibility depends on cross-border consistency in infrastructure parameters, vehicle-type parameters, controlled vocabularies and topology. If some entities publish only partial data, the ontology still brings local value; but a complete RCC service needs common governance and quality expectations across the relevant networks.

The practical model should therefore be federated implementation under central semantic governance: ERA maintains the authoritative model and common rules; national and local entities reuse them in their own systems and contribute improvements through governed channels.

### 6. How does your solution support the data exchange between borders and EU sovereignty?

The solution supports cross-border data exchange by replacing document-by-document interpretation with shared, machine-readable meaning. Railway operations are inherently cross-border: infrastructure, routes, vehicles, vehicle types, safety constraints, signalling systems, authorisation cases and certification evidence must be understood consistently across national networks. The ERA ontology gives Member States a common semantic layer for describing those assets, parameters and evidential relationships.

It supports EU sovereignty in three concrete ways.

First, it uses EU-governed public data infrastructure. The ontology is governed by ERA, released under the EUPL 1.2, and published with open semantic artefacts rather than depending on a proprietary platform or vendor-specific data model.

Second, it creates reusable European identifiers and vocabularies. Stable URIs and SKOS concepts make it possible to compare data across countries without forcing every administration into the same internal IT system. The important condition is that properties use their intended concept schemes; for example, `era:opType` should use Operational Point Types, not a divergent scheme with superficially similar codes.

Third, it improves independent verification. Because data can be queried through SPARQL and validated with SHACL, authorities can check completeness, consistency and conformance without relying only on manual reporting. The published data stories illustrate this with queries for Member State counts, infrastructure length and core-parameter completeness, and the same approach can be applied to vehicle-type, registration and compliance data. To remain accurate, those analyses should join against the ontology/SHACL/SKOS artefacts and exclude deprecated ontology properties from current compliance counts, even if the live graph still contains triples using them.

Fourth, it supports EU-level services without centralising every national system. RCC is a good illustration: infrastructure data can remain published by infrastructure managers and Member States, vehicle-type data can come from ERATV, and the EU-level semantic layer allows applications to combine them. This supports sovereignty because Europe governs the shared meanings, identifiers, validation rules and public-service logic rather than outsourcing interoperability to private bilateral mappings.

This combination is important for sovereignty: Europe keeps control of the semantic rules, the public register logic and the quality criteria, while allowing distributed implementation by Member States and infrastructure managers.

### 7. What is the first step to take to reuse your solution?

The first step is to select one concrete interoperability use case and map it to the ERA ontology and the relevant application guide: RINF for infrastructure, ERATV for authorised vehicle types, EVR for vehicle registration, or ERADIS for interoperability and safety evidence. Good starting use cases are parameter completeness by country, publication of one infrastructure-manager dataset, route-compatibility data, operational point lookup, comparison of a specific RINF parameter across Member States, or checking whether vehicle-type characteristics use the same concept schemes as infrastructure compatibility parameters.

For an RCC-oriented reuse scenario, the starting point should be deliberately narrow: select a sample origin and destination operational point, identify the relevant sections of line and tracks, verify that the required RINF infrastructure parameters are present, identify the ERATV vehicle type to test, and document which compatibility checks are reliable with the available data. This avoids the common mistake of treating a proof-of-concept route result as an operational RCC report.

A practical reuse path is:

1. Identify the objects and parameters needed for the use case in the relevant browsable Technical Annex: RINF, ERATV, EVR or ERADIS.
2. Reuse the corresponding ERA classes, properties, register indexes and SKOS concept schemes.
3. Test data against the published SHACL shapes.
4. Query the live ERA Knowledge Graph/SPARQL endpoint or a local RDF copy to compare with existing public data.
5. Publish or exchange the data using stable URIs and standard RDF serializations.
6. Document any national extension separately and propose common improvements through the ERA governance process when the issue is not purely local.
7. Add explicit validation for concept-scheme membership. For `era:opType`, check that every value is a `skos:Concept` in `http://data.europa.eu/949/concepts/op-types/OperationalPointTypes`; values from another operational-point-type scheme should be reported, corrected or mapped through a governed process.
8. Filter out deprecated ontology properties for current conformance analysis. In SPARQL, do not treat values on properties marked `owl:deprecated true` or otherwise deprecated/archaic in the ontology as valid current data unless the task is explicitly a legacy-data migration report.
9. For route compatibility reuse, verify topology and navigability data explicitly. A route-based service is only as reliable as the track connectivity, operational point modelling, vehicle-type references and compatibility parameters behind it.

This keeps reuse manageable: start small, stay aligned with the governed model, validate early, and expand from one use case to broader interoperability.

## Source notes

- ERA Ontology v3.3.4, released 10 August 2026: https://rinf.data.era.europa.eu/era-vocabulary/
- ERA SHACL shapes: https://rinf.data.era.europa.eu/era-vocabulary/era-shapes
- ERA SKOS controlled vocabularies: https://rinf.data.era.europa.eu/era-vocabulary/era-skos
- RINF Technical Annex v3.3.4, released 10 August 2026: https://rinf.data.era.europa.eu/era-vocabulary/rinf-appGuide/
- ERATV Technical Annex: https://rinf.data.era.europa.eu/era-vocabulary/eratv-appGuide/
- EVR Technical Annex: https://rinf.data.era.europa.eu/era-vocabulary/evr-appGuide/
- ERADIS Technical Annex v3.3.4, released 10 August 2026: https://rinf.data.era.europa.eu/era-vocabulary/eradis-appGuide/
- RINF Data Stories: https://rinf.data.era.europa.eu/data-stories
- RINF Route Compatibility Check app: https://rinf.data.era.europa.eu/route-compatibility
- Interoperable Europe Portal entry for the ERA Vocabulary: https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/era-vocabulary-era-ontology
