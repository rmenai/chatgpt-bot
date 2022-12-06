import logging
import random

from discord import Message
from discord.commands import ApplicationContext, slash_command
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

error_messages = [
    "I'm sorry, I'm not sure how to respond to that.",
    "Hmm...something seems to have gone wrong. Maybe try me again in a little bit.",
    "I'm tired. I can't think of anything to say right now.",
]


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

        try:
            # Remove the bot mention from the message.
            prompt = message.content.replace(f"<@{self.bot.user.id}>", "").strip()

            # Show the bot typing.
            async with message.channel.typing():
                response = await self.bot.loop.run_in_executor(None, self.handle_prompt, prompt)

                # Send the responses.
                for chunk in [response[i: i + 1800] for i in range(0, len(response), 1800)]:
                    log.debug(chunk)
                    await message.channel.send(chunk)
        except Exception as e:
            log.error(e)

            # Pick a random error message to send.
            await message.channel.send(random.choice(error_messages))

            # Dm the error to the bot owner.
            if settings.client.owner:
                await self.bot.get_user(settings.client.owner).send(f"```{repr(e)}```")

    @slash_command(guild_ids=settings.guild_ids)
    async def reset(self, ctx: ApplicationContext) -> None:
        """Reset the chat's history."""
        self.chat.reset_chat()
        await ctx.respond("Chat history has been reset.", ephemeral=True)


def setup(bot: Bot) -> None:
    """Load the `Gpt` cog."""
    bot.add_cog(Gpt(bot))
