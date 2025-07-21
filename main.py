import telebot
import requests
import os
import re
import urllib.parse

TOKEN = "7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0"
INVIDIOUS_BASE = "https://yewtu.be"  # yoki siz xohlagan boshqa instance
bot = telebot.TeleBot(TOKEN)

# YouTube URL’idan video ID ajratuvchi regex
YOUTUBE_REGEX = re.compile(
    r'(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))([A-Za-z0-9_-]{11})'
)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "YouTube havolasini yuboring, men uni yuklab beraman.")

@bot.message_handler(func=lambda m: True)
def all_messages(m):
    text = m.text.strip()
    vid_id = None
    match = YOUTUBE_REGEX.search(text)
    if match:
        vid_id = match.group(1)
    if not vid_id:
        return bot.reply_to(m, "❗️ Iltimos, faqat YouTube havolasini yuboring.")
    
    bot.send_message(m.chat.id, "⏳ Video yuklanmoqda...")
    mp4_url = f"{INVIDIOUS_BASE}/api/v1/videos/{vid_id}?format=mp4"
    
    try:
        resp = requests.get(mp4_url, stream=True, timeout=120)
        resp.raise_for_status()
        fn = f"{vid_id}.mp4"
        with open(fn, "wb") as f:
            for chunk in resp.iter_content(1024*512):
                if chunk:
                    f.write(chunk)
        with open(fn, "rb") as video:
            bot.send_video(m.chat.id, video)
        os.remove(fn)
    except Exception as e:
        bot.send_message(m.chat.id, f"❌ Yuklab bo‘lmadi: {e}")

bot.polling()
