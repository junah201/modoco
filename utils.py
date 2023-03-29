import discord


async def get_role_by_guild(guild: discord.Guild, role_id: int):
    # Get Cached Roles
    role = guild.get_role(id)

    # If the role is not cached, request directly to the Discord server
    if role == None:
        role = discord.utils.get(await guild.fetch_roles(), id=role_id)

    return role


async def get_role_by_guild_id(bot: discord.Client, guild_id: int, role_id: int):
    # Get Guild
    guild = await get_guild_by_id(bot, guild_id)

    # Get Cached Roles
    role = guild.get_role(id)

    # If the role is not cached, request directly to the Discord server
    if role == None:
        role = discord.utils.get(await guild.fetch_roles(), id=role_id)

    return role


async def get_channel_by_id(bot: discord.Client, channel_id: int):
    # Get Cached Channel
    channel = bot.get_channel(channel_id)

    # If the channel is not cached, request directly to the Discord server
    if channel == None:
        channel = discord.utils.get(await bot.fetch_channels(), id=channel_id)

    return channel


async def get_guild_by_id(bot: discord.Client, guild_id: int):
    # Get Cached Guild
    guild = bot.get_guild(guild_id)

    # If the Guild is not cached, request directly to the Discord server
    if guild == None:
        guild = await bot.fetch_guild(guild_id)

    return guild


async def get_user_by_id(bot: discord.Client, user_id: int):
    # Get Cached Guild
    user = bot.get_user(user_id)

    # 만약 해당 유저가 캐시되어 있지 않으면 디스코드 서버에 직접 요청
    if user == None:
        user = await bot.fetch_user(user_id)

    return user


def get_dummy_button():
    return discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=" ",
        disabled=True,
    )
