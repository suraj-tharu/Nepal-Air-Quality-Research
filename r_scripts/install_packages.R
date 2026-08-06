# Install required R packages for BFAST analysis
# Run this script once before executing bfast_breakpoint.R

packages_to_install <- c("bfast", "zoo", "forecast", "lubridate", "dplyr", "ggplot2")

# Check which packages are not yet installed
new_packages <- packages_to_install[!(packages_to_install %in% installed.packages()[,"Package"])]

if(length(new_packages) > 0) {
  cat("Installing missing packages:", paste(new_packages, collapse=", "), "\n")
  install.packages(new_packages, repos = "http://cran.us.r-project.org")
} else {
  cat("All required packages are already installed.\n")
}

cat("BFAST environment setup complete.\n")
