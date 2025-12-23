import asyncio
from playwright.async_api import async_playwright
import http.server
import socketserver
import threading
import os

PORT = 8000

def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

async def run():
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"http://localhost:{PORT}/index.html")

        # Login first
        await page.click('text=Ir. Nuruzzaman')
        await page.fill('input[type="password"]', '1234')
        await page.click('button:has-text("MASUK")')

        # Wait for preview to load
        await page.wait_for_selector('.preview-paper')

        # Take screenshot of the preview paper
        preview = page.locator('.preview-paper').first
        await preview.screenshot(path="verification/preview_before.png")

        print("Screenshot taken: verification/preview_before.png")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
