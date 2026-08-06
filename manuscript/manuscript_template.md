# [Insert Title Here]

**Target Journal:** [e.g., Science of the Total Environment]
**Authors:** [Your Name], [Co-authors]

## Abstract
[Background] Air pollution in Nepal is characterized by complex spatiotemporal dynamics driven by rugged topography, seasonal emissions, and meteorology. While localized studies exist, national-scale multi-pollutant assessments remain scarce. [Objectives] This study characterizes the spatiotemporal evolution, trend breakpoints, and climate linkages of six atmospheric pollutants (NO₂, SO₂, CO, O₃, HCHO, UV Aerosol Index) across Nepal's five physiographic zones from 2019 to 2025 using Sentinel-5P TROPOMI data processed via Google Earth Engine. [Methods] We integrated Mann-Kendall trend tests, Seasonal-Trend decomposition (STL), Breaks For Additive Season and Trend (BFAST), and Emerging Hotspot Analysis (EHSA). Furthermore, Wavelet Transform Coherence (WTC) and Granger causality were applied to elucidate relationships with ERA5 climate variables (temperature, precipitation, wind). [Results] [Insert 3-4 key quantitative findings, e.g., NO2 trend, BFAST detection of COVID lockdown effect, predominant hotspot categories from EHSA]. [Conclusions] These findings highlight the critical role of [insert conclusion], emphasizing the need for zone-specific mitigation strategies and offering a robust framework for monitoring air quality in data-sparse mountainous regions.

---

## 1. Introduction
Air pollution in the Hindu Kush Himalayan (HKH) region—and specifically in Nepal—poses a severe threat to public health, glacial ecosystems, and regional climate stability. Nepal is characterized by complex topography, spanning from the low-elevation Terai plains (60 m above sea level) to the High Himalayas (8,848 m). This extreme elevational gradient dictates highly localized microclimates that trap anthropogenic emissions, particularly during the dry winter and pre-monsoon seasons when thermal inversions are common. While the Kathmandu Valley has been the focus of numerous air quality studies (mostly relying on limited ground-based $PM_{2.5}$ sensors), a comprehensive, national-scale assessment of trace gases and aerosols across all physiographic zones remains critically absent in the literature. 

The advent of the Sentinel-5 Precursor (Sentinel-5P) Tropospheric Monitoring Instrument (TROPOMI) has revolutionized environmental monitoring in data-sparse regions. With its unprecedented spatial resolution of up to 5.5 × 3.5 km, TROPOMI enables the daily tracking of key pollutants including nitrogen dioxide ($NO_2$), sulfur dioxide ($SO_2$), carbon monoxide ($CO$), ozone ($O_3$), formaldehyde ($HCHO$), and the UV Aerosol Index (UVAI). Recent studies have utilized Sentinel-5P to monitor the dramatic drop in pollutants during the 2020 COVID-19 lockdowns, as well as to quantify emissions from regional forest fires. However, these studies typically employ standard linear regression or simple spatial mapping, which fail to capture the non-stationary, complex dynamics of atmospheric chemistry.

To address these limitations, this study proposes a novel, layered analytical framework that moves beyond static hotspot detection. First, we integrate **Emerging Hotspot Analysis (EHSA)** through a Space-Time Cube approach. While traditional spatial statistics identify clusters at a single point in time, EHSA categorizes the temporal evolution of these clusters (e.g., "Intensifying", "Persistent", or "Diminishing" hotspots). Second, we employ **Breaks For Additive Season and Trend (BFAST)** to decouple long-term gradual trends from abrupt structural breaks caused by policy interventions or extreme events (e.g., wildfires). Finally, because air pollution is inextricably linked to meteorology, we utilize **Wavelet Transform Coherence (WTC)** and **Granger Causality**. WTC is uniquely suited for environmental data as it resolves the time-frequency relationship between non-stationary signals, revealing localized phase differences (e.g., anti-phase relationships between rainfall and aerosols) that traditional Pearson correlations miss.

By systematically applying this 7-layer framework across Nepal’s five physiographic zones from 2019 to 2025, this study aims to: (1) map the spatiotemporal evolution of six atmospheric pollutants, (2) identify critical trend breakpoints, (3) classify emerging pollution hotspots, and (4) elucidate the multi-scale coupling mechanisms between meteorological drivers (ERA5) and air quality. Ultimately, this research provides a robust, scalable blueprint for monitoring population exposure in complex, data-sparse mountainous terrains globally.

## 2. Materials and Methods

### 2.1 Study Area and Physiographic Zonation
Nepal (26°22′ to 30°27′ N, 80°04′ to 88°12′ E) covers an area of 147,181 $km^2$. To account for the drastic topographical and climatic variations, the country was stratified into five physiographic zones based on a Digital Elevation Model (DEM): Terai (<300 m), Siwalik (300–1,500 m), Middle Mountains (1,500–3,000 m), High Mountains (3,000–5,000 m), and High Himal (>5,000 m).
*Figure 1: Study area map indicating the five physiographic zones and major urban centers.*

