/**
 * =============================================================================
 * Script 07: ERA5 Climate Variables Extraction
 * =============================================================================
 * 
 * Product: ECMWF/ERA5_LAND/MONTHLY_AGGR
 * Variables: Temperature (2m), Total Precipitation, U/V Wind (10m),
 *            Dewpoint Temperature (2m)
 * 
 * These climate variables serve as covariates for climate-pollution
 * relationship analysis (Layers 6-7 of the analytical framework).
 * =============================================================================
 */

var START_DATE = '2019-01-01';
var END_DATE = '2026-12-31';
var EXPORT_FOLDER = 'Nepal_ERA5_Climate';
var SCALE = 10000; // ERA5-Land is ~9km (0.1°), export at 10km

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

// ----- LOAD ERA5-Land MONTHLY AGGREGATED -----
var era5 = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR')
  .filterDate(START_DATE, END_DATE)
  .filterBounds(nepalGeom);

// ----- PROCESS MONTHLY DATA -----
var processMonth = function(image) {
  var date = image.date();
  var year = date.get('year');
  var month = date.get('month');
  
  // Temperature: Convert from Kelvin to Celsius
  var temp2m = image.select('temperature_2m').subtract(273.15).rename('temperature_celsius');
  
  // Dewpoint temperature: Convert K → °C
  var dewpoint = image.select('dewpoint_temperature_2m').subtract(273.15).rename('dewpoint_celsius');
  
  // Precipitation: Sum in meters, convert to mm
  var precip = image.select('total_precipitation_sum').multiply(1000).rename('precipitation_mm');
  
  // Wind speed: Compute magnitude from U and V components
  var uWind = image.select('u_component_of_wind_10m');
  var vWind = image.select('v_component_of_wind_10m');
  var windSpeed = uWind.pow(2).add(vWind.pow(2)).sqrt().rename('wind_speed_ms');
  
  // Wind direction (degrees from north, meteorological convention)
  var windDir = uWind.atan2(vWind).multiply(180 / Math.PI).add(180).rename('wind_direction_deg');
  
  // Relative Humidity approximation (from temp and dewpoint, Magnus formula)
  // RH ≈ 100 * exp(17.625 * Td / (243.04 + Td)) / exp(17.625 * T / (243.04 + T))
  var a = ee.Number(17.625);
  var b = ee.Number(243.04);
  var rhNum = dewpoint.multiply(a).divide(dewpoint.add(b)).exp();
  var rhDen = temp2m.multiply(a).divide(temp2m.add(b)).exp();
  var rh = rhNum.divide(rhDen).multiply(100).rename('relative_humidity');
  
  // Combine all bands
  var combined = temp2m
    .addBands(dewpoint)
    .addBands(precip)
    .addBands(windSpeed)
    .addBands(windDir)
    .addBands(rh)
    .clip(nepal)
    .set('year', year)
    .set('month', month)
    .set('system:time_start', date.millis());
  
  return combined;
};

var monthlyClimate = era5.map(processMonth);

// ----- ZONAL STATISTICS: By Physiographic Zone -----
var computeZonalStats = function(image) {
  var year = image.get('year');
  var month = image.get('month');
  var zoneList = ee.List([1, 2, 3, 4, 5]);
  var zoneNames = ee.List(['Terai', 'Siwalik', 'Middle_Mountains', 'High_Mountains', 'High_Himal']);
  
  var bands = ['temperature_celsius', 'dewpoint_celsius', 'precipitation_mm',
               'wind_speed_ms', 'wind_direction_deg', 'relative_humidity'];
  
  var stats = zoneList.map(function(zoneId) {
    var zoneMask = zones.eq(ee.Number(zoneId));
    var maskedImage = image.updateMask(zoneMask);
    
    var result = maskedImage.reduceRegion({
      reducer: ee.Reducer.mean().combine(ee.Reducer.stdDev(), '', true),
      geometry: nepalGeom,
      scale: SCALE,
      maxPixels: 1e10,
    });
    
    var zoneName = zoneNames.get(ee.Number(zoneId).subtract(1));
    
    return ee.Feature(null, {
      'year': year,
      'month': month,
      'zone': zoneName,
      'temp_mean': result.get('temperature_celsius_mean'),
      'temp_std': result.get('temperature_celsius_stdDev'),
      'dewpoint_mean': result.get('dewpoint_celsius_mean'),
      'precip_mean': result.get('precipitation_mm_mean'),
      'precip_std': result.get('precipitation_mm_stdDev'),
      'wind_speed_mean': result.get('wind_speed_ms_mean'),
      'wind_dir_mean': result.get('wind_direction_deg_mean'),
      'rh_mean': result.get('relative_humidity_mean'),
      'rh_std': result.get('relative_humidity_stdDev'),
    });
  });
  
  return ee.FeatureCollection(stats);
};

var allZonalStats = monthlyClimate.map(computeZonalStats).flatten();

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
var allProvinceStats = monthlyClimate.map(computeProvinceStats).flatten();

// ----- VISUALIZATION -----
var tempViz = {bands: ['temperature_celsius'], min: -10, max: 35,
  palette: ['#313695', '#4575B4', '#74ADD1', '#FEE090', '#F46D43', '#A50026']};
Map.centerObject(nepal, 7);
var latestMonth = monthlyClimate.sort('system:time_start', false).first();
Map.addLayer(latestMonth, tempViz, 'Temperature (°C) Latest');

// ----- EXPORTS -----
Export.table.toDrive({
  collection: allZonalStats,
  description: 'ERA5_monthly_zonal_stats_physiographic',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'ERA5_monthly_zonal_physiographic',
  fileFormat: 'CSV',
});

Export.table.toDrive({
  collection: allProvinceStats,
  description: 'ERA5_monthly_zonal_stats_province',
  folder: EXPORT_FOLDER,
  fileNamePrefix: 'ERA5_monthly_zonal_province',
  fileFormat: 'CSV',
});

// Export annual mean climate rasters
for (var yr = 2019; yr <= 2026; yr++) {
  var annualMean = monthlyClimate
    .filter(ee.Filter.eq('year', yr))
    .mean();
  
  Export.image.toDrive({
    image: annualMean,
    description: 'ERA5_annual_mean_' + yr,
    folder: EXPORT_FOLDER,
    fileNamePrefix: 'ERA5_annual_mean_' + yr,
    region: nepalGeom,
    scale: SCALE,
    crs: 'EPSG:4326',
    maxPixels: 1e10,
  });
}

print('ERA5 Monthly Collection Size:', monthlyClimate.size());
print('Climate Variables:', monthlyClimate.first().bandNames());
