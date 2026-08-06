/**
 * =============================================================================
 * Script 09: WorldPop Population Density Extraction
 * =============================================================================
 * 
 * Product: WorldPop/GP/100m/pop_age_sex_cons_unadj
 * Purpose: Population-weighted exposure analysis (Layer 7)
 * 
 * Note: WorldPop on GEE only has data through 2020. We use the 2020 baseline
 * for population-weighted exposure calculations across all study years.
 * =============================================================================
 */

var EXPORT_FOLDER = 'Nepal_Population';
var SCALE = 1000; // Export at 1km (aggregated from 100m)

// ----- NEPAL BOUNDARY & ZONES -----
var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
var nepalGeom = nepal.geometry();

var dem = ee.Image('USGS/SRTMGL1_003').clip(nepalGeom);
var elevation = dem.select('elevation');
var zones = ee.Image(0)
  .where(elevation.lt(300), 1)
  .where(elevation.gte(300).and(elevation.lt(1500)), 2)
  .where(elevation.gte(1500).and(elevation.lt(3000)), 3)
  .where(elevation.gte(3000).and(elevation.lt(5000)), 4)
  .where(elevation.gte(5000), 5)
  .clip(nepalGeom)
  .rename('zone');

var admin1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var provinces = admin1.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));

// ----- LOAD WORLDPOP 2020 BASELINE -----
var pop2020 = ee.ImageCollection('WorldPop/GP/100m/pop_age_sex_cons_unadj')
  .filterDate('2020-01-01', '2020-12-31')
  .filterBounds(nepalGeom)
  .select('population')
  .sum()  // Sum all age/sex bands to get total population
  .clip(nepalGeom);

// ----- ZONAL STATISTICS: By Physiographic Zone -----
var zoneList = [1, 2, 3, 4, 5];
var zoneNames = ['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal'];

var zonalFeatures = [];
for (var i = 0; i < zoneList.length; i++) {
  var zoneId = zoneList[i];
  var zoneName = zoneNames[i];
  var zoneMask = zones.eq(zoneId);
  var maskedPop = pop2020.updateMask(zoneMask);
  
  var result = maskedPop.reduceRegion({
    reducer: ee.Reducer.sum()
      .combine(ee.Reducer.mean(), '', true)
      .combine(ee.Reducer.count(), '', true),
    geometry: nepalGeom,
    scale: 100,
    maxPixels: 1e12,
  });
  
  zonalFeatures.push(ee.Feature(null, {
    'year': 2020,
    'zone': zoneName,
    'population_total': result.get('population_sum'),
    'population_density_mean': result.get('population_mean'),
    'pixel_count': result.get('population_count'),
  }));
}

var zonalPopFC = ee.FeatureCollection(zonalFeatures);

// ----- ZONAL STATISTICS: By Province -----
var provinceStats = pop2020.reduceRegions({
  collection: provinces,
  reducer: ee.Reducer.sum().combine(ee.Reducer.mean(), '', true),
  scale: 100,
});
var provincePopFC = provinceStats.map(function(f) {
  return f.set('year', 2020);
});

// ----- VISUALIZATION -----
var popViz = {
  min: 0, max: 500,
  palette: ['#FFFFCC', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026']
};

Map.centerObject(nepalGeom, 7);
Map.addLayer(pop2020, popViz, 'Population 2020');

// ----- EXPORTS -----
Export.table.toDrive({
  collection: zonalPopFC,
  description: 'Population_zonal_stats_physiographic',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'Population_zonal_physiographic',
  fileFormat: 'CSV',
});

Export.table.toDrive({
  collection: provincePopFC,
  description: 'Population_zonal_stats_province',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'Population_zonal_province',
  fileFormat: 'CSV',
});

// Export population raster for 2020 (census year reference)
Export.image.toDrive({
  image: pop2020,
  description: 'Population_density_2020',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'Population_density_2020',
  region: nepalGeom,
  scale: SCALE,
  crs: 'EPSG:4326',
  maxPixels: 1e12,
});

print('Population total (Nepal 2020):', pop2020.reduceRegion({
  reducer: ee.Reducer.sum(),
  geometry: nepalGeom,
  scale: 100,
  maxPixels: 1e12,
}).get('population'));
print('Zonal stats:', zonalPopFC);
