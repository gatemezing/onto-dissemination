#!/usr/bin/env python3
"""Build the ERADIS snapshot that era-eradis-explorer.html searches when it
cannot query ERADIS-KG live.

The dev endpoint (graph.dev.data.test-era.europa.eu) sends no CORS headers, so
a page served from GitHub Pages cannot read its answers; the production
repository requires authentication. The explorer therefore tries the endpoint
first and falls back to this snapshot, which is produced by the very queries in
eradis/snapshot-*.rq - so the snapshot and a live answer come from the same
SPARQL.

Deliberately NOT in the snapshot: signatory names (personal data - the
explorer only searches them live), contact details, and the unpublished
submissions in the draft graph.

Usage:  python3 scripts/build-eradis-snapshot.py [--endpoint URL] [--lex-endpoint URL]
Writes: scripts/assets/era-eradis-snapshot.json.gz      declarations + shared tables
        scripts/assets/era-eradis-certificates.json.gz  NoBo certificates
        (era:CertificationLevelDocument), loaded by the page on demand and
        indexing into the shared organisation / TSI / directive tables
"""
import argparse, csv, datetime, gzip, io, json, pathlib, re, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUERIES = ROOT / "eradis"
OUT = ROOT / "scripts" / "assets" / "era-eradis-snapshot.json.gz"
OUT_CERTS = ROOT / "scripts" / "assets" / "era-eradis-certificates.json.gz"
DEFAULT_ENDPOINT = "https://graph.dev.data.test-era.europa.eu/repositories/ERADIS-KG"
DEFAULT_LEX = "https://graph.dev.data.test-era.europa.eu/repositories/era-lex"

ERA = "http://data.europa.eu/949/"
COUNTRY = "http://publications.europa.eu/resource/authority/country/"
ORG_BASE = ERA + "body/organisation/eradis/"

TYPES = {  # dct:type concepts carry no prefLabel in ERADIS-KG
    ERA + "concepts/ecd-types/ECDoV": ("V", "EC declaration of verification (subsystem)"),
    ERA + "concepts/ecd-types/ECDoC": ("C", "EC declaration of conformity (interoperability constituent)"),
    ERA + "concepts/ecd-types/ECDoSU": ("S", "EC declaration of suitability for use"),
}
STATES = {  # evidence-document-states concepts carry no prefLabel either
    ERA + "concepts/evidence-document-states/inForce": "In force",
    ERA + "concepts/evidence-document-states/amended": "Amended",
    ERA + "concepts/evidence-document-states/revoked": "Revoked",
    ERA + "concepts/evidence-document-states/suspended": "Suspended",
}

# "Type of subsystem" is not a property in ERADIS-KG. It is derived from the
# base TSIs a declaration cites, whose titles name their scope. Each TSI title is
# first classified into a TSI family (order matters: telematics-for-freight
# must be tested before freight wagons), and the family is then mapped onto the
# subsystems of Directive (EU) 2016/797 Annex II. The PRM and SRT TSIs apply
# across several subsystems, so they name none - they stay searchable through
# the "To TSIs" field.
TSI_FAMILIES = [
    ("CCS", r"control-command and signal"),
    ("TAF", r"telematics applications for freight"),
    ("TAP", r"telematics applications for passenger"),
    ("WAG", r"freight wagons"),
    ("NOI", r"noise"),
    ("LOC", r"locomotives and passenger|rolling stock.{0,3}sub-?system of the trans-european high-speed"),
    ("INF", r"infrastructure"),
    ("ENE", r"energy"),
    ("SRT", r"safety in railway tunnels"),
    ("PRM", r"reduced mobility|disabilities"),
    ("OPE", r"operation and traffic management|traffic operation and management"),
]
SUBSYSTEMS = [  # (key, label, TSI families)
    ("INF", "Infrastructure", {"INF"}),
    ("ENE", "Energy", {"ENE"}),
    ("CCS", "Control-command and signalling", {"CCS"}),
    ("RST", "Rolling stock", {"LOC", "WAG", "NOI"}),
    ("OPE", "Operation and traffic management", {"OPE"}),
    ("TEL", "Telematics applications", {"TAF", "TAP"}),
]
SUBSYSTEM_OF_FAMILY = {f: k for k, _, fams in SUBSYSTEMS for f in fams}
AMENDING = re.compile(r"\b(amending|correcting|modifying)\b", re.I)
ELI = "http://data.europa.eu/eli/"
EEA_TREATY = "http://publications.europa.eu/resource/authority/treaty/EEA"


