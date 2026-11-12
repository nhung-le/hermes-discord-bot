import os
import asyncio
from dotenv import load_dotenv
from discord import Client, Intents, Message
from better_profanity import profanity
from src.openai_client import generate_casual_reply

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BOT_NAME = os.getenv("BOT_NAME", "hermes-demo")

profanity.load_censor_words()

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (id={client.user.id})")

@client.event
async def on_message(message: Message):
    if message.author.bot:
        return

    # simple alias: message starts with /chat
    if message.content.startswith('/chat'):
        text = message.content[len('/chat'):].strip() or 'Chào'
        if profanity.contains_profanity(text):
            await message.reply('Nhắc nhẹ: không chửi nha.')
            return
        await message.channel.typing()
        reply = generate_casual_reply(text, BOT_NAME)
        await message.reply(reply or 'Tui đang bận, thử lại sau.')

    # mention trigger: user mentions the bot
    if client.user in message.mentions:
        content = message.content.replace(f"<@!{client.user.id}>", '').replace(f"<@{client.user.id}>", '').strip()
        if not content:
            await message.reply('Gì đó? Nói rõ tí 😏')
            return
        if profanity.contains_profanity(content):
            await message.reply('Nhắc nhẹ: không chửi nha.')
            return
        await message.channel.typing()
        reply = generate_casual_reply(content, BOT_NAME)
        await message.reply(reply or 'Tui đang bận, thử lại sau.')

if __name__ == '__main__':
    if not DISCORD_TOKEN:
        print('Missing DISCORD_TOKEN in environment. Copy .env.example -> .env and fill it.')
    else:
        client.run(DISCORD_TOKEN)
