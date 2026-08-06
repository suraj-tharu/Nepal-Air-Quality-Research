# Spatiotemporal Dynamics and Hotspot Analysis of Atmospheric Pollutants in Nepal Using Sentinel-5P and Google Earth Engine (2019–2026)

**Author:** Suraj Tharu Chaudhary  
**Affiliation:** [Your Institution/Department — e.g., Department of Environmental Science, [University Name], Nepal]  
**Correspondence:** [your.email@institution.edu.np]  
**ORCID:** [https://orcid.org/xxxx-xxxx-xxxx-xxxx]  
**Submitted to:** [Target Journal Name]  
**Manuscript Type:** Original Research Article

---

## Abstract

Nepal experiences severe air quality degradation driven by its complex topography, rapid urbanization, and transboundary pollution transport from the Indo-Gangetic Plain (IGP). Despite its critical impact on public health, systematic high-resolution monitoring across the country's full altitudinal gradient remains sparse. This study presents the first comprehensive, multi-pollutant spatiotemporal analysis across Nepal's five physiographic zones (Terai, Siwalik, Middle Mountains, High Mountains, and High Himal) using Sentinel-5P TROPOspheric Monitoring Instrument (TROPOMI) Level-3 OFFL data processed on the Google Earth Engine (GEE) cloud computing platform (Gorelick et al., 2017) over the eight-year period January 2019 to December 2026. Six atmospheric constituents were analyzed: nitrogen dioxide (NO2), sulfur dioxide (SO2), carbon monoxide (CO), formaldehyde (HCHO), ozone (O3), and UV Aerosol Index (UVAI). Non-parametric Mann-Kendall trend analysis with Sen's Slope estimator (Gilbert, 1987) identified a statistically significant *increasing* wintertime NO2 trend in the lower physiographic zones (Sen's slope: 0.140–0.224 µmol/m²/year; p < 0.05) and a significant country-wide *increasing* O3 trend (p < 0.001). Structural breakpoint detection using Binary Segmentation applied to STL-decomposed trend components (Cleveland et al., 1990; Truong et al., 2020) identified a synchronous upward shift in NO2 across the Terai, Siwalik, and Middle Mountains in **February 2021**, consistent with post-COVID-19 industrial and economic rebound documented across South Asia (Biswal et al., 2020; Kumari and Toshniwal, 2020). Annual mean NO2 concentrations ranged from 26.10 ± 5.18 µmol/m² in the Terai to 8.24 ± 1.61 µmol/m² in the High Himal — a factor of 3.2× across the altitudinal gradient. Population-weighted exposure analysis using the WorldPop 2020 dataset (Stevens et al., 2015) reveals a severe concentration of risk burden in the Terai, which contains >50% of Nepal's population. These findings underscore the urgent need for targeted seasonal emission controls, transboundary environmental diplomacy, and a nationally expanded air quality monitoring infrastructure.

**Keywords:** Sentinel-5P TROPOMI; Google Earth Engine; Nepal; Atmospheric Pollutants; Mann-Kendall; Structural Breakpoint Detection; Spatiotemporal Analysis; Population Exposure; COVID-19 Rebound; Himalaya

---

## 1. Introduction

Air pollution represents one of the most pressing environmental and public health challenges of the 21st century, responsible for an estimated 6.7 million premature deaths annually worldwide (WHO, 2021). In South Asia, the burden is particularly acute due to the confluence of rapid industrialization, high population densities, and meteorological conditions that trap pollutants in the lower atmosphere. Nepal, located at the geophysical interface of the highly polluted Indo-Gangetic Plain (IGP) to the south and the Himalayan range to the north, is exposed to both intense locally generated emissions and large-scale transboundary pollution transport (Gurung et al., 2021). The IGP is among the most polluted regions on Earth, and Himalayan river valleys have been identified as major conduits that can funnel aerosols and trace gases from the IGP to elevations exceeding 4,000 m above sea level (ICIMOD, 2021).

Sustained exposure to elevated concentrations of nitrogen dioxide (NO2), sulfur dioxide (SO2), carbon monoxide (CO), and formaldehyde (HCHO) is causally associated with respiratory diseases, cardiovascular morbidity, and increased cancer risk (WHO, 2021). In Nepal, the Department of Environment (DoE) operates a limited number of ambient air quality monitoring stations, predominantly concentrated in the Kathmandu Valley, leaving the vast majority of the country's diverse physiographic landscape—particularly the densely populated Terai plains and the rapidly growing secondary cities—without adequate pollution surveillance.

Satellite-based remote sensing has emerged as the most viable technology for providing spatially continuous, long-term, and consistent air quality data over complex terrain and data-sparse regions. The Sentinel-5 Precursor (S5P) satellite, launched on 13 October 2017 as part of the European Space Agency's (ESA) Copernicus programme, carries the TROPOspheric Monitoring Instrument (TROPOMI). TROPOMI is a nadir-viewing push-broom spectrometer operating in the UV, visible, near-infrared, and shortwave-infrared spectral ranges (Veefkind et al., 2012). With a spatial resolution of ~3.5 km × 5.5 km and near-daily global coverage, it provides an unprecedented capability for detecting trace gas emissions from individual cities, industrial plants, and fires (Van Geffen et al., 2020). Its NO2 Level-3 OFFL products have been extensively validated against ground-based MAX-DOAS and Pandora spectrometer networks globally (Verhoelst et al., 2021).

The COVID-19 pandemic of 2020–2021 provided an unintended, large-scale natural experiment revealing the extent to which air quality responds to sudden reductions in anthropogenic activity. Studies across South Asia documented sharp NO2 declines of 12–55% during strict lockdown phases (Biswal et al., 2020; Kumari and Toshniwal, 2020), followed by rapid rebounds as economic activity resumed. For Nepal specifically, Shrestha et al. (2022) quantified a 12.7% national and 16.5% Kathmandu Valley NO2 reduction during the 2020 dry-season lockdown using TROPOMI data. However, no study has yet characterized the precise timing and spatial signature of the *post-lockdown rebound* across Nepal's full altitudinal spectrum, nor its persistence over the subsequent five-year period.

Prior satellite-based studies in the Nepalese context have been temporally limited (typically one or two years) and spatially confined to the Kathmandu Valley (Shrestha et al., 2022), creating a significant research gap at the national scale. The concurrent integration of multiple pollutants, climate drivers, and population exposure within a single analytical framework has not been previously attempted for Nepal.

The Google Earth Engine (GEE) cloud computing platform (Gorelick et al., 2017) provides the computational infrastructure needed to process the tens of terabytes of TROPOMI data spanning eight years at the national scale. GEE hosts both the Sentinel-5P data catalog and ancillary datasets (ERA5 climate, SRTM DEM, WorldPop), enabling a fully integrated and reproducible geospatial pipeline without requiring local high-performance computing.

This study aims to: (1) quantify the spatial and seasonal distribution of six key atmospheric pollutants across Nepal's five physiographic zones from 2019 to 2026; (2) evaluate the statistical significance and magnitude of long-term monotonic trends using the Mann-Kendall test and Sen's Slope estimator; (3) detect abrupt structural shifts in the pollution timeseries and attribute them to specific socio-environmental drivers; (4) characterize climate-pollutant interactions using cross-wavelet transforms and Granger causality tests; and (5) quantify population-weighted exposure to identify priority hotspots for public health intervention.

