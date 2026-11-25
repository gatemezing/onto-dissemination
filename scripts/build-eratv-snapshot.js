#!/usr/bin/env node
/* Build the snapshot that era-eratv-explorer.html falls back on.

   The explorer searches this snapshot in the browser and shows a vehicle type
   from it whenever ERATV-KG cannot be read from the page. It is produced by the
   page's own code: this script loads the pure part of the page (as the tests
   do), sends its INDEX_QUERIES and typeValuesQuery to the endpoint, and keeps
   the answers in the shape the page reads live - so a snapshot and a live
   answer come from the same SPARQL and the same typeModels().

   Labels: property names and ERATV numbers (era:eratvIndex) come from the ERA
   ontology release named by --tag, and concept labels from that release's
   SKOS vocabularies, so the page needs no ontology at run time; the endpoint's
   own ontology and SKOS graphs fill in what the release does not label.

   Deliberately NOT in the snapshot: authorisation holders, the authorisation
   comments, and any note text (rdfs:comment, rdfs:seeAlso, skos:*Note) - the
   explorer searches comments live only. Nothing here needs credentials.

   Usage:  npm install --no-save n3@2.13.12
           node scripts/build-eratv-snapshot.js [--endpoint URL] [--tag v4.0.0]
   Writes: scripts/assets/era-eratv-snapshot.json.gz, and the date in README.md */
const fs = require('fs'), os = require('os'), path = require('path'), vm = require('vm'), zlib = require('zlib');
const N3 = require('n3');

const ROOT = path.resolve(__dirname, '..');
const PAGE = path.join(ROOT, 'scripts/assets/era-eratv-explorer.html');
const OUT = path.join(ROOT, 'scripts/assets/era-eratv-snapshot.json.gz');
const README = path.join(ROOT, 'README.md');
const GITLAB = 'https://gitlab.com/api/v4/projects/era-europa-eu%2Fpublic%2Finteroperable-data-programme%2Fera-ontology%2Fera-ontology/repository';
const ERA = 'http://data.europa.eu/949/';
const RDFS_LABEL = 'http://www.w3.org/2000/01/rdf-schema#label';
const PREF_LABEL = 'http://www.w3.org/2004/02/skos/core#prefLabel';
const ERATV_INDEX = ERA + 'eratvIndex';
const CHUNK = 150, IN_FLIGHT = 4;

const arg = (name, def) => { const i = process.argv.indexOf('--' + name); return i > 0 ? process.argv[i + 1] : def; };

