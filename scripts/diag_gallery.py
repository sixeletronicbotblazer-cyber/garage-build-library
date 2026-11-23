#!/usr/bin/env python3
"""Diagnose gallery rendering: element screenshots + live DOM checks."""
import asyncio, os
from playwright.async_api import async_playwright

ROOT = "/home/z/my-project/download/garage-build-library"
URL = "file://" + os.path.join(ROOT, "index.html")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 1440, "height": 900})
        await page.goto(URL, wait_until="networkidle")
        await page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
        await page.wait_for_function(
            "Array.from(document.images).every(i=>i.complete && (i.naturalWidth>0 || !i.getAttribute('src')))",
            timeout=30000)
        # pause marquee for stable capture
        await page.add_style_tag(content=".gallery-row{animation:none!important}")
        await page.wait_for_timeout(400)
        info = await page.evaluate("""(()=>{
          const rows=[...document.querySelectorAll('.gallery-row')];
          return rows.map(r=>{
            const rect=r.getBoundingClientRect();
            const imgs=[...r.querySelectorAll('img')].slice(0,3).map(i=>({src:i.getAttribute('src'),nw:i.naturalWidth,nh:i.naturalHeight,cs:getComputedStyle(i).backgroundImage}));
            return {top:Math.round(rect.top+window.scrollY),h:Math.round(rect.height),imgs};
          });
        })()""")
        for i, r in enumerate(info):
            print(f"row {i}: top={r['top']} h={r['h']} first-img={r['imgs']}")
        rows = page.locator(".gallery-row")
        for i in range(await rows.count()):
            await rows.nth(i).screenshot(path=f"/tmp/render/row-{i}.png")
        # also viewport screenshot of the gallery area
        top = info[0]["top"]
        await page.evaluate(f"window.scrollTo(0,{max(0,top-220)})")
        await page.wait_for_timeout(300)
        await page.screenshot(path="/tmp/render/gallery-viewport.png")
        await b.close()

asyncio.run(main())
