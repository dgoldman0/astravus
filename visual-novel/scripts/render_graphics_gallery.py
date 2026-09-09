"""Build a disposable current-art review gallery from the production ledger.

No duplicated before/after paintings: images link directly to selected game art.
"""
import html
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ledger = json.loads((ROOT / '../development/visual-novel/reviews/graphics/ledger.json').read_text())
output = ROOT / '../development/visual-novel/archive/local/graphics-workspace/index.html'
output.parent.mkdir(parents=True, exist_ok=True)
cards = []
for item in ledger['assets']:
    file = item['file']
    name = Path(file).stem.replace('-', ' ')
    kind = item['kind']
    uses = sorted({use['scene'] for use in item.get('story_uses', [])})
    theme = [use.get('label', 'Theme') for use in item.get('theme_uses', [])]
    outcomes = {key: review.get('outcome', 'pending') for key, review in item['reviews'].items()}
    open_count = sum(value not in ('accepted', 'not_applicable') for value in outcomes.values())
    state = 'open' if open_count else 'reviewed'
    findings = '<br>'.join(html.escape(str(note.get('notes', note.get('note', note)))) for note in item.get('findings', []))
    dimensions = ''.join('<tr><td>'+html.escape(ledger['dimensions'][key].split(';')[0])+'</td><td>'+html.escape(value.replace('_',' '))+'</td></tr>' for key, value in outcomes.items())
    image = Path(os.path.relpath(ROOT / file, output.parent)).as_posix()
    cards.append(f'''<article data-kind="{html.escape(kind)}" data-state="{state}" data-search="{html.escape(name+' '+' '.join(uses+theme))}">
      <button class="picture" onclick="openImage(this)" data-url="{html.escape(image)}" data-title="{html.escape(name)}"><img loading="lazy" src="{html.escape(image)}" alt="{html.escape(name)}"></button>
      <h2>{html.escape(name)}</h2><p class="state">{open_count} open dimensions · {html.escape(kind)}</p>
      <p>{html.escape(', '.join(uses+theme) or 'Reference / interface use')}</p>
      <details><summary>Current findings and checks</summary><table>{dimensions}</table><p>{findings}</p><code>{item['current_sha256']}</code></details>
    </article>''')
template = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Astravus · Current graphics review</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#101a1b;color:#eee7d7;font:16px/1.5 system-ui,sans-serif}header{padding:2rem max(3vw,1rem);max-width:1100px}h1{font:2.2rem Georgia,serif;margin:.2rem 0}p{color:#c1c8bf}nav{position:sticky;top:0;z-index:2;padding:.8rem max(3vw,1rem);background:#172426;display:flex;gap:.6rem;flex-wrap:wrap}input,select,button{font:inherit}input,select{background:#243438;color:inherit;border:1px solid #647578;border-radius:4px;padding:.5rem}input{min-width:220px;flex:1}main{padding:1.5rem max(3vw,1rem);display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1.3rem}article{background:#1c2a2b;border:1px solid #344748;border-radius:6px;overflow:hidden}article h2,article p,details{margin:.7rem 1rem}h2{text-transform:capitalize;font-size:1.1rem}.picture{display:block;background:#354143;border:0;width:100%;height:270px;cursor:zoom-in}.picture img{height:100%;width:100%;object-fit:contain}.state{font-size:.85rem;color:#d6c08b}summary{cursor:pointer}table{font-size:.8rem;border-collapse:collapse}td{padding:.35rem;border-bottom:1px solid #405052}td:last-child{min-width:90px}code{font-size:.7rem;overflow-wrap:anywhere}dialog{padding:0;background:#111a1c;border:1px solid #81908d;color:inherit;max-width:96vw;max-height:96vh}dialog::backdrop{background:#000d}dialog header{display:flex;gap:1rem;align-items:center;padding:.6rem 1rem;position:sticky;top:0;background:#1d292b;max-width:none}dialog header span{flex:1;text-transform:capitalize}.image-view{overflow:auto;max-height:85vh}.image-view img{display:block;max-width:92vw;max-height:82vh;object-fit:contain}.image-view.native img{max-width:none;max-height:none}button{color:inherit;background:#344447;border:1px solid #748681;border-radius:4px;padding:.25rem .6rem}#count{padding:.5rem;min-width:130px}
</style><header><p>ASTRAVUS · PRODUCTION ART</p><h1>Current graphics review</h1><p>All selected paintings, sprites and familiars. Open an image to inspect it at its native pixel size. These are the current game files; earlier versions remain in Git. Review outcomes below distinguish source art from runtime compositing.</p></header>
<nav><input id="search" aria-label="Find image or scene" placeholder="Find image or scene"><select id="kind" aria-label="Asset type"><option value="">All image types</option><option>backgrounds</option><option>characters</option><option>cg</option><option>familiars</option></select><select id="state" aria-label="Review status"><option value="">All review states</option><option value="open">Open checks</option><option value="reviewed">Reviewed</option></select><span id="count"></span></nav>
<main>CARDS</main><dialog id="viewer"><header><span id="title"></span><button onclick="document.querySelector('.image-view').classList.toggle('native')">Fit / native pixels</button><button onclick="viewer.close()">Close</button></header><div class="image-view"><img id="large" alt=""></div></dialog>
<script>
const search=document.querySelector('#search'),kind=document.querySelector('#kind'),state=document.querySelector('#state'),viewer=document.querySelector('#viewer');
function filter(){let n=0;for(const card of document.querySelectorAll('article')){const show=(!kind.value||card.dataset.kind===kind.value)&&(!state.value||card.dataset.state===state.value)&&card.dataset.search.toLowerCase().includes(search.value.toLowerCase());card.hidden=!show;if(show)n++;}document.querySelector('#count').textContent=n+' images';}
for(const el of [search,kind,state])el.addEventListener('input',filter);filter();
function openImage(button){document.querySelector('#large').src=button.dataset.url;document.querySelector('#large').alt=button.dataset.title;document.querySelector('#title').textContent=button.dataset.title;document.querySelector('.image-view').classList.remove('native');viewer.showModal();}
viewer.addEventListener('click',e=>{if(e.target===viewer)viewer.close();});
</script></html>'''
output.write_text(template.replace('CARDS', '\n'.join(cards)))
print(output)
