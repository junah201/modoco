import discord
from discord.ext import commands
from common import const
import logging


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=const.PREFIX,
            intents=discord.Intents.all(),
            sync_command=True,
        )

        self.initial_extension = [
            "Cogs.create_voice_channel",
            "Cogs.logging_voice_state_update",
            "Cogs.errors",
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)

        await bot.tree.sync()

    async def on_ready(self):
        print(f"DISCORD BOT : {self.user}")
        print(
            f"Discord Version : {discord.__version__}")
        print(f"On ready")


if __name__ == '__main__':
    log_handler = logging.FileHandler(
        filename='discord.log', encoding='utf-8', mode='w')
    bot = Bot()
    bot.run(const.TOKEN, log_handler=log_handler)
