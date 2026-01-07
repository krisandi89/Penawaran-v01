from playwright.sync_api import sync_playwright

def verify_button_and_screenshot():
    print("Starting visual verification of Buat Baru button...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("http://localhost:8000/index.html")

        if page.is_visible("text=Login Multibangun"):
            page.click("text=Ir. Nuruzzaman")
            page.fill("input[placeholder='PIN']", "1234")
            page.click("text=MASUK")

        # Wait for Navbar to be visible
        page.wait_for_selector("text=Multibangun Offer System")

        # Take screenshot of the navbar area where "Buat Baru" is
        # We can locate the navbar container
        navbar = page.locator(".sticky.top-0")
        screenshot_path = "/home/jules/verification/buat_baru_button.png"
        navbar.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_button_and_screenshot()