### 2.2 Data Acquisition and Preprocessing
We utilized the Google Earth Engine (GEE) cloud computing platform to process Level-3 Sentinel-5P TROPOMI datasets from January 2019 to December 2025. We extracted tropospheric column densities for $NO_2$, $SO_2$, $CO$, $O_3$, $HCHO$, and absorbing aerosol index (UVAI). To ensure data reliability, rigorous Quality Assurance (QA) filters were applied (e.g., $qa\_value > 0.75$ for $NO_2$ and $> 0.5$ for $CO$). Meteorological variables—specifically 2m temperature, total precipitation, and wind vectors (u- and v-components)—were sourced from the ERA5-Land monthly aggregated dataset. Population data for exposure assessment was derived from WorldPop (1 km resolution).

### 2.3 Trend Analysis and Structural Break Detection
Long-term monotonic trends were assessed using the non-parametric **Mann-Kendall (MK) test** coupled with the **Theil-Sen slope estimator** to quantify the magnitude of change. To visualize trends without relying on normality assumptions, **Innovative Trend Analysis (ITA)** was also plotted.
To separate seasonal cycles from underlying trends and identify abrupt anomalies, we applied **Seasonal-Trend decomposition using LOESS (STL)**. Subsequently, **Breaks For Additive Season and Trend (BFAST)** was executed on the de-seasonalized time series to detect statistically significant structural breaks (e.g., shifts coinciding with national COVID-19 lockdowns in 2020 or extreme wildfire outbreaks).

### 2.4 Emerging Hotspot Analysis (EHSA)
The spatial dynamics of pollution clusters were analyzed using the **Emerging Hotspot Analysis** tool within a Space-Time Cube framework. First, the study area was aggregated into a 10 km × 10 km spatial grid with monthly time steps. The Getis-Ord $Gi^*$ statistic was calculated for each spatial bin over time. Finally, the Mann-Kendall trend test was applied to the time series of $Gi^*$ z-scores at each location to classify hotspots into 8 discrete categories, including *New*, *Consecutive*, *Intensifying*, *Persistent*, and *Diminishing* hotspots.

### 2.5 Climate-Pollution Coupling Mechanisms
The relationship between atmospheric pollutants and meteorological parameters was evaluated across multiple domains. First, **Pearson and Partial correlations** were computed to establish baseline linear relationships. 
To investigate non-stationary, scale-dependent interactions, we employed **Wavelet Transform Coherence (WTC)**. WTC decomposes the time series into time-frequency space, identifying periods where pollutants and climate variables co-oscillate. Phase arrows within the WTC spectra were used to interpret leading or lagging relationships (in-phase or anti-phase). Finally, **Granger Causality** tests were performed at lags of 1 to 6 months to determine whether historical meteorological data provides statistically significant information for predicting current pollutant levels.

## 3. Results

### 3.1 Spatiotemporal Distribution of Pollutants
*   Present annual/seasonal mean maps.
*   Discuss differences across physiographic zones.
*   *Figure 2: Spatial distribution maps.*

### 3.2 Long-term Trends and Structural Breaks
*   Present MK and Theil-Sen results.
*   Discuss BFAST breakpoints (relate to known events like 2020 lockdowns or 2021/2023 severe wildfire seasons).
*   *Figure 3: Trend significance heatmaps and BFAST plots.*

### 3.3 Evolution of Pollution Hotspots (EHSA)
*   Present the results of the Emerging Hotspot Analysis.
*   Identify where hotspots are "Intensifying" vs. "Diminishing".
*   *Figure 4: EHSA classification map (The Flagship Figure).*

### 3.4 Pollutant-Climate Interactions
*   Present correlation matrices.
*   Discuss Wavelet Coherence findings (e.g., strong annual coherence with precipitation, identifying phase lags).
*   *Figure 5: Wavelet coherence spectra and correlation heatmaps.*

### 3.5 Population Exposure Assessment
*   Present population-weighted exposure by province/zone.
*   *Table 1: Population exposure metrics.*

## 4. Discussion
*   **Interpretation of Findings:** Why do these patterns exist? (e.g., topographical trapping in Middle Mountains, transboundary transport in Terai).
*   **Comparison with Previous Studies:** How does this align or conflict with existing literature in South Asia?
*   **Policy Implications:** How can these results inform SDG 3 (Good Health) and SDG 11 (Sustainable Cities) in Nepal?
*   **Limitations:** Acknowledge S5P retrieval uncertainties over snow/ice and complex terrain, and the lack of extensive ground validation data.

## 5. Conclusion
*   Briefly summarize the main findings and reiterate the value of the methodological framework for similar regions globally.

## References
[Insert references formatted to target journal style]
