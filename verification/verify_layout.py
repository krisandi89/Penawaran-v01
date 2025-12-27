
from playwright.sync_api import sync_playwright, expect
import re

def verify_layout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Navigate to app
        page.goto("http://localhost:8000")

        # 2. Login
        page.get_by_role("button", name="Ir. Nuruzzaman").click()
        page.get_by_placeholder("PIN").fill("1234")
        page.get_by_role("button", name="MASUK").click()

        # 3. Handle Dialogs (Confirmations)
        page.on("dialog", lambda dialog: dialog.accept())

        # 4. Switch Tab to 'Penawaran Material'
        # This triggers a confirm dialog which we accept above
        page.get_by_role("button", name="Penawaran Material", exact=True).click()

        # Wait for tab switch - check class contains 'text-blue-600'
        # We use a regex to match partial class
        expect(page.get_by_role("button", name="Penawaran Material", exact=True)).to_have_class(re.compile(r"text-blue-600"))

        # 5. Verify Preview
        # The default material tab has 1 item.
        # Verify preview shows only 1 page.

        # Wait for preview to render
        page.wait_for_selector(".preview-paper")

        # Allow time for React render loop
        page.wait_for_timeout(1000)

        papers = page.locator(".preview-paper")
        count = papers.count()
        print(f"Number of pages: {count}")

        # Take screenshot
        page.screenshot(path="verification/layout_fix.png", full_page=True)

        if count == 1:
            print("SUCCESS: Content fits on 1 page.")
        else:
            print("FAILURE: Content split into multiple pages.")

        browser.close()

if __name__ == "__main__":
    verify_layout()
