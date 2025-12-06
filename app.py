import os
import telebot
import requests
from flask import Flask, request, send_file

BOT_TOKEN = os.getenv("BOT_TOKEN")
PLAYLIST = "playlist.m3u"

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
server = Flask(name)

Optimized stream checker (low memory)

def check_stream(url):
try:
r = requests.get(url, timeout=1, stream=True)
return r.status_code == 200
except:
return False

Serve playlist

@server.route("/playlist.m3u")
def serve_playlist():
return send_file(PLAYLIST, mimetype="audio/x-mpegurl")

Telegram webhook

@server.route("/webhook", methods=["POST"])
def telegram_webhook():
update = telebot.types.Update.de_json(request.data.decode("utf-8"))
bot.process_new_updates([update])
return "OK", 200

Bot commands

@bot.message_handler(commands=['start'])
def start_cmd(message):
bot.reply_to(message, "IPTV Bot Active!\nUse /refresh to update playlist.")

@bot.message_handler(commands=['refresh'])
def refresh_cmd(message):
bot.reply_to(message, "Checking playlist… (Render-safe mode)")

if not os.path.exists(PLAYLIST):  
    bot.reply_to(message, "playlist.m3u not found!")  
    return  

online = []  
offline = []  
new_list = []  

lines = open(PLAYLIST).readlines()  
meta = ""  

# Limit check to prevent Render timeout  
MAX_CHECK = 80   # 🔥 Render free safe limit  
checked = 0  

for line in lines:  
    if line.startswith("#EXTINF"):  
        meta = line  

    elif line.startswith("http"):  
        url = line.strip()  

        if checked < MAX_CHECK:  
            if check_stream(url):  
                online.append(url)  
                new_list.append(meta)  
                new_list.append(url + "\n")  
            else:  
                offline.append(url)  
            checked += 1  
        else:  
            # Skip checking to prevent timeout  
            new_list.append(meta)  
            new_list.append(url + "\n")  

    else:  
        new_list.append(line)  

# Write back new playlist safely  
with open(PLAYLIST, "w") as f:  
    f.writelines(new_list)  

bot.send_message(  
    message.chat.id,  
    f"Checked: {checked}\nOnline: {len(online)}\nOffline: {len(offline)}"  
)  

if offline:  
    bot.send_message(message.chat.id, "\n".join(offline[:20]))

Webhook setter

@server.route("/")
def set_webhook():
webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/webhook"
bot.set_webhook(url=webhook_url)
return f"Webhook set: {webhook_url}", 200

Local run

if name == "main":
server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
