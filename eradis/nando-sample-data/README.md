# NANDO notified bodies, modelled the OCR-KG way

NANDO (the Commission's register of notified bodies) publishes no open data.
This folder starts from the list page's CSV export and models it the way ERA's
Organisation Codes Register (OCR-KG) models organisations. It also measures
how the list lines up with what ERA already publishes.

| File | What it is |
|---|---|
| `body.csv` | NANDO export: bodies with an **active** notification under **legislationId 31** ([list](https://webgate.ec.europa.eu/single-market-compliance-space/notified-bodies/notified-body-list?filter=legislationId:31,notificationStatusId:1)), 67 rows, exported 2026-10-30 |
| `ocr-organisations.rq` | every OCR-KG organisation with name, short names, country, roles and website (the match input) |
| `nando-ocr-eradis-match.csv` | per NB number: OCR-KG match (confirmed / uncertain / none), its roles, and whether ERADIS knows the NB number |
| `nando-active-nobos-leg31.ttl` | the 67 bodies as `era:Body` + NOBO `era:OrganisationRole` carrying `era:nandoCode`, site, address, homepage (1,687 triples) |
| `nando-249444-ocr-pattern.ttl` | pattern for one body's **version history** (NANDO_INPUT_249444); its values are illustrative |

Regenerate with `python3 scripts/build-nando-sample.py` (queries OCR-KG live,
reads the ERADIS snapshot in `scripts/assets/`).

## The pattern

```
era:Body ─era:role→ era:OrganisationRole ─era:hasOrganisationRole→ organisation-roles/NOBO
   │                     └─ era:nandoCode "NB nnnn"     (domain is the role, as in ERADIS)
   ├─org:hasSite→ org:Site ─org:siteAddress→ locn:Address
   ├─foaf:homepage→ era:Document ─foaf:page→ <website>
   └─era:changeActivity→ era:Activity (⊑ prov:Activity): dct:type, prov:atTime
```

- A body that OCR-KG already has keeps its OCR IRI, and so does its NOBO role.
  The other bodies get placeholder IRIs under `https://example.org/nando/`.
- NANDO's site, address and homepage always get their own IRIs, so they never
  merge into OCR-KG's address resources.
- Phone, fax and e-mail are left out. OCR-KG publishes none of them, and
  several NANDO e-mails name a person.
- Not ERA terms, kept in the `nando:` namespace on purpose:
  `nando:Notification`, `nando:BodyVersion`, `nando:notificationStatus`,
  `nando:legislation/31`. Which act legislationId 31 is has not been confirmed;
  every body on the list is a rail notified body.

## Findings (measured 2026-10-30)

### NANDO vs ERADIS: matched by NB number

- **62 of 67** active bodies appear in the ERADIS snapshot.
- **5 bodies have not appeared in any published ERADIS declaration or
  certificate:** NB 1583 PIT Certification, NB 2953 TÜV SÜD Austria, NB 2971
  DNV Spain, NB 3014 INFRACERT d.o.o., NB 3017 Certifer France.
- **18 NB numbers in ERADIS are not on the active list.** These are mostly UK
  bodies (Lloyd's Register, Ricardo Certification Ltd, SGS UK, Sconrail UK,
  Railway Approvals Ltd, Delta Rail, SNC-Lavalin, AEGIS Ltd). Two names come
  back under a new number, and one more body has dropped off:
  - Certifer France: NB 2593 in ERADIS, NB 3017 on the active list.
  - PIT Certification: NB 1940 in ERADIS, NB 1583 on the active list.
  - Bureau Veritas Exploitation (NB 2681).

  Their certificates are history. Don't read them as current notified-body
  status.

### NANDO vs OCR-KG: matched by name and website, since OCR-KG has no NB numbers

| | Bodies |
|---|---|
| Confirmed in OCR-KG | **22** |
| …of which carry the NOBO role | **13** |
| …present but **without** the NOBO role | 9: P0A9 SCHIG, 3688 VUZ, YOYN Sconrail GmbH, WAUT DNV Spain, 3032 KTI, JI3U Bureau Veritas Italia, 6ZWS Certifer Italia, 6DVH CERTA, MYU2 Q Techna |
| Uncertain (same website, different legal name) | 3: NB 2915 → 1SV7 "Tüv Süd", NB 2294 → 0O18 Bureau Veritas Exploitation, NB 2269 → P0AL AFER |
| Not in OCR-KG | **42** |

- **OCR-KG's NOBO role covers 13 of the 67 active rail notified bodies (19 %).**
  A query on `organisation-roles/NOBO` misses most of them, and returns no error.
- **Five OCR-KG NOBO bodies are not on the active list:**
  - 9KH3 Vericert, HBAS Aarsleff Rail and TD9B BIV.
  - P0AA Eisenbahn-Bundesamt. EBA is the authority; its notified body is
    EISENBAHN-CERT, NB 0893, which OCR-KG lacks.
  - 7I22 ISARail s.p.a., a **duplicate** of QFVT ISARAIL, with a CRM GUID for a
    website (`http://e9feca4a-c8d1-ef11-95f5-6045bd1aa03e.com/`).
- **KTI exists twice in OCR-KG.** 3032 "Közlekedéstudományi Intézet" (role IM)
  matches NANDO's name, and 7A7R "KTI … Nonprofit Kft." shares its website.
- **Name matching needs a high bar.** At similarity 0.75 it paired TÜV SÜD
  Nederland with VIAS Nederland, RINA with Agriservice, Kiwa Latvia with
  Latvia's NSA, and rail³ with RailQ. The script confirms only at ≥ 0.9, or
  ≥ 0.75 together with the same website.

### OCR-KG change model

- Every body has **exactly one** `era:changeActivity`, at the fixed IRI
  `activity/{code}`. It can hold one change, not a history.
  `nando-249444-ocr-pattern.ttl` shows one activity per NANDO organisation
  version instead.
- About 250 activities have `dct:creator <https://www.wikidata.org/entity/{orgCode}>`,
  which is not a Wikidata item.
- The 124 revocation activities have labels that end in a stray `\"@en` inside
  a plain string, so they carry no language tag.

### NANDO data quality (in `body.csv`)

- NB 2147 is spelt "BALTIC **S**ERTIFICATION" (OCR-KG: CERTIFICATION).
- NB 2627's e-mail contains a space (`post@pl. tuv.com`). NB 0537's is a
  placeholder (`FirstnameSurname@eurofins.fi`).
- Five bodies have no website. Phone and fax formats vary freely.

### Not resolvable from this export

NANDO_INPUT_249444 cannot be identified from `body.csv`. The export carries NB
numbers but not NANDO's internal reference code. Its version history needs the
body page's own export.
