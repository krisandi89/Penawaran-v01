from playwright.sync_api import sync_playwright, expect
import time

def verify_add_material():
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
            page.on("dialog", lambda dialog: dialog.accept())
            page.get_by_role("button", name="Penawaran Material", exact=True).click()

            # 3. Click "Tambah Material"
            # It should be visible now in this tab
            add_btn = page.get_by_role("button", name="Tambah Material")
            expect(add_btn).to_be_visible()
            add_btn.click()

            # 4. Verify new item added
            # We expect 2 items now. The first one was the default, the second one is new.
            textareas = page.locator("table textarea")
            expect(textareas).to_have_count(2)

            new_item_text = textareas.nth(1).input_value()
            print(f"New Item Text: {new_item_text}")

            assert "Material Baru" in new_item_text
            assert "Merk:" in new_item_text

            # 5. Take Screenshot
            page.screenshot(path="verification/add_material_verified.png")
            print("Screenshot saved to verification/add_material_verified.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_add_material.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_add_material()
