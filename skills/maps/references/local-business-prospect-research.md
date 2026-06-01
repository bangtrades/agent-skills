# Local business prospect research workflow

Use this when the user asks for a large prospect list of businesses within a radius of a place, especially when the goal is sales targeting rather than simple nearby recommendations.

## Pattern

1. Geocode the anchor location and choose the radius in meters.
   - 5 miles = 8,047 meters.
2. Query Overpass directly for broad commercial POI tags, not just one `nearby` category:
   - `shop`
   - `amenity`
   - `office`
   - `craft`
   - `healthcare`
   - `tourism`
   - `leisure`
   - `industrial`
   - `commercial`
3. Request `out center tags;` so ways/relations get usable coordinates.
4. Compute haversine distance from the anchor and discard records outside the requested radius.
5. Deduplicate by normalized business name, preferring the nearest record.
6. Exclude obvious public infrastructure/non-prospects and obvious national chains when the user asks for privately owned/local businesses.
7. Categorize from OSM tags into sales-relevant buckets such as restaurants, auto, healthcare, dental, real estate, financial services, legal, insurance, trades, retail, vape/smoke, beauty, fitness, hospitality, and logistics.
8. Add sales-useful columns:
   - business name
   - category
   - original OSM business type
   - address/city
   - phone/website when available
   - distance miles
   - Google Maps search URL
   - revenue likelihood score
   - reason for likely revenue fit
   - suggested AI/digital-services angle
   - source and ownership-verification note
9. Export both a raw qualified pool and a curated/balanced CSV. For “at least N” requests, produce more than N if available, but keep the curated file balanced across business types so restaurants/retail do not swamp high-value professional categories.
10. Verify before finalizing:
   - row count meets the requested minimum
   - max distance is within radius
   - no empty names
   - no duplicate normalized names

## Revenue / ownership caution

Public POI data cannot prove private ownership or exact annual revenue. Frame revenue and ownership as heuristics: filter out obvious national chains, prioritize categories commonly exceeding the target revenue threshold, and include a note to verify ownership/revenue before outreach.

## Overpass query skeleton

```overpass
[out:json][timeout:180];
(
  nwr[shop](around:RADIUS_M,LAT,LON);
  nwr[amenity](around:RADIUS_M,LAT,LON);
  nwr[office](around:RADIUS_M,LAT,LON);
  nwr[craft](around:RADIUS_M,LAT,LON);
  nwr[healthcare](around:RADIUS_M,LAT,LON);
  nwr[tourism](around:RADIUS_M,LAT,LON);
  nwr[leisure](around:RADIUS_M,LAT,LON);
  nwr[industrial](around:RADIUS_M,LAT,LON);
  nwr[commercial](around:RADIUS_M,LAT,LON);
);
out center tags;
```

## Pitfalls

- Do not claim revenue or private ownership as verified unless independently checked.
- The built-in `nearby` command is good for small category searches, but broad prospecting is better handled with direct Overpass queries and custom post-processing.
- OSM coverage can be incomplete for phone/website/contact fields. Include Google Maps search URLs to make manual enrichment easy.
- Large raw POI pools need category balancing for sales usefulness; otherwise the final list tends to overrepresent restaurants and generic retail.
