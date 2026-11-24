import asyncio
from playwright.async_api import async_playwright
OUT="/home/z/my-project/download/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w,h in [(375,812),(390,844),(1440,900)]:
            pg=await b.new_page(viewport={"width":w,"height":h})
            await pg.goto("http://localhost:3000/",wait_until="load")
            await pg.evaluate("async()=>{window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,900));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,400));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            await pg.evaluate("()=>document.querySelectorAll('.reveal').forEach(el=>el.classList.add('in'))")
            clip=await pg.evaluate("""()=>{const el=document.getElementById('kits');const r=el.getBoundingClientRect();
              return {x:0,y:Math.max(0,window.scrollY+r.top-40),width:innerWidth,height:Math.min(r.height+60,2800)}}""")
            await pg.screenshot(path=OUT+f"final-{w}-offer.png",clip=clip,full_page=True)
            # guarantee section
            gclip=await pg.evaluate("""()=>{const el=document.querySelector('.guarantee');const r=el.getBoundingClientRect();
              return {x:0,y:Math.max(0,window.scrollY+r.top),width:innerWidth,height:Math.min(r.height,1200)}}""")
            await pg.screenshot(path=OUT+f"final-{w}-guarantee.png",clip=gclip,full_page=True)
            print("done",w,flush=True)
            await pg.close()
        await b.close()
asyncio.run(main())
