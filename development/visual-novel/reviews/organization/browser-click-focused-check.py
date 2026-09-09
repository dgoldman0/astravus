"""Bounded real-mouse check of browser_smoke.py's actual nested click helper."""
import ast
import asyncio
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from playwright.async_api import async_playwright

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SOURCE = ROOT / 'visual-novel/scripts/browser_smoke.py'
URL = 'http://127.0.0.1:8000/?preview=0.1-alpha'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


async def run():
    source = SOURCE.read_text()
    source_sha = sha(SOURCE)
    tree = ast.parse(source)
    check = next(n for n in tree.body if isinstance(n, ast.AsyncFunctionDef) and n.name == 'check')
    functions = {n.name: ast.get_source_segment(source, n) for n in ast.walk(check)
                 if isinstance(n, ast.AsyncFunctionDef) and n.name in ('value', 'execute', 'until', 'click_button')}
    focus_checks, clicks, cycles, errors = [], [], [], []
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--enable-unsafe-swiftshader', '--use-angle=swiftshader'])
        page = await browser.new_page(viewport={'width': 1280, 'height': 720})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text)
                if 'Full traceback:' in message.text or 'While running game code:' in message.text else None)
        await page.goto(URL)
        await page.wait_for_function('typeof window.renpy_get === "function"', timeout=90000)
        namespace = {'page': page, 'errors': errors, 'asyncio': asyncio}
        for name in ('value', 'execute', 'until', 'click_button'):
            exec(compile(functions[name], str(SOURCE) + ':' + name, 'exec'), namespace)
        value, execute, until = (namespace[k] for k in ('value', 'execute', 'until'))

        async def tracked_execute(code):
            result = await execute(code)
            if code.startswith('_browser_click_screen'):
                focus_checks.append({'click': len(clicks), **result})
            return result

        namespace['execute'] = tracked_execute

        async def click(screen, label):
            clicks.append({'screen': screen, 'label': label})
            await namespace['click_button'](screen, label)

        await until('bool(renpy.get_screen("main_menu"))')
        await page.mouse.click(220, 373)
        await until('bool(renpy.get_screen("chapter_card"))')
        await page.keyboard.press('Enter')
        await until('bool(renpy.get_screen("say"))')
        await execute('preferences.text_cps = 0\npersistent.reduced_motion = True')
        for cycle in range(8):
            text = await value('_history_list[-1].what')
            assert await value('scene_key') == 'first_memory'
            await click('quick_menu', 'Glossary')
            await until('bool(renpy.get_screen("glossary"))')
            glossary = await value('glossary_entries()')
            if cycle == 0:
                assert not glossary
            if cycle == 2:
                assert glossary, 'First Breath cue did not expose its glossary entries'
                await page.screenshot(path=str(OUT / 'browser-click-glossary.png'))
            await click('glossary', 'Return')
            await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
            assert await value('_history_list[-1].what') == text
            await click('quick_menu', 'People')
            await until('bool(renpy.get_screen("people"))')
            await click('people', 'Cali')
            assert await value('bool(renpy.get_widget("people", "people_description").get_all_text())')
            if cycle == 7:
                await page.screenshot(path=str(OUT / 'browser-click-people.png'))
            await click('people', 'Return')
            await until('bool(renpy.get_screen("say")) and not renpy.context()._menu')
            assert await value('_history_list[-1].what') == text
            cycles.append({'cycle': cycle + 1, 'scene': 'first_memory', 'text': text,
                           'glossary_keys': sorted(glossary), 'glossary_open_close': True,
                           'people_open_select_close': True, 'dialogue_unchanged_by_menus': True})
            print(f'Cycle {cycle + 1}/8 passed: {text}', flush=True)
            if cycle < 7:
                await page.keyboard.press('Space')
                await until(f'_history_list[-1].what != {text!r}')
        assert not errors, errors
        await page.screenshot(path=str(OUT / 'browser-click-returned.png'))
        browser_version = browser.version
        await browser.close()
    assert sha(SOURCE) == source_sha, 'Helper source changed during check'
    assert len(clicks) == 40
    assert sum(item['ready'] for item in focus_checks) == len(clicks)
    result = {'status': 'passed', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
              'scope': 'Eight first-memory lines only; full 32-scene smoke is separate.',
              'url': URL, 'viewport': [1280, 720], 'browser': browser_version,
              'source': str(SOURCE.relative_to(ROOT)), 'source_sha256': source_sha,
              'helper_sha256': hashlib.sha256(functions['click_button'].encode()).hexdigest(),
              'runner_sha256': sha(Path(__file__)),
              'cycles': cycles, 'actual_mouse_clicks': clicks, 'focus_checks': focus_checks,
              'errors': errors, 'source_unchanged_during_test': True,
              'screenshots': [{'file': name, 'sha256': sha(OUT / name)} for name in
                              ('browser-click-glossary.png', 'browser-click-people.png', 'browser-click-returned.png')]}
    (OUT / 'browser-click-focused-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'cycles': len(cycles), 'real_clicks': len(clicks),
                      'focus_checks': len(focus_checks), 'errors': errors}, indent=2))


if __name__ == '__main__':
    asyncio.run(run())
