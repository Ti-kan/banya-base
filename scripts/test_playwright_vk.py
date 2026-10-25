import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://vk.com/medvezhka_krsk24", timeout=15000)
            await page.wait_for_timeout(3000)
            # Find img elements
            imgs = await page.eval_on_selector_all("img", "els => els.map(e => e.src)")
            valid_imgs = [i for i in imgs if "userapi.com" in i and "camera" not in i]
            print(f"Playwright VK medvezhka found {len(valid_imgs)} userapi images:")
            for img in valid_imgs[:5]:
                print(f"  {img}")
        except Exception as e:
            print("Playwright error:", e)
        finally:
            await browser.close()

asyncio.run(main())
