import discord
import json
import os

from dotenv import load_dotenv


def getInviteEmbed(ctx):
    """
    Generates Invite embed to invite bot
    Parameters:
    -----------
    ctx: discord.Context
        Context data passed by discord when a command is invoked
    Returns:
    --------
    discord.Embed
        Showing invite URL for the bot
    """
    embed = discord.Embed(
        title='Invite link!',
        description='URL for inviting bot to your servers'
    )

    embed.add_field(
        name=":warning:  You need to be an admin to add bots :slight_smile:",
        value="https://discord.com/api/oauth2/authorize?client_id=895139487150129193&permissions=8&scope=bot"
    )

    return embed
