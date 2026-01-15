from playwright.sync_api import sync_playwright

def verify_rich_text():
    print("Starting verification...")
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
        # Note: The first item is a textarea now
        textarea = page.locator("table tbody tr textarea").first
        textarea.fill("Custom Label: Value\nThis is *bold* text.")

        # Check HTML Preview
        print("Checking HTML Preview...")

        # 1. Check "Custom Label:" is bold (Automatic detection)
        label_bold = page.locator(".preview-paper span.font-bold:has-text('Custom Label:')")
        if label_bold.count() > 0:
            print("SUCCESS: Automatic 'Custom Label:' bolding works.")
        else:
            print("FAILURE: Automatic bolding failed.")
            print(page.locator(".preview-paper table tbody tr td").first.inner_html())

        # 2. Check "*bold*" is rendered as "bold" (Markdown detection)
        markdown_bold = page.locator(".preview-paper span.font-bold:has-text('bold')")
        if markdown_bold.count() > 0:
            print("SUCCESS: Markdown '*bold*' rendering works.")
        else:
            print("FAILURE: Markdown bolding failed.")

        browser.close()

if __name__ == "__main__":
    verify_rich_text()
