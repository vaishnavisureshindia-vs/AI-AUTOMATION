from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright as sp


def run_clean_harvester():
  # Switching to a high-availability target endpoint
  url = "https://books.toscrape.com/"
  print("🚀 Testing Engine on Stable Target Endpoint...")

  with sp() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = context.new_page()

    try:
      print(f"📡 Navigating to: {url}")
      page.goto(url, timeout=10000)

      # 1. Wait for page container
      page.wait_for_selector("div.side_categories", timeout=10000)

      # 2. Extract title using native locator
      heading_element = page.locator("h1").first
      heading_text = heading_element.inner_text()

      # 3. Extract category title using native text locator
      category_element = page.get_by_text("Books", exact=True).first
      category_text = category_element.inner_text()

      print(f"✅ Main Header Found: {heading_text}")
      print(f"✅ Target Category Found: {category_text}")

    except PlaywrightTimeoutError:
      print("⚠️ Timeout: Remote server failed to respond.")
    except Exception as e:
      print(f"❌ Execution Error: {e}")
    finally:
      context.close()
      browser.close()


if __name__ == "__main__":
  run_clean_harvester()