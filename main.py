import asyncio
import googlemaps
import os
from dotenv import load_dotenv
import requests
from fastmcp import FastMCP

mcp = FastMCP("air_quality", "Use this to get the Universal Air Quality Index (AQI) for a given location. Give the address/location as input. DO NOT GIVE COORDINATES. If the address is not specific enough, ask for more details.", host="0.0.0.0", port=8000)

load_dotenv()
client = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

@mcp.tool()
def get_aqi(location: str) -> dict:
    geocode_res = client.geocode(location)

    location = geocode_res[0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
    lat = 40.61033339999999
    lng = -74.6336239

    aqi_res = requests.post(
        f"https://airquality.googleapis.com/v1/currentConditions:lookup?key={os.getenv('GOOGLE_MAPS_API_KEY')}",
        json={
            "universalAqi": True,
            "location": {
                "latitude": lat,
                "longitude": lng
            },
            "extraComputations": [
                "HEALTH_RECOMMENDATIONS",
                "DOMINANT_POLLUTANT_CONCENTRATION",
                "POLLUTANT_CONCENTRATION",
                "LOCAL_AQI",
                "POLLUTANT_ADDITIONAL_INFO"
            ],
            "languageCode": "en"
        }
    )

    return aqi_res.json()

if __name__ == "__main__":
    
    asyncio.run(mcp.run_async(
        transport="streamable-http",
        host="0.0.0.0",
        port=os.getenv("PORT", 8000)
    ))