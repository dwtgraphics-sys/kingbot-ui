"""Audit: every commander in the picker (commanders/list.json) and in the Commander Guide (index.html)
has a real image file, no 'Unknown_' names, no placeholder text. Exit code 1 on any problem."""
import json, os, re, sys
from PIL import Image
bad = []
lst = json.load(open("commanders/list.json", encoding="utf-8"))["commanders"]
for c in lst:
    p = c["img"]
    if re.search(r"unknown", c["name"], re.I):
        bad.append("unknown name: " + c["name"])
    try:
        with Image.open(p) as im:
            im.verify()
    except Exception as e:
        bad.append(f"picker image broken: {p} ({e})")
html = open("index.html", encoding="utf-8").read()
guide = re.findall(r'^    \["([^"]+)", "[LE]", "', html, re.M)
for n in guide:
    if not os.path.isfile(f"commanders/{n}.png"):
        bad.append("guide entry without image: " + n)
if "تحقق في اللعبة" in html:
    bad.append("placeholder 'تحقق في اللعبة' still present")
print(f"picker {len(lst)} · guide {len(guide)} · problems {len(bad)}")
for b in bad:
    print("  -", b)
sys.exit(1 if bad else 0)
