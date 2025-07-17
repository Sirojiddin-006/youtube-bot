import telebot
import yt_dlp
import os

bot = telebot.TeleBot("7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0")

@bot.message_handler(commands=['start'])
def boshlash(message):
    bot.reply_to(message, "Salom! YouTube videosining linkini yuboring.")

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def yuklab_olish(message):
    url = message.text
    bot.reply_to(message, "Video yuklanmoqda... biroz kuting.")

    try:
        fayl_nomi = "video.mp4"
        opts = {
            'format': 'best',
            'outtmpl': fayl_nomi
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

        with open(fayl_nomi, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(fayl_nomi)

    except Exception as e:
        bot.reply_to(message, f"Xatolik: {e}")

bot.polling()
