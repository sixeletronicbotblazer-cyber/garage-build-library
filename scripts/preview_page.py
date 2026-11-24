#!/usr/bin/env python3
"""Render the Garage Build Library page, force-paint all images (decode + scroll),
then capture desktop + mobile full-page screenshots and run interaction checks."""
import asyncio, os
from playwright.async_api import async_playwright

ROOT = "/home/z/my-project/download/garage-build-library"
OUT = "/home/z/my-project/download"
URL = "file://" + os.path.join(ROOT, "index.html")

PAINT_JS = """(async () => {
  document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
  await Promise.all(Array.from(document.images).filter(i => i.src)
    .map(i => i.decode().catch(() => {})));
  // scroll through the page so every region gets painted at least once
  const H = document.documentElement.scrollHeight;
  for (let y = 0; y <= H; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
  await new Promise(r => setTimeout(r, 300));
  window.scrollTo(0, 0);
})()"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        failed = []
        # ---- Desktop ----
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("requestfailed", lambda r: failed.append(r.url))
        await page.goto(URL, wait_until="networkidle")
        await page.evaluate(PAINT_JS)
        await page.wait_for_timeout(800)
        not_loaded = await page.evaluate(
            "[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'))")
        await page.screenshot(path=os.path.join(OUT, "preview-garage-build-desktop.png"), full_page=True)
        # ---- lightbox test ----
        await page.click(".gallery-row img", force=True)
        opened = await page.evaluate("document.getElementById('lightbox').classList.contains('open')")
        await page.screenshot(path="/tmp/render/lightbox-open.png")
        await page.keyboard.press("Escape")
        closed = await page.evaluate("!document.getElementById('lightbox').classList.contains('open')")
        # checkout preview notice test
        await page.click("a.checkout")
        notice = await page.evaluate("document.getElementById('notice').textContent")
        notice_shown = await page.evaluate("document.getElementById('notice').classList.contains('show')")
        await page.close()

        # ---- Mobile ----
        m = await browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        m.on("requestfailed", lambda r: failed.append(r.url))
        await m.goto(URL, wait_until="networkidle")
        await m.evaluate(PAINT_JS)
        await m.wait_for_timeout(800)
        overflow = await m.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
        await m.screenshot(path=os.path.join(OUT, "preview-garage-build-mobile.png"), full_page=True)
        await m.close()
        await browser.close()

        print("images not loaded:", not_loaded or "NONE")
        print("console errors:", errors or "NONE")
        print("requests failed:", failed or "NONE")
        print("lightbox open on click:", opened, "| closed on Esc:", closed)
        print("checkout notice shown:", notice_shown, "|", repr(notice))
        print("mobile horizontal overflow px:", overflow)

asyncio.run(main())
