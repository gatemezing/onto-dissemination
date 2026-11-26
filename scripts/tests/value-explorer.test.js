/* Tests for the RINF Value Explorer (scripts/assets/era-rinf-value-explorer.html,
   served as values.html): the SPARQL it sends to the ERA endpoint and the
   geometry it reads back.

   The page's script is run in a vm with a stand-in DOM (it wires its form up
   as it loads), and every generated query is parsed with sparqljs, so a
   syntax error fails here rather than on the endpoint. What each rule is for,
   with the figures measured on the live graph, is in the page's comments.

   Run:  npm install --no-save sparqljs@3.7.3 && node --test scripts/tests/value-explorer.test.js
   The live check, in a browser against the endpoint:
         python3 scripts/tests/value_explorer_check.py */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs'), path = require('path'), vm = require('vm');
const {Parser} = require('sparqljs');

/* An element that accepts whatever the page does to it while it loads. */
function stubElement(){
  const store = {classList: {add(){}, remove(){}, toggle(){}, contains: () => false}, style: {}, dataset: {}};
  return new Proxy(store, {
    get(t, k){
      if(k in t) return t[k];
      if(k === 'querySelectorAll') return () => [];
      if(k === 'querySelector' || k === 'closest') return () => stubElement();
      if(typeof k === 'string' && /^(add|remove|set|append|insert|focus|blur|click|scroll|dispatch)/.test(k)) return () => {};
      return undefined;
    },
    set(t, k, v){ t[k] = v; return true; },
  });
}
const elements = new Map();
const document = {
  getElementById: id => elements.get(id) || elements.set(id, stubElement()).get(id),
  addEventListener(){}, querySelector: () => null, querySelectorAll: () => [],
  createElement: () => stubElement(), body: stubElement(), activeElement: null,
};
const window = {addEventListener(){}, open: () => null};
const html = fs.readFileSync(path.join(__dirname, '../assets/era-rinf-value-explorer.html'), 'utf8');
const ctx = vm.createContext({document, window, location: {hash: '', href: 'http://localhost/values.html'},
  history: {replaceState(){}}, navigator: {onLine: true, clipboard: {}}, console, URL, URLSearchParams,
  setTimeout, clearTimeout, performance, AbortController, fetch: () => Promise.reject(new Error('offline'))});
