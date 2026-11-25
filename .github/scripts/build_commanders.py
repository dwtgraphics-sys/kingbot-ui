"""Build commanders/list.json from the pictures in commanders/ (file name = commander name)."""
import json, os, re
D = "commanders"
EXT = (".png", ".jpg", ".jpeg", ".webp")
items = []
for f in sorted(os.listdir(D), key=str.lower):
    stem, ext = os.path.splitext(f)
    if ext.lower() not in EXT or os.path.getsize(os.path.join(D, f)) > 2_000_000:
        continue
    name = re.sub(r"[_]+", " ", stem).strip()
    name = re.sub(r"\s+", " ", name)
    if name:
        items.append({"name": name, "img": f"{D}/{f}"})
out = {"count": len(items), "commanders": items}
old = None
try:
    old = json.load(open(f"{D}/list.json", encoding="utf-8"))
except Exception:
    pass
if old != out:
    json.dump(out, open(f"{D}/list.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("list.json updated:", len(items))
else:
    print("list.json unchanged:", len(items))
