import json
import requests

city_name = input("Enter City Name (e.g., Kochi, New Delhi, Thrissur): ").strip()     # removes any accidental trailing/leading whitespaces from the text user input
days = int(input("Enter No. of Tracking Days: "))
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
geo_params = {
    "name": city_name,
    "count": 1,
    "language": "en",
    "format": "json"
    }

try: 
    # 1. Fetch geocoding data (protected)
    geo_response = requests.get(geo_url, params=geo_params, timeout = 5)
    geo_response.raise_for_status()
    status = "SUCCESS"
    print(status)

    if geo_response.status_code == 200 and "results" in geo_response.json():
        geo_data = geo_response.json()["results"][0]
        lat = geo_data["latitude"]
        lon = geo_data["longitude"]
        resolved_name = f"{geo_data['name']}, {geo_data.get('country', '')}"
            
        print(f"Location Found: {resolved_name} (Lat: {lat}, Lon: {lon})")
        
        # 2. Fetch Weather Data using resolved coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,wind_speed_10m_max",
                "forecast_days": days,
                "timezone": "auto"
            }
        
        weather_response = requests.get(weather_url, params=weather_params, timeout=5)
        weather_response.raise_for_status()
        data = weather_response.json()

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
            with open("weather_log.json", "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=3)

        print("Dispatch schedule created successfully!")
    else:
        print(f"Could not find coordinates for city: '{city_name}'")

# Exceptions Handler Block
except requests.exceptions.Timeout:
    print(" Error: The request timed out")
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
    print(f"Network error occurred: {err}")
except requests.exceptions.JSONDecodeError as jsderr:
    print(f"JSON decode error occurred: {jsderr}")
