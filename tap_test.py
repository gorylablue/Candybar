import asyncio
from playwright.async_api import async_playwright
SEL=['#otro','.shot[data-k="cosmo"]','#vela','#mas','#d-sab + span','#enviar','#mbar .btn','.nav .ig']
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for name,w,h,touch in [('iPhone',390,844,True),('iPad',820,1180,True),('laptop',1366,768,False),('grande',1920,1080,False)]:
      ctx=await b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch)
      pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
      await pg.goto('file://'+__import__("os").path.abspath("index.html")+'');await pg.wait_for_timeout(5500)
      await pg.evaluate('scrollTo(0,innerHeight)');await pg.wait_for_timeout(600)
      res=[]
      for s in SEL:
        el=await pg.query_selector(s)
        if not el or not await el.is_visible(): res.append(f'{s}:oculto');continue
        await el.scroll_into_view_if_needed();await pg.wait_for_timeout(500)
        bb=await el.bounding_box();x=bb['x']+bb['width']/2;y=bb['y']+bb['height']/2
        hit=await pg.evaluate('([x,y,s])=>{const e=document.elementFromPoint(x,y);const t=document.querySelector(s);return !!e&&(t.contains(e)||e.contains(t)||(e.closest("label")&&e.closest("label").contains(t)))}',[x,y,s])
        res.append(f'{s}:{"ok" if hit else "TAPADO"}')
      # functional: message updates on stepper
      await pg.click('#mas'); m=await pg.text_content('#msg')
      ov=await pg.evaluate('document.documentElement.scrollWidth-innerWidth')
      print(name,'overflow',ov,'| msg 5 pers' if '5 personas' in m else '| MSG?', '|',' '.join(res),'|errs',errs)
      await ctx.close()
    await b.close()
asyncio.run(main())
