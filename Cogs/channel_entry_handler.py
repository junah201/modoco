import discord
from discord.ext import commands
import datetime
from common import config
import utils
from typing import Optional


class ChannelEntryHandler(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.welcome_channel: Optional[discord.TextChannel] = None
        self.goodbye_channel: Optional[discord.TextChannel] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.welcome_channel: discord.TextChannel = await utils.get_channel_by_id(self.bot, config.WELCOME_CHANNEL_ID)
        self.goodbye_channel: discord.TextChannel = await utils.get_channel_by_id(self.bot, config.GOODBYE_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_log_embed = discord.Embed(
            description=f"{member.mention} 님이 서버에 입장하셨습니다.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )

        await self.welcome_channel.send(
            embed=welcome_log_embed
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        goodbye_log_embed = discord.Embed(
            description=f"{member.mention} 님이 서버에서 나가셨습니다.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.now(),
        )

        await self.goodbye_channel.send(
            embed=goodbye_log_embed
        )


async def setup(bot):
    await bot.add_cog(ChannelEntryHandler(bot))
