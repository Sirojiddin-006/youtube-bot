import telebot
import yt_dlp
import os

bot = telebot.TeleBot('7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "YouTube Shorts havolasini yuboring:")

@bot.message_handler(func=lambda msg: True)
def download_video(message):
    link = message.text.strip()

    # Faqat YouTube Shorts havolalarini tekshiramiz
    if "youtube.com/shorts/" in link or "youtu.be/" in link:
        # Havolani to‘liq video formatga o‘zgartiramiz
        if "shorts" in link:
            video_id = link.split("/shorts/")[1].split("?")[0]
        elif "youtu.be/" in link:
            video_id = link.split("youtu.be/")[1].split("?")[0]
        else:
            bot.send_message(message.chat.id, "Noto‘g‘ri havola.")
            return

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        bot.send_message(message.chat.id, "Video yuklanmoqda...")

        # Fayl nomi
        filename = f"{video_id}.mp4"

        # Eng sifatli versiyasini yuklab olish uchun sozlamalar
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': filename,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            with open(filename, 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)

            os.remove(filename)

        except Exception as e:
            bot.send_message(message.chat.id, f"Xatolik yuz berdi: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Faqat YouTube Shorts havolasi yuboring.")

bot.polling()
