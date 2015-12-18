from helga.bot import bot

from helga.misc.handler import yn_handler, rn_handler


yn_handler = bot.message_handler(commands=['jn', 'janein', 'yn', 'yesno'])(yn_handler)
rn_handler = bot.message_handler(commands=['random'])(rn_handler)


def init():
    pass
