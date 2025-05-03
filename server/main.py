from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.query_tavily import run_query

app = FastAPI()

# מאפשר ל-frontend (כמו Streamlit או React) לפנות ל-API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # אם את רוצה להגביה את זה אחר כך — שימי פה את הדומיין שלך
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
async def query_data(req: Request):
    body = await req.json()
    query = body.get("query", "")
    results = run_query(query)
    return {"data": results}
