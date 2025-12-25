from playwright.sync_api import sync_playwright

def verify_bold():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the app
        page.goto("http://localhost:8000/index.html")

        try:
            page.wait_for_selector("text=Login Multibangun", timeout=5000)
            page.click("text=Admin Penawaran")
            page.fill("input[placeholder='PIN']", "1234")
            page.click("button:has-text('MASUK')")
        except:
            print("Already logged in or login screen not found immediately")

        page.wait_for_selector("text=Multibangun Offer System v2.1")

        # Add a new material item (which uses the textarea)
        page.click("button:has-text('Tambah Biaya')")

        # Wait for the textarea to appear
        page.wait_for_timeout(1000)

        # Find the textarea with id starting with item-desc-
        # The list output showed Textarea 2 ID: item-desc-1
        # The newly added one should be index 1 (if starting from 0, with 1 existing default item in multiblock template)

        # Let's find the textarea that matches our ID pattern
        item_textarea = page.locator("textarea[id^='item-desc-']").last

        textarea_id = item_textarea.get_attribute("id")
        print(f"Target Textarea ID: {textarea_id}")

        if not textarea_id:
             raise Exception("Failed to find the newly added item textarea with ID.")

        # Fill with text
        item_textarea.fill("This is a test for bolding.")

        # Select "test"
        page.evaluate(f"""
            const el = document.getElementById('{textarea_id}');
            if (el) {{
                el.focus();
                el.setSelectionRange(10, 14);
            }}
        """)

        # Click the "B" button associated with this row.
        # It is inside the same cell.
        # We can locate the button that is previous sibling or inside the same relative container.
        # Or just use the last 'Bold Selection' button
        bold_btn = page.locator("button[title='Bold Selection']").last
        bold_btn.click()

        updated_value = item_textarea.input_value()
        print(f"Updated Value: {updated_value}")

        if "*test*" in updated_value:
            print("SUCCESS: Text was bolded correctly.")
        else:
             raise Exception(f"FAILURE: Text was not bolded. Value: {updated_value}")

        page.screenshot(path="verification/verify_bold_success.png")

        browser.close()

if __name__ == "__main__":
    verify_bold()
