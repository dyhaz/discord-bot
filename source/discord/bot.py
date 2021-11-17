# bot.py
import asyncio
from threading import Thread
import os
import json
import discord

from discord.ext import commands

from source.helpers.coupon_watch import CouponWatch
from source.helpers.tweet_feed import TwitterAPI
from dotenv import load_dotenv

from source import bot_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TWITTER_FOLLOW_IDS = json.loads(os.getenv('TWITTER_FOLLOW_IDS'))

bot = commands.Bot(command_prefix='!')


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
async def on_post_coupon(desc, url):
    for guild in bot.guilds:
        g = bot.get_guild(guild.id)
        for c in g.channels:
            try:
                await c.send(desc + '\n' + url)
            except Exception as e:
                print(e)
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
    await update_status()
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


@bot.command(name='version', help='Show version')
async def version(ctx):
    if ctx.author == bot.user:
        return

    response = f'Bot version: {os.getenv("VERSION")}\nLast update: {bot_commands.get_file_modification_time(__file__)}'
    await ctx.send(response)


@bot.command(name='invite', help='Invite bot to your channel')
async def invite(ctx):
    inv = bot_commands.get_invite_embed(ctx)
    await ctx.author.send(embed=inv)
    await ctx.send(f'The invite link has been sent to your DM {ctx.author.mention} :D')


@bot.command(name='info', help='Fetch latest info')
async def info(ctx):
    twitter_api = TwitterAPI()
    try:
        favorites = twitter_api.extract_favorites()
        if len(favorites) == 0:
            await ctx.send('No info :pensive:')
        else:
            for data in favorites:
                href = f'\nhttps://twitter.com/{data.user.screen_name}/status/{data.id}'
                await ctx.send(data.text + '\n' + href)
    except Exception as e:
        await ctx.send(f'Error during processing the request: '
                       f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')


@bot.command(name='restart', help='Restart bot')
@commands.is_owner()
async def restart(ctx):
    try:
        # await bot.close()
        await bot.loop.create_task(start_stream())
        # await bot.loop.create_task(bot.run(TOKEN))
        await asyncio.sleep(5)
        await ctx.send(f':warning: Bot restarted')
    except Exception as e:
        await ctx.send(f'Error during processing the request: '
                       f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')


@bot.command(name='stop', help='Stop bot')
@commands.is_owner()
async def stop(ctx):
    try:
        await bot.close()
    except Exception as e:
        await ctx.send(f'Error during processing the request: '
                       f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')


async def update_status():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f"{len(bot.guilds)} servers!"))


async def start_stream():
    # Initialize twitter API
    twitter_api = TwitterAPI()
    await asyncio.sleep(10)
    await twitter_api.create_stream(discord_bot=bot)


async def start_watch():
    # Initialize coupon watch
    watcher1 = CouponWatch(discord_bot=bot, base_url='https://www.cuponation.co.id/grabfood')
    await asyncio.sleep(5)

    watcher2 = CouponWatch(discord_bot=bot, base_url='https://www.cuponation.co.id/gojek-voucher')
    await asyncio.sleep(5)

    # Initialize thread
    t1 = Thread(target=watcher1.monitor)
    t1.start()

    t2 = Thread(target=watcher2.monitor)
    t2.start()


def main():
    bot.loop.create_task(start_stream(), name='stream')
    bot.loop.create_task(start_watch(), name='watch')
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
