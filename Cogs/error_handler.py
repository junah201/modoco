import discord

from discord.ext import commands
from discord import app_commands
from logging import ERROR as LOG_ERROR, CRITICAL as LOG_CRITICAL
from typing import Optional
import utils
from common import config


class ErrorHandler(commands.Cog, name="errors"):
    """Errors handler."""

    def __init__(self, bot: discord.Client) -> None:
        self.bot = bot
        bot.tree.error(coro=self.__dispatch_to_app_command_handler)
        self.ERROR_LOGGING_CHANNEL = None

        self.default_error_message = "🕳️ There is an error."

    @ commands.Cog.listener()
    async def on_ready(self):
        self.ERROR_LOGGING_CHANNEL: Optional[discord.TextChannel] = await utils.get_channel_by_id(self.bot, config.ERROR_LOGGING_CHANNEL_ID)

    async def trace_error(self, level: str, error: Exception):
        if not self.ERROR_LOGGING_CHANNEL:
            raise error

        error_embed = discord.Embed(
            title=f"Error",
            description=f"""
            message : `{type(error).__name__}`
            error : `{error}`
            level : `{level}`
            File : `{error.__traceback__.tb_frame.f_code.co_filename}`
            Line : `{error.__traceback__.tb_lineno}`
            """,
            color=discord.Color.red(),
        )

        await self.ERROR_LOGGING_CHANNEL.send(embed=error_embed)

        raise error

    async def __dispatch_to_app_command_handler(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    async def __respond_to_interaction(self, interaction: discord.Interaction) -> bool:
        try:
            await interaction.response.send_message(content=self.default_error_message, ephemeral=True)
            return True
        except discord.errors.InteractionResponded:
            return False

    @ commands.Cog.listener("on_error")
    async def get_error(self, event, *args, **kwargs):
        """Error handler"""
        error = Exception(
            f"Unexpected Internal Error: (event) {event}, (args) {args}, (kwargs) {kwargs}.")
        await self.trace_error("on_error", error)

    @ commands.Cog.listener("on_command_error")
    async def get_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Command Error handler
        doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exception-hierarchy
        """

        await self.trace_error("get_command_error", error)

        try:
            if ctx.interaction:  # HybridCommand Support
                await self.__respond_to_interaction(ctx.interaction)
                edit = ctx.interaction.edit_original_response
                if isinstance(error, commands.HybridCommandError):
                    error = error.original  # Access to the original error
            else:
                try:
                    discord_message = await ctx.send(self.default_error_message)
                except discord.errors.Forbidden:
                    return
                edit = discord_message.edit
            raise error

        # ConversionError
        except commands.ConversionError as d_error:
            await edit(content=f"🕳️ {d_error}")
        # UserInputError
        except commands.MissingRequiredArgument as d_error:
            await edit(content=f"🕳️ Something is missing. `{ctx.clean_prefix}{ctx.command.name} <{'> <'.join(ctx.command.clean_params)}>`")
        # UserInputError -> BadArgument
        except commands.MemberNotFound or commands.UserNotFound as d_error:
            await edit(content=f"🕳️ Member `{str(d_error).split(' ')[1]}` not found ! Don't hesitate to ping the requested member.")
        # UserInputError -> BadUnionArgument | BadLiteralArgument | ArgumentParsingError
        except commands.BadArgument or commands.BadUnionArgument or commands.BadLiteralArgument or commands.ArgumentParsingError as d_error:
            await edit(content=f"🕳️ {d_error}")
        # CommandNotFound
        except commands.CommandNotFound as d_error:
            await edit(content=f"🕳️ Command `{str(d_error).split(' ')[1]}` not found !")
        # CheckFailure
        except commands.PrivateMessageOnly:
            await edit(content="🕳️ This command canno't be used in a guild, try in direct message.")
        except commands.NoPrivateMessage:
            await edit(content="🕳️ This is not working as excpected.")
        except commands.NotOwner:
            await edit(content="🕳️ You must own this bot to run this command.")
        except commands.MissingPermissions as d_error:
            await edit(content=f"🕳️ Your account require the following permissions: `{'` `'.join(d_error.missing_permissions)}`.")
        except commands.BotMissingPermissions as d_error:
            if not "send_messages" in d_error.missing_permissions:
                await edit(content=f"🕳️ The bot require the following permissions: `{'` `'.join(d_error.missing_permissions)}`.")
        except commands.CheckAnyFailure or commands.MissingRole or commands.BotMissingRole or commands.MissingAnyRole or commands.BotMissingAnyRole as d_error:
            await edit(content=f"🕳️ {d_error}")
        except commands.NSFWChannelRequired:
            await edit(content="🕳️ This command require an NSFW channel.")
        # DisabledCommand
        except commands.DisabledCommand:
            await edit(content="🕳️ Sorry this command is disabled.")
        # CommandInvokeError
        except commands.CommandInvokeError as d_error:
            await edit(content=f"🕳️ {d_error.original}")
        # CommandOnCooldown
        except commands.CommandOnCooldown as d_error:
            await edit(content=f"🕳️ Command is on cooldown, wait `{str(d_error).split(' ')[7]}` !")
        # MaxConcurrencyReached
        except commands.MaxConcurrencyReached as d_error:
            await edit(content=f"🕳️ Max concurrency reached. Maximum number of concurrent invokers allowed: `{d_error.number}`, per `{d_error.per}`.")
        # HybridCommandError
        except commands.HybridCommandError as d_error:
            await self.get_app_command_error(ctx.interaction, error)

    @ commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """App command Error Handler
        doc: https://discordpy.readthedocs.io/en/latest/interactions/api.html#exception-hierarchy
        """
        await self.trace_error("get_app_command_error", error)

        try:
            await self.__respond_to_interaction(interaction)
            edit = interaction.edit_original_response

            raise error
        except app_commands.CommandInvokeError as d_error:
            if isinstance(d_error.original, discord.errors.InteractionResponded):
                await edit(content=f"🕳️ {d_error.original}")
            elif isinstance(d_error.original, discord.errors.Forbidden):
                await edit(content=f"🕳️ `{type(d_error.original).__name__}` : {d_error.original.text}")
            else:
                await edit(content=f"🕳️ `{type(d_error.original).__name__}` : {d_error.original}")
        except app_commands.CheckFailure as d_error:
            if isinstance(d_error, app_commands.errors.CommandOnCooldown):
                await edit(content=f"🕳️ Command is on cooldown, wait `{str(d_error).split(' ')[7]}` !")
            else:
                await edit(content=f"🕳️ `{type(d_error).__name__}` : {d_error}")
        except app_commands.CommandNotFound:
            await edit(content=f"🕳️ Command was not found.. Seems to be a discord bug, probably due to desynchronization.\nMaybe there is multiple commands with the same name, you should try the other one.")
        except Exception as e:
            """
            Caught here:
            app_commands.TransformerError
            app_commands.CommandLimitReached
            app_commands.CommandAlreadyRegistered
            app_commands.CommandSignatureMismatch
            """

    @ commands.Cog.listener("on_view_error")
    async def get_view_error(self, interaction: discord.Interaction, error: Exception, item: any):
        """View Error Handler"""
        await self.trace_error("get_view_error", error)

        try:
            raise error
        except discord.errors.Forbidden:
            pass

    @ commands.Cog.listener("on_modal_error")
    async def get_modal_error(self, interaction: discord.Interaction, error: Exception):
        """Modal Error Handler"""
        await self.trace_error("get_modal_error", error)
        try:
            raise error
        except discord.errors.Forbidden:
            pass


async def setup(bot: discord.Client):
    await bot.add_cog(ErrorHandler(bot))
