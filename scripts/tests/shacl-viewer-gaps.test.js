/* Tests for the OWL gap analysis of the SHACL Shape Viewer
   (scripts/assets/era-shacl-viewer.html, served as shapes.html).

   The page's pure functions are loaded from the HTML file itself; the page
   part of the script is skipped without a DOM. Each check has a fixture that
   must be flagged and, where it matters, one that must not.

   Run:  npm install --no-save n3@1.17.2 && node --test scripts/tests/
   (n3 is the version the page pins from unpkg.) */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs'), path = require('path'), vm = require('vm');
const N3 = require('n3');

const html = fs.readFileSync(path.join(__dirname, '../assets/era-shacl-viewer.html'), 'utf8');
const mod = {exports: {}};
vm.runInContext([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'),
  vm.createContext({N3, module: mod, console, URL, URLSearchParams, setTimeout, clearTimeout}));
const V = mod.exports;

const PREFIXES = `
@prefix era: <http://data.europa.eu/949/> .
@prefix es: <http://data.europa.eu/949/shapes/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix time: <http://www.w3.org/2006/time#> .
`;
const ONTOLOGY = PREFIXES + `
era: a owl:Ontology ; owl:versionInfo "v9.0.0" ;
  owl:versionIRI <https://gitlab.com/x/y/-/releases/v9.0.0> .

era:Track a owl:Class ; rdfs:label "Track"@en ; rdfs:comment "A track." ; dcterms:modifed "2026-01-01" .
era:Tunnel a owl:Class ; owl:disjointWith era:Bridge .
era:Bridge a owl:Class .
era:RailTunnel a owl:Class ; rdfs:subClassOf era:Tunnel .
era:Weird a owl:Class ; rdfs:subClassOf era:Tunnel , era:Bridge .
era:BookingCancelReply a owl:Class .
era:NetRelation a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty era:elementA ; owl:qualifiedCardinality 1 ; owl:onClass era:Track ] .
era:OldClass a owl:Class ; owl:deprecated "false"^^xsd:boolean .
<http://w3.org/ns/locn#Address> a owl:Class .

era:trackParam a owl:DatatypeProperty , owl:FunctionalProperty .
era:cant a owl:DatatypeProperty ; rdfs:subPropertyOf era:trackParam ; rdfs:domain era:Track ; rdfs:range xsd:integer ;
  era:shaclShapeValidationRule es:Missing .
era:ballast a owl:DatatypeProperty ; rdfs:subPropertyOf era:trackParam ; rdfs:domain era:Track ; rdfs:range xsd:boolean ;
  era:shaclShapeValidationRule es:Loose .
era:codeType a owl:DatatypeProperty ; rdfs:range xsd:int .
era:code a owl:ObjectProperty ; rdfs:subPropertyOf era:codeType .
era:roll a owl:DatatypeProperty ;
  rdfs:range [ a rdfs:Datatype ; owl:onDatatype xsd:double ; owl:withRestrictions ( [ xsd:minInclusive "0.0"^^xsd:decimal ] ) ] .
era:company a owl:DatatypeProperty ; rdfs:domain era:Bridge .
era:carrier a owl:DatatypeProperty ; rdfs:subPropertyOf era:company .
era:tunnelLength a owl:DatatypeProperty ; rdfs:domain era:Tunnel ; rdfs:range xsd:decimal .
era:length a owl:DatatypeProperty ; rdfs:domain [ owl:unionOf ( era:Track era:Tunnel ) ] ; rdfs:range xsd:decimal .
era:name a owl:DatatypeProperty ; rdfs:range rdf:langString .
era:count a owl:DatatypeProperty ; rdfs:range xsd:integer ; era:shaclShapeValidationRule es:Gauge .
era:element a owl:ObjectProperty ; rdfs:range era:Tunnel .
era:elementA a owl:ObjectProperty ; rdfs:range era:Track .
era:reply a owl:ObjectProperty ; rdfs:domain era:CancelReply ; rdfs:range era:Track .
era:opened a owl:DatatypeProperty ; rdfs:range xsd:date .
era:multi a owl:ObjectProperty ; rdfs:domain era:Track ; rdfs:domain era:Tunnel .
era:dup a owl:DatatypeProperty ;
  rdfs:domain [ owl:unionOf ( era:Track era:Bridge ) ] , [ owl:unionOf ( era:Track era:Bridge ) ] .
era:oldProp a owl:DatatypeProperty ; owl:deprecated true .
era:removedTrainLink a owl:ObjectProperty .
era:hasPart a owl:ObjectProperty ; owl:inverseOf era:isPartOf ; rdfs:domain era:Track ; rdfs:range era:Tunnel .
era:isPartOf a owl:ObjectProperty ; rdfs:domain era:Tunnel ; rdfs:range era:Bridge .
era:gauge a owl:DatatypeProperty , owl:FunctionalProperty ; rdfs:domain era:Track ; rdfs:range xsd:string ;
  era:rinfIndex "1.1.1" ; era:shaclShapeValidationRule es:Gauge .
time:hasBeginning a owl:ObjectProperty ; rdfs:domain time:TemporalEntity .
era:rinfIndex a owl:AnnotationProperty .
era:shaclShapeValidationRule a owl:AnnotationProperty .
`;
const SHAPES = PREFIXES + `
es:TrackShape a sh:NodeShape ; sh:targetClass era:Track ;
  sh:property es:Cant , es:Ballast , es:Carrier , es:Gauge , es:Length ,
    es:ElementTrack , es:Code , es:Beginning .
es:Cant sh:path era:cant ; sh:datatype xsd:int ; sh:maxCount 1 .
es:Ballast sh:path era:ballast ; sh:datatype xsd:boolean ; sh:maxCount 1 .
es:Carrier sh:path era:carrier ; sh:datatype xsd:string .
es:Gauge sh:path era:gauge ; sh:datatype xsd:string ; era:rinfIndex "1.1.1 " , "1.2.3" .
es:Length sh:path era:length ; sh:datatype xsd:decimal ; sh:maxCount 1 .
es:ElementTrack sh:path era:element ; sh:class era:Track .
es:Code sh:path era:code ; sh:class skos:Concept .
es:Beginning sh:path time:hasBeginning .

es:BridgeShape a sh:NodeShape ; sh:targetClass era:Bridge ;
  sh:property es:TunnelLength , es:ElementBridge , es:Name , es:Count ,
    es:Undeclared , es:Old , es:LiteralElement , es:IriCount .
es:TunnelLength sh:path era:tunnelLength ; sh:datatype xsd:decimal ; sh:maxCount 1 .
es:ElementBridge sh:path era:element ; sh:class era:Bridge .
es:Name sh:path era:name ; sh:datatype xsd:string .
es:Count sh:path era:count ; sh:datatype xsd:decimal .
es:Undeclared sh:path era:removedTrainLInk .
es:Old sh:path era:oldProp .
es:LiteralElement sh:path era:element ; sh:datatype xsd:string .
es:IriCount sh:path era:count ; sh:nodeKind sh:IRI .

es:RailTunnelShape a sh:NodeShape ; sh:targetClass era:RailTunnel ; sh:property es:TunnelLength2 .
es:TunnelLength2 sh:path era:tunnelLength ; sh:datatype xsd:decimal ; sh:maxCount 1 .
es:IntervalShape a sh:NodeShape ; sh:targetClass time:ProperInterval ; sh:property es:Beginning .
es:OffShape a sh:NodeShape ; sh:targetClass era:Bridge ; sh:deactivated true ; sh:property es:OffProp .
es:OffProp sh:path era:nothingDeclared .
es:GhostShape a sh:NodeShape ; sh:targetClass era:Ghost .
es:OldClassShape a sh:NodeShape ; sh:targetClass era:OldClass .
es:NetShape a sh:NodeShape ; sh:targetClass era:NetRelation ; sh:property es:ElementA .
es:ElementA sh:path era:elementA ; sh:class era:Track .
es:AddressShape a sh:NodeShape ; sh:targetClass <http://w3.org/ns/locn#Address> .
es:Loose sh:path era:ballast .
`;
const store = ttl => new N3.Store(new N3.Parser().parse(ttl));
const ERA = 'http://data.europa.eu/949/';
// Copied into this realm: objects made inside the vm context fail deepStrictEqual on their prototype.
const run = (opts = {}) => JSON.parse(JSON.stringify(V.gapAnalysis(store(ONTOLOGY), store(SHAPES), opts)));
const rep = run({releases: [{tag: 'v9.0.0-rc.1', name: 'Candidate v9.0.0-rc.1', date: '2026-11-01'}]});
const check = id => rep.checks.find(k => k.id === id);
const terms = id => check(id).findings.map(f => f.term);
const find = (id, pred) => check(id).findings.find(pred);
const sev = (id, term, ps) => (find(id, f => f.term === term && (!ps || f.ps === ERA + 'shapes/' + ps)) || {}).severity;

test('functional super-property validated with two sub-properties together is a blocker', () => {
  const f = find('functional-super', f => f.term === ERA + 'trackParam');
  assert.equal(f.severity, 'BLOCKER');
  assert.equal(f.ns, ERA + 'shapes/TrackShape');
  assert.equal(check('functional-super').findings.length, 1);
});

test('object/datatype property mixing, and the sh:class it breaks', () => {
  assert.deepEqual(terms('property-kind'), [ERA + 'code']);
  assert.equal(sev('class-range', ERA + 'code'), 'BLOCKER');
  assert.match(find('class-range', f => f.term === ERA + 'code').detail, /inherited from era:codeType|inherited from .*codeType/);
});

test('facets typed differently from their datatype', () => {
  assert.deepEqual(terms('facet-type'), [ERA + 'roll']);
});

test('a class under two disjoint classes is unsatisfiable', () => {
  assert.deepEqual(terms('unsat-class'), [ERA + 'Weird']);
});

test('shapes asking for the wrong kind of value', () => {
  const fs = check('shape-kind').findings.map(f => f.ps);
  assert.deepEqual(fs.sort(), [ERA + 'shapes/IriCount', ERA + 'shapes/LiteralElement']);
});

test('datatype against range: disjoint is a blocker, broader is major, derived is fine', () => {
  assert.equal(sev('datatype-range', ERA + 'name'), 'BLOCKER');
  assert.equal(sev('datatype-range', ERA + 'count'), 'MAJOR');
  assert.equal(sev('datatype-range', ERA + 'cant'), undefined, 'xsd:int is derived from xsd:integer');
});

test('class against range: disjoint, unrelated', () => {
  assert.equal(sev('class-range', ERA + 'element', 'ElementBridge'), 'BLOCKER');
  assert.equal(sev('class-range', ERA + 'element', 'ElementTrack'), 'MAJOR');
});

test('domains: inherited, own disjoint, union and subclass are fine', () => {
  assert.deepEqual(terms('domain-inherited'), [ERA + 'carrier']);
  assert.equal(find('domain-inherited', () => true).group, ERA + 'company');
  const own = check('domain-own').findings;
  assert.equal(own.length, 1);
  assert.equal(own[0].severity, 'BLOCKER');
  assert.equal(own[0].ns, ERA + 'shapes/BridgeShape');
  assert.ok(!own.some(f => f.term === ERA + 'length'), 'a union domain containing the target is fine');
});

test('undeclared terms, with suggestions; deactivated shapes are skipped', () => {
  assert.deepEqual(terms('undeclared-path'), [ERA + 'removedTrainLInk']);
  assert.match(check('undeclared-path').findings[0].detail, /removedTrainLink/);
  assert.deepEqual(terms('undeclared-class'), [ERA + 'Ghost']);
  assert.deepEqual(terms('undeclared-axiom-class'), [ERA + 'CancelReply']);
  assert.match(check('undeclared-axiom-class').findings[0].detail, /BookingCancelReply/);
});

test('misspelt standard namespace', () => {
  assert.deepEqual(terms('namespace-typo'), ['http://w3.org/ns/locn#Address']);
  assert.match(check('namespace-typo').findings[0].detail, /ontology and shapes/);
});

test('functional properties without sh:maxCount 1', () => {
  assert.deepEqual(terms('functional-maxcount'), [ERA + 'gauge']);
});

test('restriction cardinality not enforced by the shape', () => {
  assert.deepEqual(terms('restriction-cardinality'), [ERA + 'elementA']);
});

test('several different domains; identical copies are duplicates, not intersections', () => {
  assert.deepEqual(terms('multiple-domain-range'), [ERA + 'multi']);
  assert.deepEqual(terms('duplicate-axioms'), [ERA + 'dup']);
});

test('deprecation: true is flagged, false is not', () => {
  assert.deepEqual(terms('deprecated-in-shapes'), [ERA + 'oldProp']);
  assert.deepEqual(terms('deprecated-no-replacement'), [ERA + 'oldProp']);
});

test('non-OWL-2 datatypes', () => {
  assert.deepEqual(terms('non-owl2-datatypes'), [ERA + 'opened']);
});

test('validation-rule links: missing, never applied, about another term', () => {
  const g = Object.fromEntries(check('validation-rule-links').findings.map(f => [f.term, f.group]));
  assert.equal(g[ERA + 'cant'], 'shape not in the shapes graph');
  assert.equal(g[ERA + 'ballast'], 'shape never applied');
  assert.equal(g[ERA + 'count'], 'shape about another term');
  assert.equal(g[ERA + 'gauge'], undefined);
  assert.equal(sev('validation-rule-links', ERA + 'ballast'), 'MAJOR');
});

test('RINF index: spaces and an index the property lacks', () => {
  const groups = check('rinf-index').findings.map(f => f.group).sort();
  assert.deepEqual(groups, ['index not on the property', 'spaces in the shape’s index']);
});

test('predicate typos with a suggestion', () => {
  const f = check('predicate-typos').findings;
  assert.equal(f.length, 1);
  assert.equal(f[0].term, 'http://purl.org/dc/terms/modifed');
  assert.match(f[0].detail, /modified/);
});

test('inverse properties that do not mirror', () => {
  assert.ok(terms('inverse-mismatch').includes(ERA + 'hasPart'));
});

test('external domains: aligned through known axioms, or suggested', () => {
  const ext = check('external-alignment').findings;
  assert.deepEqual(ext.map(f => f.ns), [ERA + 'shapes/TrackShape'], 'time:ProperInterval is a time:TemporalEntity');
  assert.equal(ext[0].severity, 'SUGGESTION');
});

test('documentation: a documented term is not flagged', () => {
  assert.ok(!terms('missing-documentation').includes(ERA + 'Track'));
  assert.ok(terms('missing-documentation').includes(ERA + 'Tunnel'));
});

test('version metadata against GitLab releases, and without them', () => {
  assert.deepEqual(check('version-metadata').findings.map(f => f.group).sort(), ['owl:versionIRI', 'owl:versionInfo']);
  const offline = run({releases: null});
  assert.equal(offline.checks.find(k => k.id === 'version-metadata').findings.length, 0);
  assert.equal(offline.meta.releasesChecked, false);
});

test('actions: most severe first, causes before consequences, passes left out', () => {
  const sevs = rep.actions.map(k => V.GAP_CHECKS.findIndex(c => c.id === k.id));
  assert.ok(rep.actions.every(k => k.status === 'fail'));
  const ranks = rep.actions.map(k => ['BLOCKER', 'MAJOR', 'MINOR', 'SUGGESTION'].indexOf(k.severity));
  assert.deepEqual(ranks, [...ranks].sort((a, b) => a - b));
  const kind = rep.actions.findIndex(k => k.id === 'property-kind'), cls = rep.actions.findIndex(k => k.id === 'class-range');
  assert.ok(kind < cls, 'the property-kind cause comes before the class-range consequence');
  assert.ok(sevs.length > 10);
});

test('counts add up, and the exports carry every finding', () => {
  const total = rep.checks.reduce((n, k) => n + k.findings.length, 0);
  assert.equal(Object.values(rep.counts).reduce((a, b) => a + b, 0), total);
  const csv = V.gapCsv(rep).trim().split('\r\n');
  assert.equal(csv.length, total + 1);
  const md = V.gapMarkdown(rep);
  assert.match(md, /^# OWL axioms against SHACL shapes/);
  assert.match(md, /## Immediate actions\n\n1\. \*\*\[BLOCKER\]/);
});

test('datatype relations follow XSD derivation and OWL 2 value spaces', () => {
  const X = 'http://www.w3.org/2001/XMLSchema#', R = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#';
  const rel = (a, b) => V.datatypeRelation(a.includes(':') && !a.startsWith('http') ? a : X + a, b.startsWith('http') ? b : X + b);
  assert.equal(rel('int', 'integer'), 'ok');
  assert.equal(rel('dateTimeStamp', 'dateTime'), 'ok');
  assert.equal(rel('string', 'http://www.w3.org/2000/01/rdf-schema#Literal'), 'ok');
  assert.equal(rel('string', R + 'PlainLiteral'), 'ok');
  assert.equal(rel('decimal', 'integer'), 'broader');
  assert.equal(rel('int', 'nonNegativeInteger'), 'overlap');
  assert.equal(rel('string', R + 'langString'), 'disjoint');
  assert.equal(rel('string', 'anyURI'), 'disjoint');
  assert.equal(rel('date', 'dateTime'), 'disjoint');
  assert.equal(V.datatypeRelation('http://www.opengis.net/ont/geosparql#wktLiteral', X + 'string'), 'unknown');
});

test('edit distance gives up past its limit', () => {
  assert.equal(V.editDistance('modifed', 'modified', 2), 1);
  assert.equal(V.editDistance('abc', 'abcdef', 2), 3);
  assert.equal(V.editDistance('section', 'action', 1), 2);
});

/* Cases from the code review: each was a false finding (or a crash) before. */
const EDGE_ONTOLOGY = PREFIXES + `
era: a owl:Ontology ; owl:versionInfo "v1" ; owl:versionIRI <https://gitlab.com/x/-/releases/v4.0%> .
era:Track a owl:Class .
era:Track2 a owl:Class .
era:code a owl:DatatypeProperty ;
  rdfs:range [ a rdfs:Datatype ; owl:onDatatype xsd:string ; owl:withRestrictions ( [ xsd:maxLength 10 ] [ xsd:pattern "[A-Z]+" ] ) ] .
era:amount a owl:DatatypeProperty ;
  rdfs:range [ a rdfs:Datatype ; owl:onDatatype xsd:decimal ; owl:withRestrictions ( [ xsd:minInclusive 0 ] ) ] .
era:x a owl:ObjectProperty ; owl:inverseOf era:y ; rdfs:range era:Track .
era:y a owl:ObjectProperty ; owl:inverseOf era:x ; rdfs:domain era:Track2 .
era:inv a owl:ObjectProperty ; era:shaclShapeValidationRule es:Inv .
era:part a owl:ObjectProperty .
era:Holder a owl:Class ;
  rdfs:subClassOf [ a owl:Restriction ; owl:onProperty era:part ; owl:maxQualifiedCardinality 1 ; owl:onClass era:Track ] .
era:count a owl:DatatypeProperty ; rdfs:range xsd:integer .
era:shaclShapeValidationRule a owl:AnnotationProperty .
`;
const EDGE_SHAPES = PREFIXES + `
es:TrackShape a sh:NodeShape ; sh:targetClass era:Track ; sh:property es:Inv , es:Count .
es:Inv sh:path [ sh:inversePath era:inv ] .
es:Count sh:path era:count ; sh:or ( [ sh:datatype xsd:string ] [ sh:datatype xsd:decimal ] ) .
es:HolderShape a sh:NodeShape ; sh:targetClass era:Holder ; sh:property es:Part .
es:Part sh:path era:part ; sh:class era:Track2 .
`;
const edge = JSON.parse(JSON.stringify(V.gapAnalysis(store(EDGE_ONTOLOGY), store(EDGE_SHAPES),
  {releases: [{tag: 'v1', name: '', date: ''}]})));
const edgeCheck = id => edge.checks.find(k => k.id === id);

test('review: length, pattern and derived-type facets are valid', () => {
  assert.equal(edgeCheck('facet-type').findings.length, 0);
});

test('review: an inverse stated both ways is checked once', () => {
  assert.equal(edgeCheck('inverse-mismatch').findings.length, 1);
});

test('review: a shape with an inverse path is applied, not "never applied"', () => {
  assert.equal(edgeCheck('validation-rule-links').findings.length, 0);
  assert.equal(edge.meta.shapes.judged, 3);
});

test('review: a qualified restriction does not bound values of another class', () => {
  assert.equal(edgeCheck('restriction-cardinality').findings.length, 0);
});

test('review: a malformed escape in owl:versionIRI is reported, not thrown', () => {
  const f = edgeCheck('version-metadata').findings;
  assert.equal(f.length, 1);
  assert.match(f[0].detail, /v4\.0%/);
});

test('review: a disjoint alternative in sh:or is grouped as disjoint', () => {
  const f = edgeCheck('datatype-range').findings;
  assert.equal(f.length, 1);
  assert.equal(f[0].group, 'disjoint datatype');
  assert.equal(f[0].severity, 'MAJOR', 'one alternative of two is disjoint');
});
