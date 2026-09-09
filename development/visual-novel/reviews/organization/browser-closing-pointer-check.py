"""Reproduce closing-theme focus directly through the chapter menu, then test it."""
import argparse, ast, asyncio, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SOURCE=ROOT/'visual-novel/scripts/browser_smoke.py'
URL='http://127.0.0.1:8000/?preview=0.1-alpha'

class FocusProbeStop(Exception): pass

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

async def run(diagnose):
    source=SOURCE.read_text()
    tree=ast.parse(source)
    owner=next(n for n in tree.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='check')
    names=('value','execute','until','click_button','check_closing_theme')
    functions={n.name:ast.get_source_segment(source,n) for n in ast.walk(owner) if isinstance(n,ast.AsyncFunctionDef) and n.name in names}
    errors, focus_checks, pointer_moves, screens, observations=[],[],[],[],[]
    mode='diagnosis' if diagnose else 'verified'
    phase='setup'
    async with async_playwright() as p:
        browser=await p.chromium.launch(args=['--enable-unsafe-swiftshader','--use-angle=swiftshader'])
        page=await browser.new_page(viewport={'width':1280,'height':720})
        await page.add_init_script("window.__pointerEvents=[];document.addEventListener('mousemove',e=>window.__pointerEvents.push({x:e.clientX,y:e.clientY,t:performance.now()}),true)")
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('console',lambda m:errors.append(m.text) if 'Full traceback:' in m.text or 'While running game code:' in m.text else None)
        await page.goto(URL)
        await page.wait_for_function('typeof window.renpy_get === "function"',timeout=90000)
        namespace={'page':page,'errors':errors,'asyncio':asyncio,'OUT':OUT}
        for name in names:
            extracted=functions[name]
            if diagnose and name=='check_closing_theme':
                extracted=extracted.replace('await page.keyboard.press("Space")\n            assert await value(\'renpy.music.get_pause(channel="closing_theme")\')', 'await page.keyboard.press("Space")\n            await until(\'renpy.music.get_pause(channel="closing_theme")\')\n            assert await value(\'renpy.music.get_pause(channel="closing_theme")\')')
            exec(compile(extracted,str(SOURCE)+':'+name,'exec'),namespace)
        value,execute,until=(namespace[name] for name in ('value','execute','until'))
        original_move=page.mouse.move
        async def tracked_move(x,y,**kwargs):
            pointer_moves.append({'x':x,'y':y,'phase':phase})
            await original_move(x,y,**kwargs)
        page.mouse.move=tracked_move
        false_checks=0
        async def tracked_execute(code):
            nonlocal false_checks
            result=await execute(code)
            if code.startswith('_browser_click_screen'):
                focus_checks.append({'phase':phase,**result})
                if result['ready']: false_checks=0
                else:
                    false_checks+=1
                    if diagnose and false_checks>=3: raise FocusProbeStop('Three consecutive unfocused observations; stop before the production 30s timeout.')
            return result
        namespace['execute']=tracked_execute
        click=namespace['click_button']
        async def snapshot(at):
            data=await execute('''_probe_screen=renpy.get_screen("chapter_end")
_probe_widgets=set()
if _probe_screen is not None: _probe_screen.visit_all(lambda item,out=_probe_widgets:out.add(id(item)))
_probe_focused=renpy.display.focus.get_focused()
_probe_texts=[]
if _probe_focused is not None: _probe_focused.visit_all(lambda item,out=_probe_texts:out.append(item.get_all_text()) if isinstance(item,renpy.text.text.Text) else None)
_probe_targets=[]
for focus in renpy.display.focus.focus_list:
    if not isinstance(focus.widget,renpy.display.behavior.Button) or focus.x is None: continue
    texts=[]
    focus.widget.visit_all(lambda item,out=texts:out.append(item.get_all_text()) if isinstance(item,renpy.text.text.Text) else None)
    if "Replay closing theme" in texts: _probe_targets.append(dict(rect=[focus.x,focus.y,focus.w,focus.h],widget_id=id(focus.widget),in_screen=id(focus.widget) in _probe_widgets))
result=dict(focused_type=str(type(_probe_focused)),focused_texts=_probe_texts,focused_id=id(_probe_focused),in_screen=id(_probe_focused) in _probe_widgets,targets=_probe_targets,mouse_pos=list(renpy.get_mouse_pos()),focus_type=renpy.display.focus.focus_type,pending_focus_type=renpy.display.focus.pending_focus_type,transition=bool(renpy.display.interface.get_ongoing_transition()),trans_pause=bool(renpy.display.interface.trans_pause),last_event=str(renpy.display.interface.last_event),mouse_event_time=renpy.display.interface.mouse_event_time,input_event_time=renpy.display.interface.input_event_time)''')
            data['at']=at
            data['browser_mouse_events']=await page.evaluate('window.__pointerEvents.slice(-8)')
            observations.append(data)
            return data
        async def screenshot(name):
            path=OUT/name
            await page.screenshot(path=str(path))
            screens.append({'file':name,'sha256':sha(path)})
        await until('bool(renpy.get_screen("main_menu"))')
        await execute('persistent.chapter_spoiler_warnings=False\npersistent.reduced_motion=True\npreferences.text_cps=0')
        await click('main_menu','Chapters')
        await until('bool(renpy.get_screen("dev_chapters"))')
        title=await value('dict(BOOK_SCENES)["annual_remembrance"]')
        await click('dev_chapters','32 · '+title)
        await until('scene_key=="annual_remembrance" and bool(renpy.get_screen("say")) and not renpy.context()._menu')
        for _ in range(8):
            if await value('bool(renpy.get_screen("book_afterword"))'): break
            old=await value('_history_list[-1].what')
            await page.keyboard.press('Space')
            await until(f'bool(renpy.get_screen("book_afterword")) or _history_list[-1].what!={old!r}')
        await until('bool(renpy.get_screen("book_afterword"))')
        phase='closing_sequence'
        try:
            await namespace['check_closing_theme']()
            status='passed'
        except FocusProbeStop as error:
            assert diagnose
            status='reproduced_unfocused_replay'
            await screenshot('browser-closing-focus-failure.png')
            before=await snapshot('unfocused_after_same_position_move')
            assert before['targets'] and not before['focused_texts'] and not before['transition'] and not before['trans_pause']
            x,y,w,h=before['targets'][0]['rect']
            px,py=(x+w/2)*2/3,(y+h/2)*2/3
            await page.mouse.move(px+2,py)
            await snapshot('after_two_pixel_nudge')
            await page.mouse.move(px,py)
            after=await snapshot('after_return_to_center')
            assert after['focused_texts']==['Replay closing theme'] and after['in_screen']
            await screenshot('browser-closing-focus-restored.png')
        if not diagnose:
            assert status=='passed'
            phase='credits_navigation'
            await click('chapter_end','Credits')
            await until('bool(renpy.get_screen("about"))')
            await screenshot('browser-closing-credits.png')
            await click('about','Return')
            await until('bool(renpy.get_screen("chapter_end")) and not renpy.context()._menu')
            await click('chapter_end','Return to title')
            await until('main_menu and bool(renpy.get_screen("main_menu"))')
            await screenshot('browser-closing-title.png')
        assert not errors,errors
        version=browser.version
        await browser.close()
    result={'status':status,'mode':mode,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'url':URL,'viewport':[1280,720],'browser':version,'scope':'Direct annual-remembrance chapter entry, actual final dialogue, complete extracted closing-theme sequence; no full-story replay.','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'helper_sha256':hashlib.sha256(functions['click_button'].encode()).hexdigest(),'closing_function_sha256':hashlib.sha256(functions['check_closing_theme'].encode()).hexdigest(),'runner_sha256':sha(Path(__file__)),'focus_checks':focus_checks,'pointer_moves':pointer_moves,'observations':observations,'screenshots':screens,'errors':errors,'credits_return_title':not diagnose}
    (OUT/f'browser-closing-pointer-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':status,'focus_checks':len(focus_checks),'pointer_moves':len(pointer_moves),'errors':errors},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--diagnose',action='store_true')
    asyncio.run(run(parser.parse_args().diagnose))
