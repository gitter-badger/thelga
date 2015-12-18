from helga.bot import bot

from .database import init_db
from .handler import add_quote_handler, \
    get_random_quote_handler, get_quote_handler, \
    search_quote_handler, list_quotes_handler


add_quote_handler = bot.message_handler(commands=['addquote'])(add_quote_handler)
get_random_quote_handler = bot.message_handler(commands=['quote'])(get_random_quote_handler)
get_quote_handler = bot.message_handler(commands=['getquote'])(get_quote_handler)
search_quote_handler = bot.message_handler(commands=['searchquote'])(search_quote_handler)
list_quotes_handler = bot.message_handler(commands=['listquotes'])(list_quotes_handler)


def init():
    init_db()
