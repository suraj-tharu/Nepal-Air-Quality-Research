/**
 * =============================================================================
 * Script 13: Static Land Characteristics Extraction
 * =============================================================================
 * 
 * Extracts static/slow-changing explanatory variables:
 * - Elevation (SRTM)
 * - Slope (derived from SRTM)
 * - Population Density (WorldPop 2020)
 * - Night-time Lights (VIIRS DNB 2020/2021 composite)
 * 
 * Used for Machine Learning predictions and spatial correlations.
 * =============================================================================
 */

var EXPORT_FOLDER = 'Nepal_Land_Characteristics';
var SCALE = 5000; // Match pollutant resolution

var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
var nepalGeom = nepal.geometry();

var admin1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var provinces = admin1.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));

// ----- 1. ELEVATION & SLOPE -----
var dem = ee.Image('USGS/SRTMGL1_003').clip(nepal);
var elevation = dem.select('elevation');
var slope = ee.Terrain.slope(dem).rename('slope');

var zones = ee.Image(0)
  .where(elevation.lt(300), 1)
  .where(elevation.gte(300).and(elevation.lt(1500)), 2)
  .where(elevation.gte(1500).and(elevation.lt(3000)), 3)
  .where(elevation.gte(3000).and(elevation.lt(5000)), 4)
  .where(elevation.gte(5000), 5)
  .rename('zone');

// ----- 2. POPULATION DENSITY -----
var pop2020 = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.eq('country', 'NPL'))
  .filter(ee.Filter.eq('year', 2020))
  .mosaic()
  .clip(nepal)
  .rename('population_count');

// ----- 3. NIGHT-TIME LIGHTS -----
var ntl = ee.ImageCollection("NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG")
  .filterDate('2020-01-01', '2020-12-31')
  .select('avg_rad')
  .median()
  .clip(nepal)
  .rename('nighttime_lights');

// ----- COMBINE -----
var combinedFeatures = elevation
  .addBands(slope)
  .addBands(pop2020)
  .addBands(ntl)
  .addBands(zones);

// ----- ZONAL STATISTICS -----
var computeZonalStats = function() {
  var zoneList = ee.List([1, 2, 3, 4, 5]);
  var zoneNames = ee.List(['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']);
  
  var stats = zoneList.map(function(zoneId) {
    var zoneMask = zones.eq(ee.Number(zoneId));
    var maskedImage = combinedFeatures.updateMask(zoneMask);
    var result = maskedImage.reduceRegion({
      reducer: ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
      geometry: nepalGeom, scale: SCALE, maxPixels: 1e10,
    });
    
    return ee.Feature(null, {
      'zone': zoneNames.get(ee.Number(zoneId).subtract(1)),
      'elevation_mean': result.get('elevation_mean'),
      'slope_mean': result.get('slope_mean'),
      'pop_mean': result.get('population_count_mean'),
      'ntl_mean': result.get('nighttime_lights_mean'),
    });
  });
  return ee.FeatureCollection(stats);
};

var zonalStats = computeZonalStats();

// ----- PROVINCE STATISTICS -----
var provinceStats = combinedFeatures.reduceRegions({
  collection: provinces,
  reducer: ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
  scale: SCALE,
});

// ----- EXPORTS -----
Export.table.toDrive({
  collection: zonalStats,
  description: 'LandCharacteristics_zonal_stats_physiographic',
  folder: EXPORT_FOLDER, fileNamePrefix: 'LandCharacteristics_zonal_physiographic', fileFormat: 'CSV',
});

Export.table.toDrive({
  collection: provinceStats,
  description: 'LandCharacteristics_zonal_stats_province',
  folder: EXPORT_FOLDER, fileNamePrefix: 'LandCharacteristics_zonal_province', fileFormat: 'CSV',
});

Export.image.toDrive({
  image: combinedFeatures,
  description: 'Static_Land_Characteristics_MultiBand',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'Nepal_Land_Characteristics_5km',
  region: nepalGeom,
  scale: SCALE, crs: 'EPSG:4326', maxPixels: 1e10,
});

print('Zonal Land Characteristics Stats:', zonalStats);
