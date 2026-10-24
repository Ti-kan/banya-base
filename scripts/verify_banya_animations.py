#!/usr/bin/env python3
import asyncio
import os
import sys
from playwright.async_api import async_playwright

ARTIFACT_DIR = "/Users/takanov/.gemini/antigravity-cli/brain/0cba8e2f-79d3-4c29-a34a-d0fa28861163"
BASE_URL = "http://localhost:3008/b/taiga-82/"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # Desktop context
        ctx = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2
        )
        await ctx.add_init_script("delete Object.getPrototypeOf(navigator).webdriver; delete navigator.webdriver; navigator.webdriver = undefined;")
        
        page = await ctx.new_page()
        print("Navigating to", BASE_URL)
        await page.goto(BASE_URL, wait_until="networkidle")
        await asyncio.sleep(0.6)

        # 1. Verify Hero animation
        hero_word_opacity = await page.evaluate("""() => {
            const spans = document.querySelectorAll('.hero-word span');
            return Array.from(spans).map(s => getComputedStyle(s).opacity);
        }""")
        print("Hero word spans opacity:", hero_word_opacity)

        # 2. Verify Section 01 & 02 unviewed vs viewed
        sec01 = page.locator("#slots-s .sh")
        await sec01.scroll_into_view_if_needed()
        await asyncio.sleep(0.8)

        sec01_state = await page.evaluate("""() => {
            const sh = document.querySelector('#slots-s .sh');
            const num = sh.querySelector('.num');
            const eyebrow = sh.querySelector('.eyebrow');
            const h2 = sh.querySelector('h2');
            const firstWord = h2.querySelector('.word-inner');
            const lead = sh.querySelector('.lead');
            return {
                sh_in: sh.classList.contains('in'),
                num_opacity: getComputedStyle(num).opacity,
                eyebrow_opacity: getComputedStyle(eyebrow).opacity,
                firstWord_opacity: firstWord ? getComputedStyle(firstWord).opacity : null,
                lead_opacity: lead ? getComputedStyle(lead).opacity : null
            };
        }""")
        print("Section 01 active state:", sec01_state)
        assert sec01_state['sh_in'] == True, "Section 01 sh should have class .in"
        assert float(sec01_state['num_opacity']) >= 0.9, "Section 01 num should be visible"

        # Screenshot 1: Sections 01 & 02
        shot1 = os.path.join(ARTIFACT_DIR, "banya_anim_sec01_02.png")
        await page.screenshot(path=shot1)
        print("Saved Screenshot 1:", shot1)

        # 3. Section 03 (#baths)
        sec03 = page.locator("#baths")
        await sec03.scroll_into_view_if_needed()
        await asyncio.sleep(0.8)

        sec03_state = await page.evaluate("""() => {
            const sec = document.querySelector('#baths');
            const sh = sec.querySelector('.sh');
            const h2 = sec.querySelector('h2');
            const firstWord = h2.querySelector('.word-inner');
            const h2Color = getComputedStyle(h2).color;
            const cards = sec.querySelectorAll('.baths > .bath');
            const btns = Array.from(cards).map(c => c.querySelector('button[data-book]').textContent.trim());
            return {
                sh_in: sh.classList.contains('in'),
                h2_color: h2Color,
                cards_count: cards.length,
                buttons: btns
            };
        }""")
        print("Section 03 state:", sec03_state)
        assert "255, 255, 255" in sec03_state['h2_color'] or sec03_state['h2_color'] == "rgb(255, 255, 255)", f"Heading should be white, got {sec03_state['h2_color']}"
        assert len(sec03_state['buttons']) == 3, "All 3 bath cards should have booking buttons"

        # Screenshot 2: Section 03
        shot2 = os.path.join(ARTIFACT_DIR, "banya_anim_sec03_night.png")
        await page.screenshot(path=shot2)
        print("Saved Screenshot 2:", shot2)

        # 4. Sections 04 & 05
        sec04 = page.locator("#price")
        await sec04.scroll_into_view_if_needed()
        await asyncio.sleep(0.8)

        shot3 = os.path.join(ARTIFACT_DIR, "banya_anim_sec04_05.png")
        await page.screenshot(path=shot3)
        print("Saved Screenshot 3:", shot3)

        # 5. Section 08 & footer
        sec08 = page.locator("#book")
        await sec08.scroll_into_view_if_needed()
        await asyncio.sleep(0.8)

        sec08_state = await page.evaluate("""() => {
            const sec = document.querySelector('#book');
            const h2 = sec.querySelector('h2');
            const h2Color = getComputedStyle(h2).color;
            const pb = getComputedStyle(sec).paddingBottom;
            return { h2_color: h2Color, padding_bottom: pb };
        }""")
        print("Section 08 state:", sec08_state)

        shot4 = os.path.join(ARTIFACT_DIR, "banya_anim_sec08_footer.png")
        await page.screenshot(path=shot4)
        print("Saved Screenshot 4:", shot4)

        # 6. Bi-directional re-trigger verification: scroll to top
        await page.evaluate("window.scrollTo(0, 0)")
        await asyncio.sleep(0.6)
        sec08_reset = await page.evaluate("""() => {
            const sh = document.querySelector('#book .sh');
            return sh.classList.contains('in');
        }""")
        print("Section 08 reset when scrolled away (bi-directional):", not sec08_reset)
        assert not sec08_reset, "Section 08 should remove .in when scrolled away"

        # 7. Mobile Viewport (390 x 844)
        m_ctx = await browser.new_context(
            viewport={"width": 390, "height": 844},
            device_scale_factor=3,
            is_mobile=True
        )
        await m_ctx.add_init_script("delete Object.getPrototypeOf(navigator).webdriver; delete navigator.webdriver; navigator.webdriver = undefined;")
        m_page = await m_ctx.new_page()
        await m_page.goto(BASE_URL, wait_until="networkidle")
        await asyncio.sleep(0.8)

        # Scroll to section 01
        await m_page.evaluate("window.scrollTo(0, 480)")
        await asyncio.sleep(0.8)

        shot5 = os.path.join(ARTIFACT_DIR, "banya_anim_mobile_390.png")
        await m_page.screenshot(path=shot5)
        print("Saved Screenshot 5:", shot5)

        await browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(main())
