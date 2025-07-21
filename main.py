import telebot
import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = '7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0'  # <-- O'zingizning Telegram bot tokenini yozing
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "YouTube havolasini yuboring (https://youtube.com/...)")

@bot.message_handler(func=lambda m: True)
def download_video(message):
    url = message.text.strip()
    if not url.startswith("https://youtube.com") and not url.startswith("https://www.youtube.com") and not url.startswith("https://youtu.be"):
        bot.reply_to(message, "❌ Bu YouTube havolasi emas.")
        return

    savefrom_url = convert_to_savefrom_url(url)
    bot.send_message(message.chat.id, "⏳ Video yuklab olinmoqda...")

    try:
        download_link = extract_download_link(savefrom_url)
        if download_link:
            video_data = requests.get(download_link, stream=True)
            filename = "video.mp4"
            with open(filename, "wb") as f:
                for chunk in video_data.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
            with open(filename, "rb") as video_file:
                bot.send_video(message.chat.id, video_file)
            os.remove(filename)
        else:
            bot.send_message(message.chat.id, "❌ Yuklab olish havolasi topilmadi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi:\n{str(e)}")

def convert_to_savefrom_url(youtube_url):
    if "youtu.be/" in youtube_url:
        video_id = youtube_url.split("/")[-1]
        return f"https://ssyoutube.com/watch?v={video_id}"
    elif "watch?v=" in youtube_url:
        return youtube_url.replace("youtube.com", "ssyoutube.com")
    else:
        return youtube_url

def extract_download_link(savefrom_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(savefrom_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # SaveFrom direct download links are inside <a> with "download-link" class or similar
    link = soup.find("a", href=True)
    if link and link["href"].startswith("https://"):
        return link["href"]
    return None

bot.polling()
