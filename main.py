from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests
import os
from dotenv import load_dotenv
load_dotenv()
TG_API_KEY = os.getenv("TG_API_KEY")
API_KEY = os.getenv("API_KEY")
from datetime import datetime
from collections import defaultdict
def get_weather(city: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ua"
    response = requests.get(url)
    if response.status_code != 200:
        return "Місто не знайдено або сталася помилка."
    data = response.json()
    forecast_data = data["list"]
    daily_temps = defaultdict(list)
    daily_desc = {}
    for entry in forecast_data:
        dt = datetime.fromtimestamp(entry["dt"])
        date_str = dt.strftime("%Y-%m-%d")
        temp = entry["main"]["temp"]
        desc = entry["weather"][0]["description"]
        if 12 <= dt.hour <= 15:
            daily_desc[date_str] = desc  # опис погоди в обід
        daily_temps[date_str].append(temp)
    result = f"🌤 Прогноз погоди на 5 днів для міста {city.title()}:\n\n"
    count = 0
    for date, temps in daily_temps.items():
        avg_temp = sum(temps) / len(temps)
        description = daily_desc.get(date, "Без опису")
        result += f"{date}: {avg_temp:.1f}°C, {description}\n"
        count += 1
        if count >= 5:
            break
    return result
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"🌡 Температура в місті {city.title()}: {temp}°C\n☁️ Стан: {description}"
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather = get_weather(city)
    await update.message.reply_text(weather)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені назву міста, і я покажу тобі погоду ☁️")
def main():
    app = ApplicationBuilder().token(TG_API_KEY).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущено...")
    app.run_polling()
if __name__ == "__main__":
    main()