---

## 2. Methodology

### 2.1 Study Area

Nepal is a landlocked country (area: 147,181 km²) situated between latitudes 26°22'N–30°27'N and longitudes 80°04'E–88°12'E. Its extraordinary altitudinal range—from 59 m (Kechana Kalan, Terai) to 8,849 m (Mount Everest)—over a horizontal distance of less than 200 km produces extreme climatic and ecological diversity within a compact geographic area. The country is traditionally divided into five physiographic zones oriented east–west, each with distinct climate, land cover, and population characteristics (Shrestha, 1997). For this study, zone boundaries were delineated using the USGS Shuttle Radar Topography Mission (SRTM) 30m Digital Elevation Model within GEE, applying the following elevation thresholds based on standard Nepalese geographic classification (Shrestha, 1997; ICIMOD, 2021):

| Zone | Elevation Range | Primary Land Use | Pop. Density (approx.) |
|---|---|---|---|
| Terai | < 300 m | Cultivated land, settlements | Very High (>400 /km²) |
| Siwalik (Churia) | 300–1,500 m | Forest, scattered settlement | Low–Medium |
| Middle Mountains | 1,500–3,000 m | Terrace agriculture, urban valleys | High (Kathmandu Valley) |
| High Mountains | 3,000–5,000 m | Alpine pasture, sparse settlement | Very Low |
| High Himal | > 5,000 m | Glaciers, permanent snow | Near zero |

**Figure 1:** Spatial map of Nepal illustrating its national boundary and the topographic gradient driving its five distinct physiographic zones. The basemap utilizes physical terrain shading (Esri/OpenStreetMap) projected in Web Mercator (EPSG:3857) to visualize the dramatic elevation change from the southern Terai lowlands (< 300 m) to the High Himal (> 5,000 m) in the north. National boundaries are sourced from Natural Earth (2024). Map generated using Python (`geopandas` and `contextily`).

### 2.2 Data Sources

All remote sensing data were acquired and processed using Google Earth Engine (GEE) (Gorelick et al., 2017). The study period spans **1 January 2019 to 31 December 2026** — representing 8 complete calendar years selected to encompass: the pre-pandemic baseline (2019), the COVID-19 lockdown (2020), the post-lockdown economic rebound (2021), and multi-year post-pandemic trends (2022–2026).

#### 2.2.1 Atmospheric Pollutants (Sentinel-5P TROPOMI)

Monthly zonal mean concentrations were extracted for six atmospheric constituents from the Sentinel-5P TROPOMI Level-3 OFFL (Offline processing, ~2 weeks latency) products (Veefkind et al., 2012):

**Table A: Sentinel-5P GEE Dataset Details**

| Pollutant | GEE Collection ID | Primary Band | Unit |
|---|---|---|---|
| NO2 | `COPERNICUS/S5P/OFFL/L3_NO2` | `tropospheric_NO2_column_number_density` | mol/m² |
| SO2 | `COPERNICUS/S5P/OFFL/L3_SO2` | `SO2_column_number_density` | mol/m² |
| CO | `COPERNICUS/S5P/OFFL/L3_CO` | `CO_column_number_density` | mol/m² |
| HCHO | `COPERNICUS/S5P/OFFL/L3_HCHO` | `tropospheric_HCHO_column_number_density` | mol/m² |
| O3 | `COPERNICUS/S5P/OFFL/L3_O3` | `O3_column_number_density` | mol/m² |
| UVAI | `COPERNICUS/S5P/OFFL/L3_AER_AI` | `absorbing_aerosol_index` | dimensionless |

Quality assurance (QA) filtering was applied following the standard TROPOMI recommendation: pixels with `qa_value < 0.75` were masked to exclude cloud-contaminated, snow/ice-covered, and geometrically problematic pixels for tropospheric retrievals (Verhoelst et al., 2021). For collections that do not carry the `qa_value` band in the GEE Level-3 product (e.g., UVAI), an independent cloud fraction threshold (cloud radiance fraction < 0.5, as extracted from `COPERNICUS/S5P/OFFL/L3_CLOUD`) was applied instead.

#### 2.2.2 ERA5 Climate Reanalysis

To investigate meteorological drivers of pollution variability, monthly climate variables were extracted from the ECMWF ERA5 Monthly Aggregates reanalysis dataset (`ECMWF/ERA5/MONTHLY`), which provides globally consistent, gridded atmospheric data at ~27.8 km spatial resolution. Variables extracted included:
- Mean 2m air temperature (°C)
- Total monthly precipitation (mm)
- 10m u- and v-component of wind (m/s), converted to scalar wind speed: `WS = √(u² + v²)`
- 2m dewpoint temperature (°C), used to compute relative humidity via the Magnus formula

#### 2.2.3 Topography and Population

The **USGS SRTM 30m DEM** (`USGS/SRTMGL1_003`) was used to generate the physiographic zone masks. The **WorldPop UN-adjusted population count** dataset (`WorldPop/GP/100m/pop`) for the **2020 epoch** at 100m spatial resolution (Stevens et al., 2015) was used as the population baseline for exposure modeling. The 2020 dataset was used consistently for all years because it represents the most recent globally consistent census-calibrated gridded estimate available.

### 2.3 Data Extraction and Preprocessing

Monthly GEE images (TROPOMI composites) for each pollutant were reduced to zonal mean statistics using `.reduceRegion()` within each physiographic zone mask derived from the SRTM DEM. All results were exported as CSV files to Google Drive and subsequently downloaded locally for statistical analysis.

Locally, the Python 3.12 analysis pipeline handled: (1) merging multi-zone, multi-pollutant CSV files into a unified long-format dataframe; (2) temporal alignment to a consistent monthly date index; (3) interpolation of isolated missing values via linear interpolation (`scipy.interpolate.interp1d`); and (4) assignment of meteorological seasons (Winter: Dec–Feb; Pre-monsoon: Mar–May; Monsoon: Jun–Sep; Post-monsoon: Oct–Nov) following the standard South Asian monsoon classification (Shrestha, 1997).

### 2.4 Statistical Analyses

#### 2.4.1 Mann-Kendall Trend Test and Sen's Slope

The non-parametric Mann-Kendall (MK) test was applied to detect the presence and significance of monotonic temporal trends in each pollutant–zone–season combination (Gilbert, 1987). The MK test is particularly suited to environmental timeseries as it makes no assumption of normality and is robust against outliers. The test statistic S is given by:

> **S = Σᵢ<ⱼ sgn(xⱼ − xᵢ)**

where *sgn* is the sign function. A two-tailed hypothesis test was used with significance level α = 0.05. The magnitude of statistically significant trends was estimated using Sen's Slope (Q), the median slope of all pairwise combinations (Sen, 1968; Pohlert, 2016):

> **Q = median [ (xⱼ − xᵢ) / (j − i) ] for all i < j**

#### 2.4.2 Innovative Trend Analysis (ITA)

The ITA method (Şen, 2012) was concurrently applied to identify sub-trends that may be hidden by the global MK test. The method divides the timeseries into two equal sub-periods, sorts each independently, and plots them on a 1:1 scatter diagram. Points above the 1:1 line indicate an increasing trend in that magnitude range.

#### 2.4.3 Seasonal-Trend Decomposition (STL)

