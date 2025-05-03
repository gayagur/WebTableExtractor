import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_tables_from_url(url):
    try:
        tables = pd.read_html(url)
        return tables
    except Exception as e:
        print(f"❌ Failed to extract tables from {url}: {e}")
        return []

def extract_table_previews(urls, max_tables=1):
    results = []
    for url in urls:
        tables = extract_tables_from_url(url)
        for i, table in enumerate(tables[:max_tables]):
            results.append({
                "url": url,
                "table_index": i,
                "preview": table.head()
            })
    return results

if __name__ == "__main__":
    # example usage
    example_urls = [
        "https://en.wikipedia.org/wiki/List_of_countries_by_average_wage",
        "https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes"
    ]
    previews = extract_table_previews(example_urls)
    for item in previews:
        print(f"✅ Table from {item['url']} (table #{item['table_index']}):")
        print(item['preview'])
