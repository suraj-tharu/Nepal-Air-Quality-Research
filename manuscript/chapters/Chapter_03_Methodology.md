# Chapter 3: Materials and Methods

## 3.1 Study Area
The study area encompasses the entire sovereign territory of Nepal, situated in the central Himalayas between the Indo-Gangetic Plain to the south and the Tibetan Plateau to the north. Due to its extreme topographic variation, Nepal experiences highly diverse micro-climates and localized atmospheric circulation patterns. To systematically analyze the altitudinal gradient of atmospheric pollutants, the country was stratified into five distinct physiographic zones based on elevation profiles derived from the Shuttle Radar Topography Mission (SRTM) Digital Elevation Model (DEM) at a 30-meter spatial resolution.

The five designated zones are:
1. **Terai (0–300 m):** The southern lowland plains, characterized by intensive agriculture, high population density, and significant transboundary influence from the Indo-Gangetic Plain.
2. **Siwalik (300–1,500 m):** The outer Himalayan foothills, heavily forested and subject to seasonal biomass burning.
3. **Middle Mountains (1,500–3,000 m):** The heavily populated mid-hills region, which includes the Kathmandu Valley, notorious for severe winter temperature inversions.
4. **High Mountains (3,000–5,000 m):** The inner Himalayan region with sparse population and limited anthropogenic emissions.
5. **High Himal (5,000–9,000 m):** The nival zone and trans-Himalayan region, functioning primarily as a pristine background site for atmospheric observations.

## 3.2 Datasets and Preprocessing
The primary data acquisition, temporal aggregation, and spatial clipping were executed utilizing the Google Earth Engine (GEE) cloud computing platform, ensuring a highly reproducible analytical pipeline. The study period was defined as January 1, 2019, to December 31, 2026, capturing a full eight-year temporal window that includes the COVID-19 pandemic perturbation.

### 3.2.1 Sentinel-5P TROPOMI Trace Gases
Atmospheric concentrations of key pollutants were acquired from the European Space Agency's (ESA) Copernicus Sentinel-5 Precursor (S5P) satellite, carrying the TROPOspheric Monitoring Instrument (TROPOMI). The Offline (OFFL) Level-3 products were utilized due to their superior radiometric calibration compared to Near Real-Time (NRTI) data.

To ensure data integrity, rigorous Quality Assurance (QA) thresholding was applied in accordance with ESA's algorithm theoretical basis documents:
- **Nitrogen Dioxide (NO₂):** Tropospheric vertical column density (qa_value > 0.75) to minimize cloud contamination.
- **Sulfur Dioxide (SO₂), Carbon Monoxide (CO), Ozone (O₃), Formaldehyde (HCHO), and Methane (CH₄):** Total column densities (qa_value > 0.5).
- **UV Aerosol Index (UVAI):** (qa_value > 0.8) to selectively identify UV-absorbing aerosols like soot, smoke, and mineral dust.

An algorithmic safeguard (`ee.Algorithms.If`) was implemented in GEE to gracefully handle edge-case historic OFFL granules (e.g., late 2018/early 2019) lacking embedded `qa_value` bands, preventing null-masking errors. Zonal statistics (median aggregation) were calculated at a 5,000-meter spatial scale and exported as monthly composites.

### 3.2.2 Meteorological and Climate Variables
Meteorological data were integrated to model the physical drivers of pollutant dispersion and retention. Monthly aggregated climate variables were extracted from the ECMWF ERA5-Land reanalysis dataset (`ECMWF/ERA5_LAND/MONTHLY_AGGR`) at a 0.1° × 0.1° resolution. The extracted parameters included:
- 2-meter Air Temperature (converted from Kelvin to Celsius)
- 2-meter Dewpoint Temperature
- Total Precipitation (converted from meters to millimeters)
- 10-meter U and V Wind Components

Additionally, static land characteristics—including population density (WorldPop) and land cover classifications (MODIS IGBP)—were integrated to proxy anthropogenic emission sources.

