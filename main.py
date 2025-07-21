import telebot
import yt_dlp
import os

# Tokeningizni shu yerga yozing
bot = telebot.TeleBot("7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "YouTube link yuboring, video yuklab beraman.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        bot.reply_to(message, "Iltimos, to‘g‘ri YouTube havolasini yuboring.")
        return

    bot.reply_to(message, "⏳ Yuklanmoqda, kuting...")

    try:
        output_file = "video.mp4"

        ydl_opts = {
            'outtmpl': output_file,
            'cookies': 'cookies_youtube.txt',  # Cookie fayl yo'li
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(output_file, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(output_file)

    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi:\n{str(e)}")

bot.polling()
