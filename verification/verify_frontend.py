from playwright.sync_api import sync_playwright

def verify_frontend_screenshot():
    print("Starting frontend screenshot verification...")
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

        # Take screenshot of the preview area
        # preview-paper
        screenshot_path = "/home/jules/verification/preview_bolding.png"
        page.locator(".preview-paper").first.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_frontend_screenshot()