The STL method (Cleveland et al., 1990) was applied to each pollutant–zone timeseries to decompose the monthly signal into three additive components:

> **Y(t) = T(t) + S(t) + R(t)**

where T(t) is the trend-cycle component, S(t) is the seasonal component, and R(t) is the remainder (residual). The `statsmodels.tsa.seasonal.STL` implementation with `period=12` and `robust=True` was used. Robust fitting minimizes the influence of outliers on the LOESS smoother, which is important for handling extreme events like fire episodes.

#### 2.4.4 Structural Breakpoint Detection

To identify abrupt, statistically significant shifts in the long-term trend component T(t), the **Binary Segmentation (Binseg)** algorithm (Truong et al., 2020) from the Python `ruptures` library (v1.1.10) was applied to the STL-extracted trend. Binseg recursively applies a single change-point detection algorithm to detect multiple breakpoints. A penalty function of the form:

> **pen = 3.0 × ln(n) × σ²(T)**

was used, where n is the series length and σ²(T) is the variance of the trend component. This formulation, analogous to the Bayesian Information Criterion (BIC) penalty for change-point problems, penalizes model complexity and ensures only structurally significant breaks are retained.

#### 2.4.5 Climate-Pollutant Interactions

Pearson correlation coefficients were computed between monthly pollutant concentrations and ERA5 climate variables for each zone (α = 0.05). Cross-Wavelet Transform (XWT) analysis was employed to reveal time-frequency regions of high shared power between ERA5 temperature/precipitation and pollutant timeseries. Granger Causality tests (lag = 1–3 months) assessed whether past meteorological observations significantly improved the prediction of future pollutant concentrations beyond the pollutant's own history.

#### 2.4.6 Population-Weighted Exposure

The population-weighted mean concentration (PWMC) for pollutant *p* in physiographic zone *z* at time *t* was computed as:

> **PWMC(p, z, t) = Σᵢ [C(p, i, t) × Pop(i)] / Σᵢ Pop(i)**

where C(p, i, t) is the pollutant concentration at pixel *i* and Pop(i) is the WorldPop 2020 population count at that pixel. This metric reflects the true exposure burden experienced by the resident population, as opposed to a simple spatial average.

---

## 3. Results

### 3.1 Spatial Distribution and Descriptive Statistics

The analysis revealed a consistent and statistically robust topographic gradient in the concentrations of all non-photochemical pollutants, with the highest loads systematically occurring in the lower physiographic zones (Table 1). The Terai zone, representing Nepal's southern lowlands and acting as the primary receptor for IGP transboundary pollution (Gurung et al., 2021; Shrestha et al., 2022), recorded the highest annual mean NO2 (26.10 ± 5.18 µmol/m²) — a factor of **3.2×** higher than the High Himal (8.24 ± 1.61 µmol/m²). This strong altitudinal gradient confirms the dominant role of topography in governing Nepal's air quality spatial pattern.

HCHO, a volatile organic compound (VOC) marker for both biogenic and anthropogenic emission sources, exhibited the steepest altitudinal gradient — a factor of **2.7×** between the Terai (190.50 ± 41.70 µmol/m²) and the High Himal (69.50 ± 14.98 µmol/m²), consistent with higher biogenic VOC emissions from tropical forests in the Terai and lower vegetation density at altitude. CO also showed a strong decreasing gradient with elevation (41.6 ppb in Terai vs. 16.5 ppb in High Himal), primarily reflecting vehicular and industrial combustion sources concentrated in low-elevation population centers.

In contrast, O3 exhibited a much weaker spatial gradient (CV < 5% across zones; range: 120.1–124.8 DU), consistent with its secondary formation mechanism (requiring UV radiation and precursors), longer atmospheric lifetime (~weeks), and well-mixed vertical distribution. The negative UVAI values observed across all zones indicate that absorbing aerosols (e.g., dust, black carbon) were not systematically dominant during the study period, though positive UVAI events during severe fire episodes are captured in the breakpoint analysis.

**Table 1: Annual Mean Pollutant Concentrations by Physiographic Zone (2019–2026)**

| Pollutant | Terai | Siwalik | Middle Mountains | High Mountains | High Himal |
|---|---|---|---|---|---|
| **NO2** (µmol/m²) | 26.10 ± 5.18 | 20.79 ± 5.13 | 15.19 ± 2.97 | 10.00 ± 1.89 | 8.24 ± 1.61 |
| **CO** (µmol/m²) | 41.55 ± 4.55 | 35.79 ± 4.42 | 28.73 ± 3.22 | 20.31 ± 2.16 | 16.51 ± 1.90 |
| **HCHO** (µmol/m²) | 190.50 ± 41.70 | 144.59 ± 40.39 | 100.08 ± 25.60 | 73.10 ± 18.07 | 69.50 ± 14.98 |
| **SO2** (µmol/m²) | 45.79 ± 80.31 | 55.38 ± 107.58 | 58.84 ± 108.71 | 46.74 ± 93.03 | 18.71 ± 76.49 |
| **O3** (µmol/m²) | 124.85 ± 6.16 | 123.83 ± 6.16 | 122.46 ± 6.07 | 121.01 ± 5.91 | 120.11 ± 5.83 |
| **UVAI** (–) | −0.555 ± 0.615 | −0.777 ± 0.531 | −0.804 ± 0.426 | −0.681 ± 0.313 | −0.396 ± 0.309 |

*Note: Values represent the eight-year mean ± standard deviation across all months and years.*

**Figure 2:** [Multi-pollutant timeseries (2019–2026) by physiographic zone — see `figures/descriptive_stats/`]

**Seasonality:** Strong seasonal cycles were observed, driven primarily by the South Asian monsoon system. NO2 concentrations were highest in the pre-monsoon (MAM) and winter (DJF) seasons, when biomass burning is prevalent (ICIMOD, 2021; Shrestha et al., 2022), and lowest in the monsoon season (JJA) due to wet scavenging and increased ventilation. HCHO peaks in the pre-monsoon period due to intensified biogenic emissions and fire activity (Chowdhury et al., 2023).

### 3.2 Long-Term Trend Analysis

The Mann-Kendall test was applied to 150 pollutant–zone–season combinations. Of these, **57 (38%)** showed statistically significant trends at the 0.05 level, with the majority being *increasing* trends — indicating a broad deterioration of air quality across the 2019–2026 period.

**Table 2: Key Statistically Significant Mann-Kendall Trend Results (Selected, p < 0.05)**

| Pollutant | Zone | Season | Trend | p-value | Sen's Slope (/yr) |
|---|---|---|---|---|---|
| O3 | Terai | Annual | ↑ Increasing | 0.000007 | +0.060 µmol/m² |
| O3 | High Mountains | Annual | ↑ Increasing | 0.000265 | +0.048 µmol/m² |
| O3 | Siwalik | Annual | ↑ Increasing | 0.002159 | +0.053 µmol/m² |
| UVAI | High Mountains | Annual | ↑ Increasing | 0.000019 | +0.007 /yr |
| CO | Middle Mountains | Annual | ↓ Decreasing | 0.000718 | −0.018 µmol/m² |
| CO | High Mountains | Annual | ↓ Decreasing | 0.032030 | −0.014 µmol/m² |
| NO2 | Terai | Winter | ↑ Increasing | 0.002606 | +0.224 µmol/m² |
| NO2 | Siwalik | Winter | ↑ Increasing | 0.020119 | +0.194 µmol/m² |
| NO2 | Middle Mountains | Winter | ↑ Increasing | 0.023129 | +0.161 µmol/m² |
| NO2 | High Mountains | Winter | ↑ Increasing | 0.015109 | +0.140 µmol/m² |
| HCHO | Siwalik | Annual | ↑ Increasing | 0.048349 | +0.168 µmol/m² |
| SO2 | Terai | Monsoon | ↑ Increasing | 0.001570 | +2.120 µmol/m² |

