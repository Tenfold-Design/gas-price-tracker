from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/gas")
def get_gas_prices(zip: str = Query(..., min_length=5, max_length=5)):
    url = "https://www.gasbuddy.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.gasbuddy.com/",
        "Origin": "https://www.gasbuddy.com"
    }
    payload = {
        "operationName": "LocationBySearchTerm",
        "variables": {
            "fuel": 1,
            "maxAge": 0,
            "search": zip
        },
        "query": """query LocationBySearchTerm($search: String, $fuel: Int, $maxAge: Int) {
            locationBySearchTerm(search: $search) {
              stations(fuel: $fuel, maxAge: $maxAge) {
                results {
                  name
                  address {
                    line1
                    locality
                    region
                    postalCode
                  }
                  prices {
                    fuel_product
                    cash {
                      price
                      posted_time
                    }
                    credit {
                      price
                      posted_time
                    }
                  }
                }
              }
            }
        }"""
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        stations = data.get("data", {}).get("locationBySearchTerm", {}).get("stations", {}).get("results", [])
        results = []

        for station in stations:
            name = station.get("nam
