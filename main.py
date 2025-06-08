from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TG_API_KEY = os.getenv("TG_API_KEY")
API_KEY = os.getenv("API_KEY")

def get_weather(city: str, date: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ua"
    response = requests.get(url)

    if response.status_code != 200:
        return "Місто не знайдено або сталася помилка."

    data = response.json()
    forecast_data = data["list"]

    hourly_forecast = []

    for entry in forecast_data:
        dt = datetime.fromtimestamp(entry["dt"])
        date_str = dt.strftime("%Y-%m-%d")

        if date_str == date:
            time_str = dt.strftime("%H:%M")
            temp = entry["main"]["temp"]
            desc = entry["weather"][0]["description"]

            hourly_forecast.append(f"{time_str}: {temp:.1f}°C, {desc}")

    if not hourly_forecast:
        return f"Прогнозу на {date} для міста {city.title()} не знайдено."

    result = f"🌤 Прогноз погоди на {date} для міста {city.title()}:\n\n"
    result += "\n".join(hourly_forecast)
    return result

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    parts = message.split(",")

    if len(parts) != 2:
        await update.message.reply_text("Будь ласка, введіть місто і дату в форматі: Місто, Дата (рік-місяць-день)")
        return

    city = parts[0].strip()
    date = parts[1].strip()

    weather = get_weather(city, date)

    await update.message.reply_text(weather)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Надішли мені місто та дату у форматі: Місто, Дата (рік-місяць-день), і я покажу тобі погодний прогноз на кожну годину!")

def main():
    app = ApplicationBuilder().token(TG_API_KEY).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущено...")

    app.run_polling()

if __name__ == "__main__":
    main()
