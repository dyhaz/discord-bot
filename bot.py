# bot.py
import asyncio
import os
import random
import json
import discord

from discord.ext import commands
from source.helpers.tweet_feed import TwitterAPI
from dotenv import load_dotenv

from source import bot_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
TWITTER_FOLLOW_IDS = json.loads(os.getenv('TWITTER_FOLLOW_IDS'))


@bot.event
async def on_stream_error(status_code='unknown'):
    for guild in bot.guilds:
        g = bot.get_guild(guild.id)
        # Send message to first channel in guild
        for c in g.channels:
            try:
                await c.send(f':warning: Connection error! Please contact administrator - {str(status_code)}')
            except Exception:
                continue
            else:
                break


@bot.event
async def on_post_tweet(raw_data):
    tweet = json.loads(raw_data)

    if str(tweet['user']['id']) not in TWITTER_FOLLOW_IDS:
        return

    for guild in bot.guilds:
        g = bot.get_guild(guild.id)
        # Send tweet to first channel in guild
        for c in g.channels:
            try:
                msg = tweet['text']
                msg += f'\nhttps://twitter.com/{tweet["user"]["screen_name"]}/status/{tweet["id"]}'
                # Uncomment this to send original links
                # for url in tweet['entities']['urls']:
                #     msg += '\n' + url['expanded_url']

                await c.send(msg)
            except Exception as e:
                print(e)
                continue
            else:
                break


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"{len(bot.guilds)} servers!"))

    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')


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


async def start_stream():
    # Initialize twitter API
    twitter_api = TwitterAPI()
    await asyncio.sleep(10)
    await twitter_api.create_stream(discord_bot=bot)


bot.loop.create_task(start_stream())
bot.run(TOKEN)
