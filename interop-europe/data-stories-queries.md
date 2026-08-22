# RINF Data Stories Queries

Extracted from the JavaScript bundles loaded by https://rinf.data.era.europa.eu/data-stories on 2026-08-22.

Placeholders used by the app were resolved with the deployed configuration:

- `SPARQL_ENDPOINT`: `https://graph.data.era.europa.eu/repositories/rinf-plus`
- `NAMED_KG_RINF`: `http://data.europa.eu/949/graph/rinf`
- `NAMED_KG_ERATV`: `http://data.europa.eu/949/graph/eratv`
- `NAMED_KG_ERA_VOCABULARY`: `http://data.europa.eu/949/graph/ontology`
- `NAMED_KG_ERA_SKOS`: `http://data.europa.eu/949/graph/skos`
- `NAMED_KG_ERA_SHACL`: `http://data.europa.eu/949/graph/shacl`

## Visible Query Catalogue (38 queries)

### 1. operational-points-per-member-state.sparql

Provide the number of operational points loaded in the Knowledge Graph, grouped by member state.

```sparql
# Provide the number of operational points, grouped by member state.


PREFIX era: <http://data.europa.eu/949/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country (COUNT(DISTINCT ?OPCanonURI) AS ?count)
WHERE {
  ?OP a era:OperationalPoint .
  ?OP era:canonicalURI ?OPCanonURI .
  ?OP era:inCountry ?inCountry .
  ?inCountry skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
  BIND (str(?label) AS ?country)
}
GROUP BY ?country
```

### 2. sections-of-line-per-member-state.sparql

Provide the number of sections of line loaded in the Knowledge Graph, grouped by member state.

```sparql
# Provide the number of sections of line, grouped by member state.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country (COUNT(DISTINCT ?SLCanonURI) AS ?count)
WHERE {
  ?SL a era:SectionOfLine .
  ?SL era:canonicalURI ?SLCanonURI .
  ?SL era:inCountry ?inCountry .
  ?inCountry skos:prefLabel ?label .
  FILTER (lang(?label) = "en")
  BIND (str(?label) AS ?country)
}
GROUP BY ?country
```

### 3. length-of-lines-per-member-state.sparql

Provide the total length of lines loaded in the Knowledge Graph, grouped by member state.

```sparql
# Provide the total length of lines, grouped by member state.
# This query sums the length of Sections of Line that are considered currently valid.

PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX era: <http://data.europa.eu/949/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country (xsd:integer(ROUND(SUM(?length))) AS ?totalLengthKm)
WHERE {
  ?element a era:SectionOfLine .
  ?element era:lengthOfSectionOfLine ?length .
  ?element era:inCountry ?inCountry .
  OPTIONAL {
    ?element era:validityStartDate ?validityStartDate .
    ?element era:validityEndDate ?validityEndDate .
  }

  # This block determines the validity status of a record by checking if the current time (NOW())
  # falls within the optional Start and End dates provided in the data.
  # Records with no dates, or dates that cover the current date, are marked as valid for filtering.
  BIND (
      IF(!BOUND(?validityStartDate) && !BOUND(?validityEndDate), 'case1-novaliditydates',
      IF(!BOUND(?validityStartDate) && ?validityEndDate >= NOW(), 'case2-noStart-ValidEnd',
      IF(?validityStartDate <= NOW() && !BOUND(?validityEndDate), 'case3-start-NoEnd',
      IF(?validityStartDate <= NOW() && ?validityEndDate>= NOW(), 'case4-insideStartEnd',
      IF(?validityEndDate<NOW(), 'case5-notValid-past',
      IF(?validityStartDate>NOW(), 'case6-notValid-future',
      'case7-notValid')))))
    ) AS ?validityDateType_root
  )

  # Filters to include only records that are either timeless or currently within their validity period.
  FILTER (?validityDateType_root IN ('case1-novaliditydates', 'case2-noStart-ValidEnd', 'case3-start-NoEnd', 'case4-insideStartEnd'))

  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
GROUP BY ?country
```

### 4. length-of-tunnels-per-member-state.sparql

Provide the total length of tunnels loaded in the Knowledge Graph, grouped by member state.

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX era: <http://data.europa.eu/949/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

# Calculate total tunnel length per member state.
# Deduplication Logic:
# - In some cases, the same Tunnel is reported multiple times (e.g., once per track inside), 
#   sometimes even with slightly different lengths for the same physical tunnel.
# - MAX(?len) is used because if multiple length values are present for the same tunnel ID,
#   this ensures we count the most complete measurement and avoid summing duplicates.
# - MAX might not be the correct value, but its deterministic and consistent.

SELECT DISTINCT ?country (xsd:integer(ROUND(SUM(?length))) AS ?totalLengthM)
WHERE {
  {
    SELECT ?tunnelId ?inCountry (MAX(?len) AS ?length) WHERE {
      ?element a era:Tunnel .
      ?element era:lengthOfTunnel ?len .

      # Use tunnelIdentification as unique ID, fallback to label or URI if not available
      OPTIONAL { ?element era:tunnelIdentification ?id . }
      OPTIONAL { ?element rdfs:label ?label . }
      BIND(COALESCE(?id, ?label, STR(?element)) AS ?tunnelId)

      # Traverse up the hierarchy (era:isPartOf*) to find the location of the tunnel.
      # Tunnels usually don't have a direct 'era:inCountry' property; they belong to
      # Tracks, which in turn belong to Sections of Line (SoL) where the country is defined.
      ?element era:isPartOf* ?parent .
      ?parent era:inCountry ?inCountry .
    }
    GROUP BY ?tunnelId ?inCountry
  }

  # Resolve country URI to English label
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
GROUP BY ?country
```

### 5. completeness-load-capability-1.sparql

Provide a comprehensive summary of data completeness (presence and lack of presence) of core parameters applicable to running tracks per member state.

```sparql
# Due to the amount of tracks and queried properties this query will LIKELY time out!!
# Its mainly here to document the data model

# Consider using the optimized queries and limit yourself to a few countries or properties

# Provide a comprehensive summary of data completeness (Presence and Absence) 
# for core track parameters per member state.
#
# PERFORMANCE OPTIMIZATION:
# - Instead of using a slow FILTER NOT EXISTS query to find missing data,
#   this query calculates it mathematically: (Total Tracks - Present Tracks = Absent Tracks).
# - DUAL VALUES OPTIMIZATION:
#   The inner VALUES ?p block ensures the engine uses property indexes for speed,
#   while the outer block ensures a row is returned for every parameter even if counts are zero.



PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Get total tracks per country
    SELECT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)
    WHERE {
      ?track a era:RunningTrack .
      ?sectionOfLine era:hasPart ?track .
      ?sectionOfLine era:inCountry ?inCountry .
    }
    GROUP BY ?inCountry
  }

  {
    VALUES ?p {
      era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking 
      era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius 
      era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration 
      era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions 
      era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed 
      era:hasAdditionalBrakingInformation era:temperatureRange era:cantDeficiency
    }
    
  }

  # Join with property presence counts
  OPTIONAL {
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksFound)
    WHERE {
       VALUES ?p {
          era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking 
          era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius 
          era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration 
          era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions 
          era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed 
          era:hasAdditionalBrakingInformation era:temperatureRange era:cantDeficiency
       }
      ?track a era:RunningTrack .
      ?track ?p ?propertyValue .
      ?sectionOfLine era:hasPart ?track .
      ?sectionOfLine era:inCountry ?inCountry.
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numTracksFound, 0) AS ?numTracksWithPropertyAsCoreParameter)
  BIND (?numTotalTracks - ?numTracksWithPropertyAsCoreParameter AS ?numTracksWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numTracksWithPropertyAsCoreParameter) / xsd:float(?numTotalTracks)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 6. completeness-load-capability-1-v2.sparql

(Optimized Version) Comprehensive summary of data completeness for core track parameters per member state (Single-Scan Optimization).

