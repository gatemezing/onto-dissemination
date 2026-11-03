#!/usr/bin/env python3
"""Compare CRD primary/subsidiary locations with RINF (rinf-plus) from the CSVs written by fetch.py.

Writes stats/*.csv and stats/summary.json. Key = era:primaryLocationCode (the TAF/TAP PLC),
because RINF mints several IRIs for one code (republishing, per-IM IRI patterns).
Usage: python3 -I scripts/compare.py [AS_OF=YYYY-MM-DD]
"""
import csv, json, math, re, sys, unicodedata, collections, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "stats"
OUT.mkdir(exist_ok=True)
AS_OF = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
CODE_RE = re.compile(r"^[A-Z]{2}[0-9]{5}$")


def rows(ep, name):
    with open(RAW / ep / f"{name}.csv", newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def by_pl(ep, name):
    d = {}
    for r in rows(ep, name):
        d[r["pl"]] = r
    return d


def wkt_point(w):
    if not w:
        return None
    m = re.search(r"POINT\s*\(\s*([+-]?[\d.]+)\s+([+-]?[\d.]+)", w)
    if not m:
        return None
    x, y = float(m.group(1)), float(m.group(2))
    return None if abs(x) < 1e-6 and abs(y) < 1e-6 else (x, y)   # POINT(0 0) = "no position", counted separately


def km(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    return re.sub(r"[^0-9a-z]+", "", s)


def load(ep):
    """Return {code: record}; record holds sets so RINF's multi-IRI codes keep every variant."""
    codes = rows(ep, "pl-code")
    country, im, name = by_pl(ep, "pl-country"), by_pl(ep, "pl-im"), by_pl(ep, "pl-name")
    flags, wkt, val, nuts = by_pl(ep, "pl-flags"), by_pl(ep, "pl-wkt"), by_pl(ep, "pl-validity"), by_pl(ep, "pl-nuts")
    ops = by_pl(ep, "pl-op") if (RAW / ep / "pl-op.csv").exists() else {}
    recs, no_code = {}, set()
    for r in codes:
        pl, code = r["pl"], r["code"].strip()
        if not code:
            no_code.add(pl)
            continue
        x = recs.setdefault(code, collections.defaultdict(set))
        x["iri"].add(pl)
        x["graph"].add(r["g"].rsplit("/", 1)[-1])
        if pl in country:
            x["country"].update(country[pl]["country"].split("|"))
        if pl in im:
            x["im"].update(im[pl]["im"].split("|"))
        if pl in name:
            if name[pl]["name_en"]:
                x["name_en"].add(name[pl]["name_en"])
            x["names"].update(n for n in name[pl]["names"].split("|") if n)
        if pl in flags:
            for f in ("passenger", "freight", "container", "handover"):
                if flags[pl][f]:
                    x[f].update(flags[pl][f].split("|"))
        if pl in wkt:
            if re.search(r"POINT\s*\(\s*[+-]?0(\.0*)?\s+[+-]?0(\.0*)?\s*\)", wkt[pl]["wkt_netref"] or wkt[pl]["wkt_direct"] or ""):
                x["zero_point"].add(True)
            p = wkt_point(wkt[pl]["wkt_netref"]) or wkt_point(wkt[pl]["wkt_direct"])
            if p:
                x["point"].add(p)
        if pl in val:
            if val[pl]["begin"]:
                x["begin"].add(val[pl]["begin"])
            if val[pl]["end"]:
                x["end"].add(val[pl]["end"])
            x["has_validity"].add(True)
        if pl in nuts:
            x["nuts3"].update(nuts[pl]["nuts3"].split("|"))
        if pl in ops:
            x["n_op"].add(int(ops[pl]["n_op"]))
            if ops[pl]["uopid"]:
                x["uopid"].add(ops[pl]["uopid"])
    return recs, no_code, ops


crd, crd_nocode, _ = load("crd")
rinf, rinf_nocode, rinf_ops = load("rinf")
crd_iris = {i for r in crd.values() for i in r["iri"]}
rinf_iris = {i for r in rinf.values() for i in r["iri"]} | rinf_nocode
S = {"as_of": AS_OF}

# ---------- 1. primary-location inventory --------------------------------------------------
S["pl"] = {
    "crd_iris": len(crd_iris), "crd_codes": len(crd), "crd_iris_without_code": len(crd_nocode),
    "crd_codes_with_several_iris": sum(1 for r in crd.values() if len(r["iri"]) > 1),
    "rinf_iris": len(rinf_iris), "rinf_codes": len(rinf), "rinf_iris_without_code": len(rinf_nocode),
    "rinf_codes_with_several_iris": sum(1 for r in rinf.values() if len(r["iri"]) > 1),
    "rinf_codes_in_several_graphs": sum(1 for r in rinf.values() if len(r["graph"]) > 1),
}
both = sorted(set(crd) & set(rinf))
crd_only = sorted(set(crd) - set(rinf))
rinf_only = sorted(set(rinf) - set(crd))
S["pl"].update({"codes_in_both": len(both), "codes_crd_only": len(crd_only), "codes_rinf_only": len(rinf_only),
                "same_iri_in_both": sum(1 for c in both if crd[c]["iri"] & rinf[c]["iri"])})

# code syntax
def bad_codes(recs):
    return sorted(c for c in recs if not CODE_RE.match(c))
S["pl"]["crd_codes_bad_pattern"] = len(bad_codes(crd))
S["pl"]["rinf_codes_bad_pattern"] = len(bad_codes(rinf))
S["pl"]["rinf_codes_bad_pattern_examples"] = bad_codes(rinf)[:15]

# ---------- 2. per country (code prefix = ISO 3166-1 alpha-2 of the allocating country) ---
prefix = lambda c: c[:2]
per = collections.defaultdict(lambda: collections.Counter())
for c, r in crd.items():
    per[prefix(c)]["crd"] += 1
    per[prefix(c)]["crd_country_" + "|".join(sorted(r["country"]))] += 0
for c in rinf:
    per[prefix(c)]["rinf"] += 1
for c in both:
    per[prefix(c)]["both"] += 1
for c in crd_only:
    per[prefix(c)]["crd_only"] += 1
for c in rinf_only:
    per[prefix(c)]["rinf_only"] += 1
crd_cty = collections.defaultdict(collections.Counter)
for c, r in crd.items():
    crd_cty[prefix(c)].update(r["country"] or {"(none)"})
with open(OUT / "pl-by-country.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["code_prefix", "crd_inCountry", "crd_codes", "rinf_codes", "in_both", "crd_only", "rinf_only", "rinf_coverage_of_crd_pct"])
    for p in sorted(per, key=lambda p: -(per[p]["crd"] + per[p]["rinf"])):
        k = per[p]
        w.writerow([p, " ".join(f"{a}:{n}" for a, n in crd_cty[p].most_common()), k["crd"], k["rinf"], k["both"], k["crd_only"], k["rinf_only"],
                    f"{100 * k['both'] / k['crd']:.1f}" if k["crd"] else ""])

# CRD country vs code prefix (inCountry is the location's country; prefix is the allocating country)
ISO2_3 = {"AT": "AUT", "BE": "BEL", "BG": "BGR", "CH": "CHE", "CZ": "CZE", "DE": "DEU", "DK": "DNK", "EE": "EST", "ES": "ESP", "FI": "FIN",
          "FR": "FRA", "GB": "GBR", "GR": "GRC", "HR": "HRV", "HU": "HUN", "IE": "IRL", "IT": "ITA", "LT": "LTU", "LU": "LUX", "LV": "LVA",
          "NL": "NLD", "NO": "NOR", "PL": "POL", "PT": "PRT", "RO": "ROU", "SE": "SWE", "SI": "SVN", "SK": "SVK", "RS": "SRB", "BA": "BIH",
          "ME": "MNE", "MK": "MKD", "AL": "ALB", "TR": "TUR", "UA": "UKR", "BY": "BLR", "RU": "RUS", "MD": "MDA", "XK": "XKX", "LI": "LIE"}
S["pl"]["crd_country_differs_from_code_prefix"] = sum(1 for c, r in crd.items() if ISO2_3.get(prefix(c)) and r["country"] and ISO2_3[prefix(c)] not in r["country"])

# ---------- 3. property completeness --------------------------------------------------------
props = ["zero_point", "country", "im", "name_en", "names", "passenger", "freight", "container", "handover", "point", "has_validity", "begin", "end", "nuts3"]
with open(OUT / "pl-completeness.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["property", "crd_codes_with_value", "crd_pct", "rinf_codes_with_value", "rinf_pct", "rinf_pct_on_shared_codes"])
    comp = {}
    for p in props:
        a = sum(1 for r in crd.values() if r[p]); b = sum(1 for r in rinf.values() if r[p]); s = sum(1 for c in both if rinf[c][p])
        comp[p] = (a, b)
        w.writerow([p, a, f"{100*a/len(crd):.1f}", b, f"{100*b/len(rinf):.1f}", f"{100*s/len(both):.1f}"])
S["pl"]["completeness"] = {p: {"crd": a, "rinf": b} for p, (a, b) in comp.items()}

# ---------- 4. value agreement on shared codes ---------------------------------------------
# RINF graphs 0080 (DB InfraGO) and 0084 (ProRail) were loaded from the same CRD pipeline
# (validity IRIs temporalFeature/YYYYMMDD_None, parameterApplicability IRIs), so agreement there is
# not independent evidence. Every tally is kept for "all", "derived" and "independent".
DERIVED_GRAPHS = {"0080", "0084"}
def group_of(c):
    return "derived" if rinf[c]["graph"] <= DERIVED_GRAPHS else "independent"
agree = collections.defaultdict(lambda: collections.OrderedDict())
by_prefix = collections.defaultdict(collections.Counter)
def tally(c, field, ok, comparable):
    for grp in ("all", group_of(c)):
        t = agree[grp].setdefault(field, collections.Counter())
        t["comparable"] += comparable
        t["agree"] += ok and comparable
    if comparable:
        by_prefix[(c[:2], field)]["comparable"] += 1
        by_prefix[(c[:2], field)]["agree"] += ok
diffs = collections.defaultdict(list)
dists = []
for c in both:
    a, b = crd[c], rinf[c]
    for f in ("country", "im", "passenger", "freight", "container", "handover", "nuts3"):
        cmp = bool(a[f]) and bool(b[f])
        ok = bool(a[f] & b[f])
        tally(c, f, ok, cmp)
        if cmp and not ok and len(diffs[f]) < 2000:
            diffs[f].append((c, "|".join(sorted(a[f])), "|".join(sorted(b[f]))))
    an = {norm(n.rsplit("@", 1)[0]) for n in a["names"]} | {norm(n) for n in a["name_en"]}
    bn = {norm(n.rsplit("@", 1)[0]) for n in b["names"]} | {norm(n) for n in b["name_en"]}
    an.discard(""); bn.discard("")
    cmp = bool(an) and bool(bn)
    tally(c, "name", bool(an & bn), cmp)
    if cmp and not an & bn and len(diffs["name"]) < 2000:
        diffs["name"].append((c, "|".join(sorted(a["name_en"] or a["names"])), "|".join(sorted(b["name_en"] or b["names"]))))
    if a["point"] and b["point"]:
        d = min(km(p, q) for p in a["point"] for q in b["point"])
        dists.append((d, c))
        tally(c, "position within 1 km", d <= 1, True)
    cmp = bool(a["begin"]) and bool(b["begin"])
    tally(c, "validity begin", bool(a["begin"] & b["begin"]), cmp)
    if cmp and not a["begin"] & b["begin"] and len(diffs["validity begin"]) < 2000:
        diffs["validity begin"].append((c, "|".join(sorted(a["begin"])), "|".join(sorted(b["begin"]))))
with open(OUT / "pl-agreement-by-prefix.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["code_prefix", "field", "comparable", "agree", "agree_pct"])
    for (px, f), t in sorted(by_prefix.items()):
        w.writerow([px, f, t["comparable"], t["agree"], f"{100*t['agree']/t['comparable']:.1f}"])
S["pl"]["shared_codes_by_group"] = collections.Counter(group_of(c) for c in both)
dists.sort()
def pct(x, n):
    return round(100 * x / n, 1) if n else None
S["pl"]["agreement"] = {grp: {f: {"comparable": t["comparable"], "agree": t["agree"], "agree_pct": pct(t["agree"], t["comparable"])} for f, t in fs.items()} for grp, fs in agree.items()}
if dists:
    ds = [d for d, _ in dists]
    q = lambda p: round(ds[min(len(ds) - 1, int(p * len(ds)))], 3)
    S["pl"]["distance_km"] = {"comparable": len(ds), "median": q(0.5), "p90": q(0.9), "p99": q(0.99), "max": round(ds[-1], 1),
                              "within_100m": sum(d <= 0.1 for d in ds), "within_1km": sum(d <= 1 for d in ds),
                              "over_1km": sum(d > 1 for d in ds), "over_10km": sum(d > 10 for d in ds), "over_100km": sum(d > 100 for d in ds)}
    with open(OUT / "pl-distance-outliers.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["code", "distance_km", "crd_point", "rinf_points", "crd_name", "rinf_name"])
        for d, c in reversed(dists):
            if d <= 10:
                break
            w.writerow([c, f"{d:.1f}", ";".join(f"{x:.5f} {y:.5f}" for x, y in crd[c]["point"]), ";".join(f"{x:.5f} {y:.5f}" for x, y in rinf[c]["point"]),
                        "|".join(crd[c]["name_en"]), "|".join(rinf[c]["name_en"] or rinf[c]["names"])])
with open(OUT / "pl-value-differences.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["field", "code", "crd", "rinf"])
    for f, lst in diffs.items():
        for c, x, y in lst:
            w.writerow([f, c, x, y])
S["pl"]["difference_breakdown"] = {f: collections.Counter(f"{x} -> {y}" for _, x, y in lst).most_common(8) for f, lst in diffs.items() if f not in ("name", "validity begin")}

# ---------- 5. CRD-internal quality ---------------------------------------------------------
def ws_issue(n):
    return n != n.strip() or "  " in n
S["crd_quality"] = {
    "pl_names_with_whitespace_runs": sum(1 for r in crd.values() if any(ws_issue(n.rsplit("@", 1)[0]) for n in r["names"])),
    "pl_without_en_name": sum(1 for r in crd.values() if not r["name_en"]),
    "pl_validity_ended_before_as_of": sum(1 for r in crd.values() if r["end"] and max(r["end"]) < AS_OF),
    "pl_validity_begins_after_as_of": sum(1 for r in crd.values() if r["begin"] and min(r["begin"]) > AS_OF),
    "pl_without_validity_begin": sum(1 for r in crd.values() if not r["begin"]),
    "pl_point_outside_europe_bbox": sum(1 for r in crd.values() for p in r["point"] if not (-32 <= p[0] <= 70 and 27 <= p[1] <= 72)),
    "pl_point_zero": sum(1 for r in crd.values() if r["zero_point"]),
    "pl_point_zero_by_prefix": collections.Counter(c[:2] for c, r in crd.items() if r["zero_point"]).most_common(),
    "rinf_pl_point_zero": sum(1 for r in rinf.values() if r["zero_point"]),
    "pl_all_flags_false_by_prefix": collections.Counter(c[:2] for c, r in crd.items() if r["passenger"] == {"false"} and r["freight"] == {"false"} and r["container"] == {"false"} and r["handover"] == {"false"}).most_common(12),
    "pl_all_flags_false": sum(1 for r in crd.values() if r["passenger"] == {"false"} and r["freight"] == {"false"} and r["container"] == {"false"} and r["handover"] == {"false"}),
}
S["crd_quality"]["pl_validity_begin_year_hist"] = collections.Counter(min(r["begin"])[:3] + "0s" for r in crd.values() if r["begin"]).most_common()

# ---------- 6. RINF operational points -> primary locations --------------------------------
op_pl_codes = {}
for pl, r in rinf_ops.items():
    op_pl_codes[pl] = int(r["n_op"])
iri2code = {i: c for c, r in rinf.items() for i in r["iri"]}
ref_codes = {iri2code[i] for i in op_pl_codes if i in iri2code}
S["rinf_op_link"] = {
    "pl_iris_referenced_by_ops": len(op_pl_codes),
    "referenced_iris_untyped_or_without_code": sum(1 for i in op_pl_codes if i not in iri2code),
    "referenced_codes": len(ref_codes),
    "referenced_codes_in_crd": len(ref_codes & set(crd)),
    "referenced_codes_missing_from_crd": len(ref_codes - set(crd)),
    "crd_codes_referenced_by_a_rinf_op": len(ref_codes & set(crd)),
    "pl_iris_referenced_by_more_than_one_op": sum(1 for n in op_pl_codes.values() if n > 1),
}
with open(OUT / "rinf-op-pl-missing-from-crd.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["code", "rinf_graphs", "rinf_iris", "uopid", "rinf_name"])
    for c in sorted(ref_codes - set(crd)):
        r = rinf[c]; w.writerow([c, "|".join(sorted(r["graph"])), "|".join(sorted(r["iri"])), "|".join(sorted(r["uopid"])), "|".join(sorted(r["name_en"] or r["names"]))])

# ---------- 7. subsidiary locations ---------------------------------------------------------
def plcode(iri):
    m = re.search(r"([A-Z]{2}\d{5})", iri)
    return m.group(1) if m else ""


def load_sl(ep):
    return rows(ep, "sl")
csl, rsl = load_sl("crd"), load_sl("rinf")
crd_pl_iris = crd_iris
sl_type = collections.Counter(r["type"] or "(none)" for r in csl)
S["sl"] = {
    "crd": len(csl), "rinf": len(rsl),
    "crd_dangling_pl_link": sum(1 for r in csl if r["pl"] and r["pl"] not in crd_pl_iris),
    "crd_without_pl_link": sum(1 for r in csl if not r["pl"]),
    "crd_with_geometry": sum(1 for r in csl if r["wkt"]),
    "crd_pl_link_in_rinf": sum(1 for r in csl if r["pl"].rsplit("/", 1)[-1] in rinf),
    "crd_type_distribution": sl_type.most_common(),
    "crd_alloc_company_codes": len({r["alloc"] for r in csl}),
    "crd_alloc_differs_from_im": sum(1 for r in csl if r["alloc"] and r["alloc"] not in (crd.get(plcode(r["pl"]), {}).get("im") or {r["alloc"]})),
    "crd_names_with_whitespace_runs": sum(1 for r in csl if ws_issue(r["name"])),
    "crd_code_length_over_10": sum(1 for r in csl if len(r["code"]) > 10),
    "crd_by_country": collections.Counter(r["country"] for r in csl).most_common(),
    "rinf_by_graph": collections.Counter(r["g"].rsplit("/", 1)[-1] for r in rsl).most_common(),
    "rinf_with_type": sum(1 for r in rsl if r["type"]),
    "rinf_pl_link_resolves_to_typed_pl": sum(1 for r in rsl if r["pl"] in rinf_iris),
}
# NOR overlap: RINF SLs are Bane NOR's own; match on (PL code, SL code)
def plcode(iri):
    m = re.search(r"([A-Z]{2}\d{5})", iri)
    return m.group(1) if m else ""
ck = {(plcode(r["pl"]), r["code"]) for r in csl if r["country"] == "NOR"}
rk = {(plcode(r["pl"]), r["code"]) for r in rsl}
S["sl"]["nor_crd"] = len(ck); S["sl"]["nor_rinf"] = len(rk); S["sl"]["nor_same_pl_and_code"] = len(ck & rk)
S["sl"]["nor_rinf_pl_codes_in_crd"] = len({p for p, _ in rk} & set(crd))
S["sl"]["nor_rinf_code_examples"] = sorted(c for _, c in rk)[:5]
S["sl"]["nor_crd_code_examples"] = sorted(c for _, c in ck)[:5]

with open(OUT / "sl-by-country-type.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["country", "type", "crd_sl"])
    for (cty, t), n in sorted(collections.Counter((r["country"], r["type"]) for r in csl).items(), key=lambda kv: -kv[1]):
        w.writerow([cty, t, n])

(OUT / "summary.json").write_text(json.dumps(S, indent=1, ensure_ascii=False, default=list))
print(json.dumps(S, indent=1, ensure_ascii=False, default=list)[:6000])
