"""
===============================================================================
SCRIPT NAME    : resilient_harvester.py
DESCRIPTION    : Dynamic Paginated API Data Harvester with Rate-Limit Backoff
                 and File Logging.
OBJECTIVE      : Harvest multi-page API datasets dynamically while handling network
                 throttling (HTTP 429) gracefully and maintaining a permanent audit log.
PURPOSE        : Demonstrates how enterprise automation scripts query dynamic paginated
                 endpoints, handle rate limits defensively, and log status to disk.
===============================================================================
"""

import logging
import time
import requests

# 1. Initialize Permanent Audit Log File
logging.basicConfig(
    filename="pipeline_audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

base_url = "https://httpbin.org/get"

print("--- 🚀 Resilient Dynamic Data Harvester ---")
search_term = input("Enter search topic (e.g., AI & Automation): ")
max_pages = int(input("Enter total pages to harvest: "))

logging.info(f"Pipeline started for topic '{search_term}', pages: {max_pages}")

for page in range(1, max_pages + 1):
  params = {"q": search_term, "page": page, "limit": 5}

  try:
    response = requests.get(base_url, params=params, timeout=5)

    # Rate Limiting Guardrail (HTTP 429 Too Many Requests)
    if response.status_code == 429:
      logging.warning(
          f"Rate limit hit on Page {page}. Cooling off for 5 seconds..."
      )
      print(f"⚠️ Rate limit hit on Page {page}. Retrying in 5 seconds...")
      time.sleep(5)
      continue

    response.raise_for_status()

    logging.info(f"Successfully harvested Page {page}: {response.url}")
    print(f"✅ Harvested Page {page} successfully!")

    # Respectful throttling delay between requests
    time.sleep(1)

  except requests.exceptions.RequestException as err:
    logging.error(f"Pipeline failed on Page {page}: {err}")
    print(f"❌ Error on Page {page}. Check pipeline_audit.log for details.")
    break

logging.info("Pipeline execution completed.")