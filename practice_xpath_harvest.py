from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright as sp

def l1():
    url = "https://quotes.toscrape.com/js/"
    print("🚀 Initializing Headless Chromium Engine practice with X path...")

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
            page.goto(url,wait_until= "networkidle",timeout=15000)
            target_xpath="xpath=//h2[contains(., 'Top Ten')]"
            page.wait_for_selector(target_xpath, timeout=15000)
            title_selector = page.query_selector(target_xpath)

                                                 
            if title_selector:
                title_main = title_selector.inner_text()
                print(" Found Title text: ",title_main)
            else:
               print("N/A")

        except PlaywrightTimeoutError:
            print("⚠️ Network timeout reached before page fully rendered.")
        except Exception as e:
            print(f"❌ Execution Error: {e}")
        finally:
            context.close()
            browser.close()
        
if __name__ == "__main__":
   l1()