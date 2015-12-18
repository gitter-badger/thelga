import random

from helga.bot import bot


def yn_handler(message):
    bot.reply_to(message, random.choice(('Ja', 'Nein')))


def rn_handler(message):
    bot.reply_to(message, "9")
