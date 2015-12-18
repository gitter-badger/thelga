import random

from helga.bot import bot


@bot.message_handler(commands=['jn'], content_types=['text'])
def yn_handler(message):
    bot.reply_to(message, random.choice(('Ja', 'Nein')))


@bot.message_handler(commands=['random'], content_types=['text'])
def rn_handler(message):
    bot.reply_to(message, "9")
