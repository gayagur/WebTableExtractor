import trafilatura
import duckdb
import pandas as pd

def extract_text_from_url(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        return trafilatura.extract(downloaded, include_tables=True)
    return None

def extract_tables_with_duckdb(raw_text):
    # Save to temporary file
    with open("temp_data.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

    # Load with DuckDB using CSV reader over raw text file (line by line table parsing)
    try:
        con = duckdb.connect()
        df = con.execute("SELECT * FROM read_csv_auto('temp_data.txt', delim='|', ignore_errors=true)").df()
        return df
    except Exception as e:
        print(f"❌ Error parsing with DuckDB: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    url = input("Enter a URL to extract tables from: ")
    text = extract_text_from_url(url)
    if not text:
        print("Failed to extract content.")
    else:
        print("Text extracted. Parsing with DuckDB...")
        df = extract_tables_with_duckdb(text)
        if not df.empty:
            print("✅ Table extracted:")
            print(df.head())
        else:
            print("No table could be extracted.")
