import logging

from discord import Message
from discord.ext import commands
from revChatGPT.revChatGPT import Chatbot

from bot.bot import Bot
from bot.core import settings

log = logging.getLogger(__name__)

config = {
    "email": settings.chat.email,
    "password": settings.chat.password,
    "session": settings.chat.session,
    "Authorization": ""
}


class Gpt(commands.Cog):
    """Manage chatGPT commands."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.chat = Chatbot(config, conversation_id=None)
        self.chat.refresh_session()

    def handle_prompt(self, prompt: str) -> str:
        """Handle the prompt."""
        response = self.chat.get_chat_response(prompt, output="text")
        return response["message"]

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        """Listen and response to user messages."""
        if self.bot.user not in message.mentions or message.author.bot:
            if not message.author.bot:
                log.debug("Message should start with bot mention.")
                log.debug(message.content)
            return

        # Remove the bot mention from the message.
        prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

        # Show the bot typing.
        async with message.channel.typing():
            response = await self.bot.loop.run_in_executor(None, self.handle_prompt, prompt)

            # Send the responses.
            for chunk in [response[i: i + 1800] for i in range(0, len(response), 1800)]:
                log.debug(chunk)
                await message.channel.send(chunk)


def setup(bot: Bot) -> None:
    """Load the `Gpt` cog."""
    bot.add_cog(Gpt(bot))
