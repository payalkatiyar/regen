import time
from playwright.sync_api import sync_playwright

# Replace this with your exact Streamlit Community Cloud URL
APP_URL = "https://regen-grid-prediction.streamlit.app/"

def wake_up_app():
    with sync_playwright() as p:
        print("Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"Navigating to {APP_URL}...")
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(5)  # Wait for any lazy elements to load
        
        # Look for Streamlit's default "Wake up app" button text
        wake_button = page.get_by_role("button", name="Wake up app", exact=False)
        
        if wake_button.is_visible():
            print("App is asleep! Clicking the 'Wake up app' button...")
            wake_button.click()
            time.sleep(10)  # Give it time to trigger the spin-up process
            print("Wake up signal sent successfully.")
        else:
            print("App is already awake and running fine.")
            
        browser.close()

if __name__ == "__main__":
    wake_up_app()
