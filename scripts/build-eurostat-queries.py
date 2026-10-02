#!/usr/bin/env python3
"""Generate the two optimised Eurostat queries, in one place for both users:

  eurostat/query-SoL-param1-optimised.rq   sections of line + track parameters
  eurostat/query-SoL-param1-geometry.rq    the same, plus each section's geometry
  eurostat/tent-query-v1-optimised.rq      TEN-T and corridor flags
  scripts/assets/era-eurostat-exporter.html  the same three, embedded

Each .rq file keeps its hand-written header (everything before the first
PREFIX line), which carries the measurements; only the query below it is
regenerated. Run after any change here:

    python3 scripts/build-eurostat-queries.py

Shape (measured 2026-10-01/02 against graph.data.era.europa.eu/rinf-plus):
- The sections valid today are resolved first, in their own subquery. DEU
  republishes every section a year ahead, so without the validity rule every
  German section counts twice (18,313 rows -> 36,648); with the test outside
  the subquery GraphDB re-ran it per joined row (81 s -> 14 s for DEU).
- Section and track fields keep the OPTIONAL chain with GROUP_CONCAT at the
  (section, track) grain. A UNION branch per field, which made the ERADIS
  queries fast, was slower here: DEU 28 s, the EU past the 120 s limit.
- The two operational points - names, UOPIDs, geometry - are aggregated per
  section in a subquery of their own. Inside the main join a point's names x
  UOPIDs x geometries multiplied with every track parameter (DEU 37 s, the EU
  past the limit); as separate per-point subqueries over every point in the
  graph they cost 50 s for DEU alone.
- Geometry comes through era:netReference/geo:hasGeometry/geo:asWKT, as the
  RINF value explorer reads it: 62,117 of 62,117 operational points and
  69,336 of 69,337 sections have one there. The WGS84 geo:location the export
  used before reaches 187 points (Lithuania only), so its location columns
  were empty everywhere else. The direct geo:hasGeometry is the fallback.
- An outer SELECT turns every empty or missing value into "no data".
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = '\t'
ND = '"no data"'
EN = 'FILTER(langMatches(lang(?{0}), "en"))'
GEOM = 'era:netReference/geo:hasGeometry/geo:asWKT'
GEOM_DIRECT = 'geo:hasGeometry/geo:asWKT'


def nd(expr, name):
    """Never an empty cell: unbound or empty becomes "no data"."""
    return f'(IF(COALESCE({expr}, "") != "", {expr}, {ND}) AS ?{name})'


def lat_lng(loc, name):
    # WKT is "POINT(lon lat)": longitude first
    rx = r'"^\\s*POINT\\s*\\(\\s*([^\\s)]+)\\s+([^\\s)]+).*$"'
    test = f'REGEX(COALESCE(?{loc}, ""), "^\\\\s*POINT", "i")'
    return [f'(IF({test}, REPLACE(?{loc}, {rx}, "$2", "i"), {ND}) AS ?{name}_lat)',
            f'(IF({test}, REPLACE(?{loc}, {rx}, "$1", "i"), {ND}) AS ?{name}_lng)']


def gc(expr, var):
    return f'(GROUP_CONCAT(DISTINCT {expr}; SEPARATOR="|") AS ?{var})'


VALID = f'''{T}{T}# The sections valid today, resolved first. DEU republishes every section a
{T}{T}# year ahead (2026-01-01..2026-12-31 and again from 2027-01-01), which would
{T}{T}# count every German section twice; sections with no dated validity (ten
{T}{T}# countries publish none) are kept. Resolving them on their own lets GraphDB
{T}{T}# run the validity test once per section, not once per joined row.
{T}{T}{{ SELECT ?sectionofline ?sectionofline_incountry WHERE {{
{T}{T}{T}?sectionofline a era:SectionOfLine ;
{T}{T}{T}{T}era:inCountry ?sectionofline_incountry .
##FILTER##
{T}{T}{T}BIND(xsd:date(SUBSTR(STR(NOW()), 1, 10)) AS ?today)
{T}{T}{T}FILTER NOT EXISTS {{ ?sectionofline era:validity/time:hasBeginning/time:inXSDDate ?vb FILTER(?vb > ?today) }}
{T}{T}{T}FILTER NOT EXISTS {{ ?sectionofline era:validity/time:hasEnd/time:inXSDDate ?ve FILTER(?ve < ?today) }}
{T}{T}}} }}'''

LINE = f'''{T}{T}OPTIONAL {{
{T}{T}{T}?sectionofline era:nationalLine ?lps .
{T}{T}{T}OPTIONAL {{ ?lps era:lineId ?lineId }}
{T}{T}{T}# LPS labels are language-tagged: without this filter every language
{T}{T}{T}# variant becomes its own value
{T}{T}{T}OPTIONAL {{ ?lps rdfs:label ?lpsLabel {EN.format('lpsLabel')} }}
{T}{T}}}'''
VALIDITY_DATES = f'''{T}{T}OPTIONAL {{
{T}{T}{T}?sectionofline era:validity ?solValidity .
{T}{T}{T}OPTIONAL {{ ?solValidity time:hasBeginning/time:inXSDDate ?validFrom }}
{T}{T}{T}OPTIONAL {{ ?solValidity time:hasEnd/time:inXSDDate ?validTo }}
{T}{T}}}'''


def ops_sub(section_geometry):
    """Everything about the section's two operational points - and, if asked,
    its own geometry - aggregated per section in a subquery of its own. In
    the main join a point's names x UOPIDs x geometries multiplied with every
    track parameter (DEU 18 s -> 37 s, the EU past the 120 s limit); here they
    only meet each other. Geometry comes through era:netReference, as the RINF
    value explorer reads it: every operational point and every section but
    one has it there (the WGS84 geo:location reached 187 of 62,117 points).
    The direct geo:hasGeometry is the fallback. For a point, a POINT if there
    is one (463 have several: the smallest, so the export is stable); MIN
    skips the rows where IF() raises an error."""
    aggs = []
    body = []
    for v, which in (('opStart', 'opStart'), ('opEnd', 'opEnd')):
        aggs += [f'(SAMPLE(?{v}) AS ?{v}_)', gc(f'?{v}Name', f'{v}Name_'), gc(f'?{v}Uopid', f'{v}Uopid_'),
                 f'(COALESCE(MIN(IF(STRSTARTS(UCASE(STR(?{v}W)), "POINT"), STR(?{v}W), ?notAPoint)), '
                 f'MIN(STR(?{v}W)), MIN(STR(?{v}DW))) AS ?{v}Loc_)']
        body.append(f'''{T}{T}OPTIONAL {{
{T}{T}{T}?sectionofline era:{which} ?{v} .
{T}{T}{T}OPTIONAL {{ ?{v} era:opName ?{v}Name }}
{T}{T}{T}OPTIONAL {{ ?{v} era:uopid ?{v}Uopid }}
{T}{T}{T}OPTIONAL {{ ?{v} {GEOM} ?{v}W }}
{T}{T}{T}OPTIONAL {{ ?{v} {GEOM_DIRECT} ?{v}DW FILTER(!BOUND(?{v}W)) }}
{T}{T}}}''')
    if section_geometry:
        aggs.append('(COALESCE(MIN(STR(?solW)), MIN(STR(?solDW))) AS ?solGeom_)')
        body.append(f'{T}{T}OPTIONAL {{ ?sectionofline {GEOM} ?solW }}\n'
                    f'{T}{T}OPTIONAL {{ ?sectionofline {GEOM_DIRECT} ?solDW FILTER(!BOUND(?solW)) }}')
    return (f'{T}# the two operational points (and the section geometry), per section\n'
            f'{T}{{ SELECT ?sectionofline\n' + '\n'.join(T + T + x for x in aggs) + f'\n{T}WHERE {{\n'
            + VALID.replace('?sectionofline_incountry WHERE', '?sectionofline_incountry WHERE', 1) + '\n'
            + '\n'.join(body) + f'\n{T}}}\n{T}GROUP BY ?sectionofline }}')


def label(subj, prop, c, l, indent=3):
    i = T * indent
    return f'{i}OPTIONAL {{ {subj} {prop} ?{c} .\n{i}{T}OPTIONAL {{ ?{c} skos:prefLabel ?{l} {EN.format(l)} }} }}'


def sol(section_geometry):
    aggs = ['(SAMPLE(?len) AS ?len_)', gc('?imCode', 'imCode_'), gc('COALESCE(?lineId, ?lpsLabel)', 'line_'),
            gc('COALESCE(?solNatureL, STR(?solNatureC))', 'solNature_'),
            gc('?validFrom', 'validFrom_'), gc('?validTo', 'validTo_')]
    aggs += [gc('COALESCE(?tenClassL, STR(?tenClassC))', 'ten_'), gc('?maxSpeed', 'speed_'),
             gc('COALESCE(?freightL, STR(?freightC))', 'freight_'), gc('COALESCE(?gaugeL, STR(?gaugeC))', 'gauge_'),
             gc('STR(?cls)', 'cls_'), gc('COALESCE(?clsTypeL, STR(?clsTypeC))', 'clsType_'),
             gc('COALESCE(?energyL, STR(?energyC))', 'energy_'), gc('COALESCE(?etcsTypeL, STR(?etcsTypeC))', 'etcs_'),
             gc('COALESCE(?gsmrL, STR(?gsmrC))', 'gsmr_')]
    where = f'''{VALID}
{T}{T}OPTIONAL {{ ?sectionofline era:lengthOfSectionOfLine ?len }}
{T}{T}# Concept-valued columns: the concept's English skos:prefLabel, or its URI
{T}{T}# for the retired codes no vocabulary labels any more (see the header)
{label('?sectionofline', 'era:solNature', 'solNatureC', 'solNatureL', 2)}
{T}{T}OPTIONAL {{ ?sectionofline era:infrastructureManager/era:roleOf/era:organisationCode ?imCode }}
{LINE}
{VALIDITY_DATES}
{T}{T}OPTIONAL {{
{T}{T}{T}?sectionofline era:hasPart ?trk .
{label('?trk', 'era:tenClassification', 'tenClassC', 'tenClassL')}
{T}{T}{T}OPTIONAL {{ ?trk era:maximumPermittedSpeed ?maxSpeed }}
{label('?trk', 'era:freightCorridor', 'freightC', 'freightL')}
{label('?trk', 'era:wheelSetGauge', 'gaugeC', 'gaugeL')}
{T}{T}{T}OPTIONAL {{
{T}{T}{T}{T}?trk era:contactLineSystem ?cls .
{label('?cls', 'era:contactLineSystemType', 'clsTypeC', 'clsTypeL', 4)}
{label('?cls', 'era:energySupplySystem', 'energyC', 'energyL', 4)}
{T}{T}{T}}}
{label('?trk', 'era:etcs/era:etcsLevelType', 'etcsTypeC', 'etcsTypeL')}
{label('?trk', 'era:gsmRVersion', 'gsmrC', 'gsmrL')}
{T}{T}}}'''
    cols = ['?sectionofline', '?sectionofline_incountry', nd('?len_', 'sectionofline_lengthofsectionofline'),
            nd('STR(?trk)', 'sectionofline_track'), nd('?imCode_', 'sectionofline_imcode'),
            nd('?line_', 'sectionofline_linenationalid_label'), nd('?solNature_', 'sectionofline_solnature')]
    for v, n in (('opStart', 'opstart'), ('opEnd', 'opend')):
        cols += [nd(f'STR(?{v}_)', f'sectionofline_{n}'), nd(f'?{v}Name_', f'sectionofline_{n}_opname'),
                 nd(f'?{v}Uopid_', f'sectionofline_{n}_uopid'), nd(f'?{v}Loc_', f'sectionofline_{n}_location'),
                 *lat_lng(f'{v}Loc_', f'sectionofline_{n}_location')]
    cols += [nd('?validFrom_', 'sectionofline_validitystartdate'), nd('?validTo_', 'sectionofline_validityenddate')]
    geoms = [ops_sub(section_geometry)]
    if section_geometry:
        cols.append(nd('?solGeom_', 'sectionofline_geometry'))
    cols += [nd('?ten_', 'sectionofline_track_tenclassification'), nd('?speed_', 'sectionofline_track_maximumpermittedspeed'),
             nd('?freight_', 'sectionofline_track_freightcorridor'), nd('?gauge_', 'sectionofline_track_wheelsetgauge'),
             nd('?cls_', 'sectionofline_track_contactlinesystem'),
             nd('?clsType_', 'sectionofline_track_contactlinesystem_contactlinesystemtype'),
             nd('?energy_', 'sectionofline_track_contactlinesystem_energysupplysystem'),
             nd('?etcs_', 'sectionofline_track_etcslevel_etcsleveltype'), nd('?gsmr_', 'sectionofline_track_gsmrversion')]
    return f'''PREFIX era:  <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>

# Outer SELECT: every empty or missing value reads "no data"
SELECT
''' + '\n'.join(T + c for c in cols) + f'''
WHERE {{
{T}{{ SELECT ?sectionofline ?sectionofline_incountry ?trk
''' + '\n'.join(T + T + a for a in aggs) + f'''
{T}WHERE {{
{where}
{T}}}
{T}GROUP BY ?sectionofline ?sectionofline_incountry ?trk }}
''' + '\n'.join(geoms) + '''
}'''


TEN = [('10', 'TENTComprehensiveNetwork'), ('20', 'TENTCoreFreightNetwork'), ('30', 'TENTCorePassengerNetwork'),
       ('40', 'OffTEN'), ('50', 'TENTExtendedCoreFreightNetwork'), ('60', 'TENTExtendedCorePassengerNetwork')]
FRC = [('10', 'RhineAlpineRFC'), ('20', 'NorthSeaMediterraneanRFC'), ('30', 'ScandinavianMediterraneanRFC'),
       ('40', 'AtlanticRFC'), ('50', 'BalticAdriaticRFC'), ('60', 'MediterraneanRFC'), ('70', 'OrientEastMedRFC'),
       ('80', 'NorthSeaBalticRFC'), ('90', 'RhineDanubeRFC'), ('100', 'AlpineWesternBalkanRFC'), ('110', 'AmberRFC')]
LVL = [('01', 'TENTCoreNetworkLevel'), ('02', 'TENTExtendedCoreNetworkLevel'), ('03', 'TENTComprehensiveNetworkLevel')]
TT = [('01', 'PassengerTraffic'), ('02', 'FreightTraffic')]
ETC = [('01', 'ScandinavianMediterraneanETC'), ('02', 'NorthSeaBalticETC'), ('03', 'MediterraneanETC'),
       ('04', 'BalticSeaAdriaticSeaETC'), ('05', 'AtlanticETC'), ('06', 'RhineDanubeETC'),
       ('07', 'BalticSeaBlackSeaAegeanSeaETC'), ('08', 'WesternBalkansEasternMediterraneanETC'),
       ('09', 'NorthSeaRhineMediterraneanETC')]
GROUPS = (('ten', 'tenc', TEN, 'TEN-T classification (era:tenClassification) - one join, six flags'),
          ('fc', 'frc', FRC, 'Rail freight corridors (era:freightCorridor) - one join, eleven flags'),
          ('lvl', 'lvl', LVL, 'TEN-T network level, via era:partOfTENT -> era:tentNetworkLevel'),
          ('tt', 'tt', TT, 'Type of traffic, via era:partOfTENT -> era:typeOfTraffic'),
          ('etc', 'etc', ETC, 'European Transport Corridors, via era:partOfTENT -> era:europeanTransportCorridor'))


def tent():
    aggs = [gc('?imCode', 'imCode_'), gc('COALESCE(?lineId, ?lpsLabel)', 'line_'),
            gc('?opStartName', 'opStartName_'), gc('?opEndName', 'opEndName_'),
            gc('?validFrom', 'validFrom_'), gc('?validTo', 'validTo_')]
    flags = []
    for var, pfx, lst, comment in GROUPS:
        aggs.append(f'# {comment}')
        for code, name in lst:
            # COALESCE: IF() on an unbound value is an error, and the flag must
            # read 0, not an empty cell
            aggs.append(f'(COALESCE(MAX(IF(?{var} = {pfx}:{code}, 1, 0)), 0) AS ?{name})')
            flags.append(f'?{name}')
    where = f'''{VALID}
{T}{T}OPTIONAL {{ ?sectionofline era:infrastructureManager/era:roleOf/era:organisationCode ?imCode }}
{LINE}
{T}{T}OPTIONAL {{ ?sectionofline era:opStart/era:opName ?opStartName }}
{T}{T}OPTIONAL {{ ?sectionofline era:opEnd/era:opName ?opEndName }}
{VALIDITY_DATES}
{T}{T}OPTIONAL {{
{T}{T}{T}?sectionofline era:hasPart ?trk .
{T}{T}{T}OPTIONAL {{ ?trk era:tenClassification ?ten }}
{T}{T}{T}OPTIONAL {{ ?trk era:freightCorridor ?fc }}
{T}{T}{T}OPTIONAL {{
{T}{T}{T}{T}?trk era:partOfTENT ?tent .
{T}{T}{T}{T}OPTIONAL {{ ?tent era:tentNetworkLevel ?lvl }}
{T}{T}{T}{T}OPTIONAL {{ ?tent era:typeOfTraffic ?tt }}
{T}{T}{T}{T}OPTIONAL {{ ?tent era:europeanTransportCorridor ?etc }}
{T}{T}{T}}}
{T}{T}}}'''
    cols = ['?sectionofline', '?sectionofline_incountry', nd('STR(?trk)', 'sectionofline_track'),
            nd('?imCode_', 'sectionofline_imcode'), nd('?line_', 'sectionofline_linenationalid_label'),
            nd('?opStartName_', 'sectionofline_opstart_opname'), nd('?opEndName_', 'sectionofline_opend_opname'),
            nd('?validFrom_', 'sectionofline_validitystartdate'), nd('?validTo_', 'sectionofline_validityenddate')] + flags
    return f'''PREFIX era:  <http://data.europa.eu/949/>
PREFIX time: <http://www.w3.org/2006/time#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX tenc: <http://data.europa.eu/949/concepts/ten-classifications/>
PREFIX frc:  <http://data.europa.eu/949/concepts/freight-corridor/>
PREFIX lvl:  <http://data.europa.eu/949/concepts/ten-t-network-levels/>
PREFIX tt:   <http://data.europa.eu/949/concepts/traffic-types/>
PREFIX etc:  <http://data.europa.eu/949/concepts/european-transport-corridors/>

# Outer SELECT: every empty or missing text value reads "no data"; the flags
# are always 0 or 1
SELECT
''' + '\n'.join(T + c for c in cols) + f'''
WHERE {{
{T}{{ SELECT ?sectionofline ?sectionofline_incountry ?trk
''' + '\n'.join(T + T + a for a in aggs) + f'''
{T}WHERE {{
{where}
{T}}}
{T}GROUP BY ?sectionofline ?sectionofline_incountry ?trk }}
}}'''




COUNTRY_EXAMPLE = '\t\t\t#FILTER(?sectionofline_incountry = <http://publications.europa.eu/resource/authority/country/FRA>)   # one country: uncomment\n'
GEOMETRY_HEADER = """# query-SoL-param1-optimised.rq plus each section's own geometry
# (sectionofline_geometry, WKT, through era:netReference like the points).
# See that file for the measurements and the reasoning; this one only adds the
# column. It repeats a section's linestring on every track row: the whole EU
# grows from 71 MB to 137 MB, and takes 114 s as one request - too close to
# the endpoint's 120 s limit. Run it one country at a time, as the exporter
# does (DEU 26 s, FRA 29 s).
#
# Endpoint: https://graph.data.era.europa.eu/repositories/rinf-plus
# Generated by scripts/build-eurostat-queries.py - edit that, not this file.

