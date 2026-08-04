import json
import requests

# Open Meteo weather API
url = "https://api.open-meteo.com/v1/forecast?latitude=8.5241&longitude=76.9366&current_weather=true"

response = requests.get(url)

print(f" HTTP Staus Code : {response.status_code}")

if response.status_code == 200:
    data = response.json()
    current = data["current_weather"]
    temp = current["temperature"]
    wind_speed = current["windspeed"] 

    if wind_speed > 20.0:
        safety_flag = False 
    else:
        safety_flag = True

    payload = {
        "location": "Thiruvanthapuram Hub", 
        "latitude": data["latitude"],
        "longitude":data["longitude"],
        "temperature_c": temp, 
        "wind_spped_kmh":wind_speed, 
        "safetyflag":current["windspeed"] <= 20.0 ,  # assigns True if wind speed <=20, else it assigns False.
        "dispatch_status":"DISPATCH SAFE ✔️"if current["windspeed"] <= 20.0 else "DISPATCH HIGH RISK WIND 🚨"
        }

    with open ("live_dispatch_weather.json","w",encoding="utf8") as weatherjson:
        json.dump(payload, weatherjson, indent=4)
    print(f"Fetch Successful ! Status: {payload['dispatch_status']}")    

else:
    print(f" API REQUEST FAILED 🚨! Status Code: {response.status_code}")

