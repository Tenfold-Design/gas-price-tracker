from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your actual ScraperAPI key
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY") or "YOUR_API_KEY_HERE"

@app.get("/api/gas")
def get_gas_prices(zip: str = Query(..., min_length=5, max_length=5)):
    # Build the ScraperAPI URL
    target_url = f"https://www.gasbuddy.com/home?search={zip}&fuel=1"
    scraper_url = f"https://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={target_url}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(scraper_url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text

        return {
            "status": "success",
            "source_url": target_url,
            "scraped_via": "ScraperAPI",
            "preview": html[:1000]  # Limit preview to reduce response size
        }

    except Exception as e:
        return {"error": str(e)}
