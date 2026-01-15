import re
from playwright.sync_api import sync_playwright

def verify_bolding():
    print("Starting verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        page.goto("http://localhost:8000/index.html")

        # Login
        page.click("text=Ir. Nuruzzaman")
        page.fill("input[placeholder='PIN']", "1234")
        page.click("text=MASUK")

        # Handle Confirm Dialog
        page.on("dialog", lambda dialog: dialog.accept())

        # Switch to Material Tab
        print("Switching to Material tab...")
        page.click("text=Penawaran Material")

        # Wait for update
        page.wait_for_timeout(1000)

        # Debug: Check text content of description to ensure we are on right tab
        desc_text = page.locator(".preview-paper .paper-content table tbody tr td").first.text_content()
        print(f"Cell text content: {desc_text[:50]}...")

        # Check HTML Preview for bold labels
        print("Checking HTML Preview for bold labels...")

        merk_bold = page.locator(".preview-paper .paper-content table span.font-bold:has-text('Merk:')")

        if merk_bold.count() > 0:
            print("SUCCESS: Found 'Merk:' in bold span.")
        else:
            print("FAILURE: 'Merk:' not found in bold span.")
            print("First cell HTML:", page.locator(".preview-paper .paper-content table tbody tr td").first.inner_html())

        browser.close()

if __name__ == "__main__":
    verify_bolding()
