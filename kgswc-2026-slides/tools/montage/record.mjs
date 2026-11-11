// Records the "one graph, many applications" montage from compose.html.
// Both apps run live inside iframes; captions and a visible cursor are drawn by the page.
// Frames come from the Chrome screencast (1920x1080 JPEG) with their timestamps,
// and are written with an ffmpeg concat list so each frame lasts as long as it was on screen.
import { chromium } from '../../node_modules/playwright-chromium/index.mjs'
import fs from 'node:fs'
import path from 'node:path'

const dir = path.dirname(new URL(import.meta.url).pathname)
const outDir = path.join(dir, 'frames')
fs.rmSync(outDir, { recursive: true, force: true }); fs.mkdirSync(outDir)

const b = await chromium.launch()
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1.5 })
const p = await ctx.newPage()
const log = (...a) => console.log(((Date.now() - T0) / 1000).toFixed(1).padStart(5), ...a)
let T0 = Date.now()
await p.goto('file://' + path.join(dir, 'compose.html'), { waitUntil: 'load' })
const fa = p.frameLocator('#fa'), fb = p.frameLocator('#fb')

// warm-up behind the title card: let both apps load, dismiss the Atlas tour
await fa.getByText('Operational Point', { exact: true }).first().waitFor({ timeout: 90000 })
await fb.getByPlaceholder(/Search labels/).waitFor({ timeout: 90000 })
await p.waitForTimeout(6000)
const skip = fb.getByText('Skip the tour'); if (await skip.count()) await skip.dispatchEvent('click')
await p.waitForTimeout(1500)

// screencast
const cdp = await ctx.newCDPSession(p)
const frames = []
cdp.on('Page.screencastFrame', async ({ data, metadata, sessionId }) => {
  frames.push({ data, t: metadata.timestamp })
  cdp.send('Page.screencastFrameAck', { sessionId }).catch(() => {})
})
await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 90, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 })
T0 = Date.now()
const wait = ms => p.waitForTimeout(ms)
const cap = html => p.evaluate(h => window.caption(h), html)
const cursorTo = async (x, y) => { await p.evaluate(([x, y]) => window.cursorTo(x, y), [x, y]); await wait(800) }
async function clickLoc(loc, opts = {}) {
  const bb = await loc.boundingBox()
  const x = opts.x ?? bb.x + bb.width / 2, y = bb.y + bb.height / 2
  await cursorTo(x, y); await p.evaluate(() => window.press())
  if (opts.x) await p.mouse.click(x, y); else await loc.click()
}

// 0 · title card
await wait(3000)

// 1 · ERA RINF unified search
log('scene A')
await p.evaluate(() => { window.show('fa'); window.card('title', false) }); await wait(900)
await cap('<b>ERA · RINF unified search</b> every operational point in the Register')
await wait(2100)
const opRow = fa.getByText('Operational Point', { exact: true }).first()
await clickLoc(opRow, { x: 272 }); await wait(1000)
await cap('<b>Filters are RINF parameters</b> = ERA Ontology properties')
await wait(1000)
await clickLoc(fa.getByText('Unique OP ID').first()); await wait(900)
await cap('<b>Unique OP ID 1.2.0.0.0.2</b> is <code>era:uopid</code>')
const input = fa.locator('input[type="text"]:not([placeholder="Search filters..."])').first()
await clickLoc(input); await input.pressSequentially('FR0000002651', { delay: 95 }); await wait(700)
await clickLoc(fa.getByRole('button', { name: 'Apply' })); await wait(2000)
await clickLoc(fa.getByRole('button', { name: 'Table View' }))
await cap('<b>Valenciennes</b> France · station · its tracks, as on the previous slide')
await wait(4000)
await clickLoc(fa.getByText('View Query').first())
await cap('<b>Under the hood</b> SPARQL over the ERA Ontology'); await wait(1200)
await cursorTo(640, 470)
for (let i = 0; i < 5; i++) { await p.mouse.wheel(0, 120); await wait(260) }
await wait(2000)
await p.keyboard.press('Escape'); await wait(600)
await p.evaluate(() => window.cursorHide())

// 2 · RINF Atlas
log('scene B')
await cap(null)
await p.evaluate(() => window.show('fb')); await wait(1100)
await cap('<b>RINF Atlas</b> a community application on the same open data')
await wait(1400)
const search = fb.getByPlaceholder(/Search labels/)
await clickLoc(search); await search.pressSequentially('Valenciennes', { delay: 85 }); await wait(900)
await clickLoc(fb.getByText(/^Results/).first()); await wait(900)
await cap('<b>Search by name</b> the station, its primary locations, tracks, sections')
await wait(1300)
await clickLoc(fb.getByText('Valenciennes', { exact: true }).first()); await wait(2800)
await cap('<b>Same IRI</b> <code>…/operationalPoint/83728fa739</code> · same graph <code>0087</code>')
await wait(3000)
const graphTab = fb.getByRole('tab', { name: 'Graph' })
await clickLoc((await graphTab.count()) ? graphTab : fb.getByText('Graph', { exact: true }).first()); await wait(1500)
await cap('<b>Graph view</b> tracks, primary locations, uopid, country: the same structure')
await wait(3300)
await p.evaluate(() => window.cursorHide())

// 3 · split screen
log('split')
await cap(null)
await p.evaluate(() => window.split()); await wait(7500)

// 4 · end card
log('end')
await p.evaluate(() => window.card('end', true)); await wait(3800)
log('stop')
await cdp.send('Page.stopScreencast'); await wait(300)
await b.close()

// write frames + concat list (durations from timestamps; last frame held 0.5 s)
const list = []
frames.forEach((f, i) => {
  const name = `f${String(i).padStart(5, '0')}.jpg`
  fs.writeFileSync(path.join(outDir, name), Buffer.from(f.data, 'base64'))
  const next = frames[i + 1]?.t ?? f.t + 0.5
  list.push(`file '${name}'`, `duration ${Math.max(0.001, next - f.t).toFixed(4)}`)
})
list.push(`file 'f${String(frames.length - 1).padStart(5, '0')}.jpg'`)
fs.writeFileSync(path.join(outDir, 'list.txt'), list.join('\n') + '\n')
console.log('frames', frames.length, 'span', (frames.at(-1).t - frames[0].t).toFixed(1), 's')
