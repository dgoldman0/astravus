"""Observe normal mural-to-treehouse rain scheduling without changing game/audio."""
import ast, asyncio, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
SOURCE=ROOT/'visual-novel/scripts/browser_smoke.py'
URL='http://127.0.0.1:8000/?preview=0.1-alpha'
SNAPSHOT='''_rain_probe = {}
for _rain_name in ("ambience", "music"):
    _rain_channel = renpy.audio.audio.get_channel(_rain_name)
    _rain_number = _rain_channel._number
    _rain_probe[_rain_name] = dict(get_playing=renpy.music.get_playing(channel=_rain_name),is_playing=renpy.music.is_playing(channel=_rain_name),pos=renpy.music.get_pos(channel=_rain_name),delay_to_10s=renpy.music.get_delay(10.0,channel=_rain_name),playing_flag=_rain_channel.playing,queue=[dict(filename=q.filename,fadein=q.fadein,loop=q.loop,tight=q.tight) for q in _rain_channel.queue],loop=list(_rain_channel.loop),default_loop=_rain_channel.default_loop,paused=_rain_channel.paused,context_pause=_rain_channel.context.pause,force_stop=_rain_channel.context.force_stop,mixer=_rain_channel.mixer,mixer_muted=renpy.game.preferences.mute.get(_rain_channel.mixer,False),actual_volume=_rain_channel.actual_volume,number=_rain_number,backend_name=(renpy.audio.renpysound.playing_name(_rain_number) if _rain_number is not None else None),backend_queue_depth=(renpy.audio.renpysound.queue_depth(_rain_number) if _rain_number is not None else None))
result=dict(scene=scene_key,bg=" ".join(renpy.get_attributes("bg") or ()),text=(_history_list[-1].what if _history_list else None),say=bool(renpy.get_screen("say")),transition=bool(renpy.display.interface.get_ongoing_transition()),trans_pause=bool(renpy.display.interface.trans_pause),skipping=renpy.config.skipping,context_menu=bool(renpy.context()._menu),pcm_ok=renpy.audio.audio.pcm_ok,channels=_rain_probe)'''

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

