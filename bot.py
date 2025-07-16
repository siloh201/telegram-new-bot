import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime
import pytz

# اطلاعات توکن و کانال
BOT_TOKEN = "8173650773:AAH5QE4ZPLc6Zr4rF-tlSM3MCu6Zr4rF"
CHANNEL_ID = "@TradeHub_University"
TIMEZONE = pytz.timezone("Asia/Tehran")

bot = Bot(token=BOT_TOKEN)

# گرفتن اخبار از Forex Factory
def get_forexfactory_news():
    url = "https://www.forexfactory.com/calendar"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = []

    for row in soup.find_all("tr", class_="calendar__row"):
        impact = row.find("td", class_="calendar__impact")
        if not impact:
            continue

        impact_level = impact.span.get("title", "")
        if "High" in impact_level:
            emoji = "🔴 High"
        elif "Medium" in impact_level:
            emoji = "🟠 Medium"
        elif "Holiday" in impact_level:
            emoji = "🏦 Bank Holiday"
        else:
            continue

        time_cell = row.find("td", class_="calendar__time")
        time_text = time_cell.text.strip() if time_cell else "?"

        currency = row.find("td", class_="calendar__currency").text.strip()
        title = row.find("td", class_="calendar__event").text.strip()
        forecast = row.find("td", class_="calendar__forecast").text.strip()
        previous = row.find("td", class_="calendar__previous").text.strip()

        news_items.append(
            f"{emoji}\n"
            f"🕐 {time_text} | 🌍 {currency}\n"
            f"📰 {title}\n"
            f"📊 Forecast: {forecast or '-'} | 📈 Previous: {previous or '-'}\n"
            "----------------------------"
        )

    return news_items

# ارسال پیام به تلگرام
def send_news():
    today = datetime.now(TIMEZONE).strftime("%Y-%m-%d")
    news = get_forexfactory_news()

    if not news:
        message = f"📊 هیچ خبر مهمی برای {today} یافت نشد."
    else:
        message = f"📊 اخبار مهم فارکس - {today}:\n\n" + "\n\n".join(news[:10])

    bot.send_message(chat_id=CHANNEL_ID, text=message)

# اجرای تابع اصلی
if name == "main":
    send_news()
