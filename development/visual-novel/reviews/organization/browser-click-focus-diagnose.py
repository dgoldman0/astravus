import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
OUT=Path('/home/kir/Documents/Projects/astravus-visual-novel/Astravus/development/visual-novel/reviews/organization')
async def run():
    async with async_playwright() as p:
        browser=await p.chromium.launch(args=['--enable-unsafe-swiftshader','--use-angle=swiftshader'])
        page=await browser.new_page(viewport={'width':1280,'height':720})
        await page.goto('http://127.0.0.1:8000/?preview=0.1-alpha')
        await page.wait_for_function('typeof window.renpy_get === "function"',timeout=90000)
        async def value(expr):
            return await page.evaluate('e=>window.renpy_get(e)',f'eval({ascii(expr)})')
        async def execute(code):
            return await page.evaluate('c=>window.renpy_exec(c)',f'exec({ascii(code)})')
        async def until(expr):
            async with asyncio.timeout(30):
                while not await value(expr): await asyncio.sleep(.1)
        async def snapshot():
            return await execute('''screen = renpy.get_screen("quick_menu")
widgets = set()
screen.visit_all(lambda item, out=widgets: out.add(id(item)))
focused = renpy.display.focus.get_focused()
focused_texts = []
if focused is not None:
    focused.visit_all(lambda item, out=focused_texts: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
buttons = []
for focus in renpy.display.focus.focus_list:
    if not isinstance(focus.widget, renpy.display.behavior.Button) or focus.x is None: continue
    texts = []
    focus.widget.visit_all(lambda item, out=texts: out.append(item.get_all_text()) if isinstance(item, renpy.text.text.Text) else None)
    if "Glossary" in texts:
        buttons.append(dict(id=id(focus.widget), rect=[focus.x,focus.y,focus.w,focus.h], texts=texts, in_screen=id(focus.widget) in widgets, is_focused=focus.widget is focused))
result=dict(focused_id=id(focused), focused_type=str(type(focused)), focused_texts=focused_texts, focused_in_screen=id(focused) in widgets, buttons=buttons, transition=bool(renpy.display.interface.get_ongoing_transition()), trans_pause=bool(renpy.display.interface.trans_pause), scene=scene_key)''')
        await until('bool(renpy.get_screen("main_menu"))')
        await page.mouse.click(220,373)
        await until('bool(renpy.get_screen("chapter_card"))')
        await page.keyboard.press('Enter')
        await until('bool(renpy.get_screen("say"))')
        await until('not renpy.display.interface.trans_pause and not renpy.display.interface.get_ongoing_transition()')
        frames=[{'at':'before_move',**await snapshot()}]
        rect=frames[0]['buttons'][0]['rect']
        x,y,w,h=rect
        await page.mouse.move((x+w/2)*2/3,(y+h/2)*2/3)
        for i in range(5):
            frames.append({'at':f'after_move_{i}',**await snapshot()})
        await page.screenshot(path=str(OUT/'browser-click-focus-diagnosis.png'))
        (OUT/'browser-click-focus-diagnosis.json').write_text(json.dumps(frames,indent=2)+'\n')
        print(json.dumps(frames,indent=2))
        await browser.close()
asyncio.run(run())
