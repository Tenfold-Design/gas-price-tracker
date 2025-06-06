from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
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
},
        "query": """
        query LocationBySearchTerm($search: String, $fuel: Int, $maxAge: Int) {
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
        }
        """
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        stations = data.get("data", {}).get("locationBySearchTerm", {}).get("stations", {}).get("results", [])
        results = []

        for station in stations:
            name = station.get("name")
            address_info = station.get("address", {})
            address = f"{address_info.get('line1', '')}, {address_info.get('locality', '')}, {address_info.get('region', '')} {address_info.get('postalCode', '')}"
            prices = station.get("prices", [])
            if prices:
                price_info = prices[0]  # Assuming regular gas is the first entry
                price = price_info.get("cash", {}).get("price") or price_info.get("credit", {}).get("price")
                updated = price_info.get("cash", {}).get("posted_time") or price_info.get("credit", {}).get("posted_time")
                results.append({
                    "name": name,
                    "address": address,
                    "price": price,
                    "updated": updated
                })

        return results

    except Exception as e:
        return {"error": str(e)}
