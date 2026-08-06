"""
Comprehensive analysis of all GEE-exported CSV files.
"""
import pandas as pd
import os
import glob

csv_dir = 'data/raw'
files = sorted(glob.glob(os.path.join(csv_dir, '*.csv')))

print(f"Found {len(files)} CSV files in {csv_dir}/\n")
print("=" * 80)

for f in files:
    df = pd.read_csv(f)
    name = os.path.basename(f)
    print(f"\n{'=' * 80}")
    print(f"FILE: {name}")
    print(f"{'=' * 80}")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    
    if 'year' in df.columns:
        print(f"Year range: {df['year'].min()} - {df['year'].max()}")
    if 'month' in df.columns:
        print(f"Month range: {df['month'].min()} - {df['month'].max()}")
    if 'zone' in df.columns:
        print(f"Zones: {df['zone'].unique().tolist()}")
    
    print(f"\nFirst 5 rows:")
    print(df.head(5).to_string())
    
    print(f"\nData types:")
    print(df.dtypes.to_string())
    
    print(f"\nNull/Missing values:")
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print(null_counts[null_counts > 0].to_string())
        null_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
        print(f"Total null percentage: {null_pct:.1f}%")
    else:
        print("No missing values!")
    
    # Numeric column statistics
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    # Exclude year, month, system:index from stats
    stat_cols = [c for c in numeric_cols if c not in ['year', 'month']]
    if stat_cols:
        print(f"\nDescriptive statistics for key variables:")
        print(df[stat_cols].describe().to_string())

print(f"\n{'=' * 80}")
print("SUMMARY")
print(f"{'=' * 80}")
print(f"Total files: {len(files)}")
total_rows = sum(pd.read_csv(f).shape[0] for f in files)
print(f"Total data rows: {total_rows}")

# Check data completeness
pollutant_files = [f for f in files if 'ERA5' not in f]
for f in pollutant_files:
    df = pd.read_csv(f)
    name = os.path.basename(f)
    if 'year' in df.columns and 'month' in df.columns and 'zone' in df.columns:
        expected = len(df['year'].unique()) * 12 * len(df['zone'].unique())
        actual = df.shape[0]
        completeness = (actual / expected * 100) if expected > 0 else 0
        print(f"{name}: {actual}/{expected} records ({completeness:.1f}% complete)")
