import asyncio
from playwright.async_api import async_playwright
OUT="/home/z/my-project/download/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w,h in [(390,844),(1440,900)]:
            pg=await b.new_page(viewport={"width":w,"height":h})
            await pg.goto("http://localhost:3000/",wait_until="load")
            await pg.wait_for_timeout(800)
            r=await pg.evaluate("""()=>{const h1=document.querySelector('.hero h1');
              const r=h1.getBoundingClientRect();
              return {h1Top:Math.round(r.top),h1Bottom:Math.round(r.bottom),vh:innerHeight,
                imgTop:Math.round(document.querySelector('.hero-image').getBoundingClientRect().top),
                btnBottom:Math.round(document.querySelector('.hero .btn').getBoundingClientRect().bottom)}}""")
            print(w,"fold:",r)
            clip=await pg.evaluate("""()=>{const el=document.getElementById('kits');
              const r=el.getBoundingClientRect();
              return {x:0,y:Math.max(0,window.scrollY+r.top-40),width:innerWidth,height:Math.min(r.height+60,2400)}}""")
            await pg.evaluate("()=>document.getElementById('kits').scrollIntoView({block:'start'})")
            await pg.wait_for_timeout(900)
            await pg.screenshot(path=OUT+f"campaign-{w}-offer.png",clip=clip,full_page=True)
            print("offer shot",w,flush=True)
            await pg.close()
        await b.close()
asyncio.run(main())
