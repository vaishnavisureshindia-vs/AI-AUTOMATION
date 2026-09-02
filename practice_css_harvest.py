from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright as sp

def l1_inst():
    url = "https://quotes.toscrape.com/js/"
    print("🚀 Initializing Headless Chromium Engine practice with CSS...")

    with sp() as p :  #Magic Portal "p" door opening 
        try:
            browser = p.chromium.launch(headless=True)   #calling the ghost
            page = browser.new_page()
            page.goto(url,wait_until= "networkidle",timeout=10000)
            title_selector = page.query_selector("h1 a")
            if title_selector:
                title_main = title_selector.inner_text()
                print(" Found Title text: ",title_main)
            else:
                print("N/A")
            
        except PlaywrightTimeoutError:
            print("⚠️ Network timeout reached before page fully rendered.")
        except Exception as e:
            print(f"❌ Execution Error: {e}")

        browser.close()
if __name__ == "__main__":
   l1_inst()


