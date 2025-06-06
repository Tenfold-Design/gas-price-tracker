from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Station(BaseModel):
    name: str
    address: str
    price: float
    updated: str

@app.get("/api/gas", response_model=List[Station])
async def get_gas_prices(zip: str = Query(...)):
    url = f"https://www.gasbuddy.com/home?search={zip}&fuel=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    listings = soup.select("div.GasStationListItem")

    stations = []
    for item in listings:
        try:
            name = item.select_one(".station-name").text.strip()
            address = item.select_one(".station-address").text.strip()
            price_text = item.select_one(".fuel-price").text.strip()
            price = float(price_text.replace("$", ""))
            updated = item.select_one(".report-time").text.strip()
            stations.append(Station(name=name, address=address, price=price, updated=updated))
        except:
            continue
    stations.sort(key=lambda x: x.price)
    return stations[:10]
