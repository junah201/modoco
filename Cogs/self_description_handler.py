import discord
from discord.ext import commands
from common import config
import utils
import asyncio
from typing import Optional
from datetime import datetime


class SelfDescriptionHandler(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.self_description_channel: Optional[discord.TextChannel] = None
        self.main_chat_channel: Optional[discord.TextChannel] = None

    class self_description_modal(discord.ui.Modal):
        def __init__(self, main_chat_channel: discord.TextChannel):
            self.main_chat_channel = main_chat_channel
            super().__init__(title="모도코 자기소개", timeout=None)

            self.short_description = discord.ui.TextInput(
                label="한줄 자기소개",
                placeholder="한줄 자기소개를 입력해주세요.",
                required=True,
            )
            self.add_item(self.short_description)

            self.github_url = discord.ui.TextInput(
                label="깃허브 주소",
                placeholder="만약 없다면 비워주세요.",
                required=False,
            )
            self.add_item(self.github_url)

        async def on_submit(self, interaction: discord.Interaction) -> None:
            introduction_embed = discord.Embed(
                title="새로운 유저가 서버에 참여했어요!",
                color=discord.Color.blue(),
                timestamp=datetime.now(),
            )
            introduction_embed.add_field(
                name="한줄 자기소개",
                value=self.short_description.value,
                inline=False,
            )
            if self.github_url.value:
                introduction_embed.add_field(
                    name="깃허브 주소",
                    value=self.github_url.value,
                    inline=False,
                )

            introduction_embed.set_author(
                name=interaction.user.name,
                icon_url=interaction.user.display_avatar.url,
            )

            default_role = await utils.get_role_by_guild(interaction.guild, config.DEFULT_ROLE_ID)
            await interaction.user.add_roles(default_role)

            await self.main_chat_channel.send(f"{interaction.user.mention}", embed=introduction_embed)
            await interaction.response.send_message(f"{interaction.user.mention}자기소개가 완료되었습니다.", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.self_description_channel: discord.TextChannel = await utils.get_channel_by_id(self.bot, config.SELF_DESCRIPTION_CHANNEL_ID)
        self.main_chat_channel: discord.TextChannel = await utils.get_channel_by_id(self.bot, config.MAIN_CHAT_CHANNEL_ID)

        # init channel
        await self.self_description_channel.purge()

        self_description_embed = discord.Embed(
            title="자기소개",
            description="자기소개에 따라 역할을 부여받을 수 있습니다.",
            color=discord.Color.blue(),
        )

        self_description_embed.set_footer(
            text="모도코",
            icon_url=config.SERVER_ICON_URL
        )

        self_description_view = discord.ui.View(timeout=None)
        self_description_button = discord.ui.Button(
            label="자기소개", style=discord.ButtonStyle.primary)

        async def self_description_button_callback(interaction: discord.Interaction):
            await interaction.response.send_modal(self.self_description_modal(self.main_chat_channel))

        self_description_button.callback = self_description_button_callback

        self_description_view.add_item(self_description_button)

        await self.self_description_channel.send(embed=self_description_embed, view=self_description_view)


async def setup(bot):
    await bot.add_cog(SelfDescriptionHandler(bot))
