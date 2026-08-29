import logging
import time
import requests

# Initialize Permanent Audit Log File
logging.basicConfig(
    filename="pipeline_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

base_url = "https://httpbin.org/get"

print("--- 🚀 Resilient Dynamic Data Harvester ---")
search_term = input("Enter search topic (e.g., AI & Automation): ")
max_pages = int(input("Enter total pages to harvest: "))

logging.info(f"\n Pipeline started for topic '{search_term}', pages: {max_pages}")

for page in range(1, max_pages + 1):
    params = {"q": search_term, "page": page, "limit": 5}
    
    max_retries = 3
    backoff_delay = 2  # Starting delay in seconds
    success = False
    
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url, params=params, timeout=5)
            
            # Defensive Throttling Guardrail (HTTP 429)
            if response.status_code == 429:
                logging.warning(f"Rate limit hit on Page {page} (Attempt {attempt + 1}/{max_retries}). Backing off for {backoff_delay}s...")
                print(f"⚠️ Rate limit hit. Retrying in {backoff_delay} seconds...")
                time.sleep(backoff_delay)
                backoff_delay *= 2  # Exponentially scale wait time
                continue
                
            # Safely raise exceptions for other HTTP errors (4xx/5xx)
            response.raise_for_status()
            
            logging.info(f"Successfully harvested Page {page}: {response.url}")
            print(f"✅ Harvested Page {page} successfully!")
            success = True
            break  # Break out of retry loop on success
            
        except requests.exceptions.RequestException as err:
            logging.error(f"Network error on Page {page}, Attempt {attempt + 1}: {err}")
            print(f"❌ Connection issue on Page {page}. Retrying...")
            time.sleep(backoff_delay)
            backoff_delay *= 2

    if not success:
        logging.critical(f"Pipeline permanently failed on Page {page} after {max_retries} attempts.")
        print(f"🚨 Failed to harvest Page {page}. Check pipeline_audit.log for deep diagnostics.")
        break

    # Respectful courtesy sleep between different page calls
    time.sleep(1)

logging.info("Pipeline execution completed.")