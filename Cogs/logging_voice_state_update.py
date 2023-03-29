import discord
from discord.ext import commands
import datetime
from common import config
import utils
from typing import Optional


class loggingVoiceStateUpdate(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.auto_generator_channel: Optional[discord.VoiceChannel] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.auto_generator_channel: discord.VoiceChannel = await utils.get_channel_by_id(self.bot, config.AUTO_VOICE_CHANNEL_GENERATOR_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if not self.auto_generator_channel:
            return

        # ignore auto generator channel
        if after.channel and after.channel.id == config.AUTO_VOICE_CHANNEL_GENERATOR_CHANNEL_ID:
            return

        # join voice channel
        if after.channel and after.channel.category.id == self.auto_generator_channel.category.id:
            join_log_embed = discord.Embed(
                title="입장",
                description=f"{member.mention} 님이 {after.channel.mention} 에 입장하셨습니다.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(),
            )
            await after.channel.send(
                embed=join_log_embed
            )

        # leave voice channel
        if before.channel and before.channel.category.id == self.auto_generator_channel.category.id and before.channel != after.channel:
            leave_log_embed = discord.Embed(
                title="퇴장",
                description=f"{member.mention} 님이 {before.channel.mention} 에서 퇴장하셨습니다.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(),
            )
            # Sending messages can fail if the channel is auto deleted
            try:
                await before.channel.send(
                    embed=leave_log_embed
                )
            except:
                pass


async def setup(bot):
    await bot.add_cog(loggingVoiceStateUpdate(bot))