"""


def write_rq(path, query, default_header):
    path = ROOT / path
    old = path.read_text() if path.exists() else ''
    header = old[:old.index('\nPREFIX ') + 1] if '\nPREFIX ' in old else default_header
    path.write_text(header + query.replace('##FILTER##\n', COUNTRY_EXAMPLE) + '\n')


def embed(html, name, query, after=None):
    """Replace (or add) `const NAME = String.raw`...`;` - raw, so the regex
    backslashes reach the endpoint as written."""
    assert '`' not in query and '${' not in query
    block = f'const {name} = String.raw`{query}`;'
    pat = re.compile(r'const ' + name + r' = (?:String\.raw)?`.*?`;', re.S)
    if pat.search(html):
        return pat.sub(lambda m: block, html, count=1)
    m = re.search(r'const ' + after + r' = (?:String\.raw)?`.*?`;', html, re.S)
    return html[:m.end()] + '\n\n' + block + html[m.end():]


if __name__ == '__main__':
    write_rq('eurostat/query-SoL-param1-optimised.rq', sol(False), GEOMETRY_HEADER)
    write_rq('eurostat/query-SoL-param1-geometry.rq', sol(True), GEOMETRY_HEADER)
    write_rq('eurostat/tent-query-v1-optimised.rq', tent(), GEOMETRY_HEADER)
    page = ROOT / 'scripts/assets/era-eurostat-exporter.html'
    html = page.read_text()
    html = embed(html, 'QUERY_SOL', sol(False))
    html = embed(html, 'QUERY_SOL_GEOM', sol(True), after='QUERY_SOL')
    html = embed(html, 'QUERY_TENT', tent())
    page.write_text(html)
    print('wrote 3 queries to eurostat/ and', page.relative_to(ROOT))
