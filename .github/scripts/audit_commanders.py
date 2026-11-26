"""Audit: every commander in the picker (commanders/list.json) and in the Commander Guide (index.html)
has a real image file, no 'Unknown_' names, no placeholder text, no spelling duplicates and no letter-monogram
avatars (TOOLS-05H). Exit code 1 on any problem."""
import json, os, re, sys, unicodedata
from PIL import Image
bad = []
html = open("index.html", encoding="utf-8").read()
alias = dict(re.findall(r'(\w+): "(\w+)"', re.search(r"const CMD_ALIAS = \{([^}]*)\}", html).group(1)))
def key(n):
    k = unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().strip()
    k = re.sub(r"\s+(?:i|ii|iii|iv|v|vi|vii)$", "", k, flags=re.I).lower()
    k = re.sub(r"[^a-z0-9]", "", k)
    return alias.get(k, k)
lst = json.load(open("commanders/list.json", encoding="utf-8"))["commanders"]
seen = {}
for c in lst:
    p = c["img"]
    if re.search(r"unknown", c["name"], re.I):
        bad.append("unknown name: " + c["name"])
    k = key(c["name"])
    if k in seen:
        bad.append(f"duplicate commander: {seen[k]} / {c['name']}")
    seen[k] = c["name"]
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception as e:
        bad.append(f"picker image broken: {p} ({e})")
files = {f for f in os.listdir("commanders") if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))}
listed = {os.path.basename(c["img"]) for c in lst}
for f in sorted(files - listed):
    bad.append("image not in list.json: " + f)
guide = re.findall(r'^    \["([^"]+)", "[LE]", "', html, re.M)
for n in guide:
    if not os.path.isfile(f"commanders/{n}.png"):
        bad.append("guide entry without image: " + n)
if "تحقق في اللعبة" in html:
    bad.append("placeholder 'تحقق في اللعبة' still present")
# zero monograms: the avatar fallback must not build initials, and the picker must hide portrait-less names
if re.search(r"slice\(0,\s*2\)\.map\(w\s*=>\s*w\[0\]\)", html):
    bad.append("letter-monogram avatar fallback still present")
if "cmdHasPortrait(n)" not in html:
    bad.append("picker does not filter commanders without a portrait")
print(f"picker {len(lst)} · guide {len(guide)} · problems {len(bad)}")
for b in bad:
    print("  -", b)
sys.exit(1 if bad else 0)