def run(endpoint, name, values=None):
    query = (QUERIES / name).read_text()
    if values is not None:
        query = query.replace("##VALUES##", " ".join(f"<{v}>" for v in values))
    req = urllib.request.Request(endpoint, data=urllib.parse.urlencode({"query": query}).encode(),
                                 headers={"Accept": "text/csv"})
    with urllib.request.urlopen(req, timeout=180) as r:
        rows = list(csv.DictReader(io.TextIOWrapper(r, encoding="utf-8")))
    print(f"  {name}: {len(rows):,} rows", file=sys.stderr)
    return rows


def eli_candidates(key, same_as):
    """ELI URIs an ERADIS-KG act key (dec-2012-88, reg_impl-2019-776,
    dir-402-2013) may have in era-lex. The key's type is not always right
    (dir-402-2013 is Implementing Regulation 402/2013), and five decisions
    only exist with a (1)/(2) suffix."""
    t, a, b = re.match(r"([a-z_]+)-(\d+)-(\d+)$", key).groups()
    year, num = (a, b) if int(a) > 1900 else (b, a)
    out = [same_as] if same_as else []
    for typ in dict.fromkeys([t, "reg", "reg_impl", "dec", "dec_impl", "dir"]):
        base = f"{ELI}{typ}/{year}/{num}"
        out += [base + "/oj", base + "(1)/oj", base + "(2)/oj"]
    return list(dict.fromkeys(out))


def resolve_in_lex(lex_endpoint, ref_rows):
    """Look every cited act up in era-lex, then follow eli:changes until the
    amendment chain closes, so each amending act's targets are known too."""
    acts, asked = {}, set()
    todo = {c for r in ref_rows for c in eli_candidates(r["ref"].rsplit("/", 1)[-1], r["eli"])}
    for _ in range(6):
        todo -= asked
        if not todo:
            break
        asked |= todo
        for r in run(lex_endpoint, "snapshot-lex.rq", sorted(todo)):
            a = acts.setdefault(r["eli"], {"title": "", "inForce": "", "basedOn": set(), "changes": set()})
            if r["title"]:
                # era-lex titles carry non-breaking spaces ("locomotives\xa0and\xa0passenger")
                title = re.sub(r"\s+", " ", r["title"])
                a["title"] = re.sub(r"\s*\(?Text with EEA relevance\.?\)?\s*$", "", title).strip()
            if r["inForce"]:
                a["inForce"] = r["inForce"].rsplit("-", 1)[-1]
            if r["basedOn"]:
                a["basedOn"].add(r["basedOn"])
            if r["changes"].startswith(ELI):
                a["changes"].add(r["changes"])
        todo = {c for a in acts.values() for c in a["changes"]}

    chosen = {}
    for r in ref_rows:
        found = [c for c in eli_candidates(r["ref"].rsplit("/", 1)[-1], r["eli"]) if c in acts]
        # Of a (1)/(2) pair, drop the EEA Joint Committee decision; then prefer
        # the act most linked by amendment to the other acts found.
        found = [c for c in found if EEA_TREATY not in acts[c]["basedOn"]] or found
        linked = lambda c: sum(c in a["changes"] for a in acts.values()) + len(acts[c]["changes"])
        chosen[r["ref"]] = max(found, key=linked) if found else ""
    return acts, chosen


def family_of_title(title):
    for key, pat in TSI_FAMILIES:
        if re.search(pat, title or "", re.I):
            return key
    return ""


def subsystem_of(eli, acts, titles, seen=()):
    """A base TSI names its subsystem in its title. An amending or correcting
    act has the subsystem of the acts it changes - when those all belong to one
    subsystem; an act amending several subsystems (2019/776, 2023/1694) has
    none. When the acts changed name no subsystem at all (2012/757 is the OPE
    TSI and also amends Decision 2007/756, which is not a TSI), the act's own
    title decides."""
    a = acts.get(eli)
    title = titles.get(eli) or (a["title"] if a else "")
    if a and a["changes"] and AMENDING.search(title) and eli not in seen:
        subs = {subsystem_of(t, acts, titles, seen + (eli,)) for t in a["changes"]} - {""}
        if len(subs) > 1:
            return ""
        if subs:
            return subs.pop()
    return SUBSYSTEM_OF_FAMILY.get(family_of_title(title), "")


