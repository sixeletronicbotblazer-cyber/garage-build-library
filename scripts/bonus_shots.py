import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w in (390,1440):
            pg=await b.new_page(viewport={"width":w,"height":900})
            await pg.goto("http://localhost:3000/",wait_until="load",timeout=30000)
            await pg.evaluate("async()=>{document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'));const k=document.getElementById('bonuses');k.scrollIntoView();await new Promise(r=>setTimeout(r,800));window.scrollBy(0,600);await new Promise(r=>setTimeout(r,500));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            await pg.locator(".bonus-box").screenshot(path=f"/home/z/my-project/download/bonus-section-{w}.png")
            print("bonus saved",w)
            await pg.evaluate("async()=>{const k=document.getElementById('kits');k.scrollIntoView();await new Promise(r=>setTimeout(r,700));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            await pg.locator(".price-grid").screenshot(path=f"/home/z/my-project/download/cards-4b-{w}.png")
            print("cards saved",w)
            await pg.close()
        await b.close()
asyncio.run(main())
