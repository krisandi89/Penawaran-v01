from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the page
        page.goto('http://localhost:8080/index.html')

        # Handle login if needed
        if page.is_visible("text=Login Multibangun"):
            print("Login screen detected. Logging in...")
            # Click first user
            page.click("text=Ir. Nuruzzaman")
            # Enter PIN
            page.fill("input[placeholder='PIN']", "1234")
            # Click Masuk
            page.click("text=MASUK")
            print("Logged in.")

        # Wait for "UP (Person)" input to appear
        page.wait_for_selector("text=UP (Person)")

        # Check for "Tambah No. Telpon" button
        if page.is_visible("text=Tambah No. Telpon"):
            print("Button 'Tambah No. Telpon' found.")
            # Click it
            page.click("text=Tambah No. Telpon")
            print("Clicked 'Tambah No. Telpon'.")
        else:
            print("Button 'Tambah No. Telpon' NOT found.")

        # Check for "Tambah Email" button
        if page.is_visible("text=Tambah Email"):
            print("Button 'Tambah Email' found.")
            # Click it
            page.click("text=Tambah Email")
            print("Clicked 'Tambah Email'.")
        else:
            print("Button 'Tambah Email' NOT found.")

        # Verify inputs appeared
        page.wait_for_selector("text=No. Telpon")
        page.wait_for_selector("text=Email")
        print("Inputs appeared.")

        # Fill inputs
        page.fill("input[placeholder='081...']", "08123456789")
        page.fill("input[placeholder='email@example.com']", "test@example.com")
        page.fill("input[placeholder='Bpk. Budi']", "Bpk. Tester")

        # Take screenshot of the form area
        page.screenshot(path="verification/frontend_form_verification.png")
        print("Screenshot 'frontend_form_verification.png' saved.")

        # Scroll to Preview area
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Wait for preview update (React re-render)
        page.wait_for_timeout(1000)

        # Take screenshot of the preview
        page.screenshot(path="verification/frontend_preview_verification.png")
        print("Screenshot 'frontend_preview_verification.png' saved.")

        browser.close()

if __name__ == "__main__":
    verify_frontend()
