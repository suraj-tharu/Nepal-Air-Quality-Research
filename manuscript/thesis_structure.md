# Thesis Structure Outline (100–150 Pages)

**Title:** Spatiotemporal Dynamics and Environmental Drivers of Atmospheric Pollutants in Nepal: A Machine Learning and Remote Sensing Approach

## Front Matter (Pages i - xv)
- Title Page
- Declaration of Originality
- Abstract
- Acknowledgements
- Table of Contents
- List of Figures (Aim: 40-60 Figures)
- List of Tables (Aim: 20-30 Tables)
- Abbreviations and Acronyms

## Chapter 1: Introduction (Pages 1 - 15)
1.1 Background of the Study
1.2 Statement of the Problem
1.3 Research Questions
1.4 Objectives of the Study (General & Specific)
1.5 Significance of the Study
1.6 Scope and Limitations
1.7 Organization of the Thesis

## Chapter 2: Literature Review (Pages 16 - 35)
2.1 Overview of Air Pollution in South Asia
2.2 The Indo-Gangetic Plain and Transboundary Transport
2.3 Satellite Remote Sensing of Trace Gases (Sentinel-5P TROPOMI)
2.4 Statistical and Machine Learning Approaches in Atmospheric Science
2.5 Impact of Extreme Events on Air Quality (COVID-19, Forest Fires)
2.6 Research Gaps in the Nepalese Context

## Chapter 3: Materials and Methods (Pages 36 - 55)
3.1 Study Area (Physiographic Zones of Nepal)
3.2 Datasets and Preprocessing (GEE workflow)
    - 3.2.1 Sentinel-5P (NO2, SO2, CO, O3, HCHO, UVAI, CH4)
    - 3.2.2 Climate Variables (ERA5 / NASA POWER)
    - 3.2.3 Land Characteristics (SRTM, WorldPop, VIIRS)
3.3 Trend Analysis Methods (Mann-Kendall, Sen's Slope, Theil-Sen)
3.4 Spatial Hotspot Analysis (Getis-Ord Gi*, Local Moran's I, Space-Time Pattern Mining)
3.5 Multivariate Statistical Analysis (PCA, Hierarchical Clustering)
3.6 Machine Learning Predictive Modeling (Random Forest, XGBoost, LightGBM, SHAP)
3.7 Extreme Event Quantification and Validation Framework

## Chapter 4: Spatiotemporal Distribution and Trends (Pages 56 - 80)
4.1 Spatial Distribution of Pollutants Across Physiographic Zones
4.2 Annual and Seasonal Variations (Climatology and Anomalies)
4.3 Pixel-wise Trend Analysis Results (Mann-Kendall Maps)
4.4 Discussion on Altitudinal Pollution Gradients (Ridge Plots)

## Chapter 5: Spatial Hotspots and Source Apportionment (Pages 81 - 95)
5.1 Identification of Persistent Pollution Hotspots
5.2 Emerging Hotspots and Space-Time Trends
5.3 Multivariate Grouping of Zones (PCA and Clustering Results)

## Chapter 6: Environmental Drivers and Predictive Modeling (Pages 96 - 115)
6.1 Correlation between Climate Variables and Pollutants
6.2 Machine Learning Model Evaluation (RMSE, MAE, R²)
6.3 Feature Importance and SHAP Value Analysis
6.4 Identifying the Dominant Drivers of Pollution Variability

## Chapter 7: Extreme Events and Ground Validation (Pages 116 - 130)
7.1 The COVID-19 Natural Experiment and Post-Pandemic Rebound
7.2 Impact of Biomass Burning and Forest Fires (April 2021 Case Study)
7.3 Winter Temperature Inversions in Urban Valleys
7.4 Ground Validation of Sentinel-5P Observations

## Chapter 8: Conclusion and Policy Recommendations (Pages 131 - 140)
8.1 Summary of Major Findings
8.2 Policy Implications for Air Quality Management in Nepal
8.3 Recommendations for Future Research

## References (Pages 141 - 150+)
- Systematic Literature Review consisting of 150-250 references in APA or Target Journal format.

## Appendices
- Appendix A: Google Earth Engine JavaScript Codes
- Appendix B: Python Scripts for Machine Learning and Statistics
- Appendix C: Supplementary Tables and Figures
