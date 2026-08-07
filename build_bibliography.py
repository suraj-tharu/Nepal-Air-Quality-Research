import requests
import json
from pathlib import Path
from datetime import datetime

# We will query OpenAlex API for high-impact papers.
# To avoid timeouts and get highly relevant results, we use specific concepts and keywords.

BASE_URL = "https://api.openalex.org/works"
HEADERS = {'User-Agent': 'NepalAirQualityResearch/1.0 (mailto:test@example.com)'}

QUERIES = [
    {
        "name": "Satellite Remote Sensing of Air Quality (Nepal/Himalayas)",
        "params": {
            "search": "Sentinel-5P OR TROPOMI AND air quality AND (Nepal OR Himalayas OR South Asia)",
            "filter": "publication_year:>2017,cited_by_count:>10",
            "sort": "cited_by_count:desc",
            "per_page": 50
        }
    },
    {
        "name": "Machine Learning in Atmospheric Science",
        "params": {
            "search": "(machine learning OR Random Forest OR LightGBM OR SHAP) AND (air quality prediction OR NO2 OR PM2.5)",
            "filter": "publication_year:>2018,cited_by_count:>20",
            "sort": "cited_by_count:desc",
            "per_page": 50
        }
    },
    {
        "name": "Extreme Events (COVID-19 and Biomass Burning)",
        "params": {
            "search": "(COVID-19 lockdown OR biomass burning OR forest fire) AND air quality AND (South Asia OR India OR Nepal)",
            "filter": "publication_year:>2019,cited_by_count:>15",
            "sort": "cited_by_count:desc",
            "per_page": 50
        }
    },
    {
        "name": "Spatial Hotspots and Trend Analysis in Air Pollution",
        "params": {
            "search": "(spatial hotspot OR Getis-Ord OR Moran OR Mann-Kendall) AND air pollution",
            "filter": "publication_year:>2015,cited_by_count:>20",
            "sort": "cited_by_count:desc",
            "per_page": 50
        }
    }
]

def format_apa(work):
    try:
        # Authors
        authors = work.get('authorships', [])
        author_str = ""
        if not authors:
            author_str = "Anonymous"
        elif len(authors) == 1:
            author_str = authors[0]['author']['display_name']
        elif len(authors) == 2:
            author_str = f"{authors[0]['author']['display_name']} & {authors[1]['author']['display_name']}"
        elif len(authors) > 2:
            author_str = f"{authors[0]['author']['display_name']} et al."

        year = work.get('publication_year', 'n.d.')
        title = work.get('title', 'No Title')
        
        # Source (Journal)
        primary_loc = work.get('primary_location', {})
        source = primary_loc.get('source', {}) if primary_loc else {}
        journal = source.get('display_name', 'Unknown Journal') if source else 'Unknown Journal'
        
        doi = work.get('doi', '')

        apa_citation = f"{author_str} ({year}). {title}. *{journal}*. {doi}"
        return apa_citation.strip()
    except Exception as e:
        return None

def build_bibliography():
    out_dir = Path("manuscript")
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "References.md"
    
    seen_dois = set()
    all_citations = []
    
    print("Querying OpenAlex API for Systematic Literature Review...")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write("# References (Systematic Literature Review)\n\n")
        f.write("*Note: Generated systematically via OpenAlex API filtering for high-impact S5P, ML, and Himalayan Air Quality literature.*\n\n")
        
        for q in QUERIES:
            print(f"Executing Query: {q['name']}")
            response = requests.get(BASE_URL, params=q['params'], headers=HEADERS)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                print(f"  -> Found {len(results)} highly cited works.")
                
                f.write(f"## {q['name']}\n")
                
                for work in results:
                    doi = work.get('doi')
                    if doi and doi in seen_dois:
                        continue
                    if doi:
                        seen_dois.add(doi)
                        
                    citation = format_apa(work)
                    if citation:
                        f.write(f"- {citation}\n")
                        all_citations.append(citation)
                f.write("\n")
            else:
                print(f"  -> Failed query: {response.status_code}")
                
    print(f"\nSuccessfully compiled {len(all_citations)} unique references into {out_file}")

if __name__ == "__main__":
    build_bibliography()
