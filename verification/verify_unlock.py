from playwright.sync_api import sync_playwright, expect
import time

def verify_unlock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        try:
            # 1. Login
            page.goto("http://localhost:8000")
            page.get_by_text("Ir. Nuruzzaman").click()
            page.get_by_placeholder("PIN").fill("1234")
            page.get_by_role("button", name="MASUK").click()

            # Wait for main screen
            expect(page.get_by_text("Multibangun Offer System")).to_be_visible()

            # 2. Switch to 'Penawaran Material' Tab
            # NOTE: Confirming dialog might appear
            page.on("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="Penawaran Material", exact=True).click()

            # 3. Verify the item is a textarea (unlocked)
            # The item description should contain "Material Geomembrane HDPE"
            # It should be in a textarea, not structured div
            textarea = page.locator("table textarea").first
            expect(textarea).to_be_visible()

            content = textarea.input_value()
            print(f"Textarea content: {content}")

            assert "Material Geomembrane HDPE" in content
            assert "Merk: Geoprotec" in content

            # 4. Verify HTML Preview
            # The preview is on the right side.
            # It should show the same text with newlines respected.
            preview_cell = page.locator(".paper-content table tbody tr td").first
            preview_text = preview_cell.inner_text()
            print(f"Preview text: {preview_text}")

            # Check for newlines/formatting visually via screenshot
            # But we can also check if text contains newlines or if separate divs are NOT used (legacy)
            # Legacy used: div > div.font-bold > Merk: ...
            # New uses: plain text inside td with whitespace-pre-wrap

            # 5. Take Screenshot
            page.screenshot(path="verification/unlocked_preview.png")
            print("Screenshot saved to verification/unlocked_preview.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_unlock()
