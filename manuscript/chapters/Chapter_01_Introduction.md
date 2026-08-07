# Chapter 1: Introduction

## 1.1 Background of the Study
The deteriorating air quality in South Asia is a pressing environmental and public health crisis, severely impacting the densely populated Indo-Gangetic Plain (IGP) and extending its influence into the fragile Himalayan ecosystems. Nepal, positioned strategically along the northern edge of the IGP, experiences unique atmospheric dynamics dictated by its dramatic altitudinal variations. The complex topography—ranging from 60 meters above sea level in the southern Terai to over 8,800 meters in the High Himal—creates a series of distinct micro-climates that profoundly influence the transport, accumulation, and dispersion of atmospheric trace gases and aerosols. While the Terai acts as a primary sink for both transboundary pollution and localized agricultural burning emissions, the mid-hill valleys (such as Kathmandu) are prone to severe winter temperature inversions that trap vehicular and industrial pollutants. Meanwhile, the high-altitude cryosphere is increasingly vulnerable to the deposition of light-absorbing aerosols (like black carbon and dust) and precursor gases (NO₂, SO₂, CO), which accelerate glacier melt and threaten regional hydrological security.

## 1.2 Statement of the Problem
Despite the severity of atmospheric pollution in the region, comprehensive spatial and temporal air quality monitoring in Nepal is severely hampered by a sparse and topographically constrained network of ground-based monitoring stations. Most regulatory-grade monitors are clustered within the Kathmandu Valley or specific urban centers, leaving vast swathes of the country—particularly the rural Terai, Siwalik, and High Mountains—without continuous data. This spatial data gap obscures the true magnitude of transboundary pollution transport, the seasonal dynamics of regional biomass burning, and the localized impact of hydro-meteorological extremes. Furthermore, traditional linear statistical models fail to capture the complex, non-linear interactions between topographic elevation, meteorological drivers (temperature, precipitation, wind), and resultant atmospheric concentrations. 

## 1.3 Research Questions
To address these critical gaps, this research investigates the following key questions:
1. What is the spatiotemporal distribution of major atmospheric trace gases (NO₂, SO₂, CO, O₃, HCHO, CH₄) and aerosols (UVAI) across the five physiographic zones of Nepal?
2. Are there statistically significant long-term trends (2019–2026) in pollutant concentrations, and how do these trends vary by season and elevation?
3. Where are the persistent and emerging spatial pollution hotspots located, and how do they evolve over time?
4. How do extreme episodic events—specifically the COVID-19 pandemic lockdown and anomalous biomass burning seasons—perturb the baseline atmospheric chemistry?
5. To what extent can advanced machine learning algorithms (Random Forest, XGBoost, LightGBM) predict ambient NO₂ concentrations based exclusively on meteorological and topographic features, and what are the dominant mechanistic drivers?

## 1.4 Objectives of the Study
### 1.4.1 General Objective
To conduct a comprehensive spatiotemporal analysis of atmospheric pollutants in Nepal using high-resolution satellite remote sensing, advanced spatial statistics, and machine learning, elucidating the complex interplay between topography, meteorology, and emission sources.

### 1.4.2 Specific Objectives
1. To quantify the altitudinal gradient and seasonal climatology of NO₂, SO₂, CO, O₃, HCHO, and UVAI utilizing Sentinel-5P TROPOMI observations (2019–2026).
2. To detect significant monotonic trends using the non-parametric Mann-Kendall test and Sen's Slope estimator.
3. To delineate persistent spatial pollution hotspots and coldspots using Getis-Ord Gi* and Local Moran's I statistics.
4. To evaluate the predictive accuracy of ensemble machine learning models and interpret complex meteorological drivers using SHAP (SHapley Additive exPlanations) values.
5. To quantify the localized impact of extreme emission perturbations, including COVID-19 lockdowns and the April 2021 catastrophic forest fires.

## 1.5 Significance of the Study
This study represents one of the most comprehensive and technologically advanced assessments of Nepal's atmospheric environment to date. By integrating state-of-the-art satellite remote sensing (Sentinel-5P) with advanced spatial pattern mining and interpretable machine learning (LightGBM + SHAP), this research bypasses the limitations of sparse ground networks and traditional linear modeling. The findings provide critical, high-resolution insights into the mechanisms driving winter inversions in the mid-hills, the magnitude of transboundary pollution in the Terai, and the vulnerability of the high-altitude Himalayas. Consequently, this research delivers an essential, data-driven foundation for policymakers, environmental agencies, and climate scientists to design targeted mitigation strategies and protect public health and the cryosphere.

## 1.6 Scope and Limitations
The scope of this research encompasses the sovereign territory of Nepal, temporally bound between January 2019 and December 2026. The primary constraint of this study is the reliance on satellite-derived total or tropospheric column densities, which, while highly correlated with surface concentrations, are not direct equivalents to volumetric, ground-level exposure metrics. Furthermore, the 5.5 km × 3.5 km spatial resolution of the TROPOMI sensor inherently smooths extreme, hyper-localized pollution peaks (e.g., specific traffic intersections) that a surface monitor would otherwise detect. 

## 1.7 Organization of the Thesis
This thesis is organized into eight chapters. Chapter 1 introduces the research context, objectives, and significance. Chapter 2 provides a systematic review of the relevant literature. Chapter 3 details the methodological framework, datasets, and analytical algorithms. Chapter 4 presents the spatiotemporal distribution and trend analysis of the pollutants. Chapter 5 explores spatial hotspots and source apportionment. Chapter 6 discusses the environmental drivers and the results of the machine learning predictive modeling. Chapter 7 analyzes the impact of extreme events and presents the ground validation. Finally, Chapter 8 synthesizes the major conclusions and offers policy recommendations.