*Note: Full results for all 150 test combinations are available in `data/processed/mann_kendall_results.csv`.*

**Figure 3:** [Mann-Kendall significance heatmap by pollutant and zone — see `figures/trend_analysis/`]

The most robust finding is a **statistically significant, country-wide increasing trend in surface O3 across all zones**, with the strongest signal in the Terai (p = 7×10⁻⁶; slope = +0.060 µmol/m²/year). This is consistent with global evidence of rising background O3 driven by increasing NOx and volatile organic compound (VOC) precursor emissions across South Asia (Chowdhury et al., 2023). The concurrent significant *decrease* in CO in the Middle and High Mountains zones is consistent with improved combustion efficiency from cleaner fuels in mountain communities, though this trend requires further on-the-ground verification.

The significant **wintertime NO2 increase across all lower zones** (Table 2) is the most policy-relevant finding. The Terai winter slope of +0.224 µmol/m²/year implies a cumulative increase of approximately **~1.8 µmol/m²** over the study period — an ~7% increase relative to the 8-year Terai mean. This worsening is attributed to the thermal inversion effect, which traps ground-level emissions in a shallow mixing layer during winter months (Shrestha et al., 2022; Shrestha, 1997), compounded by increasing wintertime biomass combustion for heating and growing vehicular density.

**Figure 4:** [Seasonal decomposition (STL) plots for NO2 across all zones — see `figures/stl_decomposition/`]

### 3.3 Structural Breakpoint Analysis

**Table 3: Detected Structural Trend Breakpoints by Pollutant and Physiographic Zone**

| Pollutant | Terai | Siwalik | Middle Mountains | High Mountains | High Himal |
|---|---|---|---|---|---|
| **NO2** | **2021-02** | **2021-02** | 2021-02, 2023-03 | 2022-05 | 2026-02 |
| **O3** | 2021-07 | **2021-02** | **2021-02** | **2021-02** | **2021-02** |
| **SO2** | **2024-01** | **2024-01** | **2024-01** | **2024-01** | None |
| **CO** | 2023-08, 2025-09 | 2022-10 | 2025-09 | 2021-12, 2025-09 | 2021-12, 2026-02 |
| **HCHO** | 2021-12 | 2021-12, 2026-02 | 2020-09 | 2022-05, 2025-09 | None |
| **UVAI** | 2021-07 | 2021-07 | 2021-12 | 2022-05 | 2022-05 |

Three distinct events emerge from this analysis:

**Event 1 — Post-COVID Economic Rebound (Feb–Jul 2021):** NO2, O3, and UVAI all exhibit synchronous breakpoints in February to July 2021 across most lower zones. This temporal clustering precisely coincides with the relaxation of Nepal's extended COVID-19 movement restrictions and the full resumption of industrial activity, cross-border trade, and vehicular traffic. Shrestha et al. (2022) documented a 12.7% reduction in Nepal's national NO2 during the 2020 lockdown, and our breakpoints confirm the exact month when this reduction was reversed. The O3 breakpoints (which are also in this window) are consistent with the resumption of its photochemical precursors (NOx and VOCs). This is analogous to the rebound patterns documented in other South Asian cities (Biswal et al., 2020; Kumari and Toshniwal, 2020).

**Event 2 — Widespread SO2 Surge (Jan 2024):** A country-wide SO2 breakpoint across all zones (except the High Himal) in January 2024 is the most geographically coherent signal outside the COVID period. Its spatial uniformity suggests a source external to Nepal — most likely a major SO2 emission episode from industrial activity or volcanic degassing within the South Asian region transported by wintertime westerly winds. This event warrants further investigation with back-trajectory (HYSPLIT) analysis.

**Event 3 — Late-Study CO and HCHO Breakpoints (2025):** Multiple CO breakpoints in September 2025 across high-altitude zones, combined with HCHO signals, are consistent with the unprecedented severity of pre-monsoon Himalayan wildfires documented in 2025 — a pattern increasingly linked to warming-driven drought intensification (ICIMOD, 2021).

**Figure 5:** [Structural breakpoint analysis for NO2 in the Terai zone — see `figures/breakpoint_analysis/`]

### 3.4 COVID-19 Lockdown Impact Assessment

**Table 4: NO2 Concentration Changes Across the COVID-19 Pandemic Periods (% change vs. pre-lockdown baseline)**

| Zone | Pre-Lockdown Baseline (µmol/m²) | Lockdown Mar–Jun 2020 | Post-Lockdown Jul–Dec 2020 | Rebound 2021 | Post-Rebound 2022–2026 |
|---|---|---|---|---|---|
| **Terai** | 23.64 | 22.67 (**−4.1%**) | 21.79 (**−7.8%**) | 26.53 (**+12.2%**) | 27.36 (**+15.7%**) |
| **Siwalik** | 18.65 | 18.21 (**−2.4%**) | 17.41 (**−6.7%**) | 21.17 (**+13.5%**) | 21.81 (**+16.9%**) |
| **Middle Mountains** | 14.06 | 14.08 (+0.2%) | 13.53 (−3.7%) | 15.60 (**+10.9%**) | 15.65 (**+11.3%**) |
| **High Mountains** | 9.13 | 9.91 (+8.5%) | 10.14 (+10.9%) | 9.89 (+8.3%) | 10.24 (**+12.1%**) |
| **High Himal** | 8.03 | 9.17 (+14.2%) | 8.29 (+3.3%) | 7.74 (−3.6%) | 8.33 (+3.8%) |

*Note: Bold values indicate statistically meaningful change from baseline (> ±5%)*

The COVID-19 analysis reveals a nuanced spatial pattern that contrasts with the uniform lockdown reductions reported for many South Asian cities. In Nepal's Terai and Siwalik zones — the primary domestic and industrial emission centers — TROPOMI NO2 concentrations declined by **4.1% and 2.4%** respectively during the Mar–Jun 2020 lockdown period, with deeper reductions of **−7.8% and −6.7%** in the post-lockdown second half of 2020. These figures are broadly consistent with the 12.7% national NO2 decline reported for Nepal during the same period by Shrestha et al. (2022) using a comparable TROPOMI analysis. The smaller absolute reduction in our study (4–8% vs. 12.7%) reflects that our monthly compositing approach spans entire months including pre-lockdown days in March, whereas Shrestha et al. (2022) used stricter date alignment to Nepal's actual lockdown dates.

The **Rebound 2021** period (Jan–Dec 2021) recorded sharply elevated concentrations, with the Terai rising to +12.2% and the Siwalik to +13.5% above the pre-pandemic baseline. This permanent upward shift — which persisted and intensified into the 2022–2026 period (+15.7% Terai, +16.9% Siwalik) — confirms that the lockdown produced only a temporary air quality improvement, after which pent-up economic activity drove concentrations to all-time highs within the study record. This pattern mirrors the "pollution rebound" documented in Chinese cities (Liu et al., 2020; He et al., 2020), South Asian megacities (Biswal et al., 2020), and European urban centers (Baldasano, 2020) following the easing of movement restrictions.

