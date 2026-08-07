# Chapter 7: Extreme Events and Ground Validation

While long-term climatic drivers and persistent spatial hotspots define the baseline atmospheric chemistry of Nepal, extreme, episodic events induce severe, short-term deviations. This chapter quantifies two major perturbations—the COVID-19 lockdown and catastrophic biomass burning—and validates the satellite observations against available ground-truth data.

## 7.1 The COVID-19 Natural Experiment and Post-Pandemic Rebound
The strict nationwide lockdown implemented by the Government of Nepal in response to the COVID-19 pandemic (March to June 2020) provided an unprecedented "natural experiment" to isolate the anthropogenic contribution to the atmospheric column.

During the lockdown period, NO₂ concentrations plummeted dramatically across the country compared to the pre-lockdown baseline (January 2019 – February 2020). The **Terai** experienced a sharp reduction, directly attributable to the sudden cessation of vehicular traffic, the halting of industrial operations (particularly brick kilns), and the shutdown of cross-border transport from India. 

However, this atmospheric cleansing was transient. The post-lockdown and 2021 rebound phases saw concentrations rapidly return to, and in some zones exceed, pre-pandemic levels. By the "Post-Rebound" period (2022–2026), NO₂ in the Terai stabilized at $27.35 \times 10^{14}$, marking a +15.7% increase over the pre-lockdown baseline, highlighting the aggressive resumption of fossil-fuel intensive economic activities.

## 7.2 Impact of Biomass Burning (April 2021 Case Study)
Unlike NO₂, which is primarily driven by fossil fuel combustion, Carbon Monoxide (CO) and UV Aerosol Index (UVAI) are robust tracers for biomass burning. In April 2021, Nepal experienced one of the most severe forest fire seasons on record, exacerbated by a prolonged winter drought and anomalous pre-monsoon heat.

During the Spring 2021 fire season, CO and UVAI spiked exponentially. The Siwalik and Middle Mountains—the most heavily forested zones—recorded massive anomalies. The UV Aerosol Index, which detects absorbing aerosols like smoke and soot, flipped from a negative baseline to highly positive values across the mid-hills, corresponding with severe degradation in surface visibility and localized air quality emergencies. This event underscores the vulnerability of Nepal's air quality to climate-induced hydro-meteorological extremes (droughts leading to mega-fires).

## 7.3 Ground Validation of Sentinel-5P Observations
To ensure the robustness of the remote sensing dataset, Sentinel-5P TROPOMI NO₂ tropospheric column densities were validated against continuous ground-based measurements. While Nepal suffers from a sparse network of regulatory-grade air quality monitors, available surface NO₂ data from the Kathmandu Valley (Middle Mountains) were utilized for this validation exercise.

The validation metrics yielded the following:
- **Root Mean Square Error (RMSE):** 7.73 
- **Mean Absolute Error (MAE):** 7.59 

While Sentinel-5P successfully captures the macroscopic spatial gradients, seasonal cyclicity, and extreme event anomalies (like the COVID drop and forest fire spikes), the absolute pixel-to-point correlation (R²) was relatively poor for highly localized urban sites. This discrepancy is a well-documented limitation of satellite remote sensing in complex mountainous terrain; the 5.5 km x 3.5 km spatial resolution of TROPOMI smooths out extreme, highly-localized surface peaks (e.g., specific traffic intersections) that a ground monitor captures perfectly. Furthermore, comparing a total column vertical density against a surface-level volumetric measurement inherently introduces bias. 

Despite this, the high signal-to-noise ratio during regional events confirms that Sentinel-5P is a highly reliable instrument for regional trend analysis and spatial hotspot detection, which are the primary objectives of this thesis.
