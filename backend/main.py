from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY") or "YOUR_API_KEY_HERE"

@app.get("/api/gas")
def get_gas_prices(zip: str = Query(..., min_length=5, max_length=5)):
    scraper_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url=https://www.gasbuddy.com/home?search={zip}&fuel=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(scraper_url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        # Placeholder parsing, replace with real HTML logic
        return {"status": "success", "message": "HTML fetched via ScraperAPI", "preview": html[:500]}

    except Exception as e:
        return {"error": str(e)}
