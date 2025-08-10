import re
import requests
import json
import time
import base64
import random
import urllib3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==== YOUTUBE ID AJRATISH FUNKSIYASI ====
def extract_video_id(url):
    patterns = [
        r'youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'youtube\.com/shorts/([a-zA-Z0-9_-]+)',
        r'youtu\.be/([a-zA-Z0-9_-]+)',
        r'youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'youtube\.com/v/([a-zA-Z0-9_-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# ==== API CHAQRISH ====
def make_api_call(url, method, data, service_name):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.youtube.com/',
        'Origin': 'https://www.youtube.com'
    }
    if service_name in ['bizft-v2', 'bizft-v3']:
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    else:
        headers['Content-Type'] = 'application/json'

    try:
        if method == 'POST':
            resp = requests.post(url, headers=headers, data=data, timeout=30, verify=False)
        else:
            resp = requests.get(url, headers=headers, timeout=30, verify=False)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {'error': f"{service_name} API error: {e}"}

# ==== 3 TA API'NI SINASH ====
def try_multiple_downloaders(url, format_code):
    apis = [
        {
            'name': 'bizft-v1',
            'url': 'https://yt.savetube.me/api/v1/video-downloader',
            'method': 'POST',
            'data': json.dumps({'url': url, 'format_code': format_code})
        },
        {
            'name': 'bizft-v2',
            'url': 'https://www.y2mate.com/mates/analyzeV2/ajax',
            'method': 'POST',
            'data': f'k_query={url}&k_page=home&hl=en&q_auto=0'
        },
        {
            'name': 'bizft-v3',
            'url': 'https://sfrom.net/mates/en/analyze/ajax',
            'method': 'POST',
            'data': f'url={url}'
        }
    ]
    for api in apis:
        result = make_api_call(api['url'], api['method'], api['data'], api['name'])
        if result and 'error' not in result:
            return result
    return None

# ==== FALLBACK DIRECT URL YASASH ====
def generate_direct_urls(video_id, format_code):
    base_urls = [
        'https://rr1---sn-oj5hn5-55.googlevideo.com/videoplayback',
        'https://rr2---sn-oj5hn5-55.googlevideo.com/videoplayback',
        'https://rr3---sn-oj5hn5-55.googlevideo.com/videoplayback'
    ]
    expire = int(time.time()) + 21600
    current_time = int(time.time())
    urls = []
    for base_url in base_urls:
        params = {
            'expire': expire,
            'ei': base64.b64encode(random.randbytes(15)).decode('utf-8'),
            'ip': '127.0.0.1',
            'id': 'o-' + base64.b64encode(random.randbytes(30)).decode('utf-8'),
            'itag': format_code,
            'source': 'youtube',
            'requiressl': 'yes',
            'mime': 'video%2Fmp4',
            'dur': '44.544',
            'lmt': str(current_time) + '000',
            'ratebypass': 'yes',
            'clen': str(random.randint(1000000, 10000000)),
            'gir': 'yes'
        }
        urls.append(base_url + '?' + '&'.join(f"{k}={v}" for k, v in params.items()))
    return urls

# ==== VIDEO INFO OLISH ====
def get_video_info(video_id):
    try:
        resp = requests.get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json", timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

# ==== TELEGRAM BOT FUNKSIYALARI ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Menga YouTube link yubor, men yuklab olish linklarini qaytaraman 📥")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    format_code = "18"

    video_id = extract_video_id(url)
    if not video_id:
        await update.message.reply_text("❌ Video ID topilmadi. Iltimos, to‘g‘ri YouTube link yuboring.")
        return

    video_info = get_video_info(video_id)
    api_result = try_multiple_downloaders(url, format_code)

    if api_result and 'response' in api_result and 'direct_link' in api_result['response']:
        primary_link = api_result['response']['direct_link']
        alternatives = generate_direct_urls(video_id, format_code)
    else:
        direct_urls = generate_direct_urls(video_id, format_code)
        primary_link = direct_urls[0]
        alternatives = direct_urls[1:]

    title = video_info['title'] if video_info else "Noma'lum video"
    reply_text = f"🎬 *{title}*\n\n📥 Asosiy yuklab olish link:\n{primary_link}\n\n🔄 Boshqa linklar:\n" + "\n".join(alternatives)

    await update.message.reply_text(reply_text, parse_mode="Markdown")

# ==== BOTNI ISHGA TUSHIRISH ====
if __name__ == "__main__":
    BOT_TOKEN = "7289724171:AAF7mfFse9t92dTChQVAlaCHPHIouI5akL4"  # <-- o‘zingizning bot tokeningizni yozing
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()