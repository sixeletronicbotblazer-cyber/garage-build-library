import sys
import asyncio, json
from playwright.async_api import async_playwright

URL="http://localhost:3000/"
WIDTHS=[320,375,390,430,768,1440]

async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        for w in WIDTHS:
            pg=await b.new_page(viewport={"width":w,"height":844})
            await pg.goto(URL,wait_until="load", timeout=30000)
            await pg.evaluate("async()=>{window.scrollTo(0,document.body.scrollHeight);await new Promise(r=>setTimeout(r,600));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,300));for(const i of document.images){if(i.complete&&i.currentSrc){try{await i.decode()}catch(e){}}}}")
            res=await pg.evaluate("""()=>{
              const d=document.documentElement,b=document.body;
              const sw=Math.max(d.scrollWidth,b.scrollWidth), cw=d.clientWidth;
              const bad=[];
              document.querySelectorAll('section, .wrap, img, .btn, .price, h1, h2, h3').forEach(el=>{
                const r=el.getBoundingClientRect();
                if(r.right>sw+1||r.left<-1) {} // marquee rows intentionally overflow their overflow-hidden parent
              });
              // elements wider than viewport (excluding marquee rows content)
              const wide=[];
              document.querySelectorAll('body *').forEach(el=>{
                if(el.closest('.gallery-row'))return;
                const r=el.getBoundingClientRect();
                if(r.width>d.clientWidth+1) wide.push(el.className||el.tagName);
              });
              const broken=[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'));
              // vertical scrollbars inside sections
              const innerScroll=[...document.querySelectorAll('section *, section')].filter(el=>{
                if(el.closest('.gallery'))return false;
                const s=getComputedStyle(el);
                return (s.overflowY==='auto'||s.overflowY==='scroll')&&el.scrollHeight>el.clientHeight+2;
              }).map(el=>el.className||el.tagName);
              return {pageHScroll: sw>cw+1, scrollW:sw, clientW:cw, wide:[...new Set(wide)].slice(0,5), brokenImg:broken, innerScroll};
            }""")
            # gallery carousel check
            gal=await pg.evaluate("""()=>{
              const rows=[...document.querySelectorAll('.gallery-row')];
              const plan=rows.find(r=>r.classList.contains('plan-row'));
              const imgs=plan? [...new Set([...plan.querySelectorAll("img")].map(i=>i.src))]:[];
              return {rows:rows.length, planImgs:imgs.length};
            }""")
            print(w, json.dumps(res), "gallery:", json.dumps(gal))
            await pg.close()
        await b.close()
asyncio.run(main())
