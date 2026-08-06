/**
 * GEE Script 10: Sentinel-2 NDVI & NDBI Extraction
 * Suraj Tharu Chaudhary — Spatiotemporal Atmospheric Pollutants Study
 *
 * Extracts monthly mean NDVI (vegetation health) and NDBI (built-up index)
 * per physiographic zone from Sentinel-2 Level-2A imagery (2019–2026).
 * Used to correlate urbanization and vegetation change with air pollution trends.
 *
 * Dataset: COPERNICUS/S2_SR_HARMONIZED
 * Cloud masking: QA60 band bitmask method (standard ESA approach)
 */

// ─────────────────────────────────────────────────────────────────────────────
// 1. Study Parameters
// ─────────────────────────────────────────────────────────────────────────────
var START_DATE  = '2019-01-01';
var END_DATE    = '2026-12-31';
var CLOUD_PROB  = 20;  // max cloud probability %

// ─────────────────────────────────────────────────────────────────────────────
// 2. Nepal Boundary
// ─────────────────────────────────────────────────────────────────────────────
var nepal = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
  .filter(ee.Filter.eq('country_na', 'Nepal'));

// ─────────────────────────────────────────────────────────────────────────────
// 3. Physiographic Zones from SRTM DEM
// ─────────────────────────────────────────────────────────────────────────────
var srtm = ee.Image('USGS/SRTMGL1_003').clip(nepal.geometry());

var zones = {
  'Terai':            srtm.lt(300),
  'Siwalik':          srtm.gte(300).and(srtm.lt(1500)),
  'Middle_Mountains': srtm.gte(1500).and(srtm.lt(3000)),
  'High_Mountains':   srtm.gte(3000).and(srtm.lt(5000)),
  'High_Himal':       srtm.gte(5000)
};

// ─────────────────────────────────────────────────────────────────────────────
// 4. Sentinel-2 Cloud Masking (QA60 bitmask)
// ─────────────────────────────────────────────────────────────────────────────
function maskS2Clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask  = 1 << 10;  // bit 10: opaque clouds
  var cirrusBitMask = 1 << 11;  // bit 11: cirrus clouds
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
               .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000); // scale to [0,1]
}

// ─────────────────────────────────────────────────────────────────────────────
// 5. Load Sentinel-2 Harmonized Surface Reflectance
// ─────────────────────────────────────────────────────────────────────────────
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(nepal.geometry())
  .filterDate(START_DATE, END_DATE)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CLOUD_PROB))
  .map(maskS2Clouds);

// ─────────────────────────────────────────────────────────────────────────────
// 6. Compute NDVI & NDBI
//    NDVI = (NIR - Red)  / (NIR + Red)     → B8, B4
//    NDBI = (SWIR - NIR) / (SWIR + NIR)    → B11, B8
// ─────────────────────────────────────────────────────────────────────────────
function addIndices(image) {
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI');
  return image.addBands([ndvi, ndbi]);
}

var s2_indices = s2.map(addIndices);

// ─────────────────────────────────────────────────────────────────────────────
// 7. Monthly Zonal Mean Extraction
// ─────────────────────────────────────────────────────────────────────────────
var months = ee.List.sequence(0, 
  ee.Date(END_DATE).difference(ee.Date(START_DATE), 'month').subtract(1));

var monthlyResults = months.map(function(monthOffset) {
  var startDate = ee.Date(START_DATE).advance(monthOffset, 'month');
  var endDate   = startDate.advance(1, 'month');

  var col = s2_indices.filterDate(startDate, endDate);
  var monthly = ee.Image(ee.Algorithms.If(
    col.size().gt(0),
    col.mean(),
    ee.Image.constant([0, 0]).rename(['NDVI', 'NDBI']).updateMask(0)
  )).clip(nepal.geometry());

  var features = Object.keys(zones).map(function(zoneName) {
    var zoneMask = zones[zoneName];
    var masked   = monthly.updateMask(zoneMask);
    var stats    = masked.select(['NDVI', 'NDBI']).reduceRegion({
      reducer:   ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
      geometry:  nepal.geometry(),
      crs:       'EPSG:4326',
      scale:     100,
      maxPixels: 1e11,
      bestEffort: true
    });
    return ee.Feature(null, stats.set('date', startDate.format('YYYY-MM'))
                                 .set('zone', zoneName));
  });

  return ee.FeatureCollection(features);
});

var flat = ee.FeatureCollection(monthlyResults).flatten();

// ─────────────────────────────────────────────────────────────────────────────
// 8. Export to Google Drive
// ─────────────────────────────────────────────────────────────────────────────
Export.table.toDrive({
  collection:  flat,
  description: 'Nepal_S2_NDVI_NDBI_Monthly_2019_2026',
  folder:      'GEE_Exports',
  fileFormat:  'CSV'
});

print('Sentinel-2 NDVI/NDBI export task started.');
print('Monitor in the GEE Tasks panel.');
