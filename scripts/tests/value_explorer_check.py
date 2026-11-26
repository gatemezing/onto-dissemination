#!/usr/bin/env python3
"""Live browser check of the RINF Value Explorer (scripts/assets/era-rinf-value-explorer.html),
against graph.data.era.europa.eu:

- the map follows the parameter: change it and run again, and the map is redrawn for the
  new parameter; its legend and "Draw map" keep working (they used to break until reload);
- an all-country map draws every country, one segment per section, and the countries that
  link tracks only by era:hasPart (Austria, Croatia) carry values;
- counts are of what is in force today: Germany's total equals an independent count of the
  tracks in force, not the doubled count that includes DB InfraGO's 2027 copy;
- a query that gets no answer is reported as such, and the rest of the run is still shown.

The failures are injected (HTTP 503) for chosen queries; everything else is live.
Needs Playwright (pip install playwright && playwright install chromium).

Usage: python3 scripts/tests/value_explorer_check.py
"""
import datetime, functools, http.server, json, pathlib, socketserver, sys, threading, urllib.request
from playwright.sync_api import sync_playwright

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"
ENDPOINT = "https://graph.data.era.europa.eu/repositories/rinf-plus"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


failures = []
def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        failures.append(what)


def sparql(query):
    req = urllib.request.Request(ENDPOINT, data=query.encode(), method="POST", headers={
        "Content-Type": "application/sparql-query", "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=150) as r:
        return json.load(r)["results"]["bindings"]


RUN_DONE = "!document.getElementById('runBtn').disabled && document.getElementById('statusArea').className !== 'loading'"
MAP_DONE = "!document.getElementById('mapBtn').disabled"

def scope(page, codes):
    page.press("#paramSearch", "Escape")     # the focused search box opens its list over the grid
    page.click("#selNone")
    for c in codes:
        page.check(f'label.cy[data-c="{c}"] input')

def choose(page, *names):
    """Selects parameters by property name (the combobox ranking is not under test here)."""
    page.evaluate("ns => ns.forEach(n => selectParam(CATALOG.find(x => x.n === n)))", list(names))

def remove(page, name):
    page.click(f'#paramChips button[data-u="http://data.europa.eu/949/{name}"]')

def run(page):
    page.click("#runBtn")
    page.wait_for_function(RUN_DONE, timeout=300000)
    page.wait_for_function(MAP_DONE, timeout=300000)   # a map on screen is redrawn after a run

def draw(page):
    page.click("#mapBtn")
    page.wait_for_timeout(200)
    page.wait_for_function(MAP_DONE, timeout=300000)

def map_state(page):
    return page.evaluate("""() => mapData && {
      mode: mapData.mode, param: mapData.mode === 'single' ? mapData.param.n : null,
      params: (mapData.params || []).map(e => e.n), segs: mapData.segs.length,
      legend: document.querySelectorAll('#mapLegend .lg').length,
      status: document.getElementById('mapStatus').textContent}""")


def main():
    srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(ASSETS)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}/era-rinf-value-explorer.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()

        print("--- the map follows the parameter (Luxembourg + Belgium)")
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(base)
        scope(page, ["LUX", "BEL"])
        choose(page, "maximumPermittedSpeed")
        run(page)
        draw(page)
        m = map_state(page)
        check(m and m["param"] == "maximumPermittedSpeed" and m["segs"] > 0, f"the speed map is drawn ({m and m['segs']} sections)")
        remove(page, "maximumPermittedSpeed")
        choose(page, "wheelSetGauge")
        check(page.is_hidden("#mapPanel"), "changing the parameter hides the previous run's map")
        run(page)
        m = map_state(page)
        check(m and m["param"] == "wheelSetGauge", f"running again redraws the map for the new parameter, unasked ({m and m['param']})")
        choose(page, "etcsLevelType")
        run(page)
        page.evaluate("() => { mapParamOff = new Set(); renderMapParamPicks(); }")
        draw(page)
        m = map_state(page)
        check(m and m["mode"] == "multi" and m["legend"] == 2, "two parameters draw one colour each")
        page.click("#mapLegend .lg >> nth=0")
        remove(page, "wheelSetGauge")
        run(page)
        m = map_state(page)
        check(m and m["mode"] == "single" and m["param"] == "etcsLevelType" and m["params"] == ["etcsLevelType"],
              "after removing one, the map is the remaining parameter's, not the stale two-parameter one")
        page.click("#mapLegend .lg >> nth=0")
        draw(page)
        m = map_state(page)
        check(m and m["segs"] > 0 and "drawn" in m["status"], "the legend and 'Draw map' still work (they used to need a reload)")
        check(not errors, f"no page errors {errors[:3]}")
        page.close()

        print("--- every country, in force today")
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(base)
        page.press("#paramSearch", "Escape")
        page.click("#selAll")
        choose(page, "maximumPermittedSpeed")
        page.uncheck("#wantDetail")
        run(page)
        day = datetime.date.today().isoformat()     # the check's own clock, not the page's
        deu = page.evaluate("lastRun.rows.reduce((s, x) => s + (x.byCountry.DEU || 0), 0)")
        q = lambda cond: (
            "PREFIX era: <http://data.europa.eu/949/> PREFIX time: <http://www.w3.org/2006/time#> "
            "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { "
            "GRAPH <http://data.europa.eu/949/graph/0080> { ?s era:maximumPermittedSpeed ?v } " + cond + " }")
        in_force = int(sparql(q('FILTER NOT EXISTS { ?s era:validity/time:hasBeginning/time:inXSDDate ?b . '
                                f'FILTER(?b > "{day}"^^xsd:date) }}'))[0]["n"]["value"])
        everything = int(sparql(q(""))[0]["n"]["value"])
        check(in_force < everything, f"Germany publishes tracks not yet in force ({everything - in_force:,} of {everything:,})")
        check(deu == in_force, f"Germany counts the {in_force:,} tracks in force on {day}, not all {everything:,} ({deu:,})")
        draw(page)
        per = page.evaluate("""() => { const by = {};
          for(const s of mapData.segs){ const c = by[s.cc] = by[s.cc] || {n: 0, v: 0}; c.n++; if(s.v !== null) c.v++; }
          return {by, all: COUNTRIES.map(c => c.c)}; }""")
        missing = [c for c in per["all"] if c not in per["by"]]
        check(not missing, f"every country is on the map ({len(per['by'])} of {len(per['all'])}; missing {missing})")
        for c in ("AUT", "HRV"):
            n, v = per["by"].get(c, {}).get("n", 0), per["by"].get(c, {}).get("v", 0)
            check(n and v / n > 0.9, f"{c} (tracks linked only by era:hasPart): {v} of {n} sections carry a value")
        sections = int(sparql(
            "PREFIX era: <http://data.europa.eu/949/> PREFIX geo: <http://www.opengis.net/ont/geosparql#> "
            "SELECT (COUNT(DISTINCT ?sol) AS ?n) WHERE { GRAPH <http://data.europa.eu/949/graph/0076> { "
            "?sol a era:SectionOfLine ; era:opStart/era:netReference/geo:hasGeometry ?x ; "
            "era:opEnd/era:netReference/geo:hasGeometry ?y } }")[0]["n"]["value"])
        check(per["by"].get("NOR", {}).get("n") == sections,
              f"Norway: one segment per section ({per['by'].get('NOR', {}).get('n')} for {sections}), however many geometries a point has")
        check(not errors, f"no page errors {errors[:3]}")
        page.close()

        print("--- a query with no answer is not 'no data'")
        page = browser.new_page(viewport={"width": 1366, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        def fail(route):
            body = route.request.post_data or ""
            if ("wheelSetGauge" in body and "ORDER BY DESC" in body) or ("graph/0088" in body and "GROUP_CONCAT(DISTINCT ?v;" in body):
                return route.fulfill(status=503, headers={"Access-Control-Allow-Origin": "*"}, body="busy (test)")
            return route.continue_()
        page.route("https://graph.data.era.europa.eu/**", fail)
        page.goto(base)
        scope(page, ["LUX", "BEL"])
        choose(page, "maximumPermittedSpeed", "wheelSetGauge")
        run(page)
        status = page.inner_text("#statusArea")
        check(status.startswith("Incomplete") and page.locator("#statusArea .retryBtn").count() == 1,
              "the status says the run is incomplete, with 'Try again'")
        check(page.locator("#coverStrip .cov.err").count() == 1 and "query failed" in page.inner_text("#coverStrip .cov.err"),
              "the failed parameter is marked 'query failed'")
        check(page.evaluate("lastRun.rows.filter(x => x.param.n === 'maximumPermittedSpeed').length") > 0,
              "the other parameter's values are still shown")
        draw(page)
        check("Missing: Belgium" in page.inner_text("#mapStatus") and page.evaluate("mapData.segs.every(s => s.cc === 'LUX')"),
              "a country whose map query failed is named, and the rest is drawn")
        check(not errors, f"no page errors {errors[:3]}")
        page.close()
        browser.close()

    print(f"{len(failures)} FAILED" if failures else "all checks pass")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
