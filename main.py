import telebot
import yt_dlp
import os

TOKEN = '7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0'
bot = telebot.TeleBot(TOKEN)

# Yuklangan videolarni vaqtinchalik saqlash uchun papka
video_folder = 'videolar'
os.makedirs(video_folder, exist_ok=True)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Salom! YouTube link yuboring, men sizga videoni yuklab beraman.")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text.strip()

    if not url.startswith("http"):
        bot.reply_to(message, "Iltimos, to'g'ri YouTube havolasini yuboring.")
        return

    bot.send_message(message.chat.id, "Video yuklanmoqda... Iltimos, kuting ⏳")

    try:
        # Yuklab olingan fayl uchun nom shabloni
        opts = {
            'outtmpl': os.path.join(video_folder, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'cookies': 'cookies_youtube.txt'
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(file_path)  # Yuklab bo‘lgach faylni o‘chiramiz

    except Exception as e:
        bot.send_message(message.chat.id, f"Xatolik yuz berdi:\n{e}")

bot.polling()
