import json
import requests

# 1. Take city name input from user
city_name = input("Enter City Name (e.g., Kochi, New Delhi, Thrissur): ").strip()     # removes any accidental trailing/leading whitespaces from the text user input
days = int(input("Enter No. of Tracking Days: "))

# 2. Call Geocoding API to resolve coordinates (to get the place longitude, latitude for further weather forecast)
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {
    "name": city_name,
    "count": 1,
    "language": "en",
    "format": "json"
}

geo_response = requests.get(geo_url, params=geo_params)

if geo_response.status_code == 200 and "results" in geo_response.json():
    geo_data = geo_response.json()["results"][0]
    
    lat = geo_data["latitude"]
    lon = geo_data["longitude"]
    resolved_name = f"{geo_data['name']}, {geo_data.get('country', '')}"
    
    print(f"Location Found: {resolved_name} (Lat: {lat}, Lon: {lon})")

    # 3. Fetch Weather Data using resolved coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,wind_speed_10m_max",
        "forecast_days": days,
        "timezone": "auto"
    }

    response = requests.get(weather_url, params=weather_params)

    if response.status_code == 200:
        data = response.json()
        daily = data["daily"]
        daily_schedule = []

        for date, temp, wind in zip(daily["time"], daily["temperature_2m_max"], daily["wind_speed_10m_max"]):
            status = "HIGH_WIND_WARNING" if wind > 15.0 else "OPERATIONAL_SAFE"
            daily_schedule.append({
                "date": date,
                "max_temp_c": temp,
                "max_wind_kmh": wind,
                "dispatch_status": status
            })

        payload = {
            "hub_location": resolved_name,
            "forecast_days_count": len(daily_schedule),
            "daily_schedule": daily_schedule
        }

        with open("dynamic_dispatch_plan.json", "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=3)

        print("Dispatch schedule created successfully!")

    else:
        print(f"Failed to fetch weather data. Code: {response.status_code}")

else:
    print(f"Could not find coordinates for city: '{city_name}'")