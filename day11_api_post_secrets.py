import os
import json
import requests
from dotenv import load_dotenv

# 1. Load variables from .env file into environment
load_dotenv()

# 2. Extract values securely
api_key = os.getenv("MOCK_API_KEY")
base_url = os.getenv("SERVICE_BASE_URL")

# Guard Clause: Ensure secrets exist before hitting the network
if not api_key or not base_url:
    print("🚨 ERROR: Missing environment variables in .env file!")
    exit(1)

print("✅ Secrets loaded securely from .env file.")

# 3. Define POST payload
new_user_payload = {
    "name": "Sarah Connor",
    "job": "Automation Engineer",
    "skills": ["Python", "API Integration", "System Architecture"]
}

# 4. Set custom headers
headers = {
    "Content-Type": "application/json"
}

# 5. Send POST request inside try-except
try:
    print("📡 Sending POST request to server...")
    
    response = requests.post(
        base_url,
        json=new_user_payload,
        headers=headers,
        timeout=5
    )
    response.raise_for_status()
    response_data = response.json()

    print(f"🎉 Success! HTTP Status Code: {response.status_code}")
    
    log_payload = {
        "status": "SUCCESS",
        "http_code": response.status_code,
        "created_user_id": response_data.get("id"),
        "created_at": response_data.get("createdAt"),
        "server_response": response_data
    }

    with open("user_creation_log.json", "w", encoding="utf-8") as f:
        json.dump(log_payload, f, indent=3)

    print("📁 Registration details saved to user_creation_log.json")

except requests.exceptions.RequestException as err:
    print(f"❌ Network Request Failed: {err}")