const html = fs.readFileSync(PAGE, 'utf8');
const mod = {exports: {}};
vm.runInContext([...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n'),
  vm.createContext({module: mod, console, URL, URLSearchParams}));
const V = mod.exports;
const ENDPOINT = arg('endpoint', V.ENDPOINT);
const TAG = arg('tag', 'v4.0.0');

async function sparql(query, accept){
  for(let attempt = 1; ; attempt++){
    try{
      const res = await fetch(ENDPOINT, {method: 'POST', credentials: 'omit',
        headers: {'Content-Type': 'application/x-www-form-urlencoded', Accept: accept},
        body: 'infer=false&query=' + encodeURIComponent(query), signal: AbortSignal.timeout(300000)});
      if(!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.text()).slice(0, 300)}`);
      return accept.includes('json') ? res.json() : V.parseTsv(await res.text());
    } catch(err){
      if(attempt >= 3) throw err;
      console.error(`  retry ${attempt}: ${err.message}`);
      await new Promise(r => setTimeout(r, 5000 * attempt));
    }
  }
}
const tsv = q => sparql(q, 'text/tab-separated-values');
/* A file of the ontology repository at the release tag, cached in the system's
   temp folder: GitLab throttles archive downloads (an occasional 406 or 429). */
async function gitlab(file, cacheName){
  const cache = path.join(os.tmpdir(), `era-ontology-${TAG.replace(/[^\w.-]/g, '_')}-${cacheName}`);
  if(fs.existsSync(cache)) return fs.readFileSync(cache);
  for(let attempt = 1; ; attempt++){
    const res = await fetch(`${GITLAB}/${file}`, {signal: AbortSignal.timeout(300000)});
    if(res.ok){ const buf = Buffer.from(await res.arrayBuffer()); fs.writeFileSync(cache, buf); return buf; }
    if(attempt >= 5) throw new Error(`GitLab ${file}: HTTP ${res.status}`);
    console.error(`  GitLab ${file}: HTTP ${res.status} ${res.headers.get("content-type")} ${(await res.text()).slice(0, 200)}, retrying in ${30 * attempt} s`);
    await new Promise(r => setTimeout(r, 30000 * attempt));
  }
}
/* The .ttl files of a .tar.gz, read with no tar dependency (ustar headers). */
function* tarFiles(gz){
  const buf = zlib.gunzipSync(gz);
  for(let off = 0; off + 512 <= buf.length;){
    const h = buf.subarray(off, off + 512);
    if(h.every(b => b === 0)) break;
    const str = (a, b) => h.subarray(a, b).toString('utf8').replace(/\0.*$/s, '');
    const name = (str(345, 500) ? str(345, 500) + '/' : '') + str(0, 100);
    const size = parseInt(str(124, 136).trim() || '0', 8), type = str(156, 157);
    const data = buf.subarray(off + 512, off + 512 + size);
    if((type === '0' || type === '') && name.endsWith('.ttl')) yield [name, data.toString('utf8')];
    off += 512 + Math.ceil(size / 512) * 512;
  }
}
const quads = (text, name) => { try{ return new N3.Parser().parse(text); } catch(e){ console.error(`  cannot parse ${name}: ${e.message}`); return []; } };
const english = l => !l.language || /^en\b/i.test(l.language);

(async () => {
  const t0 = Date.now();
  console.log(`endpoint ${ENDPOINT}`);

  // 1. the index, as the page loads it live
  const names = Object.keys(V.INDEX_QUERIES);
  const raw = Object.fromEntries(await Promise.all(names.map(async n => [n, await tsv(V.INDEX_QUERIES[n])])));
  const X = V.buildIndex(raw);
  console.log(`index: ${X.types.length} vehicle types, ${X.orgs.size} organisation roles (${((Date.now() - t0) / 1000).toFixed(0)} s)`);

  // 2. every type's values, with the page's own query, in chunks
  const uris = X.types.map(t => t.uri);
  const chunks = [];
  for(let i = 0; i < uris.length; i += CHUNK) chunks.push(uris.slice(i, i + CHUNK));
  const models = new Map();
  let done = 0;
  async function worker(){
    while(chunks.length){
      const c = chunks.shift();
      const j = await sparql(V.typeValuesQuery(c), 'application/sparql-results+json');
      for(const [u, t] of V.typeModels(j.results.bindings)) models.set(u, t);
      done += c.length;
      process.stdout.write(`\r  values: ${done} / ${uris.length} types`);
    }
  }
  await Promise.all(Array.from({length: IN_FLIGHT}, worker));
  console.log(`\nvalues: ${models.size} types with values (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  const key = u => u.startsWith(V.VT_BASE) ? u.slice(V.VT_BASE.length) : u;
  const enc = V.encodeTypes(models, key);

  // 3. labels: the properties and concepts the snapshot uses
  const props = new Set(enc.P.filter(p => p !== V.TSI_ROW)), concepts = new Set();
  const walk = v => {
    if(v.startsWith('u:') && v.slice(2).startsWith(ERA + 'concepts/')) concepts.add(v.slice(2));
    else if(v.startsWith('o:')) for(const [p, vs] of JSON.parse(v.slice(2))){ props.add(p); vs.forEach(walk); }
  };
  enc.V.forEach(walk);
  const P = {}, C = {};
  const ontology = quads((await gitlab(`files/ontology.ttl/raw?ref=${encodeURIComponent(TAG)}`, 'ontology.ttl')).toString('utf8'), 'ontology.ttl');
  let versionIRI = '';
  for(const q of ontology){
    const s = q.subject.value, p = q.predicate.value;
    if(p === 'http://www.w3.org/2002/07/owl#versionIRI' && s === ERA) versionIRI = q.object.value;
    if(!props.has(s)) continue;
    const e = P[s] || (P[s] = ['', []]);
    if(p === RDFS_LABEL && english(q.object) && !e[0]) e[0] = q.object.value;
    if(p === ERATV_INDEX && !e[1].includes(q.object.value)) e[1].push(q.object.value);
  }
  let skosFiles = 0;
  for(const [name, text] of tarFiles(await gitlab(`archive.tar.gz?sha=${encodeURIComponent(TAG)}&path=era-skos`, 'era-skos.tar.gz'))){
    skosFiles++;
    for(const q of quads(text, name))
      if(q.predicate.value === PREF_LABEL && concepts.has(q.subject.value) && english(q.object) && !C[q.subject.value]) C[q.subject.value] = q.object.value;
  }
  const fromRelease = {p: Object.values(P).filter(e => e[0] || e[1].length).length, c: Object.keys(C).length};
  // the endpoint's ontology and SKOS graphs, for what the release does not label
  for(const r of await tsv(V.ONTOLOGY_QUERY)){
    if(!props.has(r.p)) continue;
    const e = P[r.p] || (P[r.p] = ['', []]);
    if(r.label && !e[0]) e[0] = r.label;
  }
  const missing = [...concepts].filter(c => !C[c] && V.writableIri(c));
  for(let i = 0; i < missing.length; i += 400)
    for(const l of await tsv(V.conceptLabelQuery(missing.slice(i, i + 400))))
      if(!C[l.c] && (!l.lang || /^en\b/i.test(l.lang))) C[l.c] = l.label;
  for(const e of Object.values(P)) e[1].sort(V.compareIndex);
  console.log(`labels: ${props.size} properties (${fromRelease.p} named or numbered by ${TAG}), ${concepts.size} concepts ` +
    `(${fromRelease.c} labelled by ${TAG}'s ${skosFiles} SKOS files, ${Object.keys(C).length} with the endpoint's)`);

  // 4. no holder, comment or note may reach the snapshot
  const index = V.packIndex(raw);
  for(const [n, {h}] of Object.entries(index)) if(h.includes('holder')) throw new Error(`index ${n} still carries holders`);
  const banned = new Set(V.NOT_VALUES);
  for(const p of enc.P) if(banned.has(p)) throw new Error(`snapshot carries ${p}`);
  for(const v of enc.V) if(v.startsWith('o:')) for(const [p] of JSON.parse(v.slice(2))) if(banned.has(p)) throw new Error(`snapshot carries ${p} in a nested object`);

  const generated = new Date().toISOString();
  const snap = {v: 1, generated, endpoint: ENDPOINT, graph: V.GRAPH, ontology: {tag: TAG, versionIRI},
    counts: {types: X.types.length, typeIds: new Set(X.types.map(t => t.id)).size, withValues: models.size},
    index, L: {p: P, c: C}, P: enc.P, V: enc.V, T: enc.T};
  const json = JSON.stringify(snap);
  const gz = zlib.gzipSync(json, {level: 9});
  fs.writeFileSync(OUT, gz);
  console.log(`wrote ${path.relative(ROOT, OUT)}: ${(json.length / 1e6).toFixed(1)} MB JSON, ${(gz.length / 1e6).toFixed(2)} MB gzipped, in ${((Date.now() - t0) / 1000).toFixed(0)} s`);

  // 5. the date in README's "Data snapshots" table
  const readme = fs.readFileSync(README, 'utf8');
  const re = /(<!-- extract:eratv -->).*?(<!-- \/extract:eratv -->)/;
  if(!re.test(readme)) throw new Error('README.md has no <!-- extract:eratv --> marker');
  fs.writeFileSync(README, readme.replace(re, `$1${generated.slice(0, 10)}, ${X.types.length.toLocaleString('en-GB')} vehicle types$2`));
})().catch(err => { console.error(err); process.exit(1); });
