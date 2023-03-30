import discord
from discord.ext import commands
from common import config
import utils
import asyncio
from typing import Optional


class RoleHandler(commands.Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.role_assignment_channel: Optional[discord.TextChannel] = None

    class role_button(discord.ui.Button):
        def __init__(self, label: str, emoji: Optional[str], style: discord.ButtonStyle, role: discord.Role, no_duplicate_role_ids: list = []):
            super().__init__(label=label, emoji=emoji, style=style)
            self.role = role
            self.no_duplicate_role_ids = no_duplicate_role_ids

        async def callback(self, interaction: discord.Interaction):
            # already has role
            if self.role in interaction.user.roles:
                await interaction.user.remove_roles(self.role)
                await interaction.response.send_message(f"{interaction.user.mention} `{self.role.name}` 역할이 삭제되었습니다!", ephemeral=True)
                return

            # remove duplicate roles
            remove_roles = [
                role for role in interaction.user.roles if role.id in self.no_duplicate_role_ids]
            for remove_role in remove_roles:
                await interaction.user.remove_roles(await utils.get_role(interaction.guild, remove_role))

            # add role
            await interaction.user.add_roles(self.role)

            await interaction.response.send_message(f"{interaction.user.mention} `{self.role.name}` 역할이 추가되었습니다!", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.role_assignment_channel: discord.TextChannel = await utils.get_channel_by_id(self.bot, config.ROLE_ASSIGNMENT_CHANNEL_ID)

        # init channel
        await self.role_assignment_channel.purge()

        # interest roles
        interest_embed = discord.Embed(
            title="관심사",
            description="관심사에 따라 역할을 부여받을 수 있습니다.",
            color=discord.Color.blue()
        )

        interest_view = discord.ui.View(timeout=None)

        interests = [
            ("FE", "🧑‍💻", discord.ButtonStyle.primary, config.FE_ROLE_ID),
            ("BE", "👨‍💻", discord.ButtonStyle.primary, config.BE_ROLE_ID),
            ("AI", "🤖", discord.ButtonStyle.primary, config.AI_ROLE_ID),
            ("Data", "📊", discord.ButtonStyle.primary, config.DATA_ROLE_ID),
            ("Blockchain", "🔗", discord.ButtonStyle.primary, config.BLOCKCHAIN_ROLE_ID),
            ("Game", "🎮", discord.ButtonStyle.primary, config.GAME_ROLE_ID),
            ("iOS", "📱", discord.ButtonStyle.primary, config.IOS_ROLE_ID),
            ("Android", "📱", discord.ButtonStyle.primary, config.ANDROID_ROLE_ID),
            ("Cloud", "☁️", discord.ButtonStyle.primary, config.CLOUD_ROLE_ID),
            ("Devops", "🛠", discord.ButtonStyle.primary, config.DEVOPS_ROLE_ID),
            ("Infra", "🏗", discord.ButtonStyle.primary, config.INFRA_ROLE_ID),
            ("Security", "🔒", discord.ButtonStyle.primary, config.SECURITY_ROLE_ID),
            ("System", "🖥", discord.ButtonStyle.primary, config.SYSTEM_ROLE_ID),
            ("QA", "🧪", discord.ButtonStyle.primary, config.QA_ROLE_ID),
            ("Embedded", "🔌", discord.ButtonStyle.primary, config.EMBEDDED_ROLE_ID),
        ]

        for label, emoji, style, role_id in interests:
            role = await utils.get_role_by_guild(self.role_assignment_channel.guild, role_id)
            interest_view.add_item(self.role_button(
                label=label, emoji=emoji, style=style, role=role))

        await self.role_assignment_channel.send(embed=interest_embed, view=interest_view)

        # language roles
        language_embed = discord.Embed(
            title="언어",
            description="언어에 따라 역할을 부여받을 수 있습니다.",
            color=discord.Color.blue()
        )

        language_view = discord.ui.View(timeout=None)

        languages = [
            ("Java", "☕", discord.ButtonStyle.primary, config.JAVA_ROLE_ID),
            ("Swift", "📱", discord.ButtonStyle.primary, config.SWIFT_ROLE_ID),
            ("C/C++", None, discord.ButtonStyle.primary, config.C_ROLE_ID),
            ("C#", None, discord.ButtonStyle.primary, config.CSHARP_ROLE_ID),
            ("JS/TS", None, discord.ButtonStyle.primary, config.JS_ROLE_ID),
            ("Python", "🐍", discord.ButtonStyle.primary, config.PYTHON_ROLE_ID),
            ("Go", None, discord.ButtonStyle.primary, config.GO_ROLE_ID),
            ("PHP", None, discord.ButtonStyle.primary, config.PHP_ROLE_ID),
            ("Ruby", "♦️", discord.ButtonStyle.primary, config.RUBY_ROLE_ID),
            ("Rust", "⚙️", discord.ButtonStyle.primary, config.RUST_ROLE_ID),
        ]

        for label, emoji, style, role_id in languages:
            role = await utils.get_role_by_guild(self.role_assignment_channel.guild, role_id)
            language_view.add_item(self.role_button(
                label=label, emoji=emoji, style=style, role=role))

        await self.role_assignment_channel.send(embed=language_embed, view=language_view)


async def setup(bot):
    await bot.add_cog(RoleHandler(bot))
