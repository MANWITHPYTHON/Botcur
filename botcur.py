import requests
import schedule
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes

TOKEN = '7331809931:AAHMmsGcveHUzIV78YttGxB8pNfvNkLrzWM'
CHAT_ID = '1834773409'

def get_data():
    response = requests.get("https://api.currencyapi.com/v3/latest?apikey=cur_live_NOo092QJdTtthS6bU7h4uOrlOh1klXTTGo9FRV36&currencies=EUR%2CUSD%2CRUB")
    data = response.json()
    return data['data']


async def send_currency_prices(context: ContextTypes.DEFAULT_TYPE):
    currencies = get_data()  
    message = "📈 Ежедневные цены на валюты:\n"
    
    for currency_code in ['EUR', 'USD', 'RUB']:
        if currency_code in currencies:
            value = currencies[currency_code]['value']
            message += f"{currency_code} = {value:.2f}\n"
    await context.bot.send_message(chat_id=CHAT_ID, text=message)

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    
    schedule.every().day.at('06:00').do(lambda: asyncio.run(send_currency_prices(application)))

    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  

if __name__ == '__main__':
    asyncio.run(main())
