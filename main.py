import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import discord

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
COOLDOWN_MINUTES = int(os.getenv("COOLDOWN_MINUTES", "30"))

def get_message():
    try:
        with open("message.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Hey! I'm not around right now, I'll get back to you soon."

last_responded = {}

class AutoResponder(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        print(f"Auto-responder active.")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not isinstance(message.channel, discord.DMChannel):
            return

        user_id = message.author.id
        now = datetime.now(timezone.utc)

        if user_id in last_responded:
            if now - last_responded[user_id] < timedelta(minutes=COOLDOWN_MINUTES):
                return

        away_message = get_message()
        last_responded[user_id] = now
        print(f"[{now.strftime('%H:%M:%S')}] Auto-responded to {message.author}")
        await message.channel.send(away_message)

AutoResponder().run(TOKEN)
