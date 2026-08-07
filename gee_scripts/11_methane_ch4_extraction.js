/**
 * =============================================================================
 * Script 11: CH₄ (Methane) Extraction from Sentinel-5P TROPOMI
 * =============================================================================
 * 
 * Product: COPERNICUS/S5P/OFFL/L3_CH4
 * Band: CH4_column_volume_mixing_ratio_dry_air
 * QA Filter: qa_value > 0.5
 * 
 * Outputs: Monthly median composites + zonal stats (physiographic & province)
 * =============================================================================
 */

var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_S5P_CH4';
var SCALE = 5000;

// ----- NEPAL BOUNDARY & ZONES -----
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

// ----- MONTHLY COMPOSITE FUNCTION -----
var createMonthlyComposite = function(year, month) {
  var startDate = ee.Date.fromYMD(year, month, 1);
  var endDate = startDate.advance(1, 'month');
  
  var collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_CH4')
    .filterDate(startDate, endDate)
    .filterBounds(nepalGeom)
    // Some early OFFL granules lack qa_value — filter to only those that have it
    .filter(ee.Filter.listContains('system:band_names', 'qa_value'));
  
  // QA filtering: Sentinel-5P standard recommendation for CH4 is qa_value > 0.5
  var filtered = collection.map(function(img) {
    var qa = img.select('qa_value');
    var mask = qa.gt(0.5);
    return img.updateMask(mask);
  });
  
  var median = filtered.select('CH4_column_volume_mixing_ratio_dry_air')
    .median()
    .clip(nepal)
    .set('year', year)
    .set('month', month)
    .set('system:time_start', startDate.millis());
  
  return median;
};

// ----- GENERATE COMPOSITES -----
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
      reducer: ee.Reducer.mean().combine(ee.Reducer.median(), '', true)
        .combine(ee.Reducer.stdDev(), '', true).combine(ee.Reducer.count(), '', true),
      geometry: nepalGeom, scale: SCALE, maxPixels: 1e10,
    });
    var zoneName = zoneNames.get(ee.Number(zoneId).subtract(1));
    return ee.Feature(null, {
      'year': year, 'month': month, 'zone': zoneName,
      'CH4_mean': result.get('CH4_column_volume_mixing_ratio_dry_air_mean'),
      'CH4_median': result.get('CH4_column_volume_mixing_ratio_dry_air_median'),
      'CH4_stdDev': result.get('CH4_column_volume_mixing_ratio_dry_air_stdDev'),
      'CH4_count': result.get('CH4_column_volume_mixing_ratio_dry_air_count'),
    });
  });
  return ee.FeatureCollection(stats);
};

var allZonalStats = monthlyCollection.map(computeZonalStats).flatten();

// Province stats
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

// ----- VISUALIZATION -----
var ch4Viz = {min: 1750, max: 1950, palette: ['#E0F7FA', '#00BCD4', '#009688', '#388E3C']};
Map.centerObject(nepal, 7);
Map.addLayer(monthlyCollection.filter(ee.Filter.eq('year', 2024)).mean(), ch4Viz, 'CH4 Annual Mean 2024');

// ----- EXPORTS -----
Export.table.toDrive({
  collection: allZonalStats,
  description: 'CH4_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER, fileNamePrefix: 'CH4_monthly_zonal_physiographic', fileFormat: 'CSV',
});

Export.table.toDrive({
  collection: allProvinceStats,
  description: 'CH4_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER, fileNamePrefix: 'CH4_monthly_zonal_province', fileFormat: 'CSV',
});

for (var yr = 2019; yr <= 2026; yr++) {
  Export.image.toDrive({
    image: monthlyCollection.filter(ee.Filter.eq('year', yr)).mean(),
    description: 'CH4_annual_mean_' + yr, folder: EXPORT_FOLDER,
    fileNamePrefix: 'CH4_annual_mean_' + yr, region: nepalGeom,
    scale: SCALE, crs: 'EPSG:4326', maxPixels: 1e10,
  });
}

print('CH4 Monthly Collection Size:', monthlyCollection.size());
