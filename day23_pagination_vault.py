import sqlite3
import sys
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DB_FILE = "harvester_vault.db"


def init_db():
  """Establishes persistent SQLite schema for multi-page book harvesting."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS multi_page_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            price TEXT NOT NULL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  conn.commit()
  conn.close()


def run_pagination_vault():
  init_db()
  base_url = "https://books.toscrape.com/"
  max_pages = 3  # Circuit breaker threshold to prevent accidental infinite loops
  current_page = 1

  print("🚀 Initializing Multi-Page Harvester with SQLite Vault Integration...")

  with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
    )
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ),
    )
    page = context.new_page()

    try:
      print(f"📡 Navigating to initial page: {base_url}")
      page.goto(base_url, timeout=30000)

      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()

      total_inserted = 0
      total_duplicates = 0

      while current_page <= max_pages:
        print(f"\n--- 📄 Processing Page {current_page} ---")

        # 1. Synchronization Guard: Wait for grid products to render
        page.wait_for_selector("article.product_pod", timeout=10000)
        book_nodes = page.query_selector_all("article.product_pod")

        print(
            f"✅ Page {current_page}: Harvested {len(book_nodes)} product"
            " cards."
        )

        page_inserted = 0
        page_duplicates = 0

        # 2. Extract and persist items from current page
        for node in book_nodes:
          title_element = node.query_selector("h3 > a")
          title = (
              title_element.get_attribute("title")
              if title_element
              else "Unknown"
          )

          price_element = node.query_selector("p.price_color")
          price = price_element.inner_text() if price_element else "N/A"

          try:
            cursor.execute(
                """
                            INSERT INTO multi_page_books (title, price)
                            VALUES (?, ?)
                        """,
                (title, price),
            )
            page_inserted += 1
          except sqlite3.IntegrityError:
            page_duplicates += 1

        conn.commit()
        total_inserted += page_inserted
        total_duplicates += page_duplicates

        print(
            f"   💾 Saved {page_inserted} new items | 🛡️ {page_duplicates}"
            " duplicates skipped"
        )

        # 3. Locate Next Page navigation button
        next_button = page.query_selector("li.next > a")

        if not next_button:
          print("\n🛑 No 'Next' page button found. Reached end of pagination.")
          break

        if current_page >= max_pages:
          print(
              f"\n🛑 Target page limit reached ({max_pages} pages max)."
              " Stopping pagination."
          )
          break

        # 4. Programmatic Click & Wait Cycle
        print("➡️ Navigating to next page...")
        next_button.click()
        current_page += 1

      conn.close()

      print("\n=========================================")
      print("🎉 Multi-Page Harvesting Complete!")
      print(f"📦 Total New Records Stored: {total_inserted}")
      print(f"🛡️ Total Duplicates Skipped: {total_duplicates}")
      print("=========================================")

    except PlaywrightTimeoutError:
      print("⚠️ Timeout: Server response or DOM load stalled.")
    except Exception as e:
      print(f"❌ Execution Error: {e}")
    finally:
      context.close()
      browser.close()
      print("\n✅ Streams and Browser Instances Closed Cleanly.")


if __name__ == "__main__":
  run_pagination_vault()