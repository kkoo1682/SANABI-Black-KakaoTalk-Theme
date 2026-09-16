#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys
import re


# ==============================
# 기본 설정
# ==============================

PROJECT = Path(sys.argv[1]).resolve()
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


# ==============================
# 파일 복사
# ==============================

def copy_file(source, target):
    if not source.exists():
        print("파일 없음:", source)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

    print("교체:", target)


def all_files():
    return list(PROJECT.rglob("*"))


def png_files():
    return [
        p for p in all_files()
        if p.is_file() and p.suffix.lower() == ".png"
    ]


# ==============================
# 1. 메인 배경
# ==============================

MAIN_BG = ASSETS / "메인_배경.jpg"

for file in all_files():

    if not file.is_file():
        continue

    name = file.name.lower()

    if (
        "theme_maintab_cell_image" in name
        or "maintabbg" in name
        or "maintab_bg" in name
        or "mainbg" in name
    ):
        copy_file(MAIN_BG, file)


# ==============================
# 2. 채팅방 배경
# ==============================

for file in all_files():

    if not file.is_file():
        continue

    name = file.name.lower()

    if (
        "theme_chatroom_background_image" in name
        or "chatroombg" in name
        or "chatroom_bg" in name
    ):
        copy_file(MAIN_BG, file)


# ==============================
# 3. 아래쪽 캐릭터 아이콘
# ==============================

tabs = {
    1: ASSETS / "tab_01.png",
    2: ASSETS / "tab_02.png",
    3: ASSETS / "tab_03.png",
    4: ASSETS / "tab_04.png",
    5: ASSETS / "tab_05.png",
}


for number, source in tabs.items():

    if not source.exists():
        print("탭 이미지 없음:", source)
        continue

    for file in png_files():

        name = file.name.lower()

        if "theme_maintab_ico" not in name:
            continue

        if f"_{number}_" in name:
            copy_file(source, file)


# ==============================
# 4. 프로필 이미지
# ==============================

profiles = {
    "01": ASSETS / "profile_01.png",
    "02": ASSETS / "profile_02.png",
}


for number, source in profiles.items():

    if not source.exists():
        continue

    for file in png_files():

        name = file.name.lower()

        if (
            f"profileimg{number}" in name
            or f"profile_img{number}" in name
            or f"profile_{number}" in name
        ):
            copy_file(source, file)


# ==============================
# 5. 테마 색상
# ==============================

for colors in PROJECT.rglob("colors.xml"):

    text = colors.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    def change_color(match):

        name = match.group(1)
        old = match.group(2)

        key = name.lower()

        # 배경 → 검정
        if any(word in key for word in [
            "background",
            "bg",
            "surface",
            "window"
        ]):
            return f'<color name="{name}">#FF000000</color>'

        # 글자 → 흰색
        if any(word in key for word in [
            "text",
            "title",
            "label",
            "message"
        ]):
            return f'<color name="{name}">#FFFFFFFF</color>'

        # 포인트 → SANABI 느낌의 어두운 붉은색
        if any(word in key for word in [
            "accent",
            "point",
            "primary",
            "highlight"
        ]):
            return f'<color name="{name}">#FF8B2635</color>'

        return match.group(0)

    new_text = re.sub(
        r'<color\s+name="([^"]+)">([^<]+)</color>',
        change_color,
        text
    )

    if new_text != text:

        colors.write_text(
            new_text,
            encoding="utf-8"
        )

        print("색상 변경:", colors)


# ==============================
# 6. 테마 이름
# ==============================

for strings in PROJECT.rglob("strings.xml"):

    text = strings.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    text = re.sub(
        r'(<string\s+name="theme_title">).*?(</string>)',
        r'\1SANABI Black\2',
        text
    )

    text = re.sub(
        r'(<string\s+name="app_name">).*?(</string>)',
        r'\1SANABI Black\2',
        text
    )

    strings.write_text(
        text,
        encoding="utf-8"
    )

    print("테마 이름 변경:", strings)


# ==============================
# 완료
# ==============================

print("")
print("==============================")
print(" SANABI BLACK 테마 적용 완료")
print("==============================")
