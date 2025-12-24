from playwright.sync_api import sync_playwright

def verify_rich_text_screenshot():
    print("Starting rich text screenshot verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        page.goto("http://localhost:8000/index.html")

        # Login
        page.click("text=Ir. Nuruzzaman")
        page.fill("input[placeholder='PIN']", "1234")
        page.click("text=MASUK")

        page.on("dialog", lambda dialog: dialog.accept())

        # Switch to Material Tab
        print("Switching to Material tab...")
        page.click("text=Penawaran Material")
        page.wait_for_timeout(1000)

        # Clear first item and type custom text
        print("Editing text...")
        textarea = page.locator("table tbody tr textarea").first
        textarea.fill("Custom Label: Value\nThis is *bold* text.")

        # Take screenshot of the preview area
        screenshot_path = "/home/jules/verification/preview_rich_text.png"
        page.locator(".preview-paper").first.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_rich_text_screenshot()
