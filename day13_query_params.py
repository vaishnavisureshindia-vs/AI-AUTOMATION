import json
import os
import requests
from dotenv import load_dotenv

# 1. Environment & Configuration Guard
load_dotenv()

# We use a reliable public testing endpoint for dynamic query requests
base_url = "https://httpbin.org/get"

# 2. Define Dynamic Query Parameters
search_criteria = {
    "category": "AI Automation",
    "limit": 5,
    "page": 1,
    "status": "active",
}

# 3. Defensive Request Pipeline
try:
  print("📡 Sending GET request with dynamic query parameters...")

  # The params dictionary is automatically formatted into ?category=AI+Automation&limit=5...
  response = requests.get(base_url, params=search_criteria, timeout=5)

  # Check for 2xx success (raises exception for 4xx/5xx)
  response.raise_for_status()

  data = response.json()

  print(
      f"🎉 SUCCESS! Request URL constructed by library:\n{response.url}\n"
  )
  print("Reflected Query Parameters from Server:")
  print(json.dumps(data.get("args"), indent=2))

except requests.exceptions.RequestException as err:
  print(f"❌ Network Request Failed: {err}")
  exit(1)