vm.runInContext([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'), ctx);
const V = name => vm.runInContext(name, ctx);   // top-level const/let/function of the page
const run = src => vm.runInContext(src, ctx);
const parse = q => new Parser().parse(q);

const DAY = '2026-11-26';
const param = n => run('CATALOG').find(x => x.n === n);
const setScope = codes => run('chosen.clear(); ' + JSON.stringify(codes) + '.forEach(c => chosen.add(c));');
const pick = list => { ctx.__p = list; run('picked = __p;'); };
const ALL = run('COUNTRIES').map(c => c.c);
const ERA = 'http://data.europa.eu/949/';

test('every query the page can send parses, for every parameter with data', () => {
  setScope(ALL);
  const withData = run('CATALOG').filter(x => x.s > 0);
  let n = 0;
  for(const e of withData){
    pick([e]);
    const qs = [V('buildQuery')(e, false, DAY), V('buildQuery')(e, true, DAY),
                V('buildMapValueQuery')(e, 'DEU', DAY)];
    if(e.loc) qs.push(V('buildDetailQuery')(e, DAY));
    for(const q of qs){ assert.doesNotThrow(() => parse(q), e.n + '\n' + q); n++; }
  }
  for(const cc of ALL){ parse(V('buildMapTopologyQuery')(cc, DAY)); n++; }
  assert.ok(n > 800, 'checked ' + n + ' queries');
});

test('validity: what is not yet in force is left out, nothing else', () => {
  setScope(['DEU']);
  const speed = param('maximumPermittedSpeed');
  pick([speed]);
  const notYet = v => 'FILTER NOT EXISTS { ?' + v + ' era:validity/time:hasBeginning/time:inXSDDate ?' + v + 'From . ' +
                      'FILTER(?' + v + 'From > "' + DAY + '"^^xsd:date) }';
  for(const q of [V('buildQuery')(speed, false, DAY), V('buildQuery')(speed, true, DAY)])
    assert.ok(q.includes(notYet('s')), q);
  assert.ok(V('buildDetailQuery')(speed, DAY).includes(notYet('res')));
  assert.ok(V('buildMapTopologyQuery')('DEU', DAY).includes(notYet('sol')));
  assert.ok(V('buildMapValueQuery')(speed, 'DEU', DAY).includes(notYet('sol')));
  // One-sided: no rule on the end of a window, so ended and undated data stay.
  assert.ok(!V('buildQuery')(speed, false, DAY).includes('hasEnd'));
  // A day that is not a date never reaches a query.
  assert.throws(() => V('buildQuery')(speed, false, DAY + '"} DELETE {'), /malformed date/);
});

test('validity of a sub-object is read from the tracks pointing at it', () => {
  setScope(['DEU']);
  const etcs = param('etcsLevelType');
  assert.equal(etcs.loc, 'via:etcs');
  pick([etcs]);
  const q = V('buildQuery')(etcs, false, DAY);
  // left out only when a referrer is not yet valid and none is in force
  assert.match(q, /FILTER NOT EXISTS \{ \?sRef <http:\/\/data\.europa\.eu\/949\/etcs> \?s \. .*?sRefFrom > .*?FILTER NOT EXISTS \{ \?sRef2 <http:\/\/data\.europa\.eu\/949\/etcs> \?s \. FILTER NOT EXISTS \{ \?sRef2 era:validity/);
  // and the detail row's track carries its own window
  assert.ok(V('buildDetailQuery')(etcs, DAY).includes('?res <' + ERA + 'etcs> ?sub'));
});

test('part-whole links are read in either direction', () => {
  setScope(['AUT', 'GRC']);
  for(const n of ['maximumPermittedSpeed', 'umax2']){
    const e = param(n);
    pick([e]);
    const det = V('buildDetailQuery')(e, DAY), map = V('buildMapValueQuery')(e, 'AUT', DAY);
    assert.ok(det.includes('?res era:isPartOf|^era:hasPart ?parent .'), det);
    assert.ok(!/\?parent era:hasPart \?res/.test(det));
    assert.ok(map.includes('era:isPartOf|^era:hasPart ?sol'), map);
    assert.ok(!/\?trk\w* era:isPartOf \?sol/.test(map), map);
  }
  // the via: hop is kept on the map
  assert.ok(V('buildMapValueQuery')(param('umax2'), 'AUT', DAY).includes('<' + ERA + 'contactLineSystem> ?sub'));
});

test('the map is fetched per country, one section per row, a POINT preferred', () => {
  const topo = V('buildMapTopologyQuery')('AUT', DAY);
  const graphs = [...topo.matchAll(/<(http:\/\/data\.europa\.eu\/949\/graph\/[^>]+)>/g)].map(m => m[1]);
  assert.deepEqual(graphs.sort(), JSON.parse(JSON.stringify(run('BY_CODE').AUT.g)).map(g => ERA + 'graph/' + g).sort());
  assert.match(topo, /GROUP BY \?sol\s+LIMIT \d+$/);
  assert.match(topo, /MIN\(IF\(STRSTARTS\(STR\(\?wa\), "POINT"\)/);
  // values are their own query, so parameters never multiply each other's rows
  assert.ok(!topo.includes('GROUP_CONCAT'));
  const vq = V('buildMapValueQuery')(param('maximumPermittedSpeed'), 'AUT', DAY);
  assert.match(vq, /SELECT \?sol \(GROUP_CONCAT\(DISTINCT \?v;/);
  assert.ok(!vq.includes('asWKT'));
});

test('positions: signed coordinates, collections, lon/lat order', () => {
  const p = V('parsePoint');
  const plain = w => JSON.parse(JSON.stringify(p(w)));   // arrays from the vm's realm
  assert.deepEqual(plain('POINT(13.818919 50.914279)'), [50.914279, 13.818919]);
  assert.deepEqual(plain('POINT (+14.3659840 49.1908230)'), [49.190823, 14.365984]);   // Czechia, Lithuania
  assert.deepEqual(plain('POINT(-8.61 41.15)'), [41.15, -8.61]);
  assert.deepEqual(plain('~GEOMETRYCOLLECTION(LINESTRING(10.84767131 59.74791143, 10.8476 59.7478))'),
    [59.74791143, 10.84767131]);                                                        // Norway
  assert.equal(p('POINT EMPTY'), null);
  assert.equal(p(''), null);
});

test('the day of a run is the local calendar day', () => {
  assert.equal(V('validOn')(new Date(2027, 0, 1, 0, 30)), '2027-01-01');
  assert.equal(V('validOn')(new Date(2026, 10, 26, 23, 59)), '2026-11-26');
});
