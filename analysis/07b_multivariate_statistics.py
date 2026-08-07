"""
Script 07b: Multivariate Statistics

Implements ANOVA, Kruskal-Wallis, PCA, and Hierarchical Clustering
to assess significant differences across physiographic zones and group 
regions with similar pollution profiles.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

try:
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    from scipy.cluster.hierarchy import dendrogram, linkage
    import scikit_posthocs as sp
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False
    print("[WARNING] scikit-learn or scikit-posthocs not found.")

from config import PROCESSED_DIR, FIGURES_DIR, POLLUTANTS
from utils.plotting import save_figure

def run_multivariate_stats():
    print("Running Multivariate Statistics...")
    
    out_dir = FIGURES_DIR / "multivariate"
    out_dir.mkdir(exist_ok=True, parents=True)
    
    # --- 1. ANOVA / Kruskal-Wallis across Zones ---
    # We will test if pollutants are significantly different across zones
    
    # Load and combine all pollutants
    combined_data = []
    
    for pol in POLLUTANTS.keys():
        file_path = PROCESSED_DIR / f"{pol}_zonal_ts.csv"
        if file_path.exists():
            df = pd.read_csv(file_path)
            df['pollutant'] = pol
            df.rename(columns={f"{pol}_mean": 'value'}, inplace=True)
            combined_data.append(df[['zone', 'year', 'month', 'value', 'pollutant']])
            
    if not combined_data:
        print("No zonal data found.")
        return
        
    full_df = pd.concat(combined_data, ignore_index=True)
    
    stats_results = []
    
    for pol in POLLUTANTS.keys():
        pol_df = full_df[full_df['pollutant'] == pol].dropna(subset=['value'])
        if pol_df.empty: continue
        
        # Group values by zone
        groups = [group['value'].values for name, group in pol_df.groupby('zone')]
        
        if len(groups) > 1:
            # Kruskal-Wallis (non-parametric ANOVA)
            kw_stat, kw_p = stats.kruskal(*groups)
            stats_results.append({
                'pollutant': pol,
                'test': 'Kruskal-Wallis',
                'statistic': kw_stat,
                'p_value': kw_p
            })
            
            # If significant, run post-hoc (Dunn's test)
            if kw_p < 0.05 and HAS_SKLEARN:
                try:
                    dunn = sp.posthoc_dunn(pol_df, val_col='value', group_col='zone', p_adjust='bonferroni')
                    dunn.to_csv(out_dir / f"{pol}_Dunn_Posthoc.csv")
                except:
                    pass
                    
    pd.DataFrame(stats_results).to_csv(out_dir / "Kruskal_Wallis_Results.csv", index=False)
    
    if not HAS_SKLEARN:
        return
        
    # --- 2. Principal Component Analysis (PCA) & Clustering ---
    # We will aggregate data by (zone, month) to see pollution signatures
    
    pivot_df = full_df.pivot_table(index=['zone', 'month'], columns='pollutant', values='value').reset_index()
    pivot_df = pivot_df.dropna() # Drop rows with missing pollutants
    
    if pivot_df.empty:
        return
        
    features = [c for c in pivot_df.columns if c in POLLUTANTS.keys()]
    X = pivot_df[features].values
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # PCA
    pca = PCA(n_components=2)
    pcs = pca.fit_transform(X_scaled)
    
    pivot_df['PC1'] = pcs[:, 0]
    pivot_df['PC2'] = pcs[:, 1]
    
    # Plot PCA Biplot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.scatterplot(data=pivot_df, x='PC1', y='PC2', hue='zone', style='month', s=100, ax=ax)
    
    # Add loadings (vectors)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    for i, feature in enumerate(features):
        ax.arrow(0, 0, loadings[i, 0]*2, loadings[i, 1]*2, color='r', alpha=0.5, 
                 head_width=0.05, head_length=0.1)
        ax.text(loadings[i, 0]*2.2, loadings[i, 1]*2.2, feature, color='r', ha='center', va='center')
        
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)")
    ax.set_title("PCA Biplot of Pollutant Signatures")
    ax.axhline(0, color='grey', linestyle='--', lw=1)
    ax.axvline(0, color='grey', linestyle='--', lw=1)
    save_figure(fig, out_dir / "PCA_Biplot")
    
    # Hierarchical Clustering
    linked = linkage(X_scaled, 'ward')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    labels = [f"{z} (M{m})" for z, m in zip(pivot_df['zone'], pivot_df['month'])]
    
    dendrogram(linked, labels=labels, ax=ax, leaf_rotation=90, leaf_font_size=8)
    ax.set_title("Hierarchical Clustering of Zone-Month Pollution Signatures")
    ax.set_ylabel("Ward Distance")
    fig.tight_layout()
    save_figure(fig, out_dir / "Hierarchical_Clustering")
    
    print("Multivariate Statistics completed.")

if __name__ == "__main__":
    run_multivariate_stats()
