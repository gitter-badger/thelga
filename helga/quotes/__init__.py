from .database import init_db

from .handler import add_quote_handler, \
    get_random_quote_handler, get_quote_handler, \
    search_quote_handler, list_quotes_handler


def init():
    init_db()