## 3.3 Trend Analysis and Climatology
A robust non-parametric statistical framework was employed to assess long-term temporal trends, as atmospheric datasets frequently exhibit non-normal distributions and seasonal cyclicity. 

The **Mann-Kendall (MK) Trend Test** was utilized to determine the statistical significance of monotonic monotonic trends across the study period, evaluated at a 95% confidence level ($\alpha = 0.05$). To quantify the magnitude of these trends, **Sen's Slope Estimator**—a median-based, outlier-resistant metric—was calculated. 

Seasonal Time Series Decomposition (STL) via Loess was applied to disentangle the overarching multi-year trend from the intense seasonal cyclicity characteristic of the South Asian monsoon system. Furthermore, monthly climatologies and seasonal anomalies were computed across four distinct periods: Pre-monsoon (MAM), Monsoon (JJAS), Post-monsoon (ON), and Winter (DJF). 

## 3.4 Spatial Hotspot and Pattern Mining
To move beyond simple descriptive mapping, advanced spatial statistics were employed to identify statistically significant clusters of high and low pollution concentrations. Using Queen's contiguity spatial weights matrices, two primary indices were calculated:

1. **Getis-Ord Gi* Statistic:** Evaluated the degree of spatial clustering of high values (hotspots) and low values (coldspots) relative to the global mean, outputting z-scores and pseudo p-values.
2. **Local Moran's I (LISA):** Delineated specific spatial typologies, identifying High-High (clusters of intense pollution), Low-Low (pristine clusters), and spatial outliers (High-Low and Low-High).

Furthermore, Space-Time Pattern Mining was utilized to evaluate how these hotspots evolved between 2019 and 2026, categorizing them into "Persistent", "Intensifying", or "Diminishing" hotspots.

## 3.5 Multivariate Statistical Modeling
To uncover latent relationships and shared emission sources among the trace gases, multivariate dimension reduction techniques were applied:
- **Principal Component Analysis (PCA):** Synthesized the variance across all six primary pollutants into orthogonal principal components, visualized via PCA Biplots to identify specific atmospheric signatures (e.g., distinguishing combustion-related NO₂/CO emissions from biogenic/photochemical HCHO/O₃ dynamics).
- **Agglomerative Hierarchical Clustering:** Grouped the five physiographic zones into statistically distinct clusters based on their long-term atmospheric profiles, utilizing Ward's minimum variance method and Euclidean distance metrics.

## 3.6 Machine Learning Predictive Modeling
A supervised Machine Learning (ML) framework was architected to predict NO₂ concentrations (as the primary proxy for anthropogenic emissions) utilizing meteorological features and temporal variables.

Three ensemble tree-based algorithms were trained and evaluated:
1. Random Forest (RF)
2. Extreme Gradient Boosting (XGBoost)
3. Light Gradient Boosting Machine (LightGBM)

Models were evaluated using standard regression metrics, including Root Mean Square Error (RMSE), Mean Absolute Error (MAE), and the Coefficient of Determination (R²). The highest-performing model (LightGBM) was subsequently subjected to **SHAP (SHapley Additive exPlanations)** analysis. The SHAP framework deconstructs the ML model's complex, non-linear predictions into individual feature contributions, providing highly interpretable global and local insights into how variables like temperature and precipitation explicitly drive atmospheric pollution.

## 3.7 Extreme Event Quantification
Specific high-impact meteorological and anthropogenic events were isolated as sub-studies to quantify their acute effects on Nepal's atmosphere:
- **The COVID-19 Natural Experiment:** Comparing the stringency of the 2020 national lockdown against historic baselines.
- **Biomass Burning Extrems:** Analyzing the catastrophic April 2021 forest fire season and the cyclical post-monsoon crop residue burning in the Terai.
- **Winter Temperature Inversions:** Quantifying the localized trapping effect in the Middle Mountains (Kathmandu Valley) during December and January.
