"""
Master Pipeline Runner
======================
Runs all analysis scripts in the correct dependency order.
Skip any script that has already produced its output to save time.

Usage:
    cd analysis
    python run_pipeline.py            # Run all
    python run_pipeline.py --force    # Re-run everything
    python run_pipeline.py --from 04  # Start from script 04
"""

import subprocess
import sys
import time
from pathlib import Path

VENV_PYTHON = Path(__file__).parent.parent / "venv" / "Scripts" / "python.exe"
ANALYSIS_DIR = Path(__file__).parent / "analysis"

# ---------------------------------------------------------------------------
# Pipeline definition: (script_name, output_file_that_signals_completion)
# ---------------------------------------------------------------------------
PIPELINE = [
    # Phase 1 — Preprocessing
    ("01_data_preprocessing.py",       "data/processed/NO2_zonal_ts.csv"),
    ("02_descriptive_statistics.py",   "data/processed/descriptive_summary_stats.csv"),

    # Phase 2 — Trend Analysis
    ("03_trend_analysis.py",           "data/processed/mann_kendall_results.csv"),
    ("03b_advanced_trend_analysis.py", None),  # produces spatial TIFs when rasters present

    # Phase 3 — Seasonality
    ("04_stl_decomposition.py",        "data/processed/stl_components.csv"),
    ("04b_seasonality_climatology.py", None),  # produces figures

    # Phase 4 — Spatial Statistics
    ("05_spatial_statistics.py",       None),  # needs shapefile
    ("06_emerging_hotspot.py",         None),
    ("06b_emerging_hotspots.py",       None),

    # Phase 5 — Climate & Multivariate
    ("07_climate_correlation.py",      None),
    ("07b_multivariate_statistics.py", None),
    ("08_wavelet_analysis.py",         None),
    ("09_granger_causality.py",        None),

    # Phase 6 — Socioeconomic
    ("10_population_exposure.py",      None),
    ("11_breakpoint_analysis.py",      "data/processed/breakpoint_results.csv"),

    # Phase 7 — Special Analyses
    ("12_covid_lockdown_analysis.py",  "data/processed/covid_lockdown_analysis.csv"),
    ("13_era5_meteorological_analysis.py", None),
    ("14_validation_proxy.py",         "data/processed/validation_summary.csv"),

    # Phase 8 — Visualization
    ("15_spatial_map_generation.py",   None),
    ("16_summary_charts.py",           None),

    # Phase 9 — Machine Learning
    ("20_ml_pollutant_prediction.py",  None),

    # Phase 10 — Extreme Events & Validation
    ("21_extreme_events.py",           None),
    ("22_ground_validation.py",        None),

    # Phase 11 — Publication Figures
    ("30_publication_figures.py",      None),
]

def run_script(script_name, force=False, output_sentinel=None):
    """Run a single analysis script. Skip if output already exists."""
    script_path = ANALYSIS_DIR / script_name
    project_root = ANALYSIS_DIR.parent

    if not script_path.exists():
        print(f"  [SKIP] {script_name} — file not found")
        return True

    # Check if already done
    if not force and output_sentinel:
        sentinel = project_root / output_sentinel
        if sentinel.exists():
            print(f"  [DONE] {script_name} — output exists, skipping")
            return True

    print(f"\n{'='*60}")
    print(f"  Running: {script_name}")
    print(f"{'='*60}")

    start = time.time()
    result = subprocess.run(
        [str(VENV_PYTHON), str(script_path)],
        cwd=str(ANALYSIS_DIR),
        capture_output=False,  # Print output live
    )
    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"  [OK] {script_name} completed in {elapsed:.1f}s")
        return True
    else:
        print(f"  [ERROR] {script_name} failed (exit code {result.returncode})")
        return False

def main():
    force = "--force" in sys.argv
    start_from = None
    for arg in sys.argv[1:]:
        if arg.startswith("--from"):
            start_from = arg.split("=")[-1] if "=" in arg else None

    print(f"Python: {VENV_PYTHON}")
    print(f"Analysis dir: {ANALYSIS_DIR}")
    print(f"Force re-run: {force}")
    print()

    errors = []
    running = start_from is None

    for script, sentinel in PIPELINE:
        if start_from and script.startswith(start_from):
            running = True
        if not running:
            continue

        ok = run_script(script, force=force, output_sentinel=sentinel)
        if not ok:
            errors.append(script)

    print(f"\n{'='*60}")
    if errors:
        print(f"Pipeline completed with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
    else:
        print("Pipeline completed successfully!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
