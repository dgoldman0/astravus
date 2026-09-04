// Based on Ren'Py 8.5.3's worker; keep conditional headers mutable and
// revalidate browser HTTP cache entries before accepting an older response.
var cacheName = 'astravus-a-place-to-begin';

/* Start the service worker and cache all of the app's content or use the existing one */
self.addEventListener('install', function (e) {
    console.log('Service worker installed.');
    self.skipWaiting();
});

self.addEventListener('activate', function (e) {
    e.waitUntil(self.clients.claim());
});


/**
 * True if the service worker should add the request to a persistent cache.
 */
let addToCache = false;

/**
 * Serves the cached version of the request if it exists, otherwise fetches the
 * request from the network and caches it. Fetch is used in the default mode,
 * which will use the cache for most network requests, freshening the cache
 * as required.
 */
async function fetchAndCache(request) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);


    try {

        if (request.url.endsWith("?cached")) {
            request = new Request(request.url.replace("?cached", "?uncached"), request);
            let rv = await cache.match(request);

            if (rv == null) {
                rv = new Response("Not found in cache.", { status: 404, statusText: "Not found in cache." });
            }

            return rv;
        }

        // FetchEvent requests have immutable headers. Mutating them throws,
        // which previously sent every cached request to the offline fallback.
        const headers = new Headers(request.headers);
        if (cachedResponse) {
            if (cachedResponse.headers.get('Last-Modified')) {
                headers.set('If-Modified-Since', cachedResponse.headers.get('Last-Modified'));
            }
            if (cachedResponse.headers.get('ETag')) {
                headers.set('If-None-Match', cachedResponse.headers.get('ETag'));
            }
        }

        const response = await fetch(new Request(request, { headers, cache: 'no-cache' }));

        if (cachedResponse && response.status == 304) {
            return cachedResponse;
        }

        if (addToCache && response.status == 200) {
            await cache.put(request, response.clone());
        }

        return response;

    } catch (e) {

        if (cachedResponse) {
            console.log('Served from cache: ' + request.url);
            return cachedResponse;
        }

        console.log('Not found in cache: ' + request.url);

        throw e;
    }
}


/* Serve cached content when offline */
self.addEventListener('fetch', function (e) {
    e.respondWith(fetchAndCache(e.request));
});

self.addEventListener('message', function (e) {
    if (e.data[0] == "clearCache") {
        caches.delete(cacheName);
        console.log("Cache cleared in service worker.");

        addToCache = false;
    } else if (e.data[0] == "loadCache") {
        addToCache = true;
    }
});
