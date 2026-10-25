import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        try:
            url = "https://yandex.ru/maps/org/medvezhka/48231703474/gallery/"
            print("Navigating to", url)
            await page.goto(url, timeout=15000, wait_until="domcontentloaded")
            await page.wait_for_timeout(3000)
            imgs = await page.eval_on_selector_all("img", "els => els.map(e => e.src)")
            avatars = [i for i in imgs if "avatars.mds.yandex.net/get-altay" in i]
            print(f"Found {len(avatars)} Yandex altay photos for medvezhka:")
            for a in avatars[:5]:
                print(" ", a)
        except Exception as e:
            print("Error:", e)
        finally:
            await browser.close()

asyncio.run(main())
