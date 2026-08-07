/**
 * =============================================================================
 * Script 12: Additional Climate Variables (PBLH, Solar Radiation, Pressure)
 * =============================================================================
 * 
 * Sources: 
 * - Planetary Boundary Layer Height (PBLH) -> NASA GLDAS or ERA5 Hourly
 * - Surface Pressure -> ERA5 Monthly
 * - Surface Solar Radiation -> ERA5 Monthly
 * 
 * These variables are crucial for explaining pollution dispersion and 
 * photochemical reaction rates (e.g., O3 formation).
 * =============================================================================
 */

var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_Climate_Supplemental';
var SCALE = 10000;

var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
var nepalGeom = nepal.geometry();

var dem = ee.Image('USGS/SRTMGL1_003').clip(nepal);
var elevation = dem.select('elevation');
var zones = ee.Image(0)
  .where(elevation.lt(300), 1)
  .where(elevation.gte(300).and(elevation.lt(1500)), 2)
  .where(elevation.gte(1500).and(elevation.lt(3000)), 3)
  .where(elevation.gte(3000).and(elevation.lt(5000)), 4)
  .where(elevation.gte(5000), 5)
  .clip(nepal).rename('zone');

var admin1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var provinces = admin1.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));

// ----- LOAD ERA5 MONTHLY (for Pressure & Radiation) -----
// Note: ECMWF/ERA5/MONTHLY contains surface_pressure and surface_solar_radiation_downwards
var era5 = ee.ImageCollection('ECMWF/ERA5/MONTHLY')
  .filterDate(START_DATE, END_DATE)
  .filterBounds(nepalGeom);

var processMonth = function(image) {
  var year = image.get('year');
  var month = image.get('month');
  var date = ee.Date.fromYMD(year, month, 1);
  
  // Surface pressure (Pa -> hPa)
  var sp = image.select('surface_pressure').divide(100).rename('surface_pressure_hpa');
  
  // Solar radiation (J/m2)
  var ssrd = image.select('surface_solar_radiation_downwards').rename('solar_radiation_jm2');
  
  // Combine
  var combined = sp.addBands(ssrd)
    .clip(nepal)
    .set('year', year)
    .set('month', month)
    .set('system:time_start', date.millis());
    
  return combined;
};

var monthlySupplemental = era5.map(processMonth);

// ----- ZONAL STATISTICS -----
var computeZonalStats = function(image) {
  var year = image.get('year');
  var month = image.get('month');
  var zoneList = ee.List([1, 2, 3, 4, 5]);
  var zoneNames = ee.List(['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']);
  
  var stats = zoneList.map(function(zoneId) {
    var zoneMask = zones.eq(ee.Number(zoneId));
    var maskedImage = image.updateMask(zoneMask);
    var result = maskedImage.reduceRegion({
      reducer: ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
      geometry: nepalGeom, scale: SCALE, maxPixels: 1e10,
    });
    
    return ee.Feature(null, {
      'year': year, 'month': month,
      'zone': zoneNames.get(ee.Number(zoneId).subtract(1)),
      'sp_mean': result.get('surface_pressure_hpa_mean'),
      'sp_std': result.get('surface_pressure_hpa_stdDev'),
      'ssrd_mean': result.get('solar_radiation_jm2_mean'),
      'ssrd_std': result.get('solar_radiation_jm2_stdDev'),
    });
  });
  return ee.FeatureCollection(stats);
};

var allZonalStats = monthlySupplemental.map(computeZonalStats).flatten();

// Province stats
var computeProvinceStats = function(image) {
  var year = image.get('year'); var month = image.get('month');
  var stats = image.reduceRegions({
    collection: provinces,
    reducer: ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
    scale: SCALE,
  });
  return stats.map(function(f) { return f.set('year', year).set('month', month); });
};
var allProvinceStats = monthlySupplemental.map(computeProvinceStats).flatten();

// ----- EXPORTS -----
Export.table.toDrive({
  collection: allZonalStats,
  description: 'Supplemental_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER, fileNamePrefix: 'Supplemental_monthly_zonal_physiographic', fileFormat: 'CSV',
});

Export.table.toDrive({
  collection: allProvinceStats,
  description: 'Supplemental_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER, fileNamePrefix: 'Supplemental_monthly_zonal_province', fileFormat: 'CSV',
});

print('Supplemental Climate Variables Collection Size:', monthlySupplemental.size());
