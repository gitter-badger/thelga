from helga.bot import bot

import helga.quotes
import helga.misc


def main():
    helga.quotes.init()
    helga.misc.init()
    bot.polling()
