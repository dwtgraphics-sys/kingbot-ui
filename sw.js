// GUIDE-20: Kingbot dashboard service worker - makes the panel installable and shows device notifications.
// Network first: the dashboard and its data always come fresh; only the shell is kept for offline start.
const C = "kb-shell-v1";
self.addEventListener("install", e => { self.skipWaiting(); e.waitUntil(caches.open(C).then(c => c.addAll(["./", "index.html"]).catch(() => {}))); });
self.addEventListener("activate", e => { e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;           // GitHub API etc. go straight to the network
  if (e.request.mode === "navigate") e.respondWith(fetch(e.request).then(r => { const k = r.clone(); caches.open(C).then(c => c.put("index.html", k)).catch(() => {}); return r; }).catch(() => caches.match("index.html")));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(l => l.length ? l[0].focus() : self.clients.openWindow("./")));
});
