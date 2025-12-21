from playwright.sync_api import sync_playwright

def verify_layout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Load the HTML file (assuming it's served or opened directly)
        page.goto("file:///app/index.html")

        # 1. Login
        page.click("text=Ir. Nuruzzaman")
        page.fill("input[placeholder='PIN']", "1234")
        page.click("text=MASUK")

        # Wait for App to load
        page.wait_for_selector("text=Multibangun Offer System")

        # 2. Fill Data
        page.fill("input[placeholder='Pembangunan Tol...']", "Proyek Tol Jakarta-Cikampek")
        page.fill("input[placeholder='PT Contoh Sejahtera']", "PT Karya Anak Bangsa")
        page.fill("textarea[placeholder='Jl. Raya...']", "Jl. Jend. Sudirman No. 1")

        # 3. Screenshot Preview Area
        preview_element = page.locator(".preview-paper").first
        preview_element.screenshot(path="verification/layout_preview.png")

        print("Screenshot saved to verification/layout_preview.png")

        # 4. Verify Content Text (Basic checks)
        content = preview_element.inner_text()

        assert "No: 001/MRP/PWRN/XII/2025" in content or "No: 001/MRP/PWRN/XII/2024" in content
        assert "Hal: Penawaran Harga" in content
        assert "Kepada Yth:" in content
        assert "PT KARYA ANAK BANGSA" in content # Uppercase transformation in preview
        assert "Hormat kami," in content
        assert "Technical & Marketing Manager" in content # Should not be italic in style check, but text is present

        print("Text verification passed.")

        browser.close()

if __name__ == "__main__":
    verify_layout()
