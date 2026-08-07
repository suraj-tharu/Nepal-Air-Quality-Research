/**
 * =============================================================================
 * Script 01: NO₂ (Nitrogen Dioxide) Extraction from Sentinel-5P TROPOMI
 * =============================================================================
 * 
 * Product: COPERNICUS/S5P/OFFL/L3_NO2
 * Band: tropospheric_NO2_column_number_density
 * QA Filter: qa_value > 0.75
 * 
 * Outputs:
 *   1. Monthly median composites (GeoTIFF) → Google Drive
 *   2. Zonal statistics by physiographic zone (CSV) → Google Drive
 *   3. Zonal statistics by province (CSV) → Google Drive
 * 
 * Study Period: 2019-01-01 to 2025-12-31
 * =============================================================================
 */

// ----- CONFIGURATION -----
var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_S5P_NO2';
var SCALE = 5000; // 5km export resolution
var QA_THRESHOLD = 0.75;

// ----- LOAD NEPAL BOUNDARY -----
var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
var nepalGeom = nepal.geometry();

// ----- LOAD PHYSIOGRAPHIC ZONES -----
var dem = ee.Image('USGS/SRTMGL1_003').clip(nepal);
var elevation = dem.select('elevation');
var zones = ee.Image(0)
  .where(elevation.lt(300), 1)
  .where(elevation.gte(300).and(elevation.lt(1500)), 2)
  .where(elevation.gte(1500).and(elevation.lt(3000)), 3)
  .where(elevation.gte(3000).and(elevation.lt(5000)), 4)
  .where(elevation.gte(5000), 5)
  .clip(nepal)
  .rename('zone');

// ----- LOAD PROVINCE BOUNDARIES -----
var admin1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
var provinces = admin1.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));

// ----- FUNCTION: Create Monthly Composite -----
var createMonthlyComposite = function(year, month) {
  var startDate = ee.Date.fromYMD(year, month, 1);
  var endDate = startDate.advance(1, 'month');
  
  var collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2')
    .filterDate(startDate, endDate)
    .filterBounds(nepalGeom);
  
  // QA filtering: Sentinel-5P standard recommendation for NO2 is qa_value > 0.75
  var filtered = collection.map(function(img) {
    var qa = img.select('qa_value');
    var mask = qa.gt(0.75);
    return img.updateMask(mask);
  });
  
  // Compute monthly median
  var median = filtered.select('tropospheric_NO2_column_number_density')
    .median()
    .clip(nepal)
    .set('year', year)
    .set('month', month)
    .set('system:time_start', startDate.millis());
  
  return median;
};

// ----- GENERATE ALL MONTHLY COMPOSITES -----
var years = ee.List.sequence(2019, 2026);
var months = ee.List.sequence(1, 12);

var monthlyComposites = years.map(function(y) {
  return months.map(function(m) {
    return createMonthlyComposite(y, m);
  });
}).flatten();

var monthlyCollection = ee.ImageCollection.fromImages(monthlyComposites)
  .map(function(img) {
    return img.set('num_bands', img.bandNames().size());
  })
  .filter(ee.Filter.gt('num_bands', 0));

// ----- ZONAL STATISTICS: By Physiographic Zone -----
var computeZonalStats = function(image) {
  var year = image.get('year');
  var month = image.get('month');
  
  // Create zone features
  var zoneList = ee.List([1, 2, 3, 4, 5]);
  var zoneNames = ee.List(['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']);
  
  var stats = zoneList.map(function(zoneId) {
    var zoneMask = zones.eq(ee.Number(zoneId));
    var maskedImage = image.updateMask(zoneMask);
    
    var result = maskedImage.reduceRegion({
      reducer: ee.Reducer.mean()
        .combine(ee.Reducer.median(), '', true)
        .combine(ee.Reducer.stdDev(), '', true)
        .combine(ee.Reducer.count(), '', true),
      geometry: nepalGeom,
      scale: SCALE,
      maxPixels: 1e10,
    });
    
    var zoneName = zoneNames.get(ee.Number(zoneId).subtract(1));
    
    return ee.Feature(null, {
      'year': year,
      'month': month,
      'zone': zoneName,
      'NO2_mean': result.get('tropospheric_NO2_column_number_density_mean'),
      'NO2_median': result.get('tropospheric_NO2_column_number_density_median'),
      'NO2_stdDev': result.get('tropospheric_NO2_column_number_density_stdDev'),
      'NO2_count': result.get('tropospheric_NO2_column_number_density_count'),
    });
  });
  
  return ee.FeatureCollection(stats);
};

// Compute for all months
var allZonalStats = monthlyCollection.map(computeZonalStats).flatten();

// ----- ZONAL STATISTICS: By Province -----
var computeProvinceStats = function(image) {
  var year = image.get('year');
  var month = image.get('month');
  
  var stats = image.reduceRegions({
    collection: provinces,
    reducer: ee.Reducer.mean()
      .combine(ee.Reducer.median(), '', true)
      .combine(ee.Reducer.stdDev(), '', true),
    scale: SCALE,
  });
  
  return stats.map(function(f) {
    return f.set('year', year).set('month', month);
  });
};

var allProvinceStats = monthlyCollection.map(computeProvinceStats).flatten();

// ----- VISUALIZATION -----
var no2Viz = {
  min: 0,
  max: 0.0001,
  palette: ['#FFFFFF', '#FFF176', '#FFB74D', '#FF7043', '#E53935', '#880E4F']
};

// Display latest year annual mean
var annualMean2024 = monthlyCollection
  .filter(ee.Filter.eq('year', 2024))
  .mean();

Map.centerObject(nepal, 7);
Map.addLayer(annualMean2024, no2Viz, 'NO2 Annual Mean 2024');
Map.addLayer(nepal, {color: '000000'}, 'Nepal Boundary', true, 0.3);

// ----- EXPORTS -----

// Export zonal statistics CSV (Physiographic Zones)
Export.table.toDrive({
  collection: allZonalStats,
  description: 'NO2_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'NO2_monthly_zonal_physiographic',
  fileFormat: 'CSV',
});

// Export zonal statistics CSV (Provinces)
Export.table.toDrive({
  collection: allProvinceStats,
  description: 'NO2_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'NO2_monthly_zonal_province',
  fileFormat: 'CSV',
});

// Export annual mean GeoTIFFs (one per year)
for (var yr = 2019; yr <= 2026; yr++) {
  var annualMean = monthlyCollection
    .filter(ee.Filter.eq('year', yr))
    .mean();
  
  Export.image.toDrive({
    image: annualMean,
    description: 'NO2_annual_mean_' + yr,
    folder: EXPORT_FOLDER,
    fileNamePrefix: 'NO2_annual_mean_' + yr,
    region: nepalGeom,
    scale: SCALE,
    crs: 'EPSG:4326',
    maxPixels: 1e10,
  });
}

// Export seasonal mean GeoTIFFs (for each year and season)
var seasonDef = {
  'Pre_monsoon': [3, 4, 5],
  'Monsoon': [6, 7, 8, 9],
  'Post_monsoon': [10, 11],
  'Winter': [12, 1, 2]
};

print('NO2 Monthly Collection Size:', monthlyCollection.size());
print('Zonal Statistics (sample):', allZonalStats.first());
