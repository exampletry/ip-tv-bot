import os
import time
import math
import requests
import subprocess

PLAYLIST = "playlist.m3u"
GIT_BRANCH = "main"


# ------------ RAINBOW COLOR GENERATOR ----------------
def rgb_text(text, t):
    out = ""
    for i, c in enumerate(text):
        r = int((math.sin(i/2 + t) + 1) * 127)
        g = int((math.sin(i/2 + t + 2) + 1) * 127)
        b = int((math.sin(i/2 + t + 4) + 1) * 127)
        out += f"\033[38;2;{r};{g};{b}m{c}"
    return out + "\033[0m"


# ------------ ROBOTIC HEADER ----------------
def header(t):
    text = r"""
 ██████╗  ██╗ ██████╗     ████████╗██╗   ██╗
 ██╔══██╗███║██╔════╝     ╚══██╔══╝██║   ██║
 ██████╔╝╚██║███████╗        ██║   ██║   ██║
 ██╔══██╗ ██║██╔═══██╗       ██║   ██║   ██║
 ██║  ██║ ██║╚██████╔╝       ██║   ╚██████╔╝
 ╚═╝  ╚═╝ ╚═╝ ╚═════╝        ╚═╝    ╚═════╝
         PREMIUM IPTV AUTO UPDATER
    """
    return rgb_text(text, t)


# ------------ RAINBOW MOTION BG ----------------
def rainbow_motion():
    for t in range(20):
        os.system("clear")
        print(header(t/2))

        bar = rgb_text("█" * 40, t)  
        print("\n" * 2)
        print(bar)
        print("\n" * 1)
        print(rgb_text("Initializing Robotic Engine...", t))
        time.sleep(0.07)


# ------------ STREAM TEST ----------------
def check_stream(url):
    try:
        r = requests.get(url, timeout=2, stream=True)
        return r.status_code == 200
    except:
        return False


def update_playlist():
    os.system("clear")
    print(header(1))
    print("\n🚀 Checking playlist...\n")

    if not os.path.exists(PLAYLIST):
        print("❌ playlist.m3u missing!")
        return

    lines = open(PLAYLIST).read().splitlines()
    updated = []
    last = ""

    http_count = sum(1 for l in lines if l.startswith("http"))
    done = 0

    for line in lines:

        if line.startswith("#EXTINF"):
            last = line

        elif line.startswith("http"):
            url = line.strip()
            done += 1

            percent = int((done / http_count) * 100)
            progress = rgb_text("█" * int(percent/5), time.time())
            print(f"{progress} {percent}% → {url}")

            if check_stream(url):
                print("   ✔ ONLINE\n")
                updated.append(last)
                updated.append(url)
            else:
                print("   ✘ OFFLINE\n")

        else:
            updated.append(line)

    # Write final result
    with open(PLAYLIST, "w") as f:
        f.write("\n".join(updated))

    print("\n✔ playlist.m3u updated.")
    git_sync()


# ------------ GITHUB SYNC ----------------
def git_sync():
    print("\n📡 Syncing GitHub...\n")

    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", "Auto Update"], check=False)
    subprocess.run(["git", "push", "origin", GIT_BRANCH], check=False)

    print("✔ GitHub Sync Done\n")


# ------------ MAIN ----------------
def start():
    rainbow_motion()      # 🔥 safe animation
    update_playlist()

    while True:
        print("\n⏳ 30 minutes waiting...\n")
        time.sleep(1800)
        update_playlist()


if __name__ == "__main__":
    start()	

