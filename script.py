import os
import time
import requests
import subprocess
import sys

PLAYLIST = "playlist.m3u"
UPDATED = "updated.m3u"
DEAD = "dead.m3u"

GIT_BRANCH = "main"


# ---------- PREMIUM UI FX -----------
def banner():
    os.system("clear")
    print("\n")
    print("🌀🔵✨ PREMIUM IPTV AUTO-UPDATER ✨🔵🌀")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📡 Local Network Test + 🔄 GitHub Sync Auto System")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


def loading(text, t=0.04):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(t)
    print("")


def bar(percent):
    total = 25
    filled = int(total * percent)
    empty = total - filled
    print(f"🎚️ |{'█' * filled}{'░' * empty}| {int(percent * 100)}%")


def premium_section(title):
    print("\n⭐ " + title)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


# ---------- STREAM CHECK ----------
def check_stream(url):
    try:
        r = requests.get(url, timeout=2, stream=True)
        return r.status_code == 200
    except:
        return False


# ---------- AUTO UPDATE ----------
def update_playlist():

    banner()
    loading("🚀 Checking Playlist… initializing UI…")

    if not os.path.exists(PLAYLIST):
        print("❌ playlist.m3u not found!")
        return

    online_list = []
    dead_list = []
    final_lines = []

    lines = open(PLAYLIST).read().splitlines()
    last_meta = ""

    count = sum(1 for l in lines if l.startswith("http"))
    current = 0

    premium_section("🔍 STREAM TESTING STARTED")

    for line in lines:

        if line.startswith("#EXTINF"):
            last_meta = line

        elif line.startswith("http"):
            url = line.strip()
            current += 1

            percent = current / count
            bar(percent)
            print(f"🔗 {url}")

            if check_stream(url):
                print("   ✅ ONLINE")
                final_lines.append(last_meta)
                final_lines.append(url)
                online_list.append(url)
            else:
                print("   ❌ OFFLINE")
                dead_list.append(url)

        else:
            final_lines.append(line)

        print("")

    # Write updated playlist
    with open(UPDATED, "w") as f:
        f.write("\n".join(final_lines))

    # Write dead playlist
    with open(DEAD, "w") as f:
        f.write("\n".join(dead_list))

    premium_section("📊 SUMMARY")

    print(f"🟢 ONLINE CHANNELS : {len(online_list)}")
    print(f"🔴 OFFLINE CHANNELS: {len(dead_list)}")
    print(f"📁 updated.m3u saved")
    print(f"📁 dead.m3u saved")

    git_sync()


# ---------- GITHUB SYNC ----------
def git_sync():

    premium_section("📡 SYNCING WITH GITHUB…")

    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", "Auto Updated Playlist"], check=False)
    subprocess.run(["git", "push", "origin", GIT_BRANCH], check=False)

    loading("✔ GitHub Sync Complete!\n", 0.02)


# ---------- MAIN CONTROL ----------
if __name__ == "__main__":
    
    banner()
    loading("🔧 Starting IPTV Auto System...", 0.03)

    update_playlist()

    while True:
        loading("\n⏳ Waiting 30 minutes for next auto update…", 0.02)
        time.sleep(1800)
        update_playlist()
