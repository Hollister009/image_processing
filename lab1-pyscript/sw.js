const assets = [
  "./",
  "./styles/main.css",
  "./assets/logo.svg",
  "./assets/logo64.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open("static").then((cache) => {
      return cache.addAll(assets);
    })
  );
});

self.addEventListener("fetch", (e) => {
  //   console.log(`Intercepting fetch request for: ${e.request.url}`);
  e.respondWith(caches.match(e.request).then((response) => {
    return response || fetch(e.request);
  }));
});
