import discord
from discord.ext import commands
import openai
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Я снова живу"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# Загрузка токенов из переменных окружения Replit
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_ORG_ID = os.environ['OPENAI_ORG_ID']

intents = discord.Intents.all()

# Устанавливаем префиксы
prefixes = ['/']  # Пример, можно изменить префикс бота

bot = commands.Bot(command_prefix=prefixes, intents=intents)

@bot.event
async def on_ready():
    print('Спящий пробудился')

@bot.command(name='/')
async def gpt_command(ctx: commands.Context, *, args):
    openai.api_key = OPENAI_API_KEY
    openai.organization = OPENAI_ORG_ID

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": args}
        ]
    )

    await ctx.send(embed=discord.Embed(description=response['choices'][0]['message']['content']))

# Запуск бота
keep_alive()
bot.run(DISCORD_TOKEN)
