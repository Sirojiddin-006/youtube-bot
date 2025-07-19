import telebot
import yt_dlp
import os
import re

TOKEN = '7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎬 Menga YouTube havolasini yuboring (shorts ham bo'ladi). Men uni sifatli yuklab beraman.")

def to_main_url(url):
    if 'youtube.com/shorts/' in url:
        return re.sub(r'youtube\.com/shorts/([a-zA-Z0-9_-]+)', r'youtube.com/watch?v=\1', url)
    if 'youtu.be/' in url:
        return re.sub(r'youtu\.be/([a-zA-Z0-9_-]+)', r'youtube.com/watch?v=\1', url)
    return url

@bot.message_handler(func=lambda m: 'youtube.com' in m.text or 'youtu.be' in m.text)
def download_video(message):
    url = message.text.strip()
    url = to_main_url(url)

    bot.send_message(message.chat.id, "⏳ Yuklanmoqda...")

    fayl_nomi = "video.mp4"

    opts = {
        'outtmpl': fayl_nomi,
        'format': 'bestvideo+bestaudio/best',
        'cookies': 'cookies_youtube.txt',
        'quiet': True,
        'merge_output_format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        with open(fayl_nomi, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(fayl_nomi)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi: {e}")

bot.polling()
