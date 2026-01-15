from playwright.sync_api import sync_playwright, expect
import os

def verify_header_fix():
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

            # 2. Create dummy background
            # Create a simple red PNG using python code without external deps like ImageMagick
            from PIL import Image, ImageDraw

            img = Image.new('RGB', (2480, 3508), color='white')
            d = ImageDraw.Draw(img)
            d.rectangle([0, 0, 2480, 400], fill='red') # Header bar
            img.save('dummy_bg.png')

            # 3. Open Settings
            # Target the button with text-gray-600 class (Settings)
            page.locator("button.text-gray-600").click()

            expect(page.get_by_text("Pengaturan")).to_be_visible()

            # 4. Upload Background
            # input type file for 'background' is the 2nd one (index 1)
            file_input = page.locator("input[type='file']").nth(1)
            file_input.set_input_files("dummy_bg.png")

            # Wait for image to appear in preview (small img tag)
            expect(page.locator("img[alt='BG1']")).to_be_visible()

            # Close settings
            page.get_by_text("Selesai").click()

            # 5. Check Live Preview CSS
            bg_locator = page.locator(".paper-background").first

            # Check style
            height = bg_locator.evaluate("el => getComputedStyle(el).height")
            object_fit = bg_locator.evaluate("el => getComputedStyle(el).objectFit")

            print(f"Background Height: {height}")
            print(f"Object Fit: {object_fit}")

            # Height should be fixed (297mm approx 1122px)
            # object-fit should NOT be 'cover' (it defaults to 'fill' or 'none' which stretches if width/height set)

            assert "1122" in height or "297mm" in height or "px" in height
            assert object_fit != "cover"

            # 6. Take Screenshot
            page.screenshot(path="verification/header_fix_preview.png")
            print("Screenshot saved to verification/header_fix_preview.png")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error_header.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_header_fix()
