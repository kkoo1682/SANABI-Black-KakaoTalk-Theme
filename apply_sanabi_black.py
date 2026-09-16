#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
import shutil, sys, re

PROJECT = Path(sys.argv[1]).resolve()
HERE = Path(__file__).resolve().parents[1]
AS = HERE / "assets"

def pngs():
    return [p for p in PROJECT.rglob("*.png")]

def safe_copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print("COPY", src.name, "->", dst)

def replace_matching(patterns, src, limit=None):
    hits=[]
    for p in pngs():
        n=p.name.lower()
        if any(x in n for x in patterns):
            hits.append(p)
    # Avoid copying into mipmap launcher resources unless explicitly requested.
    hits=[p for p in hits if "mipmap" not in str(p).lower()]
    if limit:
        hits=hits[:limit]
    for p in hits:
        safe_copy(src,p)
    return hits

# 1) App/theme icon
icon_candidates = [p for p in pngs() if "icon" in p.name.lower() and "theme" in p.name.lower()]
if not icon_candidates:
    icon_candidates = [p for p in pngs() if p.name.lower() in {"icon.png","commonicothem e.png".replace(" ","")}]
for p in icon_candidates[:4]:
    safe_copy(AS/"tab_05.png", p)

# 2) Main/theme background: use the user's large SONNABI city image exactly as supplied.
#    The image file itself is never cropped or stretched by this script.
bg_hits = replace_matching(
    ["mainbg", "main_bg", "mainbackground", "main_background",
     "friendstab", "friendstab", "maintab_bg", "background_image"],
    AS/"main_background.jpg"
)
# If sample names differ, use the first non-chatroom background-like image.
if not bg_hits:
    for p in pngs():
        n=p.name.lower()
        if "background" in n and "chatroom" not in n and "passcode" not in n:
            safe_copy(AS/"main_background.jpg", p)
            bg_hits.append(p)
            break

# 3) Chatroom background: keep SANABI atmosphere, but don't replace every UI image.
for p in pngs():
    n=p.name.lower()
    if "chatroom" in n and "background" in n:
        safe_copy(AS/"main_background.jpg", p)

# 4) Profile images
profiles = [
    AS/"profile_01.png",
    AS/"profile_02.png",
    AS/"profile_03.png",
]
for idx, src in enumerate(profiles, 1):
    patterns = [f"profile_0{idx}", f"profile0{idx}", f"profile_{idx}", f"profile{idx}"]
    for p in pngs():
        n=p.name.lower()
        if any(x in n for x in patterns) and "background" not in n:
            safe_copy(src,p)

# 5) Main-tab character buttons.
# Android KakaoTalk theme tabs are image resources, so we replace existing tab image
# resources rather than adding a new arbitrary Android UI layout.
tab_assets = [AS/f"tab_{i:02d}.png" for i in range(1,6)]
for i, src in enumerate(tab_assets,1):
    hits=[]
    for p in pngs():
        n=p.name.lower()
        if ("tab" in n or "maintab" in n) and (str(i) in n or f"0{i}" in n):
            if "selected" not in n and "on" not in n:
                hits.append(p)
    for p in hits[:2]:
        safe_copy(src,p)

# Fallback: if no numbered tab files were detected, replace the first five small tab-like
# images (not launcher/profile/background/chat bubble assets).
if not any("tab" in p.name.lower() for p in pngs()):
    candidates=[]
    for p in pngs():
        n=p.name.lower()
        if any(k in n for k in ["main", "friend", "chat", "plus", "more"]) and "background" not in n:
            candidates.append(p)
    for src,p in zip(tab_assets,candidates[:5]):
        safe_copy(src,p)

# 6) Black palette: update existing theme color XML conservatively.
for colors in PROJECT.rglob("colors.xml"):
    text=colors.read_text(encoding="utf-8", errors="ignore")
    def repl(m):
        name=m.group(1)
        value=m.group(2)
        low=name.lower()
        if any(k in low for k in ["background","bg","surface","window"]):
            new="#FF000000"
        elif any(k in low for k in ["text","title","label","message"]):
            new="#FFFFFFFF"
        elif any(k in low for k in ["accent","point","primary","highlight"]):
            new="#FF6E1B2D"
        else:
            new=value
        return f'<color name="{name}">{new}</color>'
    text2=re.sub(r'<color\s+name="([^"]+)">([^<]+)</color>', repl, text)
    if text2 != text:
        colors.write_text(text2, encoding="utf-8")
        print("PALETTE", colors)

# 7) Theme/app name
for s in PROJECT.rglob("strings.xml"):
    text=s.read_text(encoding="utf-8", errors="ignore")
    text=re.sub(r'(<string\s+name="theme_title">).*?(</string>)', r'\1SANABI Black\2', text)
    text=re.sub(r'(<string\s+name="app_name">).*?(</string>)', r'\1SANABI Black\2', text)
    s.write_text(text, encoding="utf-8")

print("SANABI BLACK APPLY COMPLETE")
