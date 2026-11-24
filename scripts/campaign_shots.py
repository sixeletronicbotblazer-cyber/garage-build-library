import asyncio
from playwright.async_api import async_playwright
OUT="/home/z/my-project/download/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w,h in [(390,844),(1440,900)]:
            pg=await b.new_page(viewport={"width":w,"height":h})
            await pg.goto("http://localhost:3000/",wait_until="load")
            await pg.evaluate("async()=>{window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,800));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,400));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            await pg.wait_for_timeout(500)
            # first fold: top of page
            await pg.screenshot(path=OUT+f"campaign-{w}-firstfold.png")
            # offer section: timer + cards
            await pg.evaluate("()=>document.getElementById('kits').scrollIntoView({block:'start'})")
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=OUT+f"campaign-{w}-offer.png")
            # modal (mobile only, fresh session)
            if w==390:
                await pg.evaluate("()=>{sessionStorage.clear();document.getElementById('basicBtn').click()}")
                await pg.wait_for_timeout(400)
                await pg.screenshot(path=OUT+"campaign-390-modal.png")
            print("done",w,flush=True)
            await pg.close()
        await b.close()
asyncio.run(main())
