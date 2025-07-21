import telebot
import requests
import os

TOKEN = "7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0"
API_BASE = "https://youtube-download-api.matheusishiyama.repl.co"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,
        "Salom! YouTube video linkini yuboring — men uni MP4 formatida qaytaraman."
    )

@bot.message_handler(func=lambda m: "youtu.be/" in m.text or "youtube.com/watch" in m.text)
def video_handler(msg):
    url = msg.text.strip()
    bot.send_message(msg.chat.id, "⏳ Yuklanmoqda…")
    try:
        resp = requests.get(f"{API_BASE}/mp4/", params={"url": url}, stream=True, timeout=120)
        resp.raise_for_status()

        filename = "video.mp4"
        with open(filename, "wb") as f:
            for chunk in resp.iter_content(1024*1024):
                if chunk:
                    f.write(chunk)

        with open(filename, "rb") as f:
            bot.send_video(msg.chat.id, f)

        os.remove(filename)
    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Xatolik bo‘ldi: {e}")

@bot.message_handler(func=lambda m: True)
def fallback(msg):
    bot.reply_to(msg, "❗ Iltimos, faqat YouTube havolasini yuboring.")

bot.polling()
