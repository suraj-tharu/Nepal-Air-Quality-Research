/**
 * Nepal Boundaries Utility Module for Google Earth Engine
 * 
 * Provides:
 * - Nepal country boundary
 * - Province boundaries (7 provinces)
 * - Physiographic zones derived from SRTM DEM elevation
 * - Helper functions for clipping and zonal statistics
 * 
 * Usage: Copy this into your GEE script or use as a module.
 */

// =============================================================================
// NEPAL COUNTRY BOUNDARY
// =============================================================================

/**
 * Get Nepal country boundary from FAO GAUL dataset.
 * Buffer by 5km to handle edge effects in satellite data.
 */
var getNepalBoundary = function() {
  var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
  var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
  return nepal;
};

/**
 * Get Nepal boundary with buffer for edge effects.
 */
var getNepalBoundaryBuffered = function(bufferMeters) {
  bufferMeters = bufferMeters || 5000;  // Default 5km buffer
  return getNepalBoundary().geometry().buffer(bufferMeters);
};

// =============================================================================
// PROVINCE BOUNDARIES
// =============================================================================

/**
 * Get Nepal's 7 province boundaries from GAUL Level 1.
 */
var getProvinceBoundaries = function() {
  var admin1 = ee.FeatureCollection('FAO/GAUL/2015/level1');
  var nepalProvinces = admin1.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
  return nepalProvinces;
};

// =============================================================================
// PHYSIOGRAPHIC ZONES (Elevation-based)
// =============================================================================

/**
 * Create physiographic zone raster from SRTM DEM.
 * 
 * Zones:
 *   1 = Terai (< 300m)
 *   2 = Siwalik (300–1500m)
 *   3 = Middle Mountains (1500–3000m)
 *   4 = High Mountains (3000–5000m)
 *   5 = High Himal (> 5000m)
 */
var getPhysiographicZones = function() {
  var dem = ee.Image('USGS/SRTMGL1_003').clip(getNepalBoundary());
  var elevation = dem.select('elevation');
  
  var zones = ee.Image(0)
    .where(elevation.lt(300), 1)                              // Terai
    .where(elevation.gte(300).and(elevation.lt(1500)), 2)     // Siwalik
    .where(elevation.gte(1500).and(elevation.lt(3000)), 3)    // Middle Mountains
    .where(elevation.gte(3000).and(elevation.lt(5000)), 4)    // High Mountains
    .where(elevation.gte(5000), 5)                             // High Himal
    .clip(getNepalBoundary())
    .rename('zone');
  
  return zones;
};

/**
 * Get physiographic zones as feature collection (polygons).
 * Useful for zonal statistics.
 */
var getPhysiographicZonesVector = function() {
  var zones = getPhysiographicZones();
  
  // Convert raster zones to vector polygons
  var vectors = zones.reduceToVectors({
    geometry: getNepalBoundary(),
    scale: 1000,  // 1km resolution for vectorization
    geometryType: 'polygon',
    eightConnected: true,
    labelProperty: 'zone',
    maxPixels: 1e10,
  });
  
  // Add zone names
  var zoneNames = ee.Dictionary({
    1: 'Terai',
    2: 'Siwalik',
    3: 'Middle_Mountains',
    4: 'High_Mountains',
    5: 'High_Himal'
  });
  
  vectors = vectors.map(function(feature) {
    var zoneId = feature.get('zone');
    var zoneName = zoneNames.get(ee.String(ee.Number(zoneId).int().format()));
    return feature.set('zone_name', zoneName);
  });
  
  return vectors;
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

/**
 * Clip an image to Nepal boundary.
 */
var clipToNepal = function(image) {
  return image.clip(getNepalBoundary());
};

/**
 * Compute zonal statistics for an image across physiographic zones.
 * Returns a FeatureCollection with mean, median, std, min, max per zone.
 */
var zonalStatsByPhysiography = function(image, bandName) {
  var zones = getPhysiographicZonesVector();
  
  var stats = image.select(bandName).reduceRegions({
    collection: zones,
    reducer: ee.Reducer.mean()
      .combine(ee.Reducer.median(), '', true)
      .combine(ee.Reducer.stdDev(), '', true)
      .combine(ee.Reducer.minMax(), '', true),
    scale: 5000,  // ~5km matching S5P resolution
  });
  
  return stats;
};

/**
 * Compute zonal statistics by province.
 */
var zonalStatsByProvince = function(image, bandName) {
  var provinces = getProvinceBoundaries();
  
  var stats = image.select(bandName).reduceRegions({
    collection: provinces,
    reducer: ee.Reducer.mean()
      .combine(ee.Reducer.median(), '', true)
      .combine(ee.Reducer.stdDev(), '', true),
    scale: 5000,
  });
  
  return stats;
};

/**
 * Get the Nepal DEM (SRTM) for elevation context.
 */
var getNepalDEM = function() {
  return ee.Image('USGS/SRTMGL1_003').clip(getNepalBoundary());
};

// =============================================================================
// VISUALIZATION PARAMETERS
// =============================================================================
var zoneVizParams = {
  min: 1,
  max: 5,
  palette: ['#2E7D32', '#66BB6A', '#FDD835', '#FF8F00', '#FFFFFF']
};

var elevationVizParams = {
  min: 0,
  max: 8848,
  palette: ['#1a9850', '#91cf60', '#d9ef8b', '#fee08b', '#fc8d59', '#d73027', '#FFFFFF']
};

// =============================================================================
// EXPORTS
// =============================================================================
exports.getNepalBoundary = getNepalBoundary;
exports.getNepalBoundaryBuffered = getNepalBoundaryBuffered;
exports.getProvinceBoundaries = getProvinceBoundaries;
exports.getPhysiographicZones = getPhysiographicZones;
exports.getPhysiographicZonesVector = getPhysiographicZonesVector;
exports.clipToNepal = clipToNepal;
exports.zonalStatsByPhysiography = zonalStatsByPhysiography;
exports.zonalStatsByProvince = zonalStatsByProvince;
exports.getNepalDEM = getNepalDEM;
exports.zoneVizParams = zoneVizParams;
exports.elevationVizParams = elevationVizParams;
