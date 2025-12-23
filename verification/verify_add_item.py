import asyncio
from playwright.async_api import async_playwright

PORT = 8000

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"http://localhost:{PORT}/index.html")

        # Login
        await page.click('text=Ir. Nuruzzaman')
        await page.fill('input[type="password"]', '1234')
        await page.click('button:has-text("MASUK")')

        # Go to Material Tab
        await page.click('button:has-text("Penawaran Material")')

        # Click Add Item (Currently adds a structured item)
        await page.click('button:has-text("Tambah Biaya")')

        # Take screenshot of the table area
        table_area = page.locator('.border.rounded.overflow-hidden')
        await table_area.screenshot(path="verification/before_change.png")

        print("Screenshot taken: verification/before_change.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
