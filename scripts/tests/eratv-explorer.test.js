/* Tests for the ERATV Explorer (scripts/assets/era-eratv-explorer.html, served
   as eratv.html): the index built from the live queries, the in-browser search,
   and the SPARQL it is checked against.

   The page's pure functions are loaded from the HTML file itself; the page
   part of the script is skipped without a DOM. Every generated query is parsed
   with sparqljs, so a syntax error fails here rather than on the endpoint.

   Run:  npm install --no-save sparqljs@3.7.3 && node --test scripts/tests/eratv-explorer.test.js
   The live check against ERATV-KG is separate: node scripts/tests/eratv-live-parity.js */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs'), path = require('path'), vm = require('vm');
const {Parser} = require('sparqljs');

const html = fs.readFileSync(path.join(__dirname, '../assets/era-eratv-explorer.html'), 'utf8');
const mod = {exports: {}};
vm.runInContext([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'),
  vm.createContext({module: mod, console, URL}));
const V = mod.exports;
const parse = q => new Parser().parse(q);

const ERA = 'http://data.europa.eu/949/';
const VT = ERA + 'vehicleTypes/';
const CAT = ERA + 'concepts/vehicle-types/eratv/';
const ROLE = ERA + 'organisationRoles/eratv/';
const SUB_SPACES = CAT + 'Other (see article (1)(4) of directive (EU) 2016/797)';

/* Rows as the seven index queries return them (TSV, parsed). */
const RAW = {
  types: [
    {vt: VT + '11-273-0001-8-001-DEU', id: '11-273-0001-8-001', num: '11-273-0001-8', vv: '001', platform: 'Vectron', alt: 'BR 193', cat: CAT + '11', sub: CAT + 'locomotive', manu: ROLE + '12_Manufacturer'},
    // a second alternative name multiplies the row
    {vt: VT + '11-273-0001-8-001-DEU', id: '11-273-0001-8-001', num: '11-273-0001-8', vv: '001', platform: 'Vectron', alt: 'Vectron AC', cat: CAT + '11', sub: CAT + 'locomotive', manu: ROLE + '12_Manufacturer'},
    {vt: VT + '11-273-0001-8-001-The%20Netherlands', id: '11-273-0001-8-001', num: '11-273-0001-8', vv: '001', platform: 'Vectron', alt: '', cat: CAT + '11', sub: CAT + 'locomotive', manu: ROLE + '12_Manufacturer'},
    {vt: VT + '51-445-0002-1-001-EU', id: '51-445-0002-1-001', num: '51-445-0002-1', vv: '001', platform: 'Sgns', alt: '', cat: CAT + '51', sub: SUB_SPACES, manu: ROLE + '99_Manufacturer'},
    {vt: VT + '71-001-0001-1-001-POL', id: '71-001-0001-1-001', num: '71-001-0001-1', vv: '', platform: '', alt: '', cat: CAT + '71', sub: '', manu: ROLE + '77_Manufacturer'},
  ],
  current: [
    {vt: VT + '11-273-0001-8-001-DEU', status: 'Active', issued: '', modified: '', holder: ''},
    {vt: VT + '11-273-0001-8-001-DEU', status: '', issued: '2019-03-14T10:00:00+01:00', modified: '', holder: ''},
    {vt: VT + '11-273-0001-8-001-DEU', status: '', issued: '', modified: '2024-12-05T14:05:48', holder: ''},
    {vt: VT + '11-273-0001-8-001-DEU', status: '', issued: '', modified: '', holder: ERA + 'organisationRoles/41476_Manufacturer'},
    {vt: VT + '11-273-0001-8-001-The%20Netherlands', status: 'ActiveExpired', issued: '2021-06-01T00:00:00', modified: '', holder: ''},
    {vt: VT + '51-445-0002-1-001-EU', status: 'Suspended', issued: '2024-01-10T09:00:00', modified: '2025-02-01T00:00:00', holder: ''},
    // not a vehicle type of the index: ignored
    {vt: VT + 'unknown', status: 'Active', issued: '', modified: '', holder: ''},
  ],
  ein: [{vt: VT + '11-273-0001-8-001-DEU', ein: 'DE8020190001'}, {vt: VT + '51-445-0002-1-001-EU', ein: 'EU8020240283'}],
  tsi: [
    {vt: VT + '11-273-0001-8-001-DEU', tsi: 'CCS TSI (Regulation (EU) N° 2016/919)'},
    {vt: VT + '11-273-0001-8-001-DEU', tsi: 'Noise (Regulation (EU) No 1304/2014)'},
    {vt: VT + '51-445-0002-1-001-EU', tsi: 'Not conform to any TSI'},
  ],
  refs: [{vt: VT + '51-445-0002-1-001-EU', ref: '1467/1/SB/2024/CCO/PL/017/V01 '}],
  area: [{vt: VT + '11-273-0001-8-001-DEU', area: 'DE(Germany)'}],
  orgs: [
    {role: ROLE + '12_Manufacturer', name: 'Siemens Mobility GmbH', country: ''},
    {role: ROLE + '12_Manufacturer', name: '', country: 'http://publications.europa.eu/resource/authority/country/DEU'},
    {role: ROLE + '99_Manufacturer', name: 'Wagony Świdnica', country: ''},
    // 77 resolves to no organisation, as most holder roles do
  ],
};
const X = V.buildIndex(RAW);
// objects made inside the vm context have its prototypes: compare them as plain data
const plain = v => JSON.parse(JSON.stringify(v));
const ids = f => plain(X.types.filter(t => V.matches(t, f, X)).map(t => t.key)).sort();
const form = over => Object.assign(V.emptyForm(), over);

test('the index: one entry per vehicle type, multi-valued fields gathered, unknown types ignored', () => {
  assert.equal(X.types.length, 4);
  const de = X.byUri.get(VT + '11-273-0001-8-001-DEU');
  assert.deepEqual(plain(de.alts), ['BR 193', 'Vectron AC']);
  assert.deepEqual(plain(de.status), ['Active']);
  assert.deepEqual(plain(de.issued), ['2019-03-14']);
  assert.deepEqual(plain(de.modified), ['2024-12-05']);
  assert.equal(de.ms, 'DEU');
  assert.equal(X.byUri.get(VT + '11-273-0001-8-001-The%20Netherlands').ms, 'The%20Netherlands');
  assert.deepEqual(plain(X.orgs.get(ROLE + '12_Manufacturer')), {names: ['Siemens Mobility GmbH'], countries: ['DEU']});
  assert.equal(X.byUri.get(VT + '51-445-0002-1-001-EU').subs[0], SUB_SPACES);
});

test('Member States as ERATV-KG writes them in the URI', () => {
  assert.equal(V.msOf(VT + '11-273-0001-8-001-DEU', '11-273-0001-8-001'), 'DEU');
  assert.equal(V.msOf(VT + '53-002-0004-4-001-ChannelTunnel%2A', '53-002-0004-4-001'), 'ChannelTunnel%2A');
  assert.equal(V.msOf(VT + 'something-else', '11-273'), '');
  assert.equal(V.msLabel('EU'), 'European Union — authorised by ERA');
  assert.equal(V.msLabel('The%20Netherlands'), 'Netherlands');
  assert.equal(V.msLabel('Channel%20Tunnel%2A'), 'Channel Tunnel');
  assert.equal(V.msLabel('POL'), 'Poland');
});

test('labels the data does not carry', () => {
  assert.equal(V.catLabel(CAT + '51'), 'Freight wagons');
  assert.equal(V.subLabel(CAT + 'passengerTrainset'), 'Passenger trainset');
  assert.equal(V.subLabel(SUB_SPACES), 'Other (see article (1)(4) of directive (EU) 2016/797)');
  assert.equal(V.subLabel(CAT + 'Hauled%20special%20vehicle'), 'Hauled special vehicle');
  assert.equal(V.statusLabel('ActiveExpired'), 'Expired');
  assert.equal(V.roleNumber(ERA + 'organisationRoles/41476_Manufacturer'), '41476');
  assert.equal(V.roleNumber(ROLE + '1071_Manufacturer'), '1071');
});

test('the in-browser search, field by field', () => {
  const DE = '11-273-0001-8-001-DEU', NL = '11-273-0001-8-001-The%20Netherlands', EU = '51-445-0002-1-001-EU', PL = '71-001-0001-1-001-POL';
  assert.deepEqual(ids(form({})), [DE, NL, EU, PL].sort());
  assert.deepEqual(ids(form({text: 'vectron ac'})), [DE]);               // an alternative name
  assert.deepEqual(ids(form({text: '11-273'})), [DE, NL]);                // the Type ID
  assert.deepEqual(ids(form({ein: 'de80'})), [DE]);
  assert.deepEqual(ids(form({cats: [CAT + '51']})), [EU]);
  assert.deepEqual(ids(form({subs: [SUB_SPACES]})), [EU]);
  assert.deepEqual(ids(form({manuOrgs: [ROLE + '99_Manufacturer']})), [EU]);
  assert.deepEqual(ids(form({manuCountries: ['DEU']})), [DE, NL]);
  assert.deepEqual(ids(form({manuCountries: [V.NO_STATUS]})), [EU, PL]);  // no address, or no organisation at all
  assert.deepEqual(ids(form({manuName: 'świdnica'})), [EU]);
  assert.deepEqual(ids(form({tsis: ['Not conform to any TSI']})), [EU]);
  assert.deepEqual(ids(form({tsiText: '2016/919'})), [DE]);
  assert.deepEqual(ids(form({cert: '1467/1/sb'})), [EU]);
  assert.deepEqual(ids(form({ms: ['The%20Netherlands', 'EU']})), [NL, EU].sort());
  assert.deepEqual(ids(form({statuses: ['Active'], statusAll: false})), [DE]);
  assert.deepEqual(ids(form({statuses: [V.NO_STATUS], statusAll: false})), [PL]);
  assert.deepEqual(ids(form({area: 'germany'})), [DE]);
  assert.deepEqual(ids(form({from: '2020-01-01'})), [NL, EU].sort());
  assert.deepEqual(ids(form({from: '2019-03-14', to: '2019-03-14'})), [DE]);
  assert.deepEqual(ids(form({modTo: '2024-12-31'})), [DE]);
  assert.deepEqual(ids(form({text: 'vectron', ms: ['DEU']})), [DE]);
});

test('comments are searched once they are loaded', () => {
  const Y = V.buildIndex(RAW);
  V.addComments(Y, [{vt: VT + '71-001-0001-1-001-POL', text: 'Solicitud OSS V-20240506-007'}, {vt: VT + 'unknown', text: 'x'}]);
  assert.deepEqual(plain(Y.types.filter(t => V.matches(t, form({comments: 'oss v-2024'}), Y)).map(t => t.key)), ['71-001-0001-1-001-POL']);
  assert.ok(V.needsComments(form({comments: 'x'})));
});

test('form validation', () => {
  assert.match(V.validateForm(form({statuses: [], statusAll: false})), /at least one/);
  assert.match(V.validateForm(form({from: '2024-01-02', to: '2024-01-01'})), /after/);
  assert.equal(V.validateForm(form({})), '');
});

test('every generated query parses, with each field as its own clause', () => {
  const all = form({text: 'a"b\\c', ein: 'x', cats: [CAT + '11'], subs: [SUB_SPACES], manuName: 'siemens', tsis: ['CCS TSI (Regulation (EU) N° 2016/919)'],
    tsiText: '919', cert: '1467', ms: ['DEU', 'The%20Netherlands'], statuses: ['Active', V.NO_STATUS], statusAll: false, area: 'de',
    comments: 'oss', from: '2020-01-01', to: '2024-12-31', modFrom: '2021-01-01'});
  const q = V.matchSparql(all);
  parse(q);
  assert.match(q, /"a\\"b\\\\c"/);                       // quotes and backslashes escaped
  assert.match(q, /STR\(\?subCategory\) IN \("http:\/\/data\.europa\.eu\/949\/concepts\/vehicle-types\/eratv\/Other \(see/);
  assert.doesNotMatch(q, /<http[^>\s]*\s[^>]*>/);           // never an IRI with a space between <…>
  assert.match(q, /\?memberState IN \("DEU", "The%20Netherlands"\)/);
  assert.match(q, /NOT EXISTS \{ \?anyCase/);
  parse(V.matchSparql(form({manuOrgs: [ROLE + '12_Manufacturer']})));
  parse(V.matchSparql(form({manuCountries: ['DEU', V.NO_STATUS]})));
  parse(V.matchSparql(form({manuCountries: [V.NO_STATUS]})));
  parse(V.matchSparql(form({statuses: ['Pending'], statusAll: false})));
  parse(V.matchSparql(form({})));
  for(const q of Object.values(V.INDEX_QUERIES)) parse(q);
  parse(V.COMMENTS_QUERY);
  parse(V.ONTOLOGY_QUERY);
  parse(V.detailQuery(VT + '11-273-0001-8-001-DEU'));
  parse(V.conceptLabelQuery([ERA + 'concepts/temperature-ranges/10']));
});

test('IRIs that SPARQL cannot write are recognised', () => {
  assert.equal(V.writableIri(SUB_SPACES), false);
  assert.equal(V.writableIri(CAT + 'Hauled%20special%20vehicle'), true);
});

test('ERATV parameter numbers sort numerically, unnumbered last', () => {
  const ix = ['4.13.10', '', '4.2', '4.13.2.3', '0.1', '4.13.2', '4.1.3.b', '4.1.3', '4.1.3.a'];
  assert.deepEqual(plain([...ix].sort(V.compareIndex)), ['0.1', '4.1.3', '4.1.3.a', '4.1.3.b', '4.2', '4.13.2', '4.13.2.3', '4.13.10', '']);
});

test('TSV parsing keeps escaped tabs and newlines inside literals', () => {
  const rows = V.parseTsv('?vt\t?text\n<http://x/a>\t"line 1\\nline\\t2 \\"q\\""\n');
  assert.deepEqual(plain(rows), [{vt: 'http://x/a', text: 'line 1\nline\t2 "q"'}]);
});

test('a record with two statuses and two dates matches on either, in both searches', () => {
  const vt = VT + '13-100-0001-0-001-SWE';
  const Y = V.buildIndex({types: [{vt, id: '13-100-0001-0-001', num: '', vv: '', platform: '', alt: '', cat: CAT + '11', sub: '', manu: ''}],
    current: [{vt, status: 'Pending'}, {vt, status: 'Active'}, {vt, issued: '2018-05-01T00:00:00'}, {vt, issued: '2023-02-01T00:00:00'}],
    ein: [], tsi: [], refs: [], area: [], orgs: []});
  const hit = f => Y.types.filter(t => V.matches(t, f, Y)).length;
  assert.equal(hit(form({statuses: ['Pending'], statusAll: false})), 1);
  assert.equal(hit(form({statuses: ['Active'], statusAll: false})), 1);
  assert.equal(hit(form({statuses: ['Revoked'], statusAll: false})), 0);
  assert.equal(hit(form({from: '2020-01-01'})), 1);
  assert.equal(hit(form({to: '2019-01-01'})), 1);
  assert.equal(hit(form({from: '2019-01-01', to: '2022-12-31'})), 0);
  assert.deepEqual(plain(Y.types[0].issued), ['2018-05-01', '2023-02-01']);
});

test('IRIs SPARQL cannot write are compared as strings, the rest go in VALUES', () => {
  const q = V.matchSparql(form({cats: [CAT + 'with space'], manuOrgs: [ROLE + '12_Manufacturer']}));
  parse(q);
  assert.ok(q.includes(`FILTER(STR(?category) IN ("${CAT}with space"))`));
  assert.ok(q.includes(`VALUES ?manufacturer { <${ROLE}12_Manufacturer> }`));
});

test('CSV cells are quoted when needed and never start a formula', () => {
  assert.equal(V.csvCell('a,b'), '"a,b"');
  assert.equal(V.csvCell('say "x"'), '"say ""x"""');
  assert.equal(V.csvCell('=HYPERLINK("x")'), `"'=HYPERLINK(""x"")"`);
  assert.equal(V.csvCell('@SUM(1)'), "'@SUM(1)");
  assert.equal(V.csvCell('\t DMG, s.r.o.'), `"'\t DMG, s.r.o."`);
  assert.equal(V.csvCell('-'), '-');            // a placeholder, not a formula
  assert.equal(V.csvCell('-12.5'), '-12.5');    // a number stays a number
  assert.equal(V.csvCell('-cmd'), "'-cmd");
  assert.equal(V.csvCell(null), '');
});
