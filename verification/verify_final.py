from playwright.sync_api import sync_playwright

def verify_final():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Login
        page.goto("http://localhost:8000/index.html")
        page.get_by_role("button", name="Ir. Nuruzzaman").click()
        page.fill("input[type='password']", "1234")
        page.click("button:has-text('MASUK')")

        # 2. Check "Buat Baru" button
        buat_baru = page.get_by_role("button", name="Buat Baru")
        if buat_baru.is_visible():
            print("PASS: 'Buat Baru' button is visible.")
        else:
            print("FAIL: 'Buat Baru' button missing.")

        # 3. Simulate adding data and saving to trigger logic check (we won't go through full replace flow to avoid complexity, just showing the UI)
        page.fill("input[placeholder='PT Contoh Sejahtera']", "Test Client")
        page.fill("input[placeholder='Pembangunan Tol...']", "Test Project")

        # Take screenshot of the main UI with the button
        page.screenshot(path="verification/final_ui.png")
        print("Screenshot saved to verification/final_ui.png")

        browser.close()

if __name__ == "__main__":
    verify_final()