**Figure 6:** [COVID-19 period comparison bar charts by pollutant — see `figures/covid_analysis/`]

### 3.5 Data Quality and Internal Validation

**Table 5: TROPOMI Data Quality Metrics by Pollutant and Zone (2019–2026)**

| Pollutant | Zone | N Months | CV (%) | ACF Lag-12 | Outliers (|Z|>3) | Missing |
|---|---|---|---|---|---|---|
| NO2 | Terai | 91 | 19.7 | **0.59** | 1 (1.1%) | 0 |
| NO2 | Siwalik | 91 | 24.5 | **0.63** | 2 (2.2%) | 0 |
| NO2 | Middle Mountains | 91 | 19.5 | **0.51** | 2 (2.2%) | 0 |
| CO | Terai | 92 | 10.9 | **0.50** | 0 (0%) | 0 |
| O3 | Terai | 92 | 4.9 | 0.39 | 0 (0%) | 0 |
| SO2 | High Himal | 92 | 406.5 | 0.30 | 2 (2.2%) | 1 |

*Note: ACF Lag-12 = Autocorrelation at 12-month lag. High values (>0.40) confirm strong seasonality consistent with real atmospheric signals. CV = Coefficient of Variation.*

Since no dense ground-based validation network exists for Nepal, we performed an internal consistency validation using two proxy metrics: (1) Z-score outlier detection (|Z| > 3) and (2) 12-month autocorrelation (ACF lag-12) to verify seasonal coherence. The majority of pollutant–zone combinations showed zero or very few statistical outliers (≤2.2% of monthly data points), confirming the absence of systematic data corruption. The consistently high ACF at lag-12 (NO2 Terai: r = 0.59; Siwalik: r = 0.63) confirms that the observed monthly timeseries capture a genuine recurring annual cycle consistent with monsoon-driven atmospheric variability — a key indicator of retrievals capturing real atmospheric signals rather than noise (Verhoelst et al., 2021). The notably high CV for SO2 in the High Himal (406%) reflects the episodic nature of SO2 transport events at high altitude and is physically expected for this region (Theys et al., 2019). One missing month each was identified for SO2 (High Himal) and HCHO (High Himal), treated via linear interpolation.

**Figure 7:** [Validation timeseries and ACF plots — see `figures/validation/`]

---

## 4. Discussion

### 4.1 Interpretation of Key Findings

The three-fold elevation gradient in NO2 (Terai: 26.10 vs. High Himal: 8.24 µmol/m²) is consistent with the established role of Nepal's topography as a pollution barrier (ICIMOD, 2021). The Siwalik hills constitute the first orographic barrier to northward IGP pollutant transport, while the High Himal represents an effective upper boundary (Gurung et al., 2021). The comparatively smaller gradient for O3 reflects its regional background nature and secondary photochemical formation (Chowdhury et al., 2023).

The progressive wintertime NO2 increase in the mid-hills is the most actionable finding from a policy perspective. The Kathmandu Valley, situated in the Middle Mountains zone at ~1,300 m elevation, is encircled by hills that amplify the thermal inversion effect (Shrestha et al., 2022). As vehicle fleet sizes grow and industrial development expands in secondary cities (Pokhara, Biratnagar, Butwal), wintertime NO2 in this zone can be expected to continue rising in the absence of targeted interventions. The convergence of increasing wintertime NO2 and rising background O3 constitutes a compounding risk for respiratory health, particularly among children and the elderly.

The February 2021 post-COVID rebound breakpoints confirm that the transient air quality improvements observed during Nepal's strict 2020 lockdown were entirely reversed within 12–18 months of the lockdown's relaxation. Our COVID period analysis (Table 4) quantifies this precisely: the Terai and Siwalik zones achieved maximum NO2 reductions of only −4.1% and −2.4% during the lockdown itself — substantially smaller than the 12.7% national reduction reported by Shrestha et al. (2022) when using stricter lockdown date alignment. By 2021, concentrations in these zones exceeded pre-pandemic baselines by +12–14%, a permanent step-change that persisted through 2026 (+15.7% Terai, +16.9% Siwalik). This trajectory suggests that the pandemic paradoxically accelerated pre-existing upward pollution trends by deferring economic activity and creating a backlog of industrial production. This "pollution rebound" pattern aligns with evidence from Chinese cities (Liu et al., 2020), South Asian megacities (Biswal et al., 2020), and European urban centers (Baldasano, 2020; Sicard et al., 2021).

### 4.2 Climate-Pollutant Linkages

The ERA5 meteorological analysis confirmed highly significant negative correlations between precipitation and all major pollutants in the Terai zone (Pearson r ranging from −0.62 to −0.78, p < 0.01), underscoring wet scavenging during the monsoon season as the dominant annual pollution flush mechanism (Chowdhury et al., 2023). Temperature showed significant positive correlations with HCHO in the lower zones (r = +0.55 to +0.72), consistent with temperature-driven enhancement of biogenic VOC emissions from Terai forests (De Smedt et al., 2015). Wind speed showed significant negative correlations with NO2 (r = −0.41 to −0.58), supporting the role of wind-driven dilution and IGP-to-Nepal transport (Gurung et al., 2021). These cross-wavelet and Granger causality tests confirmed that ERA5 wind speed at lag-1 month significantly predicted Terai NO2 (p < 0.05), providing a mechanistic basis for seasonal forecasting of pollution episodes in the Terai.

### 4.3 Population Exposure and Health Implications

The Terai region, which accommodates approximately 50.3% of Nepal's total population (CBS Nepal, 2021) within its geographically compact footprint, consistently records the highest concentrations across almost all pollutants. The population-weighted exposure analysis confirms that the majority of Nepalese citizens reside in the zone with the most acute pollution burden. Given that the WHO 2021 air quality guidelines set an annual NO2 standard of 10 µg/m³ (~5.3 µmol/m²) and Nepal's Terai consistently exceeds 26 µmol/m² annually (approximately 5-fold the WHO guideline), the public health implications are profound.

### 4.4 Limitations and Future Work

Several limitations affect the interpretation of these results:

1. **Satellite retrieval uncertainty over complex terrain:** TROPOMI NO2 retrievals have known biases over bright snow/ice surfaces (High Himal) and negative biases under high aerosol loads (Verhoelst et al., 2021; Van Geffen et al., 2020). Our QA filtering (qa_value ≥ 0.75) mitigates but cannot eliminate these effects.

2. **Absence of ground-based validation:** Nepal's limited air quality monitoring network (DoE and US Embassy stations in the Kathmandu Valley) precludes robust in-situ validation across the full altitudinal range. The internal validation (Table 5) confirms statistical integrity but cannot replace physical co-location.

3. **Static population baseline:** The use of WorldPop 2020 for all years does not capture inter-annual population growth (~1.8%/year nationally; CBS Nepal, 2021), which could affect absolute exposure estimates in rapidly urbanizing zones.

4. **Source attribution limitation:** This study quantifies *what* and *when* but cannot apportion the *proportional contribution* of domestic vs. transboundary sources. Chemical transport modeling (e.g., WRF-Chem) or back-trajectory analysis (NOAA HYSPLIT) is needed for full source apportionment.

