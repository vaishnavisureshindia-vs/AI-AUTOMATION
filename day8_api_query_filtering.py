import json
import requests

url = "https://api.open-meteo.com/v1/forecast"
days = int(input(" No: of Tracking days : "))

query_params ={
    "latitude": 9.312,
    "longitude": 76.2673,
    "daily": "temperature_2m_max,wind_speed_10m_max",
    "forecast_days": days,
    "timezone": "auto"
    }
response = requests.get(url,params=query_params)

if response.status_code == 200:
    data = response.json()
    print(" Processing the Forecast : ")
    daily = data["daily"]  #daily is a dictionary key like others - "longitude", "latitude", "timezone"
    daily_schedule = []

    for date,temp,wind in zip(daily["time"],daily["temperature_2m_max"],daily["wind_speed_10m_max"]):   # zip pairs the index wise information in "daily" list together so that a single day info is accessed in 1 loop
        day_entry = {
            "date":date,
            "max_temp_c": temp,
            "max_wind_kmh": wind,
            "dispatch_status" :"HIGH WIND WARNING" if wind > 15.0 else "OPERATIONAL SAFE"
        }
        daily_schedule.append(day_entry)

    payload = {
        "hub_location" : "Kochi Port Hub",
        "forecast_days_count": len(daily_schedule),
        "daily schedule": daily_schedule 
    }
    with open("3day_dispatch_plan.json","w",encoding ="utf-8") as f:
        json.dump(payload,f,indent=3)
    print(" Dispatch schedule created successfully !")       

    with open("3day_dispatch_plan.json","r",encoding ="utf-8") as f:
        file = json.load(f)

        print("=="*25)
        print(" Forecast Report for Dispatch : ")
        print("=="*25)
        print(json.dumps(file, indent = 3))
else:
    print(f" Failed to fetch forecast data. Code: {response.status_code}")       
