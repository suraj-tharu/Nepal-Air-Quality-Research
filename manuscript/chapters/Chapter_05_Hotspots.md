# Chapter 5: Spatial Hotspots and Source Apportionment

## 5.1 Identification of Persistent Pollution Hotspots
While descriptive statistics provide a macroscopic view of altitudinal gradients, spatial autocorrelation techniques—specifically the Getis-Ord Gi* statistic and Local Moran's I (LISA)—were essential for pinpointing statistically significant, localized pollution clusters.

Across the 8-year study period (2019–2026), the analysis revealed an unambiguous and persistent "High-High" clustering (hotspots) concentrated entirely within the southern **Terai** and lower **Siwalik** belts. For NO₂, CO, and SO₂, these low-elevation zones exhibited Gi* z-scores significantly greater than 2.58 ($p < 0.01$), confirming intense and sustained pollution agglomeration.

Conversely, the **High Mountains** and **High Himal** consistently emerged as significant "Low-Low" coldspots. The sheer topographic relief of the Himalayas acts as a formidable physical barrier, preventing the northward advection of boundary layer pollutants from the Indo-Gangetic Plain (IGP), thereby preserving the pristine atmospheric quality of the high-altitude cryosphere.

## 5.2 Emerging Hotspots and Space-Time Trends
The application of Space-Time Pattern Mining allowed for the classification of these spatial clusters over time. 

The central Terai (bordering heavily industrialized Indian states like Uttar Pradesh and Bihar) was categorized as a **"Persistent Hotspot,"** meaning it remained a statistically significant hotspot for more than 90% of the temporal bins. 

More concerningly, specific urban nodes within the **Middle Mountains**—most notably the Kathmandu Valley—were classified as **"Intensifying Hotspots"** for NO₂ during the winter season. This indicates that while the annual mean might be relatively stable, the severity of the localized pollution trapping during winter temperature inversions is worsening year-over-year.

## 5.3 Multivariate Grouping of Physiographic Zones
To objectively confirm these visual and spatial observations, unsupervised Machine Learning (Agglomerative Hierarchical Clustering and Principal Component Analysis) was applied to the complete multi-pollutant dataset.

### 5.3.1 Hierarchical Clustering
The clustering dendrogram unequivocally segregated the five physiographic zones into three distinct atmospheric regimes:
1. **The High-Pollution Sink:** The Terai and Siwalik grouped together with a very low linkage distance, indicating nearly identical atmospheric pollutant profiles dominated by high NO₂ and anthropogenic signatures.
2. **The Transitional Zone:** The Middle Mountains formed a distinct, independent cluster. It acts as an atmospheric bridge, displaying moderate baseline pollution but acute seasonal spikes due to local vehicular emissions and winter inversions.
3. **The Pristine Background:** The High Mountains and High Himal clustered tightly together, characterized by consistently low values across all evaluated trace gases.

### 5.3.2 Principal Component Analysis (PCA)
The PCA biplot revealed that the first principal component (PC1), explaining over 68% of the variance, was heavily loaded by NO₂, SO₂, and CO. This strongly implies a shared, dominant anthropogenic combustion source (vehicular emissions, brick kilns, and transboundary industrial transport) driving the bulk of atmospheric variability in the lower elevations. The second principal component (PC2) was dominated by O₃ and HCHO, distinguishing biogenic emissions and secondary photochemical formation processes, which peaked during the high-insolation pre-monsoon months.
