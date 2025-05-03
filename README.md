# 🧠 Tavily Table Extractor with DuckDB

This Streamlit app lets users search for real-world data sources using the Tavily API, and then extract potential tables using DuckDB and Trafilatura from selected URLs.

---

## 🚀 Features

- Ask data-related questions (e.g., "Inflation rates by country")
- Fetch relevant websites using Tavily
- Extract raw HTML content using `trafilatura`
- Attempt to convert unstructured text into tables using `duckdb`

---

## 📦 Installation

1. Clone this repo or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🖥️ Run the App

```bash
streamlit run app_duckdb_streamlit.py
```

---

## 🧪 Example Queries

- "Average salary in Israel 2023"
- "Top AI startups funding 2024"
- "Inflation rates by country"
- "GDP by country over the last 5 years"

---

## ✅ Requirements

- Python 3.8+
- Internet connection (for Tavily + source URLs)

---

Enjoy exploring web data tables! 🔍📊
