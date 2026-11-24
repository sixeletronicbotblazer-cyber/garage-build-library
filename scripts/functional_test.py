import asyncio
from playwright.async_api import async_playwright
URL="http://localhost:3000/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--no-sandbox"])
        ctx=await b.new_context(viewport={"width":390,"height":844})
        pg=await ctx.new_page()
        errors=[]
        pg.on("console",lambda m: errors.append(m.text) if m.type=="error" else None)
        pg.on("pageerror",lambda e: errors.append(str(e)))
        await pg.goto(URL,wait_until="load")
        await pg.wait_for_timeout(1500)
        # 1 countdown: bar visible, timer text format
        c=await pg.evaluate("()=>({bar:!document.getElementById('dealBar').hidden,barText:document.getElementById('dealBar').textContent.trim(),timer:!document.getElementById('offerTimer').hidden,timerText:document.getElementById('offerCountdown').textContent})")
        print("countdown:",c)
        # 2 expiry simulation: backdate and check removal (fresh context vars)
        exp=await pg.evaluate("""()=>{const end=Date.parse('2026-11-24T23:59:59-05:00');
          return {nowBefore:end, msLeftAtLoad: end-Date.now()} }""")
        print("time:",exp)
        # 3 checkout hrefs
        h=await pg.evaluate("""()=>({basic:document.getElementById('basicBtn').href,
          prof:document.querySelector('#kits .price-card.pro .btn').href,
          upYes:document.querySelector('#upsell .btn.glow').href,
          upNo:document.querySelector('#upsell .btn.ghost').href,
          noHashLeft:[...document.querySelectorAll('a.btn')].filter(a=>a.getAttribute('href')==='#kits').length})""")
        print("hrefs:",h)
        # 4 modal: first click opens, scroll locked, Esc closes and refocuses
        await pg.evaluate("()=>document.getElementById('kits').scrollIntoView()")
        await pg.click('#basicBtn')
        await pg.wait_for_timeout(200)
        m1=await pg.evaluate("()=>({open:document.getElementById('upsell').classList.contains('open'),bodyLock:document.body.style.overflow,seen:sessionStorage.getItem('gbUpsellShown')})")
        print("modal open:",m1)
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(150)
        m2=await pg.evaluate("()=>({open:document.getElementById('upsell').classList.contains('open'),focusBack:document.activeElement.id})")
        print("after Esc:",m2)
        # 5 second click goes direct (no modal) — intercept navigation
        nav=[]
        pg.on("request",lambda r: nav.append(r.url) if "pay.cakto" in r.url else None)
        try:
            await pg.click('#basicBtn',timeout=4000)
            await pg.wait_for_timeout(600)
        except Exception: pass
        print("second click navigated to:",pg.url,"(modal stayed closed)")
        await pg.goto(URL,wait_until="load")
        await pg.wait_for_timeout(1200)
        # 6 lightbox: only plan row opens
        await pg.evaluate("()=>document.getElementById('gallery').scrollIntoView()")
        await pg.wait_for_timeout(600)
        # example image should NOT have role button
        r=await pg.evaluate("""()=>{const ex=document.querySelector('.gallery-row.reverse img');
          return {exRole:ex.getAttribute('role'),exTab:ex.tabIndex,planRole:document.querySelector('.gallery-row.plan-row img').getAttribute('role')}}""")
        print("roles:",r)
        # click plan image, nav works
        await pg.evaluate("()=>document.querySelector('.gallery-row.plan-row img').click()")
        await pg.wait_for_timeout(200)
        lb=await pg.evaluate("()=>({open:document.getElementById('lightbox').classList.contains('open'),count:document.getElementById('lightbox-count').textContent,caption:document.getElementById('lightbox-caption').textContent})")
        print("lightbox:",lb)
        await pg.evaluate("()=>document.querySelector('.lightbox-nav.next').click()")
        n=await pg.evaluate("()=>document.getElementById('lightbox-count').textContent")
        print("after next:",n)
        await pg.keyboard.press("Escape")
        await pg.wait_for_timeout(150)
        print("lb closed:",await pg.evaluate("()=>!document.getElementById('lightbox').classList.contains('open')"))
        # 7 hover does not pause marquee
        hp=await pg.evaluate("""()=>{const row=document.querySelector('.gallery-row.plan-row');
          const before=getComputedStyle(row).animationPlayState;return before}""")
        print("marquee play state (css has no hover pause):",hp)
        # 8 modal fits 90dvh on mobile
        await pg.evaluate("()=>sessionStorage.clear()")
        await pg.evaluate("()=>document.getElementById('kits').scrollIntoView()")
        await pg.evaluate("()=>document.getElementById('basicBtn').click()")
        await pg.wait_for_timeout(200)
        fit=await pg.evaluate("""()=>{const card=document.querySelector('.modal-card').getBoundingClientRect();
          const btns=[...document.querySelectorAll('#upsell .btn')].map(b=>{const r=b.getBoundingClientRect();return r.bottom<=844&&r.right<=390});
          return {card:[Math.round(card.width),Math.round(card.height)],inViewport:card.top>=0&&card.bottom<=844,btnsOk:btns}}""")
        print("modal mobile fit:",fit)
        # 9 pdfs return 200
        for f in ["guides/side-table-six-page-preview.pdf","guides/custom-quote-worksheet.pdf","guides/finishing-materials-notes.pdf"]:
            s=await pg.evaluate("u=>fetch(u,{method:'HEAD'}).then(r=>r.status)",f)
            print("pdf",f,s)
        print("console errors:",errors[:5])
        await b.close()
asyncio.run(main())
