/* Check graphics support before starting Ren'Py's WebAssembly runtime. */
(() => {
    "use strict";

    function hasWebGL() {
        for (const name of ["webgl2", "webgl"]) {
            try {
                const canvas = document.createElement("canvas");
                const gl = canvas.getContext(name);
                if (gl && !gl.isContextLost()) {
                    gl.getExtension("WEBGL_lose_context")?.loseContext();
                    return true;
                }
            } catch (_) {
                // Embedded views may reject context creation outright.
            }
        }
        return false;
    }

    function showFallback() {
        const style = document.createElement("style");
        style.textContent = `
            html, body { margin: 0; min-height: 100%; background: #07191d; }
            #startup-fallback { box-sizing: border-box; max-width: 760px;
                margin: 10vh auto; padding: 40px; color: #eee7d8;
                font: 19px/1.6 system-ui, sans-serif; }
            #startup-fallback .eyebrow { color: #d3bb8e; letter-spacing: .25em; font-size: 14px; }
            #startup-fallback h1 { font: 36px/1.25 Georgia, serif; color: #f4e7cb; }
            #startup-fallback a { display: inline-block; margin: 16px 0;
                padding: 12px 22px; color: #07191d; background: #dfc68e;
                text-decoration: none; border-radius: 3px; }
            #startup-fallback a:focus-visible, #startup-fallback input:focus-visible {
                outline: 3px solid #eee7d8; outline-offset: 5px; }
            #startup-fallback input { box-sizing: border-box; display: block;
                width: 100%; margin-top: 8px; padding: 12px; font: inherit;
                color: #d5dfd6; background: #142e31; border: 1px solid #466062; }
            #startup-fallback .detail { color: #b6c3b9; font-size: 16px; }
        `;
        document.head.append(style);
        const panel = document.createElement("main");
        panel.id = "startup-fallback";
        panel.innerHTML = `
            <p class="eyebrow">ASTRAVUS · A PLACE TO BEGIN</p>
            <h1>Open the chapter in your browser</h1>
            <p>This view cannot provide the graphics support the game needs.
               Open it in a full browser, or play the desktop version.</p>
            <a id="open-browser" target="_blank" rel="noopener">Open in browser</a>
            <label for="game-address">Or copy this address into your browser:</label>
            <input id="game-address" readonly spellcheck="false">
            <p class="detail">If you are already in a full browser, enable WebGL
               graphics support or use the desktop version.</p>
        `;
        document.body.replaceChildren(panel);
        panel.querySelector("#open-browser").href = window.location.href;
        const address = panel.querySelector("#game-address");
        address.value = window.location.href;
        address.addEventListener("click", () => address.select());
    }

    function loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement("script");
            script.src = src;
            script.onload = resolve;
            script.onerror = () => reject(new Error(`Could not load ${src}`));
            document.body.append(script);
        });
    }

    async function updateServiceWorker() {
        if (!navigator.serviceWorker) return;
        try {
            const registration = await navigator.serviceWorker.register('./service-worker.js', {
                updateViaCache: 'none'
            });
            const worker = registration.installing || registration.waiting;
            if (worker) {
                await new Promise(resolve => {
                    const finish = () => {
                        clearTimeout(timeout);
                        worker.removeEventListener('statechange', check);
                        resolve();
                    };
                    const check = () => {
                        if (worker.state === 'activated' || worker.state === 'redundant') finish();
                    };
                    // Offline play can continue with an already installed worker.
                    const timeout = setTimeout(finish, 5000);
                    worker.addEventListener('statechange', check);
                    check();
                });
            }
        } catch (error) {
            console.warn('Offline support could not be updated.', error);
        }
    }

    if (!hasWebGL()) {
        showFallback();
        return;
    }

    // renpy-pre.js must configure Module before the engine script executes.
    updateServiceWorker().then(() => loadScript("renpy-pre.js")).then(() => loadScript("renpy.js")).catch(error => {
        const message = document.createElement("p");
        message.textContent = "The game could not finish loading. Reload this page to try again.";
        message.style.cssText = "position:relative;padding:2rem;background:#07191d;color:#eee7d8";
        document.body.append(message);
        console.error(error);
    });
})();
