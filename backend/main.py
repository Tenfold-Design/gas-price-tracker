from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SCRAPER_API_KEY = "de52e1cbf1583015dc81e2bc74161d9e"
SCRAPER_URL = "http://api.scraperapi.com"

@app.get("/api/gas")
async def get_gas_prices(zip: str):
    target_url = f"https://www.gasbuddy.com/home?search={zip}&fuel=1"
    response = requests.get(
        SCRAPER_URL,
        params={"api_key": SCRAPER_API_KEY, "url": target_url}
    )

    if response.status_code != 200:
        return {"status": "error", "message": "Failed to fetch data."}

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    cards = soup.find_all("div", class_="GenericStationListItem__stationListItem___3Jmn4")

    for card in cards:
        try:
            name = card.find("h3").text.strip()
            price = card.find("span", class_="StationDisplayPrice__price___3rARL").text.strip()
            address = card.find("div", class_="StationDisplay__address___1U4sr").text.strip()
            results.append({
                "name": name,
                "price": price,
                "address": address
            })
        except Exception:
            continue

    return {
        "status": "success",
        "zip": zip,
        "source_url": target_url,
        "stations": results
    }