def notation_from_uri(uri):
    # .../dir-2016-797 -> 2016/797 ; .../reg_impl-2019-776 -> 2019/776 ; dir-402-2013 -> 402/2013
    m = re.search(r"/[a-z_]+-(\d+)-(\d+)$", uri)
    return f"{m.group(1)}/{m.group(2)}" if m else uri.rsplit("/", 1)[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    ap.add_argument("--lex-endpoint", default=DEFAULT_LEX)
    args = ap.parse_args()
    print(f"Querying {args.endpoint}", file=sys.stderr)

    decl_rows = run(args.endpoint, "snapshot-declarations.rq")
    link_rows = run(args.endpoint, "snapshot-links.rq")
    org_rows = run(args.endpoint, "snapshot-organisations.rq")
    ref_rows = run(args.endpoint, "snapshot-references.rq")
    ver_rows = run(args.endpoint, "snapshot-versions.rq")
    cert_rows = run(args.endpoint, "snapshot-certificates.rq")
    cert_link_rows = run(args.endpoint, "snapshot-certificate-links.rq")
    cert_ver_rows = run(args.endpoint, "snapshot-certificate-versions.rq")

    orgs, org_idx = [], {}
    for r in sorted(org_rows, key=lambda r: (r["orgName"] or "").lower()):
        org_idx[r["org"]] = len(orgs)
        cc = r["orgCountry"].replace(COUNTRY, "") if r["orgCountry"] else ""
        # [name, ISO 3166 alpha-3, registration/VAT numbers, NANDO code, URI key]
        # - the key rebuilds the URI (ORG_BASE + key) for live queries.
        key = r["org"][len(ORG_BASE):] if r["org"].startswith(ORG_BASE) else r["org"]
        orgs.append([r["orgName"] or key, cc, r["registration"], r["nandoCode"], key])

    acts, chosen = resolve_in_lex(args.lex_endpoint, ref_rows)
    # ERADIS-KG's own title is the fallback for the (1)/(2) decisions, which
    # era-lex holds without an English title.
    own_title = lambda r: re.sub(r"\s+", " ", r["label"]) if r["label"] and not r["label"].startswith(("20", "19")) else ""
    titles = {chosen[r["ref"]]: acts[chosen[r["ref"]]]["title"] or own_title(r) for r in ref_rows if chosen[r["ref"]]}
    refs = {"tsi": [], "dir": []}
    ref_idx = {}
    unresolved = []
    for r in sorted(ref_rows, key=lambda r: notation_from_uri(r["ref"])):
        kind, uri = r["kind"], r["ref"]
        eli = chosen[uri]
        if not eli:
            unresolved.append(uri)
        title = titles.get(eli) or own_title(r)
        in_force = 1 if eli and acts[eli]["inForce"] == "inForce" else 0
        sub = ""
        if kind == "tsi":
            sub = subsystem_of(eli, acts, titles) if eli else SUBSYSTEM_OF_FAMILY.get(family_of_title(title), "")
        # [notation, title, ERADIS-KG key, subsystem ("" = none), ELI in era-lex, in force]
        ref_idx[uri] = (kind, len(refs[kind]))
        refs[kind].append([notation_from_uri(uri), title, uri.rsplit("/", 1)[-1], sub, eli, in_force])
    if unresolved:
        print(f"  not found in era-lex: {', '.join(u.rsplit('/', 1)[-1] for u in unresolved)}", file=sys.stderr)

    versions = {r["documentId"]: int(r["versions"]) for r in ver_rows}

    # ---- NoBo certificates (era:CertificationLevelDocument) ----------------
    snapshot_day = datetime.date.today().isoformat()
    cert_key = lambda uri: int(uri.rsplit("/", 1)[-1])
    # Every current certificate whose dct:replaces chain reaches an older one.
    # A list, not a single value: the chain is not always closed - 3089
    # replaces 3091, yet 3091 carries no dct:isReplacedBy and so is current too.
    currents_of = {}
    for r in cert_ver_rows:
        currents_of.setdefault(r["older"], []).append(r["current"])
    cert_types, cert_type_idx = [], {}
    modules, module_idx = [], {}
    cert_states = []
    certs, cert_idx = [], {}
    for r in cert_rows:
        uri = r["certificate"]
        if uri in cert_idx:
            continue  # a second description or validity row
        if r["type"] and r["type"] not in cert_type_idx:
            cert_type_idx[r["type"]] = len(cert_types)
            cert_types.append([r["type"].rsplit("/", 1)[-1], r["typeLabel"] or r["type"].rsplit("/", 1)[-1]])
        states = sorted(st.rsplit("/", 1)[-1] for st in r["states"].split("|") if st)
        for st in states:
            if st not in cert_states:
                cert_states.append(st)
        # Several dates of issue are common (1,631). In 90 of those one of
        # them is the validity END recorded as a date of issue (issued
        # 2026-09-19 = valid until 2026-09-19), and a few are typos (3019).
        # The date shown is therefore the latest one that is neither the
        # validity end nor after today; the others stay searchable, as in
        # the SPARQL, which matches any dct:issued.
        issued = sorted(set(d for d in r["issued"].split("|") if d))
        usable = [d for d in issued if d != r["validUntil"]] or issued
        past = [d for d in usable if d <= snapshot_day]
        primary = past[-1] if past else (usable[0] if usable else "")
        issued = [d for d in issued if d != primary] + ([primary] if primary else [])
        m = re.search(r"id=(\d+)", r["eradisPage"] or "")
        cert_idx[uri] = len(certs)
        certs.append({
            "k": cert_key(uri), "n": r["certNumber"],
            "ty": cert_type_idx.get(r["type"]), "v": int(r["version"]),
            "st": [cert_states.index(st) for st in states],
            "d": issued[-1] if issued else "", "ds": issued[:-1],
            "vf": r["validFrom"], "vu": r["validUntil"],
            # the ERADIS page id, kept only where it differs from the key
            "p": int(m.group(1)) if m and int(m.group(1)) != cert_key(uri) else None,
            "nb": org_idx.get(r["noboOrg"]), "a": org_idx.get(r["applicantOrg"]),
            # object of assessment; the first 200 characters are what the
            # search and the table use - the full text is in the live record
            "x": re.sub(r"\s+", " ", r["description"] or "")[:200],
            "mf": [], "mo": [], "ts": [], "di": [], "ti": [], "pv": [], "re": 0, "dc": 0,
        })
    for r in cert_link_rows:
        i = cert_idx.get(r["certificate"])
        if i is None:
            continue
        c, k, v = certs[i], r["kind"], r["value"]
        if k == "manu" and v in org_idx and org_idx[v] not in c["mf"]:
            c["mf"].append(org_idx[v])
        elif k == "module":
            code = v.rsplit("/", 1)[-1]
            if code not in module_idx:
                module_idx[code] = len(modules)
                modules.append(code)
            if module_idx[code] not in c["mo"]:
                c["mo"].append(module_idx[code])
        elif k in ("tsi", "dir") and v in ref_idx and ref_idx[v][1] not in c["ts" if k == "tsi" else "di"]:
            c["ts" if k == "tsi" else "di"].append(ref_idx[v][1])
        elif k == "title" and v not in c["ti"]:
            c["ti"].append(v)
        elif k == "prev" and v not in c["pv"]:
            c["pv"].append(v)
        elif k == "restr":
            c["re"] = 1

    decls, decl_idx = [], {}
    cited_by = {}   # certificate key -> declarations citing it (any version)
    for r in decl_rows:
        uri = r["declaration"]
        if uri in decl_idx:
            continue  # extra dct:description value
        page = r["eradisPage"]
        m = re.search(r"id=(\d+)", page or "")
        decl_idx[uri] = len(decls)
        decls.append({
            "u": uri.rsplit("/", 1)[-1],
            "id": r["documentId"],
            "t": TYPES[r["type"]][0],
            "s": list(STATES).index(r["state"]),
            "v": int(r["version"]),
            "vn": versions.get(r["documentId"], 1),
            "d": r["issued"],
            "p": int(m.group(1)) if m else None,
            "a": org_idx.get(r["applicantOrg"]),
            "r": org_idx.get(r["authorisedRepOrg"]),
            "x": (r["description"] or "")[:280],
            "nb": [], "ti": [], "ts": [], "di": [], "ce": [], "re": 0,
        })

    for r in link_rows:
        i = decl_idx.get(r["declaration"])
        if i is None:
            continue
        d, k, v = decls[i], r["kind"], r["value"]
        if k == "nobo" and v in org_idx and org_idx[v] not in d["nb"]:
            d["nb"].append(org_idx[v])
        elif k == "title" and v not in d["ti"]:
            d["ti"].append(v)
        elif k in ("tsi", "dir") and v in ref_idx and ref_idx[v][1] not in d["ts" if k == "tsi" else "di"]:
            d["ts" if k == "tsi" else "di"].append(ref_idx[v][1])
        elif k == "cert" and v != "deleted" and v not in [c[0] for c in d["ce"]]:
            # [certificate number, date issued, key of the current certificate
            # to open (0 = none among the current published ones), further
            # current certificates this one is an earlier version of]. Counted
            # like the SPARQL "?certificate dct:replaces* ?cited".
            targets = ([r["ref"]] if r["ref"] in cert_idx else []) + currents_of.get(r["ref"], [])
            keys = list(dict.fromkeys(certs[cert_idx[t]]["k"] for t in targets if t in cert_idx))
            d["ce"].append([v, r["extra"], keys[0] if keys else 0] + ([keys[1:]] if len(keys) > 1 else []))
            for key in keys:
                cited_by.setdefault(key, set()).add(i)
        elif k == "restr":
            d["re"] = 1

    # Drop empty keys to keep the file small; the page treats missing as empty.
    # Index 0 is a real organisation / type, so only the 0/1 flags drop at 0.
    def compact(rec, flags=("re", "dc")):
        for k in [k for k, v in rec.items() if v is None or v == "" or v == [] or (k in flags and v == 0)]:
            del rec[k]
    for d in decls:
        compact(d)

    snapshot = {
        "generated": datetime.date.today().isoformat(),
        "endpoint": args.endpoint,
        "graph": ERA + "graph/eradis",
        "orgBase": ORG_BASE,
        "refBase": ERA + "legislation/requirements/",
        "lexEndpoint": args.lex_endpoint,
        "types": {v[0]: v[1] for v in TYPES.values()},
        "states": list(STATES.values()),
        "subsystems": [[k, label] for k, label, _ in SUBSYSTEMS],
        "subsystemBasis": "Directive (EU) 2016/797 Annex II, derived from the TSIs cited",
        "orgs": orgs,
        "tsis": refs["tsi"],
        "dirs": refs["dir"],
        "decls": decls,
    }
    raw = json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")).encode()
    OUT.write_bytes(gzip.compress(raw, 9, mtime=0))
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(decls):,} declarations, {len(orgs):,} organisations, "
          f"{len(raw)/1e6:.1f} MB JSON -> {OUT.stat().st_size/1e6:.2f} MB gzip", file=sys.stderr)

    for c in certs:
        c["dc"] = len(cited_by.get(c["k"], ()))
        compact(c)
    cert_snapshot = {
        "generated": snapshot["generated"],
        "types": cert_types,
        "modules": modules,
        "states": cert_states,
        "certs": certs,
    }
    raw = json.dumps(cert_snapshot, ensure_ascii=False, separators=(",", ":")).encode()
    OUT_CERTS.write_bytes(gzip.compress(raw, 9, mtime=0))
    linked = sum(1 for d in decls for c in d.get("ce", []) if c[2])
    multi = sum(1 for d in decls for c in d.get("ce", []) if len(c) > 3)
    total = sum(len(d.get("ce", [])) for d in decls)
    print(f"Wrote {OUT_CERTS.relative_to(ROOT)}: {len(certs):,} certificates, "
          f"{len(raw)/1e6:.1f} MB JSON -> {OUT_CERTS.stat().st_size/1e6:.2f} MB gzip; "
          f"{linked:,} of {total:,} declaration-certificate links resolved ({multi} reach two current certificates)", file=sys.stderr)


if __name__ == "__main__":
    main()
