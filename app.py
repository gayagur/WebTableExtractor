import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

st.set_page_config(page_title="Web Table Extractor", layout="wide")
st.title("🌐Web Table Extractor")


def fetch_sources_from_tavily(query):
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "query": f"""Find datasets or tables related to: {query}.
    Please prefer results from reliable data sources such as:
    Kaggle, Statista, Our World in Data, World Bank, IMF, UNdata, OECD, Trading Economics, or national government data portals.
    Only return real websites with downloadable or viewable tables. Do not include long raw tables in the description.""",
        "search_depth": "advanced",
        "include_answer": False,
        "include_tables": False
    }

    try:
        response = requests.post("https://api.tavily.com/search", json=body, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        st.error(f"Error during request: {e}")
        return {}
def extract_csv_from_links(url):
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True) if any(a["href"].endswith(ext) for ext in [".csv", ".xlsx"])]
        if links:
            csv_url = links[0] if links[0].startswith("http") else requests.compat.urljoin(url, links[0])
            if csv_url.endswith(".csv"):
                return pd.read_csv(csv_url)
            elif csv_url.endswith(".xlsx"):
                return pd.read_excel(csv_url)
    except Exception as e:
        st.warning(f"Couldn't extract downloadable table: {e}")
    return pd.DataFrame()

def extract_table_from_url_if_relevant(url, query):
    try:

        tables = pd.read_html(url)
        if tables:
            keywords = [word.lower() for word in query.split() if len(word) > 3]
            for table in tables:
                table_str = table.astype(str).to_string().lower()
                found_keywords = [kw for kw in keywords if kw in table_str]
                if len(found_keywords) >= 2:
                    return table
    except:
        pass


    df = extract_csv_from_links(url)
    if not df.empty:
        return df

    return pd.DataFrame()



if "results" not in st.session_state:
    st.session_state["results"] = []
if "current_query" not in st.session_state:
    st.session_state["current_query"] = ""

sample_queries = [
    "Average monthly salary in Israel",
    "Inflation rates by country 2023",
    "Top AI startups by funding",
    "GDP by country over the last 5 years"
]

query = st.text_input("🔍 Ask a data-related question", value=st.session_state["current_query"], placeholder="e.g., AI startup funding in 2024")

st.markdown("**Sample queries:**")
cols = st.columns(len(sample_queries))
for i, q in enumerate(sample_queries):
    if cols[i].button(q):
        query = q
        st.session_state["current_query"] = query
        with st.spinner("Searching sources..."):
            data = fetch_sources_from_tavily(query)
        st.session_state["results"] = data.get("results", [])

if st.button("Search"):
    st.session_state["current_query"] = query
    with st.spinner("Searching sources..."):
        data = fetch_sources_from_tavily(query)
    st.session_state["results"] = data.get("results", [])

results = st.session_state["results"]
if results:
    st.subheader("🔗 Relevant data sources:")
    for idx, res in enumerate(results):
        url = res.get("url")
        title = res.get("title", "No Title")
        content = res.get("content", "No description available.")
        st.markdown(f"### [{title}]({url})")
        st.write(content)

        if st.button("🔎 Extract table", key=f"extract_{idx}"):
            with st.spinner("Trying to extract a relevant table..."):
                table = extract_table_from_url_if_relevant(url, query)
            if not table.empty:
                st.success("✅ Table extracted!")
                st.dataframe(table)
                st.download_button("Download CSV", table.to_csv(index=False), file_name=f"table_{idx}.csv", key=f"dl_{idx}")
            else:
                st.warning("No relevant structured table found.")
else:
    st.info("Enter a query and click Search to begin.")
