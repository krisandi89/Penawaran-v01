from playwright.sync_api import sync_playwright

def verify_align_middle():
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

        # Check if the table cells have align-middle class
        # We need to look at the LIVE PREVIEW table (right side), not the input form (left side).
        # The live preview is inside .preview-paper .paper-content table

        # Locate the table in the preview area
        preview_table = page.locator(".preview-paper table").first

        # Get the first row in tbody
        first_row_cells = preview_table.locator("tbody tr").first.locator("td")

        # Columns 1, 2, 3 (0-indexed: 1, 2, 3) should have align-middle
        # Column 0 is Material
        # Column 1 is Quantity (align-middle)
        # Column 2 is Price (align-middle)
        # Column 3 is Total (align-middle)

        count = first_row_cells.count()
        print(f"Found {count} cells in first row.")

        for i in range(1, 4):
            cell = first_row_cells.nth(i)
            class_attr = cell.get_attribute("class")
            print(f"Cell {i} classes: {class_attr}")
            if "align-middle" not in class_attr:
                raise Exception(f"Cell {i} does NOT have align-middle class!")

        print("SUCCESS: HTML cells have align-middle.")

        page.screenshot(path="verification/verify_align_middle.png")
        browser.close()

if __name__ == "__main__":
    verify_align_middle()
