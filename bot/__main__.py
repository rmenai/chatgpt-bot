import discord
import logging

from bot.bot import Bot
from bot.core import settings
from bot.utils.extensions import walk_extensions

log = logging.getLogger(__name__)

# Initiate the bot.
intents = discord.Intents.all()
bot = Bot(intents=intents)

# Load all cogs extensions.
for ext in walk_extensions():
    bot.load_extension(ext)

bot.run(settings.client.token)
