/* Live check of the ERATV Explorer (scripts/assets/era-eratv-explorer.html):
   loads the index from ERATV-KG exactly as the page does, then runs a set of
   searches both ways - in the page's own matcher over the index, and as the
   SPARQL the page generates - and fails on any difference in the vehicle
   types returned. Then it checks the snapshot the page falls back on
   (scripts/assets/era-eratv-snapshot.json.gz) against live answers: the same
   types in the index, and the same values per configuration for a sample of
   types. Needs network access to graph.uat.data.test-era.europa.eu.

   Run:  node scripts/tests/eratv-live-parity.js        (Node 18 or later) */
const fs = require('fs'), path = require('path'), vm = require('vm'), zlib = require('zlib');

const html = fs.readFileSync(path.join(__dirname, '../assets/era-eratv-explorer.html'), 'utf8');
const mod = {exports: {}};
vm.runInContext([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'),
  vm.createContext({module: mod, console, URL, URLSearchParams}));
const V = mod.exports;

async function sparql(query){
  const res = await fetch(V.ENDPOINT, {method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/tab-separated-values'},
    body: 'infer=false&query=' + encodeURIComponent(query)});
  if(!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
  return V.parseTsv(await res.text());
}
const form = over => Object.assign(V.emptyForm(), over);

(async () => {
  const t0 = Date.now();
  const names = Object.keys(V.INDEX_QUERIES);
  const results = await Promise.all(names.map(n => sparql(V.INDEX_QUERIES[n])));
  const X = V.buildIndex(Object.fromEntries(names.map((n, i) => [n, results[i]])));
  console.log(`index: ${X.types.length} vehicle types, ${X.orgs.size} organisation roles, ` +
    names.map((n, i) => `${n} ${results[i].length}`).join(', ') + ` (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
  V.addComments(X, await sparql(V.COMMENTS_QUERY));

  // values taken from the index, so the cases follow the data
  const count = (keyFn) => { const m = new Map(); for(const t of X.types) for(const k of [].concat(keyFn(t))) m.set(k, (m.get(k) || 0) + 1); return [...m.entries()].sort((a, b) => b[1] - a[1]); };
  const topManu = count(t => t.manus)[0][0];
  const subsWithSpace = count(t => t.subs).map(e => e[0]).filter(s => / /.test(s));
  const tsiTop = count(t => t.tsis).slice(0, 2).map(e => e[0]);
  const CAT = 'http://data.europa.eu/949/concepts/vehicle-types/eratv/';
  const cases = {
    'everything': form({}),
    'Type ID part': form({text: '11-273'}),
    'alternative name': form({text: 'vectron'}),
    'platform word': form({text: 'traxx'}),
    'EIN part': form({ein: 'PL80'}),
    'category freight wagons': form({cats: [CAT + '51']}),
    'subcategory with spaces in the IRI': form({subs: subsWithSpace}),
    'one manufacturer': form({manuOrgs: [topManu]}),
    'manufacturers in Germany': form({manuCountries: ['DEU']}),
    'manufacturers without a country': form({manuCountries: [V.NO_STATUS]}),
    'manufacturer name': form({manuName: 'alstom'}),
    'TSI wording picked': form({tsis: tsiTop}),
    'TSI wording text': form({tsiText: '2016/919'}),
    'not conform to any TSI': form({tsis: ['Not conform to any TSI']}),
    'certificate reference': form({cert: '/SB/'}),
    'Member States NL + ERA': form({ms: ['The%20Netherlands', 'EU']}),
    'status valid only': form({statuses: ['Active'], statusAll: false}),
    'status expired, suspended, withdrawn, none': form({statuses: ['ActiveExpired', 'Suspended', 'Withdrawn', V.NO_STATUS], statusAll: false}),
    'area of use': form({area: 'RFI'}),
    'comments': form({comments: 'OSS'}),
    'authorised 2024': form({from: '2024-01-01', to: '2024-12-31'}),
    'updated since 2025-03': form({modFrom: '2025-03-01'}),
    'combined': form({cats: [CAT + '11'], ms: ['DEU', 'POL'], statuses: ['Active'], statusAll: false, from: '2020-01-01'}),
  };
  let failed = 0;
  for(const [name, f] of Object.entries(cases)){
    const local = new Set(X.types.filter(t => V.matches(t, f, X)).map(t => t.uri));
    const s0 = Date.now();
    const live = new Set((await sparql(V.matchSparql(f))).map(r => r.vt));
    const onlyLive = [...live].filter(u => !local.has(u)), onlyPage = [...local].filter(u => !live.has(u));
    const ok = !onlyLive.length && !onlyPage.length && local.size > 0;
    if(!ok) failed++;
    console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}: ${local.size} in the page, ${live.size} live (${((Date.now() - s0) / 1000).toFixed(1)} s)` +
      (onlyLive.length ? `\n     only live: ${onlyLive.slice(0, 3).join(' ')}` : '') + (onlyPage.length ? `\n     only in the page: ${onlyPage.slice(0, 3).join(' ')}` : '') +
      (!local.size ? '\n     (no match: the case tests nothing)' : ''));
  }
  // the snapshot: the same types as the live index, and the same values for a sample of types
  const snap = JSON.parse(zlib.gunzipSync(fs.readFileSync(path.join(__dirname, '../assets/era-eratv-snapshot.json.gz'))));
  const SX = V.buildIndex(V.unpackIndex(snap.index));
  const liveKeys = new Set(X.types.map(t => t.key)), snapKeys = new Set(SX.types.map(t => t.key));
  const newer = [...liveKeys].filter(k => !snapKeys.has(k)), gone = [...snapKeys].filter(k => !liveKeys.has(k));
  console.log(`snapshot of ${snap.generated.slice(0, 10)} (ontology ${snap.ontology.tag}): ${SX.types.length} types; ` +
    `${newer.length} live types not in it, ${gone.length} in it no longer live`);
  const flat = t => JSON.stringify({direct: [...t.direct], sets: t.sets.map(x => ({...x, values: [...x.values]}))});
  const pick = [X.types.find(t => t.tsis.length > 2), X.types.find(t => t.key.includes('The%20Netherlands')), ...X.types.filter((t, i) => i % 400 === 7)]
    .filter((t, i, all) => t && snapKeys.has(t.key) && all.findIndex(x => x && x.key === t.key) === i);
  const res = await fetch(V.ENDPOINT, {method: 'POST', headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json'},
    body: 'infer=false&query=' + encodeURIComponent(V.typeValuesQuery(pick.map(t => t.uri)))});
  const liveModels = V.typeModels((await res.json()).results.bindings);
  let differ = 0;
  for(const t of pick){
    const a = flat(liveModels.get(t.uri) || {direct: new Map(), sets: []}), b = flat(V.decodeType(snap, t.key, t.uri) || {direct: new Map(), sets: []});
    if(a !== b){ differ++; console.log(`     values differ for ${t.key}`); }
  }
  console.log(`${differ ? 'FAIL' : 'ok  '} the snapshot's values of ${pick.length} types match a live query` + (differ ? ` except ${differ} (rebuild the snapshot if the data changed)` : ''));
  if(differ) failed++;
  console.log(failed ? `${failed} FAILED` : 'all searches agree');
  process.exit(failed ? 1 : 0);
})().catch(err => { console.error(err); process.exit(2); });
