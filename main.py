import discord
from discord.ext import commands
from openai import OpenAI, OpenAIError
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
OPENAI_ORG_ID = os.environ.get('OPENAI_ORG_ID')

# Инициализируем клиент один раз при запуске
openai_client = OpenAI(api_key=OPENAI_API_KEY, organization=OPENAI_ORG_ID)

intents = discord.Intents.all()

# Устанавливаем префиксы
prefixes = ['!gpt ']  # Используем !gpt вместо '/' — команда // некорректна

bot = commands.Bot(command_prefix=prefixes, intents=intents)

@bot.event
async def on_ready():
    print('Спящий пробудился')

@bot.command(name='ask')
async def gpt_command(ctx: commands.Context, *, args):
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": args}
            ]
        )
        reply = response.choices[0].message.content
        await ctx.send(embed=discord.Embed(description=reply))
    except OpenAIError as e:
        await ctx.send(f"Ошибка API: {e}")
    except Exception as e:
        await ctx.send("Произошла ошибка при обработке запроса.")

# Запуск бота
keep_alive()
bot.run(DISCORD_TOKEN)