async def run():
    source=SOURCE.read_text()
    owner=next(n for n in ast.parse(source).body if isinstance(n,ast.AsyncFunctionDef) and n.name=='check')
    functions={n.name:ast.get_source_segment(source,n) for n in ast.walk(owner) if isinstance(n,ast.AsyncFunctionDef) and n.name in ('value','execute','click_button')}
    errors,console,requests,samples,steps=[],[],[],[],[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(args=['--enable-unsafe-swiftshader','--use-angle=swiftshader'])
        page=await browser.new_page(viewport={'width':1280,'height':720})
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('console',lambda message:console.append({'type':message.type,'text':message.text}) if message.type in ('warning','error') else None)
        page.on('requestfailed',lambda request:requests.append({'url':request.url,'failure':request.failure}))
        await page.goto(URL)
        await page.wait_for_function('typeof window.renpy_get==="function"',timeout=90000)
        await page.evaluate("""() => {
            window.__rainAudioTrace=[];
            const ctx=renpyAudio.context, names=new WeakMap(); let activeName=null;
            const log=(event, data={})=>window.__rainAudioTrace.push({event, at:performance.now(), audioTime:ctx.currentTime,...data});
            const state=channel=>({name:renpyAudio.playing_name(channel),pos:renpyAudio.get_pos(channel),duration:renpyAudio.get_duration(channel),depth:renpyAudio.queue_depth(channel)});
            for (const operation of ['queue','fadeout','dequeue','stop']) {
                const original=renpyAudio[operation];
                renpyAudio[operation]=function(...args){
                    const channel=args[0], before=state(channel), previous=activeName;
                    if(operation==='queue')activeName=args[2];
                    log(operation+'_before',{channel,args,before});
                    try {return original.apply(this,args);} finally {log(operation+'_after',{channel,after:state(channel)});activeName=previous;}
                };
            }
            const decode=ctx.decodeAudioData;
            ctx.decodeAudioData=function(data,onSuccess,onError){
                const name=activeName; log('decode_begin',{name});
                return decode.call(this,data,buffer=>{names.set(buffer,name);log('decode_ready',{name,duration:buffer.duration});onSuccess(buffer);},error=>{log('decode_error',{name,error:String(error)});if(onError)onError(error);});
            };
            const create=ctx.createBufferSource;
            ctx.createBufferSource=function(...args){
                const source=create.apply(this,args);
                for(const operation of ['start','stop']){
                    const original=source[operation];
                    source[operation]=function(...values){log('source_'+operation,{name:names.get(source.buffer)||null,args:values});return original.apply(this,values);};
                }
                return source;
            };
        }""")
        namespace={'page':page,'errors':errors,'asyncio':asyncio}
        for name in ('value','execute','click_button'):exec(compile(functions[name],str(SOURCE)+':'+name,'exec'),namespace)
        value,execute,click=(namespace[name] for name in ('value','execute','click_button'))
        async def until(expression,seconds=30):
            async with asyncio.timeout(seconds):
                while not await value(expression):await asyncio.sleep(.1)
            await asyncio.sleep(.25)
        namespace['until']=until
        async def sample(at,elapsed=None):
            state=await execute(SNAPSHOT)
            state.update(at=at,elapsed=elapsed)
            state['browser']=await page.evaluate("({visibility:document.visibilityState,audioContext:renpyAudio.context.state})")
            samples.append(state)
            print(json.dumps({'at':at,'elapsed':elapsed,'scene':state['scene'],'ambience':state['channels']['ambience']['get_playing'],'backend':state['channels']['ambience']['backend_name'],'queue':state['channels']['ambience']['queue'],'pos':state['channels']['ambience']['pos'],'text':state['text']}),flush=True)
            return state
        await until('bool(renpy.get_screen("main_menu"))')
        await execute('persistent.chapter_spoiler_warnings=False\npersistent.reduced_motion=True\npreferences.text_cps=0')
        await click('main_menu','Chapters')
        await until('bool(renpy.get_screen("dev_chapters"))')
        title=await value('dict(BOOK_SCENES)["mural_remembrance"]')
        await click('dev_chapters','30 · '+title)
        await until('scene_key=="mural_remembrance" and bool(renpy.get_screen("say")) and not renpy.context()._menu')
        await sample('mural_entry')
        for index in range(15):
            state=await value('dict(scene=scene_key,text=_history_list[-1].what,bg=" ".join(renpy.get_attributes("bg") or ()))')
            steps.append(state)
            if state['scene']=='treehouse_remembrance':break
            assert state['scene']=='mural_remembrance',state
            await page.keyboard.press('Space')
            await asyncio.sleep(.06)
        else: raise AssertionError('Did not reach treehouse remembrance')
        started=asyncio.get_running_loop().time()
        await sample('first_treehouse_observation',0.0)
        await page.screenshot(path=str(OUT/'browser-rain-trace-at-cue.png'))
        for target in (.25,.5,1.0,2.0,3.0,5.0,10.0):
            remaining=started+target-asyncio.get_running_loop().time()
            if remaining>0:await asyncio.sleep(remaining)
            await sample('treehouse_stationary',asyncio.get_running_loop().time()-started)
        await page.screenshot(path=str(OUT/'browser-rain-trace-after-10s.png'))
        version=browser.version
        audio_trace=await page.evaluate("window.__rainAudioTrace")
        await browser.close()
    files=['visual-novel/game/options.rpy','visual-novel/game/friendships_book_one.rpy','visual-novel/game/audio/rain.ogg','visual-novel/game/audio/garden_air.ogg','visual-novel/.cache/renpy-8.5.3-sdk/renpy/audio/audio.py','visual-novel/.cache/renpy-8.5.3-sdk/renpy/audio/music.py']
    result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'url':URL,'browser':version,'viewport':[1280,720],'scope':'Observational Web Audio queue/fade/decode/start/stop wrappers preserve original calls. Actual chapter-menu entry to mural followed by normal Space advances into treehouse; no game/audio overrides. Ten seconds stationary after first treehouse observation.','rain_by_10s':samples[-1]['channels']['ambience']['get_playing']=='audio/rain.ogg','backend_rain_by_10s':samples[-1]['channels']['ambience']['backend_name']=='audio/rain.ogg','samples':samples,'dialogue_steps':steps,'audio_trace':audio_trace,'errors':errors,'console':console,'failed_requests':requests,'smoke_source_sha256_at_extraction':hashlib.sha256(source.encode()).hexdigest(),'helper_sha256':hashlib.sha256(functions['click_button'].encode()).hexdigest(),'runner_sha256':sha(Path(__file__)),'supporting_inputs_checked_after_run':[{'path':f,'sha256':sha(ROOT/f)} for f in files],'screenshots':[{'file':f,'sha256':sha(OUT/f)} for f in ('browser-rain-trace-at-cue.png','browser-rain-trace-after-10s.png')]}
    (OUT/'browser-rain-trace.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'rain_by_10s':result['rain_by_10s'],'backend_rain_by_10s':result['backend_rain_by_10s'],'errors':errors,'failed_requests':requests},indent=2))

if __name__=='__main__':asyncio.run(run())
