/**
 * =============================================================================
 * Script 04: O₃ (Ozone) Extraction from Sentinel-5P TROPOMI
 * =============================================================================
 * 
 * Product: COPERNICUS/S5P/OFFL/L3_O3
 * Band: O3_column_number_density
 * =============================================================================
 */

var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_S5P_O3';
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
  
  var collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_O3')
    .filterDate(startDate, endDate)
    .filterBounds(nepalGeom);
  
  // QA filtering: Sentinel-5P standard recommendation for O3 is qa_value > 0.5
  var filtered = collection.map(function(img) {
    var hasQA = img.bandNames().contains('qa_value');
    var mask = ee.Image(ee.Algorithms.If(
      hasQA,
      img.select('qa_value').gt(0.5),
      ee.Image(1)
    ));
    return img.updateMask(mask);
  });
  
  var median = filtered.select('O3_column_number_density')
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
      'O3_mean': result.get('O3_column_number_density_mean'),
      'O3_median': result.get('O3_column_number_density_median'),
      'O3_stdDev': result.get('O3_column_number_density_stdDev'),
      'O3_count': result.get('O3_column_number_density_count'),
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

var o3Viz = {min: 0.10, max: 0.16, palette: ['#E8EAF6', '#7986CB', '#3949AB', '#1A237E']};
Map.centerObject(nepal, 7);
Map.addLayer(monthlyCollection.filter(ee.Filter.eq('year', 2024)).mean(), o3Viz, 'O3 Annual Mean 2024');

Export.table.toDrive({
  collection: allZonalStats, description: 'O3_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER, fileNamePrefix: 'O3_monthly_zonal_physiographic', fileFormat: 'CSV',
});
Export.table.toDrive({
  collection: allProvinceStats, description: 'O3_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER, fileNamePrefix: 'O3_monthly_zonal_province', fileFormat: 'CSV',
});
for (var yr = 2019; yr <= 2026; yr++) {
  Export.image.toDrive({
    image: monthlyCollection.filter(ee.Filter.eq('year', yr)).mean(),
    description: 'O3_annual_mean_' + yr, folder: EXPORT_FOLDER,
    fileNamePrefix: 'O3_annual_mean_' + yr, region: nepalGeom,
    scale: SCALE, crs: 'EPSG:4326', maxPixels: 1e10,
  });
}
print('O3 Monthly Collection Size:', monthlyCollection.size());
