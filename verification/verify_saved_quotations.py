from playwright.sync_api import sync_playwright

def verify_saved_quotations():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the app
        page.goto("http://localhost:8000/index.html")

        try:
            page.wait_for_selector("text=Login Multibangun", timeout=5000)
            print("Login screen found")

            # Login first
            # Click user 3 (Admin)
            page.click("text=Admin Penawaran")

            # Fill PIN
            page.fill("input[placeholder='PIN']", "1234")

            # Click MASUK
            page.click("button:has-text('MASUK')")

        except:
            print("Already logged in or login screen not found immediately, checking main app")

        # Now wait for main app title
        page.wait_for_selector("text=Multibangun Offer System v2.1")

        # 1. Fill out some form data
        # Use simple css selectors based on placeholder or order

        # Client Name: "PT Contoh Sejahtera" placeholder
        page.fill("input[placeholder='PT Contoh Sejahtera']", "PT Test Sejahtera")

        # No Surat: It has value={formData.noSurat}, so it might not be empty initially.
        # It's the input following "Nomor Surat" label.
        no_surat_input = page.locator("label:has-text('Nomor Surat') + input")

        # Ensure we found it
        if no_surat_input.count() == 0:
             no_surat_input = page.locator("div").filter(has_text="Nomor Surat").locator("input")

        # Clear and fill
        no_surat_input.fill("001/MRP/PWRN/TEST/VERIFY")

        # 2. Click "SIMPAN"
        # Handle dialog
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("button:has-text('SIMPAN')")

        # Wait a bit
        page.wait_for_timeout(1000)

        # 3. Click "Data Tersimpan"
        page.click("button:has-text('Data Tersimpan')", force=True)

        # 4. Verify the modal opens and shows the saved item
        # Wait for the modal content specifically
        modal_content = page.locator(".fixed.inset-0").filter(has_text="Letter Number")

        # Verify the row exists INSIDE the modal table body
        # Row should contain our ID
        saved_row = modal_content.locator("tr", has_text="001/MRP/PWRN/TEST/VERIFY")

        try:
            saved_row.wait_for(state="visible", timeout=5000)
            print("Saved item found in modal table!")
        except:
            print("Saved item NOT found in modal table. Taking failure screenshot.")
            page.screenshot(path="verification/saved_quotations_failure.png")
            raise Exception("Verification Failed: Saved item not found in modal table.")

        # Take success screenshot
        page.screenshot(path="verification/saved_quotations_modal.png")
        print("Screenshot saved to verification/saved_quotations_modal.png")

        browser.close()

if __name__ == "__main__":
    verify_saved_quotations()