```sparql
# This query is already optimised, but might still time out !!
# consider limiting yourself to one country or a few properties

# Provide a comprehensive summary of data completeness (Presence and Absence) 
# for core track parameters per member state.
#
# PERFORMANCE OPTIMIZATION:
# - Instead of joining two separate SELECTs for (Total Tracks) and (Found Tracks),
#   this query uses a Single-Scan Optimization to calculate both counts in a single pass.
# - HIERARCHY OPTIMIZATION:
#   Uses early-filtering combined with explicit hierarchy (?track era:isPartOf ?sol) 
#   instead of broad or reverse property path traversals.



PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTotalTracks) (COUNT(DISTINCT ?track_with_p) AS ?numFound)
    WHERE {
       VALUES ?p {
          era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking 
          era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius 
          era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration 
          era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions 
          era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed 
          era:hasAdditionalBrakingInformation era:temperatureRange era:cantDeficiency
       }
      ?track a era:RunningTrack .
      
      # Canonical path to country (RunningTrack -> SectionOfLine -> Country)
      ?track era:isPartOf ?sol .
      ?sol era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?track ?p ?propertyValue .
        BIND(?track AS ?track_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numTracksWithPropertyAsCoreParameter)
  BIND (?numTotalTracks - ?numTracksWithPropertyAsCoreParameter AS ?numTracksWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numTracksWithPropertyAsCoreParameter) / xsd:float(?numTotalTracks)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 7. track-completeness-investigator.sparql

Quick Track Data Investigator: Get exact counts and percentages for any country and property (faster response to total summary).

```sparql
# Track Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
# Setup: 
# 1. Select the country by uncommenting its URI in the first VALUES block.
# 2. Select the property by uncommenting its URI (one line) in the second VALUES block.
# you can select multiple in both sections, but expect slower runtime

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  # --- STEP 1: SELECT COUNTRY ---
  VALUES ?inCountry {
    <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
    # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
    # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
    # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
    # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
    # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
    # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
    # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
    # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
    # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
    # <http://publications.europa.eu/resource/authority/country/FRA> # France
    # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
    # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
    # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
    # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
    # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
    # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
    # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
    # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
    # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
    # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
    # <http://publications.europa.eu/resource/authority/country/POL> # Poland
    # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
    # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
    # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
    # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
    # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
  }

  # --- STEP 2: SELECT PROPERTY ---
  VALUES ?p {
    era:wheelSetGauge # 1.1.1.1.2.1-WheelSetGauge (Currently ACTIVE)
    # era:gaugingProfile # 1.1.1.1.2.2-GaugingProfile
    # era:railInclination # 1.1.1.1.2.3-RailInclination
    # era:eddyCurrentBraking # 1.1.1.1.2.4.1-EddyCurrentBraking
    # era:magneticBraking # 1.1.1.1.2.4.1.1-MagneticBraking
    # era:minimumWheelDiameter # 1.1.1.1.2.4.2-MinWheelDiameter
    # era:minimumHorizontalRadius # 1.1.1.1.2.5-MinHorizontalRadius
    # era:protectionLegacySystem # 1.1.1.1.3.1.2-ProtectionLegacySystem
    # era:legacyRadioSystem # 1.1.1.1.3.2.1-LegacyRadioSystem
    # era:maximumTrainDeceleration # 1.1.1.1.3.3-MaxTrainDeceleration
    # era:gradientProfile # 1.1.1.1.3.4-GradientProfile
    # era:hasHotAxleBoxDetector # 1.1.1.1.3.5-HotAxleBoxDetector
    # era:hasSevereWeatherConditions # 1.1.1.1.3.6-SevereWeatherConditions
    # era:trackLoadCapability # 1.1.1.1.2.4-TrackLoadCapability
    # era:maximumBrakingDistance # 1.1.1.1.2.4.3-MaxBrakeDistance
    # era:maximumPermittedSpeed # 1.1.1.1.2.4.4-MaxPermittedSpeed
    # era:hasAdditionalBrakingInformation # 1.1.1.1.2.4.5-AddBrakeInfo
    # era:temperatureRange # 1.1.1.1.4.1-TemperatureRange
    # era:cantDeficiency # 1.1.1.1.5.1-CantDeficiency
  }

  # --- STEP 3: DATA RETRIEVAL ---
  # Counts total tracks per country (RunningTrack class is used in RINF graph)
  {
    SELECT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotal)
    WHERE {
      ?track a era:RunningTrack .
      ?sectionOfLine era:hasPart ?track .
      ?sectionOfLine era:inCountry ?inCountry .
    }
    GROUP BY ?inCountry
  }

  # Counts tracks with property ?p
  OPTIONAL {
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numFound)
    WHERE {
      ?track a era:RunningTrack .
      ?track ?p ?propertyValue .
      ?sectionOfLine era:hasPart ?track .
      ?sectionOfLine era:inCountry ?inCountry.
    }
    GROUP BY ?inCountry ?p
  }

  # --- STEP 4: RESOLVE NAMES AND MATH ---
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100 AS ?percentage)

} ORDER BY ?country
```

### 8. track-completeness-investigator-v2.sparql

Quick Track Data Investigator using Single-Scan Optimization and explicit hierarchy for improved performance.

```sparql
# Track Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit hierarchy (?track era:isPartOf ?sol) which is typically faster for 
#   large datasets than broader property-path or reverse-path joins.
# - The query is designed to minimize scans on country-level properties by using early filtering 
#   in the innermost block.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTotal) (COUNT(DISTINCT ?track_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:wheelSetGauge # 1.1.1.1.2.1-WheelSetGauge (Currently ACTIVE)
         # era:gaugingProfile # 1.1.1.1.2.2-GaugingProfile
         # era:railInclination # 1.1.1.1.2.3-RailInclination
         # era:eddyCurrentBraking # 1.1.1.1.2.4.1-EddyCurrentBraking
         # era:magneticBraking # 1.1.1.1.2.4.1.1-MagneticBraking
         # era:minimumWheelDiameter # 1.1.1.1.2.4.2-MinWheelDiameter
         # era:minimumHorizontalRadius # 1.1.1.1.2.5-MinHorizontalRadius
         # era:protectionLegacySystem # 1.1.1.1.3.1.2-ProtectionLegacySystem
         # era:legacyRadioSystem # 1.1.1.1.3.2.1-LegacyRadioSystem
         # era:maximumTrainDeceleration # 1.1.1.1.3.3-MaxTrainDeceleration
         # era:gradientProfile # 1.1.1.1.3.4-GradientProfile
         # era:hasHotAxleBoxDetector # 1.1.1.1.3.5-HotAxleBoxDetector
         # era:hasSevereWeatherConditions # 1.1.1.1.3.6-SevereWeatherConditions
         # era:trackLoadCapability # 1.1.1.1.2.4-TrackLoadCapability
         # era:maximumBrakingDistance # 1.1.1.1.2.4.3-MaxBrakeDistance
         # era:maximumPermittedSpeed # 1.1.1.1.2.4.4-MaxPermittedSpeed
         # era:hasAdditionalBrakingInformation # 1.1.1.1.2.4.5-AddBrakeInfo
         # era:temperatureRange # 1.1.1.1.4.1-TemperatureRange
         # era:cantDeficiency # 1.1.1.1.5.1-CantDeficiency
       }
       
      ?track a era:RunningTrack .
      
      # Canonical path to country (RunningTrack -> SectionOfLine -> Country)
      ?track era:isPartOf ?sol .
      ?sol era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?track ?p ?propertyValue .
        BIND(?track AS ?track_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100 AS ?percentage)

} ORDER BY ?country
```

### 9. completeness-core-parameters-sol-general.sparql

Provide a comprehensive summary of Sections of Line (SoLs) property completeness per member state.

```sparql
# Provide a comprehensive summary of Sections of Line (SoL) completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Instead of joining two separate SELECTs for (Total SoLs) and (Found SoLs),
#   this query uses a Single-Scan Optimization to calculate both counts in a single pass.
# - DUAL VALUES OPTIMIZATION:
#   The inner VALUES ?p block ensures the engine uses property indexes for speed,
#   while the outer block ensures a row is returned for every parameter even if counts are zero.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalSoLs ?numSoLsWithPropertyAsCoreParameter ?numSoLsWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?sectionOfLine) AS ?numTotalSoLs) (COUNT(DISTINCT ?sol_with_p) AS ?numFound)
    WHERE {
       VALUES ?p {
          era:lengthOfSectionOfLine era:nationalLine
       }
      ?sectionOfLine a era:SectionOfLine .
      ?sectionOfLine era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?sectionOfLine ?p ?propertyValue .
        BIND(?sectionOfLine AS ?sol_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numSoLsWithPropertyAsCoreParameter)
  BIND (?numTotalSoLs - ?numSoLsWithPropertyAsCoreParameter AS ?numSoLsWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numSoLsWithPropertyAsCoreParameter) / xsd:float(?numTotalSoLs)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 10. sol-completeness-investigator.sparql

Quick SoL Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Section of Line Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit filtering in the innermost block to minimize the scan size.


PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?sectionOfLine) AS ?numTotal) (COUNT(DISTINCT ?sol_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:lengthOfSectionOfLine # 1.1.0.0.0.1-SectionOfLineLength (Currently ACTIVE)
         # era:lineReference # 1.1.1.1.1.1-LineReference
       }
       
      ?sectionOfLine a era:SectionOfLine .
      ?sectionOfLine era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?sectionOfLine ?p ?propertyValue .
        BIND(?sectionOfLine AS ?sol_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100 AS ?percentage)

} ORDER BY ?country
```

### 11. completeness-core-parameters-op-general.sparql

Provide a comprehensive summary of Operational Point (OP) property completeness per member state.

```sparql
# Provide a comprehensive summary of Operational Point (OP) completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Instead of joining two separate SELECTs for (Total OPs) and (Found OPs),
#   this query uses a Single-Scan Optimization to calculate both counts in a single pass.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?numTotalOPs ?numOPsWithNationalLine ?numOPsWithoutNationalLine
  ?completenessPercentage
