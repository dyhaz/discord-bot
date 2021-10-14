# bot.py
import os
import random

from discord.ext import commands
from source.helpers.tweet_feed import TwitterAPI
from dotenv import load_dotenv

from source import bot_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')
    bot.loop.create_task(start_stream(bot))


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='ping', help='Ping')
async def ping(ctx):
    print(f"{ctx.author} ping")
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    if ctx.author == bot.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='invite', help='Invite bot to your channel')
async def invite(ctx):
    inv = bot_commands.getInviteEmbed(ctx)
    await ctx.author.send(embed=inv)
    await ctx.send(f'The invite link has been sent to your DM {ctx.author.mention} :D')


@bot.event
async def on_post_tweet(raw_data):
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    c = bot.get_guild(guild.id)
    await c.send(raw_data.text)


async def start_stream(test_bot):
    # Initialize twitter API
    twitter_api = TwitterAPI()
    await twitter_api.create_stream(test_bot)

bot.run(TOKEN)
