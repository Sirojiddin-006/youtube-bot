import telebot
import requests
import os

TOKEN = "7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0"
INVIDIOUS_BASE = "https://yewtu.be"  # siz tanlagan instance
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "YouTube havolasini yuboring, video MP4 sifatda yuboriladi.")

@bot.message_handler(func=lambda m: "youtu.be/" in m.text or "youtube.com/watch" in m.text)
def downloader(m):
    url = m.text.strip()
    # video id ajratish
    if "youtu.be/" in url:
        vid = url.split("/")[-1]
    else:
        import urllib.parse
        vid = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("v", [None])[0]
    if not vid:
        return bot.reply_to(m, "❗ Xato: Video ID topilmadi.")
    
    bot.send_message(m.chat.id, "⏳ Video yuklanmoqda...")
    # MP4 linkini tuzish
    download_url = f"{INVIDIOUS_BASE}/api/v1/videos/{vid}?format=mp4"
    try:
        resp = requests.get(download_url, stream=True, timeout=120)
        resp.raise_for_status()
        fn = f"{vid}.mp4"
        with open(fn, "wb") as f:
            for ch in resp.iter_content(1024*512):
                if ch:
                    f.write(ch)
        with open(fn, "rb") as f:
            bot.send_video(m.chat.id, f)
        os.remove(fn)
    except Exception as e:
        bot.send_message(m.chat.id, f"❌ Yuklab bo'lmadi: {e}")

@bot.message_handler(func=lambda m: True)
def fallback(m):
    bot.reply_to(m, "Faqat YouTube havolasini yuboring.")

bot.polling()