WHERE {
  {
    SELECT ?inCountry (COUNT(DISTINCT ?op) AS ?numTotalOPs) (COUNT(DISTINCT ?op_with_nationalLine) AS ?numOPsWithNationalLine)
    WHERE {
      ?op a era:OperationalPoint ;
          era:inCountry ?inCountry .
      OPTIONAL {
        ?sol a era:SectionOfLine ;
             era:nationalLine ?nationalLine .
        {
          ?sol era:opStart ?op .
        }
        UNION
        {
          ?sol era:opEnd ?op .
        }
        BIND (?op AS ?op_with_nationalLine)
      }
    }
    GROUP BY ?inCountry
  }
  BIND (?numTotalOPs - ?numOPsWithNationalLine AS ?numOPsWithoutNationalLine)
  BIND (round((xsd:float(?numOPsWithNationalLine) / xsd:float(?numTotalOPs)) * 10000) / 100 AS ?completenessPercentage)
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country
```

### 12. op-completeness-investigator.sparql

Quick OP Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Operational Point Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit filtering in the innermost block to minimize the scan size.


PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?country ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry
             (COUNT(DISTINCT ?op) AS ?numTotal)
             (COUNT(DISTINCT ?op_with_nationalLine) AS ?found)
      WHERE {
        VALUES ?inCountry {
           <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
           # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
           # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
           # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
           # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
           # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
           # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
           # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
           # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
           # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
           # <http://publications.europa.eu/resource/authority/country/FRA> # France
           # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
           # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
           # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
           # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
           # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
           # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
           # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
           # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
           # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
           # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
           # <http://publications.europa.eu/resource/authority/country/POL> # Poland
           # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
           # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
           # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
           # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
           # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
        }

        ?op a era:OperationalPoint ;
            era:inCountry ?inCountry .

        OPTIONAL {
          ?sol a era:SectionOfLine ;
               era:nationalLine ?nationalLine .

          {
            ?sol era:opStart ?op .
          }
          UNION
          {
            ?sol era:opEnd ?op .
          }

          BIND(?op AS ?op_with_nationalLine)
        }
      }
      GROUP BY ?inCountry
  }

  ?inCountry skos:prefLabel ?countryLabel .
  FILTER(lang(?countryLabel) = "en")
  BIND(str(?countryLabel) AS ?country)

  BIND(?numTotal - ?found AS ?numMissing)
  BIND(ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100 AS ?percentage)
}
ORDER BY ?country
```

### 13. completeness-core-parameters-tunnel-general.sparql

Provide a comprehensive summary of Tunnel property completeness per member state.

```sparql
# Provide a comprehensive summary of Tunnel completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Mathematically calculates missing data: (Total Tunnels - Tunnels with Property = Absent Tunnels).
# - Single-Scan Optimization: Total and Found in one pass

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalTunnels ?numTunnelsWithPropertyAsCoreParameter ?numTunnelsWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?tunnel) AS ?numTotalTunnels) (COUNT(DISTINCT ?tunnel_with_p) AS ?numFound)
    WHERE {
      VALUES ?p { era:lengthOfTunnel era:rollingStockFireCategory era:tunnelIdentification }
      ?tunnel a era:Tunnel .
      
      # Canonical path to country
      ?tunnel era:isPartOf ?parent .
      ?parent era:isPartOf ?grandparent .
      ?grandparent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?tunnel ?p ?propertyValue .
        BIND(?tunnel AS ?tunnel_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numTunnelsWithPropertyAsCoreParameter)
  BIND (?numTotalTunnels - ?numTunnelsWithPropertyAsCoreParameter AS ?numTunnelsWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numTunnelsWithPropertyAsCoreParameter) / xsd:float(?numTotalTunnels)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 14. tunnel-completeness-investigator.sparql

Quick Tunnel Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Tunnel Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit hierarchy (?tunnel era:isPartOf ?parent . ?parent era:isPartOf ?grandparent)
#   which is faster for jurisdiction filtering.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?tunnel) AS ?numTotal) (COUNT(DISTINCT ?tunnel_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:lengthOfTunnel # 1.1.1.1.6.1-TunnelLength (Currently ACTIVE)
         # era:rollingStockFireCategory # 1.1.1.1.6.1.1-FireCategory
         # era:tunnelIdentification # 1.1.1.1.6.1.2-TunnelID
       }
       
      ?tunnel a era:Tunnel .
      
      # Canonical path to country
      ?tunnel era:isPartOf ?parent .
      ?parent era:isPartOf ?grandparent .
      ?grandparent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?tunnel ?p ?propertyValue .
        BIND(?tunnel AS ?tunnel_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (IF(?numTotal > 0, ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100, 0) AS ?percentage)

} ORDER BY ?country
```

### 15. completeness-core-parameters-siding-general.sparql

Provide a comprehensive summary of Siding property completeness per member state .

```sparql
# Provide a comprehensive summary of Siding completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Mathematically calculates missing data: (Total Sidings - Sidings with Property = Absent Sidings).
# - Uses single scan to find total and found sidings property counts
 
PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalSidings ?numSidingsWithPropertyAsCoreParameter ?numSidingsWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?siding) AS ?numTotalSidings) (COUNT(DISTINCT ?siding_with_p) AS ?numFound)
    WHERE {
       VALUES ?p {
          era:lengthOfSiding era:minimumHorizontalRadius
       }
      ?siding a era:Siding .
      
      # Canonical path to country
      ?siding era:isPartOf ?parent .
      ?parent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?siding ?p ?propertyValue .
        BIND(?siding AS ?siding_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numSidingsWithPropertyAsCoreParameter)
  BIND (?numTotalSidings - ?numSidingsWithPropertyAsCoreParameter AS ?numSidingsWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numSidingsWithPropertyAsCoreParameter) / xsd:float(?numTotalSidings)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 16. siding-completeness-investigator.sparql

Quick Siding Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Siding Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit hierarchy (?siding era:isPartOf ?parent) which is faster for jurisdiction filtering.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?siding) AS ?numTotal) (COUNT(DISTINCT ?siding_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:lengthOfSiding # 1.1.1.1.7.1-SidingLength (Currently ACTIVE)
         # era:minimumHorizontalRadius # 1.1.1.1.7.2-MinHorizRad
       }
       
      ?siding a era:Siding .
      
      # Canonical path to country
      ?siding era:isPartOf ?parent .
      ?parent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?siding ?p ?propertyValue .
        BIND(?siding AS ?siding_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (IF(?numTotal > 0, ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100, 0) AS ?percentage)

} ORDER BY ?country
```

### 17. completeness-core-parameters-platform-general.sparql

Provide a comprehensive summary of Platform Edge property completeness per member state.

```sparql
# Provide a comprehensive summary of Platform Edge completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Mathematically calculates missing data: (Total Platforms - Found Platforms = Absent Platforms).
# - Single-Scan Optimization: Total and Found in one pass

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalPlatforms ?numPlatformsWithPropertyAsCoreParameter ?numPlatformsWithoutPropertyAsCoreParameter ?completenessPercentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?platform) AS ?numTotalPlatforms) (COUNT(DISTINCT ?platform_with_p) AS ?numFound) 
    WHERE {
       VALUES ?p {
          era:platformId era:lengthOfPlatform era:platformHeight
       }
      ?platform a era:PlatformEdge .
      
      # Canonical path to country
      ?platform era:isPartOf ?parent .
      ?parent era:isPartOf ?grandparent .
      ?grandparent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?platform ?p ?propertyValue .
        BIND(?platform AS ?platform_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numPlatformsWithPropertyAsCoreParameter)
  BIND (?numTotalPlatforms - ?numPlatformsWithPropertyAsCoreParameter AS ?numPlatformsWithoutPropertyAsCoreParameter)
  BIND (ROUND((xsd:float(?numPlatformsWithPropertyAsCoreParameter) / xsd:float(?numTotalPlatforms)) * 10000) / 100 AS ?completenessPercentage)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 18. platform-completeness-investigator.sparql

Quick Platform Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Platform Completeness Quick-Investigator: Returns counts and percentages for a specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts and found counts in a single pass (Single-Scan Optimization).
# - It uses explicit hierarchy (?platform era:isPartOf ?parent . ?parent era:isPartOf ?grandparent)
#   which is faster for jurisdiction filtering.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotal ?found ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?platform) AS ?numTotal) (COUNT(DISTINCT ?platform_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:platformId # 1.1.1.1.8.1-PlatformID (Currently ACTIVE)
         # era:lengthOfPlatform # 1.1.1.1.8.2-PlatformLength
         # era:platformHeight # 1.1.1.1.8.3-PlatformHeight
       }
       
      ?platform a era:PlatformEdge .
      
      # Canonical path to country
      ?platform era:isPartOf ?parent .
      ?parent era:isPartOf ?grandparent .
      ?grandparent era:inCountry ?inCountry .
      
      OPTIONAL { 
        ?platform ?p ?propertyValue .
        BIND(?platform AS ?platform_with_p)
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?found)
  BIND (?numTotal - ?found AS ?numMissing)
  BIND (IF(?numTotal > 0, ROUND((xsd:float(?found) / xsd:float(?numTotal)) * 10000) / 100, 0) AS ?percentage)

} ORDER BY ?country
```

### 19. completeness-core-parameters-contactlinesystem-general.sparql

Provide a comprehensive summary of Contact Line System (CLS) property completeness per member state.

```sparql
# Provide a comprehensive summary of Contact Line System (CLS) completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Mathematically calculates missing data: (Total Tracks - Found Tracks = Absent Tracks).
# - Single-Scan Optimization: Total and Found in one pass

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalTracks ?numTracksWithCLS ?numTracksWithoutCLS ?numTracksWithPropertyOnCLS ?numTracksMissingPropertyOnCLS ?completenessPercentageOnElectrified
WHERE {
  {
    # Single-Scan Optimization: Total, Electrified, and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTotalTracks) (COUNT(DISTINCT ?track_with_cls) AS ?numTracksWithCLS) (COUNT(DISTINCT ?track_with_p) AS ?numFoundProperty)
    WHERE {
      VALUES ?p { era:energySupplySystem era:contactLineSystemType }
      ?track a era:RunningTrack .  
      
      # Canonical path to country
      ?track era:isPartOf ?parent .
      ?parent era:inCountry ?inCountry .

      OPTIONAL {
        ?track era:contactLineSystem ?cls .
        BIND(?track AS ?track_with_cls)
        OPTIONAL {
          ?cls ?p ?propertyValue .
          BIND(?track AS ?track_with_p)
        }
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (xsd:integer(?numTotalTracks) - xsd:integer(COALESCE(?numTracksWithCLS, 0)) AS ?numTracksWithoutCLS)
  BIND (COALESCE(?numFoundProperty, 0) AS ?numTracksWithPropertyOnCLS)
  BIND (xsd:integer(COALESCE(?numTracksWithCLS, 0)) - ?numTracksWithPropertyOnCLS AS ?numTracksMissingPropertyOnCLS)
  
  # Completeness % only for the electrified tracks
  BIND (IF(?numTracksWithCLS > 0, 
           ROUND((xsd:float(?numTracksWithPropertyOnCLS) / xsd:float(?numTracksWithCLS)) * 10000) / 100, 
           0) AS ?completenessPercentageOnElectrified)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 20. cls-completeness-investigator.sparql

Quick CLS Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Contact Line System (CLS) Quick-Investigator: Returns exact counts for specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts of electrified tracks and found property counts in a single pass.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotalElectrified ?numFound ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total Electrified and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track_with_cls) AS ?numTotalElectrified) (COUNT(DISTINCT ?track_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:energySupplySystem # 1.1.1.2.2.1.1-EnergySupplySystem (Currently ACTIVE)
         # era:contactLineSystemType # 1.1.1.2.2.1.2-CLSType
       }
       
      ?track a era:RunningTrack .  
      ?track era:isPartOf ?sol .
      ?sol era:inCountry ?inCountry .

      OPTIONAL {
        ?track era:contactLineSystem ?cls .
        BIND(?track AS ?track_with_cls)
        OPTIONAL {
          ?cls ?p ?propertyValue .
          BIND(?track AS ?track_with_p)
        }
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numFound)
  BIND (?numTotalElectrified - ?numFound AS ?numMissing)
  BIND (IF(?numTotalElectrified > 0, 
            ROUND((xsd:float(?numFound) / xsd:float(?numTotalElectrified)) * 10000) / 100, 
            0) AS ?percentage)

} ORDER BY ?country
```

### 21. completeness-core-parameters-traindetectionsystem-general.sparql

Provide a comprehensive summary of Train Detection System (TDS) property completeness per member state (Optimized Single-Scan Version).

```sparql
# Provide a comprehensive summary of Train Detection System (TDS) completeness.
#
# PERFORMANCE OPTIMIZATION:
# - Mathematically calculates missing data: (Total Tracks - Found Tracks = Absent Tracks).
# - Single-Scan Optimization: Total and Found in one pass

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?p ?country ?numTotalTracks ?numTracksWithTDS ?numTracksWithoutTDS ?numTracksWithPropertyOnTDS ?numTracksMissingPropertyOnTDS ?completenessPercentageOnDetected
WHERE {
  {
    # Single-Scan Optimization: Total, TDS-equipped, and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTotalTracks) (COUNT(DISTINCT ?track_with_tds) AS ?numTracksWithTDS) (COUNT(DISTINCT ?track_with_p) AS ?numFoundProperty)
    WHERE {
      VALUES ?p { era:trainDetectionSystemType }
      ?track a era:RunningTrack .  
      
      # Canonical path to country
      ?track era:isPartOf ?parent .
      ?parent era:inCountry ?inCountry .

      OPTIONAL {
        ?track era:trainDetectionSystem ?tds .
        BIND(?track AS ?track_with_tds)
        OPTIONAL {
          ?tds ?p ?propertyValue .
          BIND(?track AS ?track_with_p)
        }
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Calculations for completeness metrics
  BIND (xsd:integer(?numTotalTracks) - xsd:integer(COALESCE(?numTracksWithTDS, 0)) AS ?numTracksWithoutTDS)
  BIND (COALESCE(?numFoundProperty, 0) AS ?numTracksWithPropertyOnTDS)
  BIND (xsd:integer(COALESCE(?numTracksWithTDS, 0)) - ?numFoundProperty AS ?numTracksMissingPropertyOnTDS)
  
  # Completeness % only for the tracks with a detection system
  BIND (IF(?numTracksWithTDS > 0, 
           ROUND((xsd:float(?numFoundProperty) / xsd:float(?numTracksWithTDS)) * 10000) / 100, 
           0) AS ?completenessPercentageOnDetected)

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?country ?p
```

### 22. tds-completeness-investigator.sparql

Quick TDS Data Investigator: Get exact counts and percentages for any country and property.

```sparql
# Train Detection System (TDS) Quick-Investigator: Returns exact counts for specific country/parameter.
#
# PERFORMANCE OPTIMIZATION (Optimized Version):
# - This version calculates total counts of TDS-equipped tracks and found property counts in a single pass.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?country ?p ?numTotalDetected ?numFound ?numMissing ?percentage
WHERE {
  {
    # Single-Scan Optimization: Total TDS-equipped and Found in one pass
    SELECT ?inCountry ?p (COUNT(DISTINCT ?track_with_tds) AS ?numTotalDetected) (COUNT(DISTINCT ?track_with_p) AS ?numFound)
    WHERE {
       # --- STEP 1: SELECT COUNTRY ---
       VALUES ?inCountry {
         <http://publications.europa.eu/resource/authority/country/ESP> # Spain (Currently ACTIVE)
         # <http://publications.europa.eu/resource/authority/country/AUT> # Austria
         # <http://publications.europa.eu/resource/authority/country/BEL> # Belgium
         # <http://publications.europa.eu/resource/authority/country/BGR> # Bulgaria
         # <http://publications.europa.eu/resource/authority/country/HRV> # Croatia
         # <http://publications.europa.eu/resource/authority/country/CYP> # Cyprus
         # <http://publications.europa.eu/resource/authority/country/CZE> # Czechia
         # <http://publications.europa.eu/resource/authority/country/DNK> # Denmark
         # <http://publications.europa.eu/resource/authority/country/EST> # Estonia
         # <http://publications.europa.eu/resource/authority/country/FIN> # Finland
         # <http://publications.europa.eu/resource/authority/country/FRA> # France
         # <http://publications.europa.eu/resource/authority/country/DEU> # Germany
         # <http://publications.europa.eu/resource/authority/country/GRC> # Greece
         # <http://publications.europa.eu/resource/authority/country/HUN> # Hungary
         # <http://publications.europa.eu/resource/authority/country/IRL> # Ireland
         # <http://publications.europa.eu/resource/authority/country/ITA> # Italy
         # <http://publications.europa.eu/resource/authority/country/LVA> # Latvia
         # <http://publications.europa.eu/resource/authority/country/LTU> # Lithuania
         # <http://publications.europa.eu/resource/authority/country/LUX> # Luxembourg
         # <http://publications.europa.eu/resource/authority/country/MLT> # Malta
         # <http://publications.europa.eu/resource/authority/country/NLD> # Netherlands
         # <http://publications.europa.eu/resource/authority/country/POL> # Poland
         # <http://publications.europa.eu/resource/authority/country/PRT> # Portugal
         # <http://publications.europa.eu/resource/authority/country/ROU> # Romania
         # <http://publications.europa.eu/resource/authority/country/SVK> # Slovakia
         # <http://publications.europa.eu/resource/authority/country/SVN> # Slovenia
         # <http://publications.europa.eu/resource/authority/country/SWE> # Sweden
       }
       # --- STEP 2: SELECT PROPERTY ---
       VALUES ?p {
         era:trainDetectionSystemType # 1.1.1.2.2.4.1-TDSType
       }
       
      ?track a era:RunningTrack .  
      ?track era:isPartOf ?sol .
      ?sol era:inCountry ?inCountry .

      OPTIONAL {
        ?track era:trainDetectionSystem ?tds .
        BIND(?track AS ?track_with_tds)
        OPTIONAL {
          ?tds ?p ?propertyValue .
          BIND(?track AS ?track_with_p)
        }
      }
    }
    GROUP BY ?inCountry ?p
  }

  # Label resolution
  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)

  # Calculations for completeness metrics
  BIND (COALESCE(?numFound, 0) AS ?numFound)
  BIND (?numTotalDetected - ?numFound AS ?numMissing)
  BIND (IF(?numTotalDetected > 0, 
            ROUND((xsd:float(?numFound) / xsd:float(?numTotalDetected)) * 10000) / 100, 
            0) AS ?percentage)

} ORDER BY ?country
```

### 23. tracks-per-country-tracks-nonTSIcompliant.sparql

Number of tracks, per country, that are not TSI compliant (train detection systems).

```sparql
# Count running tracks per country where train detection systems are not TSI compliant
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:isPartOf for efficient hierarchical navigation (Track -> SectionOfLine)
# - Early filtering on era:RunningTrack type reduces candidate set
# - Single-scan pattern groups by country after filtering
#
# TSI COMPLIANCE DOCUMENTATION:
# - era:hasTSITrainDetection (RINF 1.1.1.3.4.1, 1.2.1.1.3.1): Boolean property indicating
#   if there is any train detection system installed that is fully compliant with TSI CCS
# - This is the PRIMARY and NON-DEPRECATED property for checking train detection TSI compliance
# - Value "false" means the train detection system does NOT meet TSI requirements
# - Note: Individual tsiCompliant* properties (tsiCompliantCompositeBrakeBlocks, etc.)
#   on TrainDetectionSystem are DEPRECATED per EU Regulation 2019/777 amendment

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country (COUNT(DISTINCT ?track) AS ?countTracks)
WHERE {
  # Filter running tracks with non-TSI compliant train detection
  ?track a era:RunningTrack ;
         era:hasTSITrainDetection false ;
         era:isPartOf ?sol .

  # Navigate to country and resolve human-readable label
  ?sol a era:SectionOfLine ;
       era:inCountry ?inCountry .

  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?country)
}
GROUP BY ?country
ORDER BY ?country
```

### 24. tracks-neighbouring-countries-Ukraine.sparql

Types of gauging profiles of tracks in neighbouring countries to Ukraine.

```sparql
# Find distinct gauging profiles of running tracks in countries neighbouring Ukraine
# (Hungary, Romania, Slovakia, Poland)
#
# PERFORMANCE OPTIMIZATION:
# - VALUES block at the start allows early filtering by country
# - Uses era:isPartOf for efficient hierarchical navigation (Track -> SectionOfLine)
# - Early type filtering on era:RunningTrack reduces candidate set
#
# GAUGING PROFILE DOCUMENTATION:
# - era:gaugingProfile (RINF 1.1.1.1.6.1.1): Indicates the gauging profile that applies
#   to a track, defining the maximum vehicle dimensions that can pass safely
# - This is critical for cross-border compatibility, especially with countries like
#   Ukraine which may use different track gauges (1520mm vs standard 1435mm)
# - The query shows which gauging profiles exist in Ukraine's neighboring countries
#   to assess infrastructure compatibility for trans-European corridors
# - Gauging profile URIs should follow pattern: http://data.europa.eu/949/concepts/gaugings/{code}
#   where code references specific profiles like GA, GB, GC, etc.

PREFIX era: <http://data.europa.eu/949/>
PREFIX country: <http://publications.europa.eu/resource/authority/country/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?countryName ?gaugingProfile ?gaugingProfileLabel
WHERE {
  # Define countries bordering Ukraine
  VALUES ?inCountry {country:HUN country:ROU country:SVK country:POL}

  # Navigate from country to tracks with gauging profiles
  ?track a era:RunningTrack ;
         era:isPartOf ?sol ;
         era:gaugingProfile ?gaugingProfile .

  ?sol a era:SectionOfLine ;
       era:inCountry ?inCountry .

  # Resolve human-readable labels (optional as some concepts may not have labels)
  OPTIONAL { ?gaugingProfile skos:prefLabel ?gpLabel }

  ?inCountry skos:prefLabel ?countryLabel .
  FILTER (lang(?countryLabel) = "en")
  BIND (str(?countryLabel) AS ?countryName)
  BIND (COALESCE(str(?gpLabel), REPLACE(str(?gaugingProfile), ".*/(\\d+)$", "Profile $1")) AS ?gaugingProfileLabel)
}
ORDER BY ?countryName ?gaugingProfileLabel
```

### 25. unreachable-operational-points.sparql

Identify source Operational Points (only departing tracks, unreachable by arrival).

```sparql
# Identify "SOURCE" Operational Points (only departing tracks, no arriving tracks)
# These are unreachable from the perspective that trains can only LEAVE, not ARRIVE
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for better indexing
# - FILTER NOT EXISTS patterns efficiently check absence of conditions
#
# TRACK DIRECTION DOCUMENTATION (RINF 1.1.1.0.3.1):
# - era-dir:10 = "Normal" - departure direction (from opStart to opEnd)
# - era-dir:20 = "Reverse" - arrival direction (from opEnd to opStart)
# - era-dir:30 = "Both" - bidirectional
#
# TOPOLOGY EXPLANATION:
# This query finds OPs where ALL connected tracks only allow departures:
# 1. At least one SoL starts at the OP with outgoing tracks (direction 10)
# 2. NO tracks with reverse (20) or bidirectional (30) directions in those SoLs
# 3. NO other SoLs starting from OP have incoming capability (20 or 30)
# 4. NO SoLs ending at OP have outgoing tracks that would allow arrival (10 or 30)
#
# PERFORMANCE TRICK: Using canonicalURI for consistent OP identity across relationships

PREFIX era: <http://data.europa.eu/949/>
PREFIX era-dir: <http://data.europa.eu/949/concepts/track-running-directions/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?op ?uopid ?country WHERE {
    # Main OP to be analyzed
    ?op era:canonicalURI ?opCanonUri ;
        era:inCountry ?inCountry ;
        era:uopid ?uopid .

    # Main SoL to be analyzed with tracks only departing from the start OP
    ?sol a era:SectionOfLine ;
         era:hasPart [ era:trackDirection era-dir:10 ] ;
         era:opStart ?op .

    # Condition: There are no other tracks in the main SoL with arriving directions
    FILTER NOT EXISTS {
        ?sol era:hasPart [ era:trackDirection era-dir:20 ]
    }
    FILTER NOT EXISTS {
        ?sol era:hasPart [ era:trackDirection era-dir:30 ]
    }

    # Condition: There are no SoLs also departing on the main OP with tracks having arriving directions
    FILTER NOT EXISTS {
        ?sol1 era:opStart ?op ;
              era:hasPart [ era:trackDirection era-dir:20 ]
    }
    FILTER NOT EXISTS {
        ?sol1 era:opStart ?op ;
              era:hasPart [ era:trackDirection era-dir:30 ]
    }

    # Condition: There are no other SoLs arriving on the main OP with tracks having arriving directions
    FILTER NOT EXISTS {
        ?sol2 era:opEnd ?op ;
              era:hasPart [ era:trackDirection era-dir:10 ]
    }
    FILTER NOT EXISTS {
        ?sol2 era:opEnd ?op ;
              era:hasPart [ era:trackDirection era-dir:30 ]
    }

    # Resolve human-readable country label
    ?inCountry skos:prefLabel ?countryLabel .
    FILTER (lang(?countryLabel) = "en")
    BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?op ?country
```

### 26. sink-operational-points.sparql

Identify sink Operational Points (only arriving tracks, dead-ends).

```sparql
# Identify "SINK" Operational Points (only arriving tracks, no departing tracks)
# These are dead-ends where trains can only ARRIVE, not LEAVE
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for better indexing
# - FILTER NOT EXISTS patterns efficiently check absence of conditions
#
# TRACK DIRECTION DOCUMENTATION (RINF 1.1.1.0.3.1):
# - era-dir:10 = "Normal" - departure direction (from opStart to opEnd)
# - era-dir:20 = "Reverse" - arrival direction (from opEnd to opStart)
# - era-dir:30 = "Both" - bidirectional
#
# TOPOLOGY EXPLANATION:
# This query finds OPs where ALL connected tracks only allow arrivals:
# 1. At least one connected SoL allows movement INTO the OP:
#    - opEnd with direction 10
#      OR
#    - opStart with direction 20
# 2. No connected SoL allows movement OUT OF the OP:
#    - no opStart with direction 10 or 30
#    - no opEnd with direction 20 or 30
# 3. The query is the logical inverse of "source/unreachable" operational points
#
# PERFORMANCE TRICK: Using canonicalURI for consistent OP identity across relationships

PREFIX era: <http://data.europa.eu/949/>
PREFIX era-dir: <http://data.europa.eu/949/concepts/track-running-directions/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?op ?uopid ?country WHERE {
    ?op era:inCountry ?inCountry ;
        era:uopid ?uopid .

    {
        ?sol a era:SectionOfLine ;
             era:opEnd ?op ;
             era:hasPart/era:trackDirection era-dir:10 .
    }
    UNION
    {
        ?sol a era:SectionOfLine ;
             era:opStart ?op ;
             era:hasPart/era:trackDirection era-dir:20 .
    }

    FILTER NOT EXISTS {
        ?sol1 a era:SectionOfLine ;
              era:opStart ?op ;
              era:hasPart/era:trackDirection ?dir1 .
        FILTER(?dir1 IN (era-dir:10, era-dir:30))
    }

    FILTER NOT EXISTS {
        ?sol2 a era:SectionOfLine ;
              era:opEnd ?op ;
              era:hasPart/era:trackDirection ?dir2 .
        FILTER(?dir2 IN (era-dir:20, era-dir:30))
    }

    ?inCountry skos:prefLabel ?countryLabel .
    FILTER(lang(?countryLabel) = "en")
    BIND(str(?countryLabel) AS ?country)
}
ORDER BY ?op ?country
```

### 27. disconnected-operational-points.sparql

Identify disconnected Operational Points.

```sparql
# Identify disconnected Operational Points (no connected Sections of Line)
# These are OPs that exist in the database but have no railway lines connecting to them
#
# PERFORMANCE OPTIMIZATION:
# - FILTER NOT EXISTS patterns efficiently check absence of connections
# - Border points are excluded as they may legitimately have connections only in foreign networks
#
# OPERATIONAL POINT TYPE DOCUMENTATION:
# - era-op-types:90 = Border point (excluded from this analysis)
# - Border points may appear disconnected in national data as connections exist in neighboring countries
# - era-op-types:140 = Domestic border point (also should be excluded but not in old query)
#
# TOPOLOGY EXPLANATION:
# This query identifies data quality issues where:
# 1. An OP exists but has NO SoLs ending at it (no incoming lines)
# 2. AND has NO SoLs starting from it (no outgoing lines)
# 3. This could indicate:
#    - Data entry errors (OP created but SoLs not linked)
#    - Planned infrastructure not yet connected
#    - Decommissioned infrastructure not properly removed
#
# PERFORMANCE TRICK: Using canonicalURI for consistent OP identity across relationships

PREFIX era: <http://data.europa.eu/949/>
PREFIX era-op-types: <http://data.europa.eu/949/concepts/op-types/rinf/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?op ?uopid ?country WHERE {
    # Main OP to be analyzed
    ?op era:inCountry ?inCountry ;
        era:uopid ?uopid .

    # Condition: Operational point is not a border point (may have connections in foreign networks)
    FILTER NOT EXISTS {
        ?op era:opType era-op-types:90  # International border point
    }
    FILTER NOT EXISTS {
        ?op era:opType era-op-types:140  # Domestic border point
    }

    # Condition: There are no SoLs reaching the OP (no incoming connections)
    FILTER NOT EXISTS {
        ?sol era:opEnd ?op
    }

    # Condition: There are no SoLs leaving from the OP (no outgoing connections)
    FILTER NOT EXISTS {
        ?sol era:opStart ?op
    }

    # Resolve human-readable country label
    ?inCountry skos:prefLabel ?countryLabel .
    FILTER (lang(?countryLabel) = "en")
    BIND (str(?countryLabel) AS ?country)
}
ORDER BY ?op ?country
```

### 28. ten-t-1-highSpeedLoadModelCompliance.sparql

Determine the compliance of tracks of a specific section of line, with the High Speed Load Model (HSLM) - era:highSpeedLoadModelCompliance, RINF index 1.1.1.1.2.4.2.

```sparql
# Determine the compliance of tracks with the High Speed Load Model (HSLM)
# Property: era:highSpeedLoadModelCompliance (RINF index 1.1.1.1.2.4.2)
# Documentation: https://data.europa.eu/949/highSpeedLoadModelCompliance
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Early filtering reduces the number of tracks to examine
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - The query filters by operational point names at both ends of a section
# - Case-insensitive matching is used ("i" flag in regex)

PREFIX era: <http://data.europa.eu/949/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId ?highSpeedLoadModelCompliance
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Paris-Montparnasse", "i"))
  FILTER (regex(?op_endName, "Bif 420000/553000", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get high speed load model compliance (may be absent)
  OPTIONAL {
    ?track era:highSpeedLoadModelCompliance ?highSpeedLoadModelCompliance
  }

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId
```

### 29. ten-t-2-lineReference.sparql

Classification of a specific section of line according to the INF TSI - era:lineCategory, RINF index 1.2.1.0.2.2.

```sparql
# Classification of a section of line according to the INF TSI
# Property: era:lineCategory (RINF index 1.2.1.0.2.2)
# Documentation: https://data.europa.eu/949/lineCategory
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Retrieves human-readable SKOS labels for line categories
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - The query filters by operational point names at both ends of a section
# - Case-insensitive matching is used ("i" flag in regex)
# - lineCategory is a classification according to TSI (e.g., P1, P2, P3, P4, P5, P6, F1, F2)
# - Note: A track may have multiple line categories assigned

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?lineNationalId ?op_startName ?op_endName ?track ?trackId ?lineCategory
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Dendermonde", "i"))
  FILTER (regex(?op_endName, "Zele", "i"))

  # Get the national line ID (may be absent)
  OPTIONAL { ?sol era:lineNationalId ?lineNationalId }

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get line category with human-readable label
  ?track era:lineCategory ?lineCategoryURI .
  ?lineCategoryURI skos:prefLabel ?lineCategory .
  FILTER (lang(?lineCategory) = "en")

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId ?lineCategory
```

### 30. ten-t-3-numberofTracks.sparql

Number of tracks for a specific section of line.

```sparql
# Number of tracks for a specific section of line
# Filters tracks based on their validity dates to count only currently valid tracks
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Early filtering reduces the number of tracks to examine
# - Validity date filtering ensures only currently applicable tracks are counted
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - The query filters by operational point names at both ends of a section
# - Case-insensitive matching is used ("i" flag in regex)
# - Only counts tracks that are currently valid (based on validityStartDate and validityEndDate)

PREFIX era: <http://data.europa.eu/949/>

SELECT (COUNT(DISTINCT ?track) AS ?tracks)
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Dendermonde", "i"))
  FILTER (regex(?op_endName, "Zele", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .

  # Check validity dates
  OPTIONAL {
    ?track era:validityStartDate ?validityStartDate .
    ?track era:validityEndDate ?validityEndDate .
  }

  # Classify validity status
  BIND (
    COALESCE(
      IF(!BOUND(?validityStartDate) && !BOUND(?validityEndDate), 'case1-novaliditydates',
      IF(!BOUND(?validityStartDate) && ?validityEndDate >= NOW(), 'case2-noStart-ValidEnd',
      IF(?validityStartDate <= NOW() && !BOUND(?validityEndDate), 'case3-start-NoEnd',
      IF(?validityStartDate <= NOW() && ?validityEndDate >= NOW(), 'case4-insideStartEnd',
      IF(?validityEndDate < NOW(), 'case5-notValid-past',
      IF(?validityStartDate > NOW(), 'case6-notValid-future',
      'case7-notValid'))))))
    ) AS ?validityDateType
  )

  # Filter to include only currently valid tracks
  FILTER (?validityDateType IN ('case1-novaliditydates', 'case2-noStart-ValidEnd', 'case3-start-NoEnd', 'case4-insideStartEnd'))
}
```

### 31. ten-t-4-contactlinesystems.sparql

Type of contact line systems of the tracks in a specific section of line.

```sparql
# Type of contact line systems of the tracks in a specific section of line
# Property: era:contactLineSystemType (RINF index 1.1.1.2.2.2)
# Documentation: https://data.europa.eu/949/contactLineSystemType
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Retrieves human-readable SKOS labels for contact line system types
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - A track may have multiple contact line systems (e.g., for different sections or configurations)

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId ?clstype
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Dendermonde", "i"))
  FILTER (regex(?op_endName, "Zele", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get contact line system and its type with human-readable label
  ?track era:contactLineSystem ?cls .
  ?cls era:contactLineSystemType ?clstypeURI .
  ?clstypeURI skos:prefLabel ?clstype .
  FILTER (lang(?clstype) = "en")

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId ?clstype
```

### 32. ten-t-5-wheelSetGauge.sparql

Wheel set gauge of the tracks in a specific section of line.

```sparql
# Wheel set gauge of the tracks in a specific section of line
# Property: era:wheelSetGauge (RINF index 1.2.1.0.3.1)
# Documentation: https://data.europa.eu/949/wheelSetGauge
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Retrieves human-readable SKOS labels for wheel set gauge types
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - Wheel set gauge defines the nominal distance between the running faces of the rails
# - Common values include 1435mm (standard gauge), 1520mm, 1668mm, etc.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId ?wheelSetGauge
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Paris-Montparnasse", "i"))
  FILTER (regex(?op_endName, "Bif 420000/553000", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get wheel set gauge with human-readable label
  ?track era:wheelSetGauge ?wheelSetGaugeURI .
  ?wheelSetGaugeURI skos:prefLabel ?wheelSetGauge .
  FILTER (lang(?wheelSetGauge) = "en")

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId ?wheelSetGauge
```

### 33. ten-t-6-energySupplySystem.sparql

Energy supply system associated to the tracks in a specific section of line.

```sparql
# Energy supply system associated to the tracks in a specific section of line
# Property: era:energySupplySystem (RINF index 1.1.1.2.2.3)
# Documentation: https://data.europa.eu/949/energySupplySystem
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Retrieves human-readable SKOS labels for energy supply systems
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - Energy supply system is accessed through the contact line system
# - Common values include AC 25kV 50Hz, DC 3kV, DC 1.5kV, AC 15kV 16.7Hz, etc.

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId ?energySupplySystem
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Dendermonde", "i"))
  FILTER (regex(?op_endName, "Zele", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get energy supply system through contact line system with human-readable label
  ?track era:contactLineSystem ?cls .
  ?cls era:energySupplySystem ?energySupplySystemURI .
  ?energySupplySystemURI skos:prefLabel ?energySupplySystem .
  FILTER (lang(?energySupplySystem) = "en")

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId ?energySupplySystem
```

### 34. ten-t-comprehensive-section-properties.sparql

Comprehensive query demonstrating multiple track properties: wheel set gauge, contact line system type, energy supply system, GSM-R version, maximum permitted speed, ETCS level type and baseline.

```sparql
# Comprehensive query: Multiple track properties for a specific section of line
# This query demonstrates how to retrieve various track properties in a single query
# Properties included:
# - era:wheelSetGauge (RINF 1.2.1.0.3.1): Nominal track gauge
# - era:contactLineSystemType (RINF 1.1.1.2.2.2): Type of contact line system
# - era:energySupplySystem (RINF 1.1.1.2.2.3): Energy supply system (via contact line system)
# - era:gsmRVersion (RINF 1.1.1.3.7.1): GSM-R version installed
# - era:maximumPermittedSpeed (RINF 1.2.1.0.4.1): Maximum permitted speed
# - era:etcsLevelType (RINF 1.1.1.3.2.3): ETCS level type
# - era:etcsBaseline (RINF 1.1.1.3.2.4): ETCS baseline version
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - All complex properties are OPTIONAL to handle incomplete data gracefully
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - This query pattern is efficient for getting multiple properties in one request
# - SKOS labels are retrieved with English language filter for human readability

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId
  ?wheelSetGauge ?contactLineSystemType ?energySupplySystem
  ?gsmRVersion ?maximumPermittedSpeed ?etcsLevelType ?etcsBaseline
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Dendermonde", "i"))
  FILTER (regex(?op_endName, "Zele", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Wheel set gauge (nominal track gauge)
  OPTIONAL {
    ?track era:wheelSetGauge ?wheelSetGaugeURI .
    ?wheelSetGaugeURI skos:prefLabel ?wheelSetGauge .
    FILTER (lang(?wheelSetGauge) = "en")
  }

  # Contact line system type and energy supply system
  OPTIONAL {
    ?track era:contactLineSystem ?cls .
    OPTIONAL {
      ?cls era:contactLineSystemType ?clsTypeURI .
      ?clsTypeURI skos:prefLabel ?contactLineSystemType .
      FILTER (lang(?contactLineSystemType) = "en")
    }
    OPTIONAL {
      ?cls era:energySupplySystem ?essURI .
      ?essURI skos:prefLabel ?energySupplySystem .
      FILTER (lang(?energySupplySystem) = "en")
    }
  }

  # GSM-R version
  OPTIONAL {
    ?track era:gsmRVersion ?gsmRVersionURI .
    ?gsmRVersionURI skos:prefLabel ?gsmRVersion .
    FILTER (lang(?gsmRVersion) = "en")
  }

  # Maximum permitted speed (literal value)
  OPTIONAL {
    ?track era:maximumPermittedSpeed ?maximumPermittedSpeed .
  }

  # ETCS level type and baseline
  OPTIONAL {
    ?track era:etcsLevel ?etcsLevelObj .
    OPTIONAL {
      ?etcsLevelObj era:etcsLevelType ?etcsLevelTypeURI .
      ?etcsLevelTypeURI skos:prefLabel ?etcsLevelType .
      FILTER (lang(?etcsLevelType) = "en")
    }
    OPTIONAL {
      ?etcsLevelObj era:etcsBaseline ?etcsBaselineURI .
      ?etcsBaselineURI skos:prefLabel ?etcsBaseline .
      FILTER (lang(?etcsBaseline) = "en")
    }
  }

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId
```

### 35. ten-t-9-gaugingCheckLocation.sparql

Location of particular points requiring specific checks due to deviations from gauging, for tracks in a specific section of line.

```sparql
# Location of particular points requiring specific checks due to deviations from gauging
# Property: era:gaugingCheckLocation (RINF index 1.2.1.0.3.3)
# Documentation: https://data.europa.eu/949/gaugingCheckLocation
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - gaugingCheckLocation is a string value describing the location
# - This property may not be present if no gauging deviations exist on the track

PREFIX era: <http://data.europa.eu/949/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId ?gaugingCheckLocation
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Hintergasse", "i"))
  FILTER (regex(?op_endName, "Braz", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Get gauging check location (optional - may not exist)
  OPTIONAL {
    ?track era:gaugingCheckLocation ?gaugingCheckLocation .
  }

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId
```

### 36. ten-t-11-etcsBaselineAndLevel.sparql

If ETCS in operation, fill in parameters ETCS Baseline and ETCS Level, for tracks in a specific section of line.

```sparql
# Combined query: ETCS Baseline and Level together
# Properties: era:etcsBaseline (RINF 1.1.1.3.2.4) and era:etcsLevelType (RINF 1.1.1.3.2.3)
# Documentation: https://data.europa.eu/949/etcsBaseline, https://data.europa.eu/949/etcsLevelType
#
# PERFORMANCE OPTIMIZATION:
# - Uses era:hasPart instead of deprecated era:track for efficient hierarchy navigation
# - Uses era:opStart/opEnd directly without canonicalURI indirection
# - Filters on specific operational points to limit the search space
# - Retrieves both ETCS baseline and level type in a single query
#
# USAGE NOTE:
# - Modify the FILTER regex patterns to search for different sections of line
# - Case-insensitive matching is used ("i" flag in regex)
# - This query demonstrates accessing multiple properties of the same nested object (etcsLevel)
# - ETCS (European Train Control System) baseline and level are related: level indicates
#   the operating relationship between track and train, baseline is the software version
# - Both properties are accessed through the era:etcsLevel object

PREFIX era: <http://data.europa.eu/949/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?sol ?solLabel ?op_startName ?op_endName ?track ?trackId
  ?etcsLevelType ?etcsBaseline ?highSpeedLoadModelCompliance
WHERE {
  # Find section of line
  ?sol a era:SectionOfLine .

  # Navigate to start and end operational points
  ?sol era:opStart ?op_start .
  ?op_start era:opName ?op_startName .

  ?sol era:opEnd ?op_end .
  ?op_end era:opName ?op_endName .

  # Filter for specific section (modify these patterns as needed)
  FILTER (regex(?op_startName, "Paris-Montparnasse", "i"))
  FILTER (regex(?op_endName, "Bif 420000/553000", "i"))

  # Get tracks that are part of this section
  ?sol era:hasPart ?track .
  ?track era:trackId ?trackId .

  # Optional: High speed load model compliance (included as related property)
  OPTIONAL {
    ?track era:highSpeedLoadModelCompliance ?highSpeedLoadModelCompliance .
  }

  # Optional: ETCS level with baseline and type
  # Both properties are accessed through the same etcsLevel object
  OPTIONAL {
    ?track era:etcsLevel ?etcsLevelObj .

    # Get ETCS baseline version
    OPTIONAL {
      ?etcsLevelObj era:etcsBaseline ?etcsBaselineURI .
      ?etcsBaselineURI skos:prefLabel ?etcsBaseline .
      FILTER (lang(?etcsBaseline) = "en")
    }

    # Get ETCS level type
    OPTIONAL {
      ?etcsLevelObj era:etcsLevelType ?etcsLevelTypeURI .
      ?etcsLevelTypeURI skos:prefLabel ?etcsLevelType .
      FILTER (lang(?etcsLevelType) = "en")
    }
  }

  # Optional: Get section label if available
  OPTIONAL { ?sol rdfs:label ?solLabel }
}
ORDER BY ?trackId
```

### 37. track_rinf_properties_with_location.sparql

RINF properties for Tracks with location data.

```sparql
# This query lists Track names, Start and End Positions in terms of Kilometer Posts on lines
# and properties that are relevant to rcc calculations
#
# In the query UI you can set the output format to CSV, for better excel import of the result
#
# Possible 3-letter country codes:
# AUT, BEL, BGR, HRV, CZE, DNK, EST, FIN, FRA, DEU, GRC, HUN, ITA, LVA,
# LTU, LUX, NLD, NOR, POL, PRT, ROU, SVK, SVN, ESP, SWE, CHE, GBR, IRL
#
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX era: <http://data.europa.eu/949/>
PREFIX eu-pub-country: <http://publications.europa.eu/resource/authority/country/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country ?line ?sol ?startPosition ?endPosition ?trackName ?rinfIndex ?parameterLabel (GROUP_CONCAT(DISTINCT ?fullValue; separator=" | ") as ?group)
WHERE {

  ###############################################
  #                                             #
  #   Section of values you might want to edit  #
  #                                             #
  ###############################################

  # Provide here a list of properties you are interested in, if you comment out the line,
  # All rcc relevant properties will be listed
  VALUES ?rinfIndex {"1.1.1.1.3.1.1"}

  # Which countries are you interested in
  # If you provide line names its strictly not necesssary, but will greatly improve performance
  VALUES ?country { eu-pub-country:FRA eu-pub-country:BEL }

  # What lines do you want to see, omit if you want all of them (this could be slow though)
  VALUES ?line {"830000-1"}

  # you can limit which part you want to have info on, makes really only sense when you have one line
  # comment it out for the whole line
  FILTER (?endKp < 500)
  FILTER (?startKp > 300)

  ##############################################
  #                                            #
  #      FYI, edit on your own peril           #
  #                                            #
  ##############################################

  ?sol a era:SectionOfLine;
  	era:inCountry ?country;
    era:nationalLine/era:lineId ?line;

    era:netReference/era:startsAt/era:hasLrsCoordinate [
        era:kmPost/era:kilometer ?startKp;
        era:offsetFromKilometricPost ?startOffset
    ] ;

    era:netReference/era:endsAt/era:hasLrsCoordinate [
        era:kmPost/era:kilometer ?endKp;
        era:offsetFromKilometricPost ?endOffset
    ].

    bind (concat(str(?startKp), "+", str(?startOffset)) as ?startPosition)
    bind (concat(str(?endKp), "+", str(?endOffset)) as ?endPosition)

  ?track era:isPartOf ?sol;
    rdfs:label ?trackName;
    ?parameter ?value.

  ?parameter era:rinfIndex ?rinfIndex;
    rdfs:label ?parameterLabel;

    # if you comment out this, all parameters of tracks will be listed, not just rcc relevant ones
    era:usedInRCCCalculations "true"^^xsd:boolean.


  bind (concat(?parameterLabel, " (", ?rinfIndex, ")") as ?parameterLabelCombined)

  # SectionOfLine related properties start with 1.1
  filter(strStarts(?rinfIndex, "1.1"))

  # values that are IRIs are not very readable, here we resolve them if possible
  # to readable labels

  optional {?value skos:prefLabel ?skosValue }
  optional {?value rdfs:label ?labelValue }

  bind(coalesce(?skosValue, ?labelValue, ?value) as ?fullValue)
}

# this groups multi valued properties into one group
group by ?country ?line ?sol ?startPosition ?endPosition ?trackName ?rinfIndex ?parameterLabel
```

### 38. op_rinf_properties_with_location.sparql

RINF properties for Operational Points with location data.

```sparql
# This query lists Operational Point (OP) names, their identifiers, railway locations,
# and properties that are relevant for RINF calculations, including location on lines.
#
# In the query UI you can set the output format to CSV, for better excel import of the result
#
# Possible 3-letter country codes:
# AUT, BEL, BGR, HRV, CZE, DNK, EST, FIN, FRA, DEU, GRC, HUN, ITA, LVA,
# LTU, LUX, NLD, NOR, POL, PRT, ROU, SVK, SVN, ESP, SWE, CHE, GBR, IRL
#
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX wgs: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX era: <http://data.europa.eu/949/>
PREFIX eu-pub-country: <http://publications.europa.eu/resource/authority/country/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT DISTINCT ?country ?op ?opid ?opName ?railwayLocation ?line ?trackName ?type ?rinfIndex ?parameterLabel (GROUP_CONCAT(DISTINCT ?fullValue; separator=" | ") as ?group)
WHERE {

  ###############################################
  #                                             #
  #   Section of values you might want to edit  #
  #                                             #
  ###############################################

  # Provide here a list of properties you are interested in, if you comment out the line,
  # all RCC relevant properties will be listed
  #VALUES ?rinfIndex {"1.1.1.1.3.1.1"}

  # Which countries are you interested in
  VALUES ?country { eu-pub-country:FRA eu-pub-country:BEL }

  # What lines do you want to see, omit if you want all of them (this could be slow though)
  VALUES ?line {"830000-1"}

  # What type of track do you want to query(you can omit one if you want, but not both ) 
  VALUES ?type { era:RunningTrack era:Siding}

  # You can limit which part you want to have info on, makes really only sense when you have one line
  # comment it out for the whole line
  FILTER (?startKp < 500)
  FILTER (?startKp > 300)

  ##############################################
  #                                            #
  #      FYI, edit on your own peril           #
  #                                            #
  ##############################################

  ?op a era:OperationalPoint;
    era:inCountry ?country;
    era:opName ?opName;
    era:uopid ?opid;

    era:netReference/era:hasLrsCoordinate [
      era:kmPost [
        era:kilometer ?startKp;
        era:hasLRS/era:lineId ?line
      ];
      era:offsetFromKilometricPost ?startOffset
    ].

  bind (concat(str(?startKp), "+", str(?startOffset)) as ?railwayLocation)

  ?track a ?type;
    era:isPartOf ?op;
    rdfs:label ?trackName;
    ?parameter ?value.

  ?parameter era:rinfIndex ?rinfIndex;
    rdfs:label ?parameterLabel;

    # if you comment out this, all parameters of tracks will be listed, not just RCC relevant ones
    era:usedInRCCCalculations "true"^^xsd:boolean.

  bind (concat(?parameterLabel, " (", ?rinfIndex, ")") as ?parameterLabelCombined)

  # OperationalPoint related properties start with 1.2
  filter(strStarts(?rinfIndex, "1.2"))

  # Values that are IRIs are not very readable, here we resolve them if possible
  # to readable labels

  optional { ?value skos:prefLabel ?skosValue }
  optional { ?value rdfs:label ?labelValue }

  bind(coalesce(?skosValue, ?labelValue, ?value) as ?fullValue)
}

# This groups multi-valued properties into one group per OP/Track/Parameter combination
group by ?country ?op ?opid ?opName ?railwayLocation ?line ?trackName ?type ?rinfIndex ?parameterLabel
```


## SPARQL Notebooks (3 files)

### Notebook 1. completeness.sparqlbook

Notebook aggregating queries for checking the completeness of parameters per country.

```sparql
[
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Auxiliar query to retrieve core parameters elements"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?Class ?p\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> \n{VALUES ?p {era:trackLoadCapability era:loadCapabilityLineCategory era:loadCapabilitySpeed era:maximumPermittedSpeed era:hasSevereWeatherConditions era:gaugingProfile era:gradientProfile era:minimumHorizontalRadius era:wheelSetGauge era:railInclination era:minimumWheelDiameter era:maximumTrainDeceleration era:eddyCurrentBraking era:magneticBraking era:hasHotAxleBoxDetector era:cantDeficiency era:contactLineSystemType era:energySupplySystem era:rollingStockFireCategory era:protectionLegacySystem era:legacyRadioSystem era:trainDetectionSystemType era:maximumBrakingDistance era:hasAdditionalBrakingInformation era:lineReference era:gaugingProfile era:length era:platformHeight era:temperatureRange era:geographicalLocationOperationalPoint era:gaugingProfile} \n  ?xx a ?Class .  \n  ?xx ?p ?value\n  }\n} ORDER BY ?Class"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Contact line system details in Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?track ?cls ?p #?rinfIndex  \nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:energySupplySystem era:contactLineSystemType}\n  ?track a era:Track .  \n  ?track era:contactLineSystem ?cls .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?cls ?p ?propertyValue .}\n  }\n} ORDER BY ?track ?cls LIMIT 1000 "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Contact line system details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:energySupplySystem era:contactLineSystemType}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:energySupplySystem era:contactLineSystemType}\n  ?track a era:Track .  \n  ?track era:contactLineSystem ?cls .\n  ?cls ?p ?propertyValue .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:energySupplySystem era:contactLineSystemType}\n  ?track a era:Track .  \n  ?track era:contactLineSystem ?cls .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?cls ?p ?propertyValue .}\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Operational point details in Spain (no results)"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?entity ?p ?rinfIndex  \nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:lineReference}\n  ?entity a era:OperationalPoint .\n  ?entity era:inCountry ?inCountry .\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?entity ?p ?propertyValue}\n  }\n} ORDER BY ?entity LIMIT 1000 \n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Operational point details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalEntities ?numEntitiesWithPropertyAsCoreParameter ?numEntitiesWithoutPropertyAsCoreParameter\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:lineReference}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?entity) AS ?numTotalEntities)\nWHERE {\n  ?entity a era:OperationalPoint .\n  ?entity era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:lineReference}\n  ?entity a era:OperationalPoint .\n  ?entity era:inCountry ?inCountry .\n  ?entity ?p ?propertyValue .\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:lineReference}\n  ?entity a era:OperationalPoint .\n  ?entity era:inCountry ?inCountry .\n  FILTER NOT EXISTS {?entity ?p ?propertyValue }\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Platform details in Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?entity ?p ?rinfIndex  \nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:platformId era:length era:platformHeight}\n  ?entity a era:Platform .\n  ?track a era:Track.\n  ?track era:platform ?entity .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine era:inCountry ?inCountry .\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?entity ?p ?propertyValue}\n  }\n} ORDER BY ?entity LIMIT 1000 \n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Platform details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nSELECT DISTINCT ?p ?inCountry ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:platformId era:length era:platformHeight}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?entity a era:Platform .\n  ?track a era:Track.\n  ?track era:platform ?entity .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine era:inCountry ?inCountry  \n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:platformId era:length era:platformHeight}\n  ?entity a era:Platform .\n  ?track a era:Track.\n  ?track era:platform ?entity .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine era:inCountry ?inCountry  .\n  ?entity ?p ?propertyValue .\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:platformId era:length era:platformHeight}\n  ?entity a era:Platform .\n  ?track a era:Track.\n  ?track era:platform ?entity .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine era:inCountry ?inCountry  \n  FILTER NOT EXISTS {?entity ?p ?propertyValue .}\n} \n}\n}\n} ORDER BY ?p ?inCountry"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Siding details for Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?entity ?p ?rinfIndex  \nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:length era:minimumHorizontalRadius}\n  ?entity a era:Siding .\n  ?op a era:OperationalPoint .\n  ?op era:siding ?entity .\n  ?op era:inCountry ?inCountry .\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?entity ?p ?propertyValue}\n  }\n} ORDER BY ?entity LIMIT 1000 \n "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Siding details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalEntities ?numEntitiesWithPropertyAsCoreParameter ?numEntitiesWithoutPropertyAsCoreParameter\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:length era:minimumHorizontalRadius}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?entity) AS ?numTotalEntities)\nWHERE {\n  ?entity a era:Siding .\n  ?op a era:OperationalPoint .\n  ?op era:siding ?entity .\n  ?op era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:length era:minimumHorizontalRadius}\n  ?entity a era:Siding .\n  ?entity ?p ?propertyValue .\n  ?op a era:OperationalPoint .\n  ?op era:siding ?entity .\n  ?op era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:length era:minimumHorizontalRadius}\n  ?entity a era:Siding .\n  ?op a era:OperationalPoint .\n  ?op era:siding ?entity .\n  ?op era:inCountry ?inCountry\n  FILTER NOT EXISTS {?entity ?p ?propertyValue }\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Section of line details for Spain (no results)"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?sectionOfLine ?p ?rinfIndex  \nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:length}\n  ?sectionOfLine a era:SectionOfLine .  \n  ?sectionOfLine era:inCountry ?inCountry.\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex}\n  FILTER NOT EXISTS {?sectionOfLine ?p ?propertyValue }\n  }\n} ORDER BY ?sectionOfLine LIMIT 1000 "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Section of line details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalSOLs ?numSOLsWithPropertyAsCoreParameter ?numSOLsWithoutPropertyAsCoreParameter\nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:length}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?sectionOfLine) AS ?numTotalSOLs)\nWHERE {\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?sectionOfLine) AS ?numSOLsWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:length}\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine ?p ?propertyValue .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?sectionOfLine) AS ?numSOLsWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:length}\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?sectionOfLine ?p ?propertyValue . VALUES ?p {era:length}}\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Tracks details for Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?track ?p #?rinfIndex  \nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed era:hasAdditionalBrakingInformation era:minimumTemperature era:maximumTemperature era:cantDefficiency}\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?track ?p ?propertyValue .}\n  }\n} ORDER BY ?track LIMIT 1000 "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Tracks details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed era:hasAdditionalBrakingInformation era:minimumTemperature era:maximumTemperature era:cantDefficiency}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed era:hasAdditionalBrakingInformation era:minimumTemperature era:maximumTemperature era:cantDefficiency}\n  ?track a era:Track .  \n  ?track ?p ?propertyValue .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:wheelSetGauge era:gaugingProfile era:railInclination era:eddyCurrentBraking era:magneticBraking era:minimumWheelDiameter era:minimumHorizontalRadius era:protectionLegacySystem era:legacyRadioSystem era:maximumTrainDeceleration era:gradientProfile era:hasHotAxleBoxDetector era:hasSevereWeatherConditions era:trackLoadCapability era:maximumBrakingDistance era:maximumPermittedSpeed era:hasAdditionalBrakingInformation era:minimumTemperature era:maximumTemperature era:cantDefficiency}\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?track ?p ?propertyValue .}\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Train detection system details for Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?track ?tds ?p #?rinfIndex  \nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:trainDetectionSystemType}\n  ?track a era:Track .  \n  ?track era:trainDetectionSystem ?tds .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?tds ?p ?propertyValue .}\n  }\n} ORDER BY ?track ?tds LIMIT 1000 "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Train detection system details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalTracks ?numTracksWithPropertyAsCoreParameter ?numTracksWithoutPropertyAsCoreParameter\nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:trainDetectionSystemType}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:trainDetectionSystemType}\n  ?track a era:Track .  \n  ?track era:trainDetectionSystem ?tds .\n  ?tds ?p ?propertyValue .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?track) AS ?numTracksWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:trainDetectionSystemType}\n  ?track a era:Track .  \n  ?track era:trainDetectionSystem ?tds .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?tds ?p ?propertyValue .}\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Tunnels details for Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?entity ?p ?rinfIndex  \nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  VALUES ?p {era:length era:rollingStockFireCategory era:tunnelIdentification}\n  ?entity a era:Tunnel .\n  ?entity era:inCountry ?inCountry.\n  GRAPH <http://data.europa.eu/949/graph/ontology> {?p era:rinfIndex ?rinfIndex} .\n  FILTER NOT EXISTS {?entity ?p ?propertyValue }\n  }\n} ORDER BY ?entity LIMIT 1000 "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness core parameters - Tunnels details in general"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?p ?inCountry ?numTotalEntities ?numEntitiesWithPropertyAsCoreParameter ?numEntitiesWithoutPropertyAsCoreParameter\nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?p {era:length era:rollingStockFireCategory era:tunnelIdentification}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?entity) AS ?numTotalEntities)\nWHERE {\n  ?entity a era:Tunnel .\n  ?entity era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithPropertyAsCoreParameter)\nWHERE {\n  VALUES ?p {era:length era:rollingStockFireCategory era:tunnelIdentification}\n  ?entity a era:Tunnel .\n  ?entity ?p ?propertyValue .\n  ?entity era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry ?p (COUNT(DISTINCT ?entity) AS ?numEntitiesWithoutPropertyAsCoreParameter) \nWHERE {\n  VALUES ?p {era:length era:rollingStockFireCategory era:tunnelIdentification}\n  ?entity a era:Tunnel .\n  ?entity era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?entity ?p ?propertyValue }\n} \n}\n}\n} ORDER BY ?p ?inCountry "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness load capabilities - Query 1"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?inCountry ?numTotalTracks ?numTracksWithLoadCapability ?numTracksWithoutLoadCapability\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTracksWithLoadCapability)\nWHERE {\n  ?track a era:Track .  \n  ?track era:trackLoadCapability ?loadCapability .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n} OPTIONAL\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTracksWithoutLoadCapability) \nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?track era:trackLoadCapability ?loadCapability .}\n} \n}\n}\n}\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness load capabilities - Query 2 all completed"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?inCountry ?numTotalTracks ?numTracksWithLoadCapability ?numTracksWithoutLoadCapability\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTracksWithLoadCapability)\nWHERE {\n  ?track a era:Track .  \n  ?track era:trackLoadCapability ?loadCapability .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n}\nFILTER (?numTotalTracks = ?numTracksWithLoadCapability)\nBIND(0 AS ?numTracksWithoutLoadCapability)\n}\n}\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness load capabilities - Query 2 all missing"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?inCountry ?numTotalTracks ?numTracksWithLoadCapability ?numTracksWithoutLoadCapability\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTotalTracks)\nWHERE {\n  ?track a era:Track .  \n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n}\n{\nSELECT DISTINCT ?inCountry (COUNT(DISTINCT ?track) AS ?numTracksWithoutLoadCapability)\nWHERE {\n  ?track a era:Track .  \n  FILTER NOT EXISTS {?track era:trackLoadCapability ?loadcapability} .\n  ?sectionOfLine era:track ?track .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n} \n}\nBIND(0 AS ?numTracksWithLoadCapability)\n}\n}\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Completeness load capabilities - Details for Spain"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?inCountry ?sectionOfLine ?trackWithoutLoadCapability\nWHERE {\n  GRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?inCountry {<http://publications.europa.eu/resource/authority/country/ESP>} .\n  ?trackWithoutLoadCapability a era:Track .  \n  ?sectionOfLine era:track ?trackWithoutLoadCapability .\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?inCountry.\n  FILTER NOT EXISTS {?trackWithoutLoadCapability era:trackLoadCapability ?loadcapability .}\n  }\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Length of lines per member state and type"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT ?id ?inCountry ?y ?totalLengthKm WHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{SELECT DISTINCT ?inCountry ?y (round(xsd:decimal(SUM(?length)/1000)) AS ?totalLengthKm)\nWHERE {\n  ?element a ?y .\n  ?element era:length ?length .\n  ?element era:inCountry ?inCountry.\n}}\nSERVICE <http://publications.europa.eu/webapi/rdf/sparql>{\n      ?inCountry dc:identifier ?id}\n      }\n}\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Length of lines per member state - Only sections of line"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX era: <http://data.europa.eu/949/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT ?id ?inCountry ?totalLengthKm {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{SELECT DISTINCT ?inCountry (round(xsd:decimal(SUM(?length)/1000)) AS ?totalLengthKm)\nWHERE {\n  ?element a era:SectionOfLine .\n  ?element era:length ?length .\n  ?element era:inCountry ?inCountry.\n}}\nSERVICE <http://publications.europa.eu/webapi/rdf/sparql>{\n      ?inCountry dc:identifier ?id}\n      }\n}\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Length of lines per member state"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX era: <http://data.europa.eu/949/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\nPREFIX xsd:<http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT ?id ?inCountry ?totalLengthKm {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{SELECT DISTINCT ?inCountry (round(xsd:decimal(SUM(?length)/1000)) AS ?totalLengthKm)\nWHERE {\n  ?element a ?y .  # currently includes sections of line and tunnels\n  ?element era:length ?length .\n  ?element era:inCountry ?inCountry.\n}}\nSERVICE <http://publications.europa.eu/webapi/rdf/sparql>{\n      ?inCountry dc:identifier ?id}\n      }\n}\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Operational points per member state"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX era: <http://data.europa.eu/949/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\n\nSELECT DISTINCT ?id ?inCountry ?count\nWHERE{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{SELECT DISTINCT ?inCountry (COUNT(DISTINCT ?OP) AS ?count)\nFROM <http://data.europa.eu/949/graph/rinf>\nWHERE {\n      ?OP a era:OperationalPoint.\n      ?OP era:canonicalURI ?OP .\n      ?OP era:inCountry ?inCountry.\n}}\nSERVICE <http://publications.europa.eu/webapi/rdf/sparql>{\n      ?inCountry dc:identifier ?id\n}\n}\n} "
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Sections of line per member state"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX dc: <http://purl.org/dc/elements/1.1/>\n\nSELECT DISTINCT ?id ?inCountry ?count\nWHERE{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n{SELECT DISTINCT ?inCountry (COUNT(DISTINCT ?SL) AS ?count)\nWHERE {\n      ?SL a era:SectionOfLine.\n      ?SL era:canonicalURI ?SL .\n      ?SL era:inCountry ?inCountry.\n}}\nSERVICE <http://publications.europa.eu/webapi/rdf/sparql>{\n      ?inCountry dc:identifier ?id\n}\n}\n}\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Tracks from neighboring countries to Ukraine"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX era: <http://data.europa.eu/949/>\nPREFIX country: <http://publications.europa.eu/resource/authority/country/>\n\nSELECT DISTINCT ?country ?gprofile\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?country {country:HUN country:ROU country:SVK country:POL}\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track . \n  ?track era:gaugingProfile ?gprofile .\n }\n}  ORDER BY ?country"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Tracks non TSI compliant per country"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT ?country (COUNT(DISTINCT ?track) AS ?countTracks)\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track .  \n  ?track era:hasTSITrainDetection "false"^^xsd:boolean \n}\n}  ORDER BY ?country\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Tracks with train detection system non TSI compliant per country"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?country ?p (COUNT(DISTINCT ?track) AS ?numberTracks)\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track .  \n  ?track era:trainDetectionSystem ?tds .\n  ?tds a era:TrainDetectionSystem .\n  VALUES ?p {era:tsiCompliantCompositeBrakeBlocks era:tsiCompliantFerromagneticWheel era:tsiCompliantMaxImpedanceWheelset era:tsiCompliantMetalConstruction era:tsiCompliantMetalFreeSpace era:tsiCompliantRSTShuntImpedance era:tsiCompliantSandCharacteristics era:tsiCompliantSanding era:tsiCompliantShuntDevices } \n  ?tds ?p <http://data.europa.eu/949/concepts/tsi-compliances/rinf/not_TSI_compliant>\n  }\n}  ORDER BY ?country ?p"
  }
]
```

### Notebook 2. otherqueries.sparqlbook

Notebook aggregating other queries.

```sparql
[
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Number of tracks, per country, that are not TSI compliant"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT ?country (COUNT(DISTINCT ?track) AS ?countTracks)\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track .  \n  ?track era:hasTSITrainDetection "false"^^xsd:boolean \n}\n}  ORDER BY ?country\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Number of tracks, per country, whose associated train detection systems are not TSI compliant."
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT ?country ?p (COUNT(DISTINCT ?track) AS ?numberTracks)\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track .  \n  ?track era:trainDetectionSystem ?tds .\n  ?tds a era:TrainDetectionSystem .\n  VALUES ?p {era:tsiCompliantCompositeBrakeBlocks era:tsiCompliantFerromagneticWheel era:tsiCompliantMaxImpedanceWheelset era:tsiCompliantMetalConstruction era:tsiCompliantMetalFreeSpace era:tsiCompliantRSTShuntImpedance era:tsiCompliantSandCharacteristics era:tsiCompliantSanding era:tsiCompliantShuntDevices } \n  ?tds ?p <http://data.europa.eu/949/concepts/tsi-compliances/rinf/not_TSI_compliant>\n  }\n}  ORDER BY ?country ?p"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# Types of gauging profiles of tracks in neighbouring countries to Ukraine."
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX country: <http://publications.europa.eu/resource/authority/country/>\n\nSELECT DISTINCT ?country ?gprofile\nWHERE {\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n  VALUES ?country {country:HUN country:ROU country:SVK country:POL}\n  ?sectionOfLine a era:SectionOfLine .\n  ?sectionOfLine era:inCountry ?country .\n  ?sectionOfLine era:track ?track .\n  ?track a era:Track . \n  ?track era:gaugingProfile ?gprofile .\n }\n}  ORDER BY ?country"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# INSPIRE data generation. Example of link generation from tracks"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX inspire: <http://inspire.ec.europa.eu/ont/net#> \nCONSTRUCT { \n?track a inspire:Link; \ninspire:Link.startNode ?startOP; \ninspire:Link.endNode ?endOP. \n?startOP a inspire:Node. \n ?endOP a inspire:Node.\n} WHERE {\n?track a era:Track;\n^era:track [\nera:opStart ?startOP;\nera:opEnd ?endOP;\nera:inCountry <http://publications.europa.eu/resource/authority/country/BEL>\n].\n}" 
  }
]
```

### Notebook 3. tentqueries.sparqlbook

Notebook aggregating queries related to the TEN-T data space.

```sparql
[
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 1 - Determine the compliance of tracks with the High Speed Load Model (HSLM)"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\n    GRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    OPTIONAL {?track era:highSpeedLoadModelCompliance ?highSpeedLoadModelCompliance} .\n}\n}\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 2 - Classification of a line according to the INF TSI"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\n    GRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:lineNationalId ?x .\n    ?sol era:track ?track .\n    ?track era:lineCategory ?lineCategory .\n    }\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 3 - Number of tracks for a sectin of line."
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT (COUNT(DISTINCT ?track) AS ?tracks)\n{\n    GRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n}\n}\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 4 - Type of contact line systems of the tracks in a section of line"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:contactLineSystem ?cls .\n    ?cls era:contactLineSystemType ?clstype .\n}\n}\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 5 - Wheel set gauge of the tracks of a section of line"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:wheelSetGauge ?wheelSetGauge .\n}\n}\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 6 - Energy supply system associated to the tracks of a section of line"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:contactLineSystem ?cls .\n    ?cls era:energySupplySystem ?energySupplySystem .\n    }\n}\n\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 7 - ERTMS / ETCS application level of a track, which expresses the possible operating relationships between track and train"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\r\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \r\n# \r\nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.\n    ?op_start era:opName ?op_startName .\n    ?sol era:opEnd ?op_end.\n    ?op_end era:opName ?op_endName .\n    FILTER (regex(?op_startName,"Dendermonde")) .\n    FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:etcsLevel ?etcsLevel .\n    ?etcsLevelURI era:etcsLevelType ?etcsLevelType .\n    FILTER(uri(?etcsLevel)=?etcsLevelURI)\n    }\n}\n\n\n\n\n"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 8 - ETCS baseline installed in the track"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:etcsLevel ?etcsLevel .\n    OPTIONAL{?etcsLevelURI era:etcsBaseline ?etcsBaseline .\n    FILTER(uri(?etcsLevel)=?etcsLevelURI)} .\n    }\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 9 - Location of particular points requiring specific checks due to deviations from gauging"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    OPTIONAL {?track era:gaugingCheckLocation ?location .}\n    }\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 10 - Combined transport profile for semi-trailers"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:profileNumberSemiTrailers ?profileNumberSemiTrailers .\n    }\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 11 - If ETCS in operation, fill in parameters ETCS Baseline and ETCS Level for tracks"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    OPTIONAL {?track era:highSpeedLoadModelCompliance "true"^^xsd:boolean} .\n\n    OPTIONAL {?track era:etcsLevel ?etcsLevel} .\n    OPTIONAL {?etcsLevelURI era:etcsBaseline ?etcsBaseline .\n      FILTER(uri(?etcsLevel)=?etcsLevelURI) .}\n\n    OPTIONAL{?etcsLevelURI era:etcsLevelType ?etcsLevelType .\n    FILTER(uri(?etcsLevel)=?etcsLevelURI) }\n\n}\n\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 12 - GSM-R version installed in the tracks of a section of line"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:gsmRVersion ?gsmRVersion .\n}\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 13 - Maximum Axle Load (note that this parameter does not exist and we use minAxleLoad instead, which returns currently no values)"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:trainDetectionSystem ?trainDetSyst .\n    ?trainDetSyst era:tdsMinAxleLoadVehicleCategory ?minAxleLoadVehCat .\n    OPTIONAL{ ?minAxleLoadVehCat era:minAxleLoad ?minAxleLoad} \n    }\n\n}"
  },
  {
    "kind": 1,
    "language": "markdown",
    "value": "# TEN-T 14 - Nominal maximum operational speed on the line as a result of INF, ENE and CCS subsystem characteristics expressed in kilometres/hour"
  },
  {
    "kind": 2,
    "language": "sparql",
    "value": "#\n# Query [endpoint=https://graph.data.era.europa.eu/repositories/rinf-plus] Query \n# \nPREFIX era: <http://data.europa.eu/949/>\n\nSELECT DISTINCT *\n{\nGRAPH <http://data.europa.eu/949/graph/rinf> {\n    ?sol a era:SectionOfLine. \n    ?sol era:opStart ?op_start.   ?op_start era:opName ?op_startName .      FILTER (regex(?op_startName,"Dendermonde")) .\n    ?sol era:opEnd ?op_end.       ?op_end era:opName ?op_endName .          FILTER (regex(?op_endName,"Zele")).\n    ?sol era:track ?track .\n    ?track era:trackId ?trackId .\n    ?track era:maximumPermittedSpeed ?maximumPermittedSpeed \n    }\n\n}"
  }
]
```


## Internal Computed Story Queries

These are used by the Data Stories app to list and load computed/report-backed stories.

### list-computed-stories.sparql

```sparql
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?iri ?title ?description WHERE {
  ?iri dct:title ?title .
  OPTIONAL { ?iri dct:description ?description . }
}
```

### get-computed-story-details.sparql

```sparql
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?iri ?title ?description ?details WHERE {
  BIND(<${{IRI}}> as ?iri).
  ?iri dct:title ?title .
  OPTIONAL { ?iri dct:description ?description . }
  ?iri <http://data.europa.eu/949/rinf/reports/viewJson> ?details .
}
```
