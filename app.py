from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd

app = FastAPI()

# Autoriser accès depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Charger le CSV
df = pd.read_csv("materiaux.csv", dtype=str).fillna("")

@app.get("/search/")
def search(q: str):
    q = q.lower()
    results = df[df.apply(
        lambda row: q in row["code"].lower() or q in row["designation"].lower(),
        axis=1
    )]
    return results.to_dict(orient="records")

# Servir le frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
