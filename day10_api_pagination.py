import json
import requests

current_page = 1
max_pages = 3      # Fetch 3 pages total
items_per_page = 10
all_comments = []  # Master list for aggregated records

print("--- Starting Multi-Page Ingestion ---")

while current_page <= max_pages:
    url = "https://jsonplaceholder.typicode.com/comments"
    query_params = {
        "_page": current_page,
        "_limit": items_per_page
    }

    try:
        response = requests.get(url, params=query_params, timeout=5)
        response.raise_for_status()
        page_data = response.json()

        # Stop if an empty list is returned
        if not page_data:
            print(f"No more data available at Page {current_page}.")
            break

        # Extend master list with items from the current page
        all_comments.extend(page_data)
        print(f"✅ Page {current_page} fetched: {len(page_data)} comments added.")

        current_page += 1

    except requests.exceptions.RequestException as err:
        print(f"❌ Error fetching Page {current_page}: {err}")
        break

# Save final aggregated dataset
payload = {
    "status": "SUCCESS",
    "pages_processed": current_page - 1,
    "total_records_retrieved": len(all_comments),
    "comments": all_comments
}

with open("aggregated_comments.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=3)

print("--- Processing Complete! Output saved to aggregated_comments.json ---")