from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright as sp


def l1():
  url = "https://quotes.toscrape.com/js/"
  print("🚀 Initializing Headless Chromium Engine practice with XPath...")

  with sp() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = context.new_page()

    try:
      print("📡 Requesting page...")
      page.goto(url, timeout=30000)

      # FIX: Target h3 tag instead of h2 (or use //* to match regardless of tag)
      target_xpath = "xpath=//h3[contains(., 'Top Ten')]"

      print("⏳ Waiting for XPath target in DOM...")
      page.wait_for_selector(target_xpath, timeout=10000)

      title_selector = page.query_selector(target_xpath)

      if title_selector:
        print("✅ Found Title text:", title_selector.inner_text())
      else:
        print("N/A")

    except PlaywrightTimeoutError:
      print("⚠️ Timeout: Element tag or text mismatch.")
    except Exception as e:
      print(f"❌ Execution Error: {e}")
    finally:
      context.close()
      browser.close()


if __name__ == "__main__":
  l1()