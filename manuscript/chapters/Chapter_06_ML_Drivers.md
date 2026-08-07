# Chapter 6: Environmental Drivers and Predictive Modeling

## 6.1 Climate-Pollutant Correlation Analysis
Atmospheric pollutant concentrations are not solely dictated by emission inventories; they are deeply modulated by meteorological conditions. To quantify these relationships, Pearson correlation coefficients were calculated between monthly NO₂ concentrations and ERA5 meteorological variables across the five physiographic zones.

The analysis revealed a consistent, strong negative correlation between NO₂ and **Total Precipitation** across all zones (e.g., $r \approx -0.75$ in the Siwalik). This statistically validates the intense wet deposition and atmospheric scavenging effect of the South Asian Monsoon. **2-meter Temperature** also exhibited a strong inverse relationship; higher summer temperatures coincide with boundary layer expansion (diluting surface concentrations) and the aforementioned monsoon rains, whereas low winter temperatures are associated with shallow boundary layers, frequent inversions, and high pollutant retention. 

## 6.2 Machine Learning Model Evaluation
To move from linear correlation to predictive, non-linear modeling, a supervised Machine Learning (ML) framework was architected. The objective was to predict NO₂ concentrations using a suite of geographical and meteorological features (Elevation, Temperature, Precipitation, Wind vectors).

Three advanced, tree-based ensemble algorithms were evaluated: Random Forest, Extreme Gradient Boosting (XGBoost), and Light Gradient Boosting Machine (LightGBM).

The models were trained on 80% of the dataset and validated against a 20% holdout test set. The performance metrics demonstrated the superior capability of gradient boosting algorithms in capturing complex atmospheric dynamics:

| Model | Root Mean Square Error (RMSE) | Mean Absolute Error (MAE) | Coefficient of Determination (R²) |
| :--- | :--- | :--- | :--- |
| Random Forest | 3.258 | 2.368 | 0.841 |
| XGBoost | 3.410 | 2.374 | 0.826 |
| **LightGBM** | **2.965** | **2.055** | **0.868** |

**LightGBM** emerged as the optimal model, successfully explaining 86.8% of the variance (R² = 0.868) in NO₂ concentrations across Nepal. This high predictive accuracy confirms that meteorological variables and topographic elevation are sufficient to predict the vast majority of spatial and temporal NO₂ variability, independent of real-time emission inventories.

## 6.3 Feature Importance and SHAP Value Analysis
While the LightGBM model provided excellent predictive power, tree-based ensembles are inherently "black boxes". To extract mechanistic insights, the **SHAP (SHapley Additive exPlanations)** framework was applied to the LightGBM model. SHAP values deconstruct the model’s predictions, revealing the exact marginal contribution of each feature.

### 6.3.1 Global Feature Importance
The native LightGBM feature importance and the global SHAP summary plot both identified **Elevation (Zone)** and **2m Temperature** as the overwhelmingly dominant drivers of NO₂ concentration, vastly outperforming precipitation and wind vectors. 

### 6.3.2 Local SHAP Effects
The SHAP summary plot provided critical insights into the *directionality* of these effects:
- **Temperature:** Lower temperature values (blue dots on the SHAP plot) consistently pushed the NO₂ prediction higher (positive SHAP value), mechanically confirming the winter inversion effect.
- **Precipitation:** High precipitation events (red dots) resulted in negative SHAP values, quantifying the exact magnitude of the monsoon wash-out effect.
- **Wind:** U and V wind components exhibited highly non-linear, bifurcated SHAP distributions, suggesting that specific wind directional regimes (e.g., southerly winds from the IGP vs. northerly winds from the Tibetan plateau) have drastically different impacts on local NO₂ accumulation.

Ultimately, the ML pipeline demonstrates that while anthropogenic sources govern the baseline emission *quantity*, local topography (elevation) and seasonal meteorology (temperature and precipitation) are the primary modulators of the *observed atmospheric concentration*.
