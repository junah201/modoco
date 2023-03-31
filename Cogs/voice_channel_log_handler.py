import discord
from discord.ext import commands
import datetime
from common import config
import utils
from typing import Optional


class VoiceChannelLogHandler(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.auto_generator_channel: Optional[discord.VoiceChannel] = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.auto_generator_channel: discord.VoiceChannel = await utils.get_channel_by_id(self.bot, config.AUTO_VOICE_CHANNEL_GENERATOR_CHANNEL_ID)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member | discord.User,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if not self.auto_generator_channel:
            return

        # ignore auto generator channel
        if after.channel and after.channel.id == config.AUTO_VOICE_CHANNEL_GENERATOR_CHANNEL_ID:
            return

        # ignore if channel is not changed
        if before.channel and after.channel and before.channel.id == after.channel.id:
            return

        # join voice channel
        if after.channel and after.channel.category_id == self.auto_generator_channel.category_id:
            join_log_embed = discord.Embed(
                title=f"맴버가 들어왔어요.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.now(),
            )
            join_log_embed.set_author(
                name=member.name,
                icon_url=member.display_avatar.url,
            )
            join_log_embed.set_footer(
                text="모도코",
                icon_url=config.SERVER_ICON_URL
            )
            await after.channel.send(
                embed=join_log_embed
            )

        # leave voice channel
        if before.channel and before.channel.category_id == self.auto_generator_channel.category_id and before.channel != after.channel:
            leave_log_embed = discord.Embed(
                title="맴버가 나갔어요.",
                color=discord.Color.red(),
                timestamp=datetime.datetime.now(),
            )
            leave_log_embed.set_author(
                name=member.name,
                icon_url=member.display_avatar.url,
            )
            leave_log_embed.set_footer(
                text="모도코",
                icon_url=config.SERVER_ICON_URL
            )
            # Sending messages can fail if the channel is auto deleted
            try:
                await before.channel.send(
                    embed=leave_log_embed
                )
            except:
                pass


async def setup(bot):
    await bot.add_cog(VoiceChannelLogHandler(bot))
