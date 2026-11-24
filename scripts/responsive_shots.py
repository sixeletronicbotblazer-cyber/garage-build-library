import asyncio
from playwright.async_api import async_playwright
OUT="/home/z/my-project/download/"
async def shot(pg,name,clip=None,full=False):
    await pg.screenshot(path=OUT+name,clip=clip,full_page=True)
    print("saved",name,flush=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w,h in [(360,780),(390,844),(1280,800)]:
            pg=await b.new_page(viewport={"width":w,"height":h})
            await pg.goto("http://localhost:3000/",wait_until="load",timeout=30000)
            await pg.evaluate("async()=>{window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,700));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,300));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            # hero: section top through just past mockup
            hr=await pg.evaluate("()=>{const el=document.querySelector('.hero');const r=el.getBoundingClientRect();const t=window.scrollY+r.top;return {x:0,y:t,width:innerWidth,height:Math.min(r.height,1400)}}")
            await shot(pg,f"resp-{w}-hero.png",clip=hr)
            # gallery
            gr=await pg.evaluate("()=>{const el=document.getElementById('gallery');const r=el.getBoundingClientRect();return {x:0,y:window.scrollY+r.top,width:innerWidth,height:Math.min(r.height,1100)}}")
            await shot(pg,f"resp-{w}-gallery.png",clip=gr)
            # pricing
            pr=await pg.evaluate("()=>{const el=document.getElementById('kits');const r=el.getBoundingClientRect();return {x:0,y:window.scrollY+r.top,width:innerWidth,height:Math.min(r.height,1500)}}")
            await shot(pg,f"resp-{w}-pricing.png",clip=pr)
            if w==360:
                # hero img size check
                chk=await pg.evaluate("()=>{const i=document.querySelector('.hero-image');const r=i.getBoundingClientRect();const pr=document.querySelector('.price-card img').getBoundingClientRect();return {heroImg:[r.width,r.height],heroRight:r.right,priceImg:[pr.width,pr.height]}}")
                print(w,chk,flush=True)
            await pg.close()
        await b.close()
asyncio.run(main())
