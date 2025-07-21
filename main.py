import telebot
import requests

bot = telebot.TeleBot("7289724171:AAE5JjM2vDYMoI9voC92tdqVuX97y4hB1z0")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎬 YouTube Shorts yuklovchi botga xush kelibsiz!\nFaqat Shorts havolasini yuboring.")

@bot.message_handler(func=lambda message: True)
def get_link(message):
    url = message.text.strip()

    # YouTube Shorts havolasini tekshiramiz
    if not ("youtube.com/shorts/" in url or "youtu.be" in url):
        bot.reply_to(message, "❗️ Iltimos, faqat YouTube Shorts havolasini yuboring.")
        return

    try:
        # Video ID ni ajratib olamiz
        if "shorts" in url:
            video_id = url.split("shorts/")[1].split("?")[0]
        elif "youtu.be" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            bot.reply_to(message, "❗️ Havola noto‘g‘ri ko‘rinmoqda.")
            return

        # API dan yuklab olish havolasini so‘raymiz
        api_url = f"https://piped.video/streams/{video_id}"
        response = requests.get(api_url)

        if response.status_code != 200:
            bot.reply_to(message, "❌ Yuklab bo‘lmadi. Iltimos, keyinroq urinib ko‘ring.")
            return

        data = response.json()

        # Eng sifatli video linkni topamiz
        best_video = max(data['videoStreams'], key=lambda v: v['height'])
        download_link = best_video['url']

        bot.send_message(message.chat.id, f"✅ Yuklab olish havolasi:\n{download_link}")

    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}")

bot.polling()
