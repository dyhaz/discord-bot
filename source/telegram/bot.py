import logging
import os
import asyncio
import threading

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

from source.helpers.tweet_feed import TwitterAPI

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    chat_id = update.message.chat.id

    update.message.reply_text(f'Your chat ID: {chat_id}')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def get_info():
    twitter_api = TwitterAPI()
    try:
        favorites = twitter_api.extract_favorites()
        if len(favorites) == 0:
            return 'No info :pensive:'
        else:
            for data in favorites:
                href = f'\nhttps://twitter.com/{data.user.screen_name}/status/{data.id}'
                return data.text + '\n' + href
    except Exception as e:
        return f'Error during processing the request: {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}'


async def send_random_message(bot):
    while True:
        await asyncio.sleep(10)
        # print('this is background process')
        bot.send_message(text=await get_info(), chat_id=-1001413657707)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run background thread
    t = threading.Thread(target=asyncio.run, args=(send_random_message(updater.bot),))
    t.start()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
