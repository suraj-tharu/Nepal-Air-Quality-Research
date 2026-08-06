/**
 * =============================================================================
 * Script 08: MODIS Land Cover Extraction
 * =============================================================================
 * 
 * Product: MODIS/061/MCD12Q1 (Annual Land Cover Type)
 * Purpose: Contextualize emission sources with land use patterns
 * =============================================================================
 */

var EXPORT_FOLDER = 'Nepal_LandCover';
var SCALE = 500; // MODIS native resolution

var countries = ee.FeatureCollection('FAO/GAUL/2015/level0');
var nepal = countries.filter(ee.Filter.eq('ADM0_NAME', 'Nepal'));
var nepalGeom = nepal.geometry();

// IGBP classification legend
var igbpNames = [
  'Evergreen Needleleaf Forests', 'Evergreen Broadleaf Forests',
  'Deciduous Needleleaf Forests', 'Deciduous Broadleaf Forests',
  'Mixed Forests', 'Closed Shrublands', 'Open Shrublands',
  'Woody Savannas', 'Savannas', 'Grasslands',
  'Permanent Wetlands', 'Croplands', 'Urban and Built-up',
  'Cropland/Natural Vegetation Mosaics', 'Permanent Snow and Ice',
  'Barren', 'Water Bodies'
];

var igbpPalette = [
  '05450a', '086a10', '54a708', '78d203', '009900',
  'c6b044', 'dcd159', 'dade48', 'fbff13', 'b6ff05',
  '27ff87', 'c24f44', 'a5a5a5', 'ff6d4c', '69fff8',
  'f9ffa4', '1c0dff'
];

// Get annual land cover for each year
var years = ee.List.sequence(2019, 2023); // MCD12Q1 has ~2 year lag

var annualLandCover = years.map(function(yr) {
  var startDate = ee.Date.fromYMD(yr, 1, 1);
  var endDate = ee.Date.fromYMD(yr, 12, 31);
  
  var lc = ee.ImageCollection('MODIS/061/MCD12Q1')
    .filterDate(startDate, endDate)
    .first()
    .select('LC_Type1')  // IGBP classification
    .clip(nepal)
    .set('year', yr);
  
  return lc;
});

var lcCollection = ee.ImageCollection.fromImages(annualLandCover);

// ----- LAND COVER AREA STATISTICS -----
var computeLcStats = function(image) {
  var year = image.get('year');
  
  // Pixel area in km²
  var pixelArea = ee.Image.pixelArea().divide(1e6); // m² to km²
  
  // Compute area per class
  var areaByClass = pixelArea.addBands(image).reduceRegion({
    reducer: ee.Reducer.sum().group({
      groupField: 1,
      groupName: 'lc_class',
    }),
    geometry: nepalGeom,
    scale: SCALE,
    maxPixels: 1e10,
  });
  
  var groups = ee.List(areaByClass.get('groups'));
  
  var features = groups.map(function(item) {
    var dict = ee.Dictionary(item);
    return ee.Feature(null, {
      'year': year,
      'lc_class': dict.get('lc_class'),
      'area_km2': dict.get('sum'),
    });
  });
  
  return ee.FeatureCollection(features);
};

var allLcStats = lcCollection.map(computeLcStats).flatten();

// ----- VISUALIZATION -----
var lcViz = {min: 1, max: 17, palette: igbpPalette};
Map.centerObject(nepal, 7);
Map.addLayer(lcCollection.filter(ee.Filter.eq('year', 2023)).first(), lcViz, 'Land Cover 2023');

// ----- EXPORTS -----
Export.table.toDrive({
  collection: allLcStats,
  description: 'LandCover_annual_area_stats',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'LandCover_annual_area',
  fileFormat: 'CSV',
});

// Export land cover rasters
var lcList = lcCollection.toList(lcCollection.size());
for (var i = 0; i < 5; i++) {
  var yr = 2019 + i;
  Export.image.toDrive({
    image: ee.Image(lcList.get(i)),
    description: 'LandCover_' + yr,
    folder: EXPORT_FOLDER,
    fileNamePrefix: 'LandCover_IGBP_' + yr,
    region: nepalGeom,
    scale: SCALE,
    crs: 'EPSG:4326',
    maxPixels: 1e10,
  });
}

print('Land Cover Collection Size:', lcCollection.size());
