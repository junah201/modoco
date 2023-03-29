import discord
from discord import app_commands
from discord.ext import commands
import json
import datetime
from common import const
import sys


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def Ping(self, ctx):
        await ctx.send(f"As of `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`, the current ping is `{round(self.bot.latency*1000)}ms`")

    @app_commands.command(name="test", description="test")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("test")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        print("on error")
        exc = sys.exc_info()
        user = await self.bot.fetch_user(const.DEVELOPER_ID)
        today = datetime.datetime.today().strftime("%Y_%m_%d")
        now = datetime.datetime.now()

        await user.send(f"[{now}]ERROR : {event} : {str(exc[0].__name__)} : {str(exc[1])}   ")


async def setup(bot):
    await bot.add_cog(test(bot))
