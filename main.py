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

    fayl_nomi = "video.mp4"
    opts = {
        'format': 'best',
        'outtmpl': fayl_nomi,
        'cookies': 'cookies_youtube.txt',  # to'g'ri joyda ekanligiga ishonch hosil qiling
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # Fayl borligini tekshirish
        if os.path.exists(fayl_nomi):
            with open(fayl_nomi, 'rb') as video:
                bot.send_video(message.chat.id, video)
            os.remove(fayl_nomi)
        else:
            bot.reply_to(message, "Video yuklab olinmadi yoki fayl topilmadi.")

    except Exception as e:
        bot.reply_to(message, f"Xatolik yuz berdi: {e}")

bot.polling()