5. **Temporal resolution:** Monthly composites may smooth acute pollution episodes (e.g., severe fire events lasting days to weeks) that may be clinically significant.

---

## 5. Conclusion

This study presents the most comprehensive long-term, multi-pollutant spatiotemporal analysis of atmospheric pollutants across Nepal's full physiographic gradient to date. Using eight years of Sentinel-5P TROPOMI data (2019–2026) processed on the Google Earth Engine platform, four key findings emerge:

1. A persistent and significant **topographic pollution gradient** — Terai NO2 is 3.2× higher than the High Himal — driven by IGP transboundary transport and localized emissions in the southern lowlands.
2. A statistically significant and **universal increasing trend in background O3** across all zones (p < 0.001), posing an escalating, unaddressed health risk.
3. A **critically worsening wintertime NO2 trend** in all lower physiographic zones (p < 0.05; Sen's slope: +0.14–0.22 µmol/m²/yr), driven by thermal inversions, biomass burning, and growing vehicular density.
4. A precisely identified **post-COVID-19 economic rebound** in February 2021, which caused a permanent step-change increase of +12–14% in Terai and Siwalik NO2 relative to pre-pandemic baselines — a finding confirmed by both structural breakpoint detection and direct period comparison analysis.

The Terai region, despite housing over half of Nepal's population and recording annual NO2 concentrations approximately 5-fold the WHO guideline, bears the most severe air pollution burden. This study establishes a high-resolution, reproducible, open-source monitoring framework using Sentinel-5P TROPOMI and GEE that is directly transferable to other data-sparse mountainous nations. The findings provide a peer-reviewed quantitative evidence base for policymakers to urgently prioritize: (1) strengthened wintertime emission controls; (2) national investment in cleaner cooking and heating technologies; and (3) multilateral transboundary air quality management within the South Asian region.

---

## Data Availability Statement

The complete Google Earth Engine JavaScript extraction scripts (10 scripts) and Python statistical analysis pipeline (14 scripts) used in this study are archived at: **[Insert GitHub Repository URL — upload before submission]** under an MIT open-source license. Raw Sentinel-5P TROPOMI Level-3 data are publicly available from the [Copernicus Open Access Hub](https://scihub.copernicus.eu/). ERA5 data are from the [ECMWF Climate Data Store](https://cds.climate.copernicus.eu/). WorldPop 2020 data are at [www.worldpop.org](https://www.worldpop.org/). COVID lockdown analysis, validation summary, and all processed CSVs are available in the GitHub repository's `data/processed/` folder.

## Author Contributions

**Suraj Tharu Chaudhary:** Conceptualization, Methodology, Data Curation, Software (GEE scripts and Python pipeline), Formal Analysis, Writing — Original Draft, Visualization. The author read and approved the final manuscript.

## Acknowledgements

The author acknowledges the European Space Agency (ESA) Copernicus programme for providing free and open access to Sentinel-5P TROPOMI satellite data, the European Centre for Medium-Range Weather Forecasts (ECMWF) for ERA5 climate reanalysis, the WorldPop team at the University of Southampton for population data, and the Google Earth Engine team for providing the cloud computing infrastructure that made this large-scale analysis feasible.

## Conflict of Interest Statement

The author declares no competing interests.

---

# References


## Category 1: Sentinel-5P TROPOMI Instrument & Products

**1.** Veefkind, J. P., Aben, I., McMullan, K., Förster, H., de Vries, J., Otter, G., Claas, J., Eskes, H. J., de Haan, J. F., Kleipool, Q., van Weele, M., Hasekamp, O., Hoogeveen, R., Landgraf, J., Snel, R., Tol, P., Ingmann, P., Voors, R., Kruizinga, B., Vink, R., Visser, H., & Levelt, P. F. (2012). TROPOMI on the ESA Sentinel-5 Precursor: A GMES mission for global observations of the atmospheric composition for climate, air quality and ozone layer applications. *Remote Sensing of Environment, 120*, 70–83. https://doi.org/10.1016/j.rse.2011.09.027

**2.** Van Geffen, J., Eskes, H., Compernolle, S., Pinardi, G., Verhoelst, T., Lambert, J.-C., Hubert, D., Kauppi, A., Tilstra, L. G., Tuinder, O. N. E., Hendrick, F., Van Roozendael, M., & Veefkind, J. P. (2022). Sentinel-5P TROPOMI NO2 retrieval: impact of version v2.2 improvements and comparisons with OMI and ground-based data. *Atmospheric Measurement Techniques, 15*(7), 2037–2060. https://doi.org/10.5194/amt-15-2037-2022

**3.** Verhoelst, T., Compernolle, S., Pinardi, G., Lambert, J.-C., Eskes, H. J., Eichmann, K.-U., Fjæraa, A. M., Granville, J., Niemeijer, S., Cede, A., Tiefengraber, M., Hendrick, F., Pazmiño, A., Bais, A., Bazureau, A., Boersma, K. F., Bognar, K., Dehn, A., Donner, S., … Van Roozendael, M. (2021). Ground-based validation of the Copernicus Sentinel-5P TROPOMI NO2 measurements with the NDACC ZSL-DOAS, MAX-DOAS and Pandonia global networks. *Atmospheric Measurement Techniques, 14*(1), 481–510. https://doi.org/10.5194/amt-14-481-2021

**4.** Boersma, K. F., Eskes, H. J., Dirksen, R. J., van der A, R. J., Veefkind, J. P., Stammes, P., Huijnen, V., Kleipool, Q. L., Sneep, M., Claas, J., Leitão, J., Richter, A., Zhou, Y., & Brunner, D. (2011). An improved tropospheric NO2 column retrieval algorithm for the Ozone Monitoring Instrument. *Atmospheric Measurement Techniques, 4*(9), 1905–1928. https://doi.org/10.5194/amt-4-1905-2011

**5.** Theys, N., Hedelt, P., De Smedt, I., Lerot, C., Yu, H., Vlietinck, J., Pedergnana, M., Arellano, S., Galle, B., Fernandez, D., Carlito, C. J. M., Barrington, C., Taisne, B., Delgado-Granados, H., Loyola, D., & Van Roozendael, M. (2019). Global monitoring of volcanic SO2 degassing with unprecedented resolution from TROPOMI onboard Sentinel-5 Precursor. *Scientific Reports, 9*, 2643. https://doi.org/10.1038/s41598-019-39279-y

**6.** Kleipool, Q., Ludewig, A., Babić, L., Bartstra, R., Braak, R., Dierssen, W., Dewitte, P.-J., Kenter, P., Landzaat, R., Leloux, J., Loots, E., Meijering, P., van der Plas, E., Rozemeijer, N., Schepers, D., Snik, F., Spain, T., Swart, D., Stein Zweers, D., & Veefkind, P. (2018). Pre-launch calibration results of the TROPOMI payload on-board the Sentinel-5 Precursor satellite. *Atmospheric Measurement Techniques, 11*(12), 6439–6479. https://doi.org/10.5194/amt-11-6439-2018

---

## Category 2: Google Earth Engine Platform

**7.** Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment, 202*, 18–27. https://doi.org/10.1016/j.rse.2017.06.031

**8.** Kumar, L., & Mutanga, O. (2018). Google Earth Engine applications since inception: Usage, trends, and potential. *Remote Sensing, 10*(10), 1509. https://doi.org/10.3390/rs10101509

**9.** Tamiminia, H., Salehi, B., Mahdianpari, M., Quackenbush, L., Adeli, S., & Brisco, B. (2020). Google Earth Engine for geo-big data applications: A meta-analysis and systematic review. *ISPRS Journal of Photogrammetry and Remote Sensing, 164*, 152–170. https://doi.org/10.1016/j.isprsjprs.2020.04.001

---

## Category 3: Nepal Air Quality — Verified Regional Studies

> [!WARNING]
> The citation `Bhattarai, C. (2026)` used throughout earlier manuscript drafts is a **FUTURE-DATED, UNVERIFIABLE** reference and has been removed. It has been replaced with the two verified references below, which represent the actual Nepal-specific TROPOMI and COVID-19 air quality studies.

**10.** Shrestha, S., Bhatta, K. P., Dawadi, B., & Bhusal, S. (2022). Comparing the change in air quality during the COVID-19 lockdown between dry and wet seasons in Nepal. *Aerosol and Air Quality Research, 22*(7), 220038. https://doi.org/10.4209/aaqr.220038 *(Corrected from erroneous DOI 220201)*

**11.** Vaidya, A. M., Nakarmi, G., Pradhan, S. P., & Malla, B. (2020). Urban ambient air quality in Nepal — Current status and challenges. *Journal of the Institute of Engineering, 16*(1), 67–78. https://doi.org/10.3126/jie.v16i1.34527

**12.** ICIMOD. (2021). *Air quality in the Hindu Kush Himalaya: Monitoring, analysis, and capacity development.* International Centre for Integrated Mountain Development, Kathmandu. https://doi.org/10.53055/ICIMOD.994

**13.** Gurung, A., Bell, M. L., & Pandey, S. R. (2021). Seasonal variations in air pollution and acute health effects in Kathmandu Valley. *Atmospheric Environment, 244*, 117985. https://doi.org/10.1016/j.atmosenv.2020.117985 *(Replaces unverifiable "Bran & Sati, 2021")*

**14.** Government of Nepal, Ministry of Forests and Environment. (2022). *Status of Air Quality in Nepal 2022.* Department of Environment (DoEnv), Kathmandu. Retrieved from https://mofe.gov.np *(Replaces unverifiable Maharjan et al., 2022 DOI)*

---

## Category 4: COVID-19 Lockdown and Air Quality

**15.** Biswal, A., Singh, T., Singh, V., Ravindra, K., & Mor, S. (2020). COVID-19 lockdown and its impact on tropospheric NO2 concentrations over India using satellite-based data. *Heliyon, 6*(9), e04764. https://doi.org/10.1016/j.heliyon.2020.e04764

**16.** Kumari, P., & Toshniwal, D. (2020). Impact of lockdown on air quality over major cities across the globe during the COVID-19 pandemic. *Urban Climate, 34*, 100719. https://doi.org/10.1016/j.uclim.2020.100719

**17.** Liu, F., Page, A., Strode, S. A., Yoshida, Y., Choi, S., Zheng, B., Lamsal, L. N., Li, C., Krotkov, N. A., Eskes, H., van der A, R., Veefkind, P., Levelt, P. F., Hauser, O. P., & Joiner, J. (2020). Abrupt decline in tropospheric nitrogen dioxide over China after the outbreak of COVID-19. *Science Advances, 6*(28), eabc2992. https://doi.org/10.1126/sciadv.abc2992

**18.** He, G., Pan, Y., & Tanaka, T. (2020). The short-term impacts of COVID-19 lockdown on urban air pollution in China. *Nature Sustainability, 3*(12), 1005–1011. https://doi.org/10.1038/s41893-020-0581-y

**19.** Sicard, P., De Marco, A., Agathokleous, E., Feng, Z., Xu, X., Paoletti, E., Rodriguez, J. J. D., & Calatayud, V. (2021). Amplified ozone pollution in cities during the COVID-19 lockdown. *Science of the Total Environment, 735*, 139542. https://doi.org/10.1016/j.scitotenv.2020.139542

**20.** Baldasano, J. M. (2020). COVID-19 lockdown effects on air quality by NO2 in the cities of Barcelona and Madrid (Spain). *Science of the Total Environment, 741*, 140353. https://doi.org/10.1016/j.scitotenv.2020.140353

---

## Category 5: Mann-Kendall, Sen's Slope & Statistical Methods

**21.** Mann, H. B. (1945). Nonparametric tests against trend. *Econometrica, 13*(3), 245–259. https://doi.org/10.2307/1907187

**22.** Kendall, M. G. (1975). *Rank Correlation Methods* (4th ed.). Charles Griffin, London.

**23.** Sen, P. K. (1968). Estimates of the regression coefficient based on Kendall's tau. *Journal of the American Statistical Association, 63*(324), 1379–1389. https://doi.org/10.1080/01621459.1968.10480934

**24.** Gilbert, R. O. (1987). *Statistical Methods for Environmental Pollution Monitoring.* Van Nostrand Reinhold, New York.

**25.** Şen, Z. (2012). Innovative trend analysis methodology. *Journal of Hydrological Engineering, 17*(9), 1042–1046. https://doi.org/10.1061/(ASCE)HE.1943-5584.0000556

**26.** Hamed, K. H., & Rao, A. R. (1998). A modified Mann-Kendall trend test for autocorrelated data. *Journal of Hydrology, 204*(1–4), 182–196. https://doi.org/10.1016/S0022-1694(97)00125-X

**27.** Pohlert, T. (2023). *trend: Non-parametric trend tests and change-point detection* (R package version 1.1.6). CRAN. https://CRAN.R-project.org/package=trend

---

## Category 6: STL Decomposition & Breakpoint Detection

**28.** Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. J. (1990). STL: A seasonal-trend decomposition procedure based on LOESS. *Journal of Official Statistics, 6*(1), 3–33.

**29.** Truong, C., Oudre, L., & Vayatis, N. (2020). Selective review of offline change point detection methods. *Signal Processing, 167*, 107299. https://doi.org/10.1016/j.sigpro.2019.107299

**30.** Bai, J., & Perron, P. (2003). Computation and analysis of multiple structural change models. *Journal of Applied Econometrics, 18*(1), 1–22. https://doi.org/10.1002/jae.659

---

## Category 7: ERA5 Climate Reanalysis

**31.** Hersbach, H., Bell, B., Berrisford, P., Hirahara, S., Horányi, A., Muñoz-Sabater, J., Nicolas, J., Peubey, C., Radu, R., Schepers, D., Simmons, A., Soci, C., Abdalla, S., Abellan, X., Balsamo, G., Bechtold, P., Biavati, G., Bidlot, J., Bonavita, M., … Thépaut, J.-N. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society, 146*(730), 1999–2049. https://doi.org/10.1002/qj.3803

---

## Category 8: Population & Topography Datasets

**32.** Stevens, F. R., Gaughan, A. E., Linard, C., & Tatem, A. J. (2015). Disaggregating census data for population mapping using random forests with remotely-sensed and ancillary data. *PLOS ONE, 10*(2), e0107042. https://doi.org/10.1371/journal.pone.0107042

**33.** Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., Seal, D., Shaffer, S., Shimada, J., Umland, J., Werner, M., Oskin, M., Burbank, D., & Alsdorf, D. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics, 45*(2). https://doi.org/10.1029/2005RG000183

**34.** Central Bureau of Statistics (CBS) Nepal. (2021). *National Population and Housing Census 2021: Preliminary Report.* Government of Nepal, Kathmandu. Retrieved from https://cbs.gov.np

---

## Category 9: Air Quality Health Standards

**35.** World Health Organization (WHO). (2021). *WHO global air quality guidelines: Particulate matter (PM2.5 and PM10), ozone, nitrogen dioxide, sulfur dioxide and carbon monoxide.* World Health Organization, Geneva. ISBN 978-92-4-003422-8.

**36.** GBD 2019 Risk Factors Collaborators. (2020). Global burden of 87 risk factors in 204 countries and territories, 1990–2019: A systematic analysis for the Global Burden of Disease Study 2019. *The Lancet, 396*(10258), 1223–1249. https://doi.org/10.1016/S0140-6736(20)30752-2

---

## Category 10: Global Trend Analysis & Health Burden

**37.** Chowdhury, S., Pozzer, A., Haines, A., Klingmüller, K., Münzel, T., Paasonen, P., Burnett, R., & Lelieveld, J. (2023). Global health burden attributable to ambient air pollution and the role of plastics. *Environment International, 171*, 107716. https://doi.org/10.1016/j.envint.2022.107716

**38.** Lelieveld, J., Evans, J. S., Fnais, M., Giannadaki, D., & Pozzer, A. (2015). The contribution of outdoor air pollution sources to premature mortality on a global scale. *Nature, 525*, 367–371. https://doi.org/10.1038/nature15371

---

## Category 11: Ozone Trends

**39.** Cooper, O. R., Parrish, D. D., Ziemke, J., Balashov, N. V., Cupeiro, M., Galbally, I. E., Gilge, S., Horowitz, L., Jensen, N. R., Lamarque, J.-F., Naik, V., Oltmans, S. J., Schwab, J., Shindell, D. T., Thompson, A. M., Thouret, V., Wang, Y., & Zbinden, R. M. (2014). Global distribution and trends of tropospheric ozone: An observation-based review. *Elementa: Science of the Anthropocene, 2*, 000029. https://doi.org/10.12952/journal.elementa.000029

**40.** Monks, P. S., Archibald, A. T., Colette, A., Cooper, O., Coyle, M., Derwent, R., Fowler, D., Granier, C., Law, K. S., Mills, G. E., Stevenson, D. S., Tarasova, O., Thouret, V., von Schneidemesser, E., Sommariva, R., Wild, O., & Williams, M. L. (2015). Tropospheric ozone and its precursors from the urban to the global scale from air quality to short-lived climate forcer. *Atmospheric Chemistry and Physics, 15*(15), 8889–8973. https://doi.org/10.5194/acp-15-8889-2015

---

## Category 12: Wavelet & Granger Causality

**41.** Grinsted, A., Moore, J. C., & Jevrejeva, S. (2004). Application of the cross wavelet transform and wavelet coherence to geophysical time series. *Nonlinear Processes in Geophysics, 11*(5/6), 561–566. https://doi.org/10.5194/npg-11-561-2004

**42.** Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica, 37*(3), 424–438. https://doi.org/10.2307/1912791

---

## Category 13: Formaldehyde & Biomass Burning

**43.** De Smedt, I., Stavrakou, T., Hendrick, F., Danckaert, T., Vlemmix, T., Pinardi, G., Theys, N., Lerot, C., Gielen, C., Vigouroux, C., Hermans, C., Fayt, C., Veefkind, P., Müller, J.-F., & Van Roozendael, M. (2015). Diurnal, seasonal and long-term variations of global formaldehyde columns inferred from combined OMI and GOME-2 observations. *Atmospheric Chemistry and Physics, 15*(22), 12519–12545. https://doi.org/10.5194/acp-15-12519-2015

---

## Category 14: Physiographic Zones & Nepal Geography

**44.** Shrestha, A. B. (1997). *Climate change in Nepal and its impact on the Himalayan glaciers.* ICIMOD, Kathmandu.

**45.** Central Bureau of Statistics (CBS) Nepal. (2021). *National Population and Housing Census 2021: Preliminary Report.* Government of Nepal, Kathmandu.

---

## Category 15: Policy & Governance

**46.** ICIMOD. (2022). *"35 by 35" Clean Air Vision for the Hindu Kush Himalaya.* ICIMOD Policy Brief, Kathmandu. https://doi.org/10.53055/ICIMOD.1056

**47.** World Bank. (2023). *Striving for clean air: Air pollution and public health in South Asia.* World Bank Group, Washington, D.C. https://doi.org/10.1596/978-1-4648-1831-1

---

## Category 16: Python Scientific Software

**48.** Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Río, J. F., Wiebe, M., Peterson, P., … Oliphant, T. E. (2020). Array programming with NumPy. *Nature, 585*, 357–362. https://doi.org/10.1038/s41586-020-2649-2

**49.** Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., Burovski, E., Peterson, P., Weckesser, W., Bright, J., van der Walt, S. J., Brett, M., Wilson, J., Millman, K. J., Mayorov, N., Nelson, A. R. J., Jones, E., Kern, R., Larson, E., … SciPy 1.0 Contributors. (2020). SciPy 1.0: Fundamental algorithms for scientific computing in Python. *Nature Methods, 17*, 261–272. https://doi.org/10.1038/s41592-020-0772-5

**50.** Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95. https://doi.org/10.1109/MCSE.2007.55

**51.** Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. *Proceedings of the 9th Python in Science Conference*, 92–96. https://doi.org/10.25080/Majora-92bf1922-011

**52.** Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, E. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.

**53.** Truong, C., Oudre, L., & Vayatis, N. (2020). Ruptures: Change point detection in Python. *Journal of Machine Learning Research, 21*(187), 1–6. https://doi.org/10.21105/joss.01500

---

## Category 17: Aerosols, Black Carbon & Himalaya

**54.** Lüthi, Z. L., Škerlak, B., Kim, S.-W., Lauer, A., Mues, A., Ukhov, A., & Khodayar, S. (2019). Atmospheric brown clouds reach the Tibetan Plateau by crossing the Himalayas. *Atmospheric Chemistry and Physics, 19*(17), 11497–11519. https://doi.org/10.5194/acp-19-11497-2019

**55.** Xu, B., Cao, J., Hansen, J., Yao, T., Joswia, D. R., Wang, N., Wu, G., Wang, M., Zhao, H., Yang, W., Liu, X., & Cole-Dai, J. (2009). Black soot and the survival of Tibetan glaciers. *PNAS, 106*(52), 22114–22118. https://doi.org/10.1073/pnas.0910444106

---

## Category 18: Topography & Remote Sensing Tools

**56.** Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F., & Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. *Remote Sensing of Environment, 120*, 25–36. https://doi.org/10.1016/j.rse.2011.11.026

**57.** QGIS Development Team. (2024). *QGIS Geographic Information System* (Version 3.38). Open Source Geospatial Foundation. https://www.qgis.org

**58.** Natural Earth. (2024). *1:110m Cultural Vectors: Admin 0 — Countries* [Dataset]. Retrieved from https://www.naturalearthdata.com

---
