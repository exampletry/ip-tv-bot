import os
import time
import requests
import subprocess
import sys
import random

PLAYLIST = "playlist.m3u"
UPDATED = "updated.m3u"
DEAD = "dead.m3u"
GIT_BRANCH = "main"


# ------------------------------------------------------
#            GLASS UI PREMIUM EFFECT FUNCTIONS
# ------------------------------------------------------

def clear():
    os.system("clear")


def glass_line(text="", width=60):
    space = width - len(text)
    return f"│  {text}{' ' * space}│"


def glass_box(title, width=60):
    clear()
    border = "┌" + "─" * (width + 2) + "┐"
    end =    "└" + "─" * (width + 2) + "┘"
    
    print("\033[97m")   # white glow foreground
    print(border)
    print(glass_line(" "))
    print(glass_line(f"✨ {title}"))
    print(glass_line(" "))
    print(end)
    print("\033[0m")


def frosted_glass_panel(lines: list, width=60):
    border = "╭" + "─" * (width + 2) + "╮"
    end =    "╰" + "─" * (width + 2) + "╯"
    print("\033[97m")
    print(border)
    for ln in lines:
        space = width - len(ln)
        print(f"│ {ln}{' ' * space} │")
    print(end)
    print("\033[0m")


def typing_glass(text, speed=0.02):
    print("\033[97m│ ", end="")
    for c in text:
        print(c, end="", flush=True)
        time.sleep(speed)
    print("\033[0m")


def glass_progress(percent):
    bar_len = 40
    filled = int(bar_len * percent)
    empty = bar_len - filled
    print(
        f"\033[97m│ ░{'█' * filled}{' ' * empty}░ {int(percent * 100)}% │\033[0m"
    )


# ------------------------------------------------------
#                    STREAM CHECK
# ------------------------------------------------------

def check_stream(url):
    try:
        r = requests.get(url, timeout=2, stream=True)
        return r.status_code == 200
    except:
        return False


# ------------------------------------------------------
#                   MAIN UPDATE FUNCTION
# ------------------------------------------------------

def update_playlist():

    glass_box("IPTV Auto Updater - Glass Edition ✨")
    time.sleep(0.3)

    if not os.path.exists(PLAYLIST):
        frosted_glass_panel(["❌ playlist.m3u not found!"])
        return

    lines = open(PLAYLIST).read().splitlines()
    last_meta = ""

    online_list = []
    dead_list = []
    final = []

    total = sum(1 for l in lines if l.startswith("http"))
    done = 0

    frosted_glass_panel(["🔍 STREAM TESTING STARTED", " "])

    for line in lines:
        if line.startswith("#EXTINF"):
            last_meta = line
        elif line.startswith("http"):
            url = line.strip()
            done += 1

            glass_progress(done / total)
            typing_glass(f"Checking: {url}", 0.004)

            if check_stream(url):
                typing_glass("✔ ONLINE")
                final.append(last_meta)
                final.append(url)
                online_list.append(url)
            else:
                typing_glass("✖ OFFLINE")
                dead_list.append(url)

            print("")
        else:
            final.append(line)

    open(UPDATED, "w").write("\n".join(final))
    open(DEAD, "w").write("\n".join(dead_list))

    frosted_glass_panel([
        "📊 SUMMARY",
        f"🟢 ONLINE  : {len(online_list)}",
        f"🔴 OFFLINE : {len(dead_list)}",
        "📁 updated.m3u saved",
        "📁 dead.m3u saved"
    ])

    git_sync()


# ------------------------------------------------------
#                     GIT HUB SYNC
# ------------------------------------------------------

def git_sync():

    frosted_glass_panel(["📡 Syncing With GitHub…"])

    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", "Glass Update"], check=False)
    subprocess.run(["git", "push", "origin", GIT_BRANCH], check=False)

    frosted_glass_panel(["✔ GitHub Sync Complete!"])


# ------------------------------------------------------
#                     AUTO LOOP
# ------------------------------------------------------

if __name__ == "__main__":
    glass_box("Starting Glass UI System…")
    time.sleep(0.5)

    update_playlist()

    while True:
        frosted_glass_panel(["⏳ Waiting 30 minutes…"])
        time.sleep(1800)
        update_playlist()	

