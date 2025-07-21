import telebot
import yt_dlp
import os
import uuid

BOT_TOKEN = '7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "YouTube havolasini yuboring, men uni sizga video ko'rinishida yuboraman.")

@bot.message_handler(func=lambda message: True)
def download_youtube_video(message):
    url = message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url):
        bot.reply_to(message, "Iltimos, faqat YouTube havolasini yuboring.")
        return

    bot.reply_to(message, "Videoni yuklab olayapman, biroz kuting...")

    fayl_nomi = f"{uuid.uuid4()}.mp4"
    try:
        opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': fayl_nomi,
            'cookiefile': 'cookies_youtube.txt'  # Agar fayldan olishni istasangiz
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        with open(fayl_nomi, 'rb') as video:
            bot.send_video(message.chat.id, video)

    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {str(e)}")

    finally:
        if os.path.exists(fayl_nomi):
            os.remove(fayl_nomi)

bot.infinity_polling()
