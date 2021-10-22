# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import getopt
import sys
import source.telegram.bot
import source.discord.bot


def main(argv):
    bot = ''
    try:
        opts, args = getopt.getopt(argv, "hb:", ["bot="])
    except getopt.GetoptError:
        print('main.py -b <bot>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -b <bot>')
            sys.exit()
        elif opt in ("-b", "--bot"):
            bot = arg

    # Use a breakpoint in the code line below to debug your script.
    print(f'Launching the bot')  # Press Ctrl+F8 to toggle the breakpoint.

    if bot == 'telegram':
        source.telegram.bot.main()

    if bot == 'discord':
        source.discord.bot.main()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
