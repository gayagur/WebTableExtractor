import requests
import os

TAVILY_API_KEY = "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"

def run_query(query: str):
    headers = {
        "Authorization": f"Bearer {TAVILY_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "include_raw_content": False,
        "include_images": False,
        "include_tables": True
    }

    response = requests.post("https://api.tavily.com/search", json=body, headers=headers)

    if response.ok:
        results = response.json()
        if "tables" in results and results["tables"]:
            return results["tables"][0]["rows"]
        else:
            return [{"Error": "No table found in results"}]
    else:
        return [{"Error": f"API request failed: {response.text}"}]
