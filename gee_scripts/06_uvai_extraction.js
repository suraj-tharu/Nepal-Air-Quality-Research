/**
 * =============================================================================
 * Script 06: UVAI (UV Aerosol Index) Extraction from Sentinel-5P TROPOMI
 * =============================================================================
 * 
 * Product: COPERNICUS/S5P/OFFL/L3_AER_AI
 * Band: absorbing_aerosol_index
 * Note: No QA threshold filtering needed for UVAI; positive values indicate
 *       absorbing aerosols (dust, smoke), negative = non-absorbing (sulfate)
 * =============================================================================
 */

var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_S5P_UVAI';
var SCALE = 5000;

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

var createMonthlyComposite = function(year, month) {
  var startDate = ee.Date.fromYMD(year, month, 1);
  var endDate = startDate.advance(1, 'month');
  
  var collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_AER_AI')
    .filterDate(startDate, endDate)
    .filterBounds(nepalGeom);
  
  // No QA filtering for UVAI — use all valid pixels
  var median = collection.select('absorbing_aerosol_index')
    .median()
    .clip(nepal)
    .set('year', year)
    .set('month', month)
    .set('system:time_start', startDate.millis());
  
  return median;
};

var years = ee.List.sequence(2019, 2026);
var months = ee.List.sequence(1, 12);
var monthlyComposites = years.map(function(y) {
  return months.map(function(m) { return createMonthlyComposite(y, m); });
}).flatten();
var monthlyCollection = ee.ImageCollection.fromImages(monthlyComposites)
  .map(function(img) {
    return img.set('num_bands', img.bandNames().size());
  })
  .filter(ee.Filter.gt('num_bands', 0));

var computeZonalStats = function(image) {
  var year = image.get('year'); var month = image.get('month');
  var zoneList = ee.List([1, 2, 3, 4, 5]);
  var zoneNames = ee.List(['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']);
  var stats = zoneList.map(function(zoneId) {
    var zoneMask = zones.eq(ee.Number(zoneId));
    var maskedImage = image.updateMask(zoneMask);
    var result = maskedImage.reduceRegion({
      reducer: ee.Reducer.mean().combine(ee.Reducer.median(), '', true)
        .combine(ee.Reducer.stdDev(), '', true).combine(ee.Reducer.count(), '', true),
      geometry: nepalGeom, scale: SCALE, maxPixels: 1e10,
    });
    return ee.Feature(null, {
      'year': year, 'month': month,
      'zone': zoneNames.get(ee.Number(zoneId).subtract(1)),
      'UVAI_mean': result.get('absorbing_aerosol_index_mean'),
      'UVAI_median': result.get('absorbing_aerosol_index_median'),
      'UVAI_stdDev': result.get('absorbing_aerosol_index_stdDev'),
      'UVAI_count': result.get('absorbing_aerosol_index_count'),
    });
  });
  return ee.FeatureCollection(stats);
};
var allZonalStats = monthlyCollection.map(computeZonalStats).flatten();

var computeProvinceStats = function(image) {
  var year = image.get('year'); var month = image.get('month');
  var stats = image.reduceRegions({
    collection: provinces,
    reducer: ee.Reducer.mean().combine(ee.Reducer.median(), '', true)
      .combine(ee.Reducer.stdDev(), '', true),
    scale: SCALE,
  });
  return stats.map(function(f) { return f.set('year', year).set('month', month); });
};
var allProvinceStats = monthlyCollection.map(computeProvinceStats).flatten();

// UVAI visualization: negative=blue (non-absorbing), 0=white, positive=red (absorbing)
var uvaiViz = {min: -1, max: 3, palette: ['#2196F3', '#BBDEFB', '#FFFFFF', '#FFCDD2', '#F44336', '#880E4F']};
Map.centerObject(nepal, 7);
Map.addLayer(monthlyCollection.filter(ee.Filter.eq('year', 2024)).mean(), uvaiViz, 'UVAI Annual Mean 2024');

Export.table.toDrive({
  collection: allZonalStats, description: 'UVAI_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER, fileNamePrefix: 'UVAI_monthly_zonal_physiographic', fileFormat: 'CSV',
});
Export.table.toDrive({
  collection: allProvinceStats, description: 'UVAI_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER, fileNamePrefix: 'UVAI_monthly_zonal_province', fileFormat: 'CSV',
});
for (var yr = 2019; yr <= 2026; yr++) {
  Export.image.toDrive({
    image: monthlyCollection.filter(ee.Filter.eq('year', yr)).mean(),
    description: 'UVAI_annual_mean_' + yr, folder: EXPORT_FOLDER,
    fileNamePrefix: 'UVAI_annual_mean_' + yr, region: nepalGeom,
    scale: SCALE, crs: 'EPSG:4326', maxPixels: 1e10,
  });
}
print('UVAI Monthly Collection Size:', monthlyCollection.size());
