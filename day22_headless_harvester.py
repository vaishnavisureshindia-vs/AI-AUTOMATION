import sys
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def run_headless_harvester():
  # Target dynamic URL for testing DOM extraction
  target_url = "https://quotes.toscrape.com/js/"

  print("🚀 Initializing Headless Chromium Engine...")

  with sync_playwright() as p:
    # Step 1: Launch Headless Browser Instance (headless=True runs in background)
    browser = p.chromium.launch(headless=True)

    # Step 2: Open an Isolated Browser Context (Acts like a fresh Incognito session)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )

    # Step 3: Open a New Page Tab
    page = context.new_page()

    try:
      print(f"📡 Navigating to target: {target_url}")

      # Step 4: Navigate and Wait for Network to Settle (Handles JS Rendering)
      page.goto(target_url, wait_until="networkidle", timeout=15000)

      # Step 5: Query DOM Tree Elements using CSS Selectors
      quote_elements = page.query_selector_all("div.quote")

      print(
          f"✅ Page Rendered Successfully! Extracted {len(quote_elements)}"
          " DOM elements.\n"
      )

      print("--- 📊 Harvested Dynamic Elements ---")
      for index, quote in enumerate(quote_elements[:3], start=1):
        # Extract inner text of child nodes inside each quote container
        text_node = quote.query_selector("span.text")
        author_node = quote.query_selector("small.author")

        quote_text = text_node.inner_text() if text_node else "N/A"
        author_name = author_node.inner_text() if author_node else "N/A"

        print(f"[{index}] Author: {author_name}")
        print(f"    Quote: {quote_text}\n")

    except PlaywrightTimeoutError:
      print("⚠️ Network timeout reached before page fully rendered.")
    except Exception as e:
      print(f"❌ Execution Error: {e}")
    finally:
      # Step 6: Clean Shutdown of Browser Context and Process Streams
      context.close()
      browser.close()
      print("✅ Headless Browser Streams Closed Safely.")


if __name__ == "__main__":
  run_headless_harvester()