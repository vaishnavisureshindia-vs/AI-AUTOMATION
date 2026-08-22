# Bearer Token Authentication Practice 
import json
import os
import requests
from dotenv import load_dotenv

# 1. Load secret token from .env
load_dotenv()
api_token = os.getenv("MOCK_API_KEY")

if not api_token:
  print("🚨 ERROR: MOCK_API_KEY missing from .env file!")
  exit(1)

# 2. Construct production-grade headers
headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/json",
    "User-Agent": "AutomationPipeline/1.0 (DevStudio)",
}

endpoint_url = "https://httpbin.org/headers"

# 3. Execute GET request with custom headers
try:
  print("📡 Sending authenticated request with custom headers...")
  response = requests.get(endpoint_url, headers=headers, timeout=5)
  response.raise_for_status()

  data = response.json()
  print("🎉 Server successfully validated and reflected our headers!")
  print(json.dumps(data, indent=2))

except requests.exceptions.RequestException as err:
  print(f"❌ Request failed: {err}")