# Script: BFAST Breakpoint Detection (Layer 4)
# Performs Breaks For Additive Season and Trend (BFAST) analysis
# to detect abrupt changes in pollutant time series (e.g., COVID-19 lockdowns, wildfires).

suppressPackageStartupMessages({
  library(bfast)
  library(zoo)
  library(lubridate)
  library(dplyr)
})

# Setup Paths
project_root <- dirname(dirname(normalizePath(sys.frame(1)$ofile)))
data_dir <- file.path(project_root, "data", "processed")
out_dir <- file.path(project_root, "figures", "bfast_breakpoints")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

pollutants <- c("NO2", "SO2", "CO", "O3", "HCHO", "UVAI")
start_year <- 2019

cat("Running BFAST Breakpoint Detection...\n")

results_list <- list()

for (pol in pollutants) {
  file_path <- file.path(data_dir, paste0(pol, "_zonal_ts.csv"))
  
  if (!file.exists(file_path)) {
    next
  }
  
  cat(paste("  -> Analyzing", pol, "\n"))
  df <- read.csv(file_path)
  
  # Ensure date is Date object
  df$date <- as.Date(df$date)
  
  zones <- unique(df$zone)
  
  for (z in zones) {
    zone_data <- df %>% filter(zone == z) %>% arrange(date)
    
    # Create time series object (frequency 12 for monthly)
    # Ensure start year and month match the data's first row
    first_date <- zone_data$date[1]
    start_c <- c(year(first_date), month(first_date))
    
    ts_data <- ts(zone_data[[paste0(pol, "_mean")]], start=start_c, frequency=12)
    
    # Handle missing values if any
    if(any(is.na(ts_data))) {
        ts_data <- na.approx(ts_data)
    }
    
    if (length(ts_data) < 36) {
        cat(paste("    [WARNING] Not enough data for BFAST in", z, "(need >= 3 yrs)\n"))
        next
    }
    
    # Run BFAST
    # h = minimal segment size (0.15 = 15% of the time series)
    # season = "harmonic"
    # max.iter = maximum iterations
    tryCatch({
      fit <- bfast(ts_data, h=0.15, season="harmonic", max.iter=3)
      
      # Plot and save
      pdf(file.path(out_dir, paste0("BFAST_", pol, "_", z, ".pdf")), width=10, height=8)
      plot(fit, main=paste("BFAST:", pol, "-", gsub("_", " ", z)))
      dev.off()
      
      # Extract breakpoints if they exist
      trend_breaks <- NA
      season_breaks <- NA
      
      if (!is.na(fit$output[[1]]$bp.Vt[1])) {
          trend_breaks <- paste(time(ts_data)[fit$output[[1]]$bp.Vt], collapse=",")
      }
      if (!is.na(fit$output[[1]]$bp.Wt[1])) {
          season_breaks <- paste(time(ts_data)[fit$output[[1]]$bp.Wt], collapse=",")
      }
      
      results_list[[length(results_list) + 1]] <- data.frame(
        Pollutant = pol,
        Zone = z,
        Trend_Breakpoints = trend_breaks,
        Seasonal_Breakpoints = season_breaks
      )
      
    }, error = function(e) {
      cat(paste("    [ERROR] BFAST failed for", pol, z, ":", e$message, "\n"))
    })
  }
}

if (length(results_list) > 0) {
  final_results <- bind_rows(results_list)
  write.csv(final_results, file.path(data_dir, "bfast_results.csv"), row.names=FALSE)
  cat(paste("\nSaved BFAST results to", file.path(data_dir, "bfast_results.csv"), "\n"))
}
