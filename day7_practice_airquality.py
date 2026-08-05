import json
import requests

url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=28.6600&longitude=77.2300&current=pm10,pm2_5,european_aqi"
response = requests.get(url)

print(f" HTTP Staus Code : {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print (data)    # output seen in the terminal
    current = data["current"]
    
    payload = {
        "Hub name": "New Delhi, India",
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "Time zone": data["timezone"],
        "Time offset seconds": data["utc_offset_seconds"],
        "time": current["time"],
        "PM 2.5":current["pm2_5"],
        "Indian AQI": current["european_aqi"],
        "Air Quality safety flag": current["pm2_5"] <= 25 ,
        "Alert Level": "SAFE AIR" if current["european_aqi"] <= 50 else "UNHEALTHY AIR"
    }
    with open("airquality_report.json", "w", encoding="utf-8") as f:
        json.dump(payload,f, indent=3)         # payload dictionary info updated in the created json file
    print(f"Fetch Successful ! Status: {payload['Alert Level']}")   

else:
    print(f" Failed to Fetch Air Quality Details! Status: {response.status_code}")  



