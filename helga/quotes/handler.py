import re

from helga.bot import bot

from .helper import format_quote, format_quotes, format_quotes_list
from .database import add_quote, get_random_quote, get_quote, search_quote, list_quotes


def add_quote_handler(message):
    if hasattr(message, 'reply_to_message'):
        try:
            quote = add_quote(message)
            bot.reply_to(message, "Quote #{} added successfully. \U0001F60B".format(quote.quote_id))
        except AttributeError:
            bot.reply_to(message, "Sorry, there has been an error. \U0001F622")
    else:
        bot.reply_to(message, "Sorry, don’t know what to add. \U0001F615")


def get_random_quote_handler(message):
    quote = get_random_quote(message)
    try:
        bot.send_message(message.chat.id, format_quote(quote))
    except AttributeError:
        bot.send_message(message.chat.id, "Sorry, I don’t have any quotes for this chat yet. Go add some! \U0001F609")


def get_quote_handler(message):
    match = re.match('/getquote(@\w+)?\s(\d+)', message.text)
    try:
        quote_id = match.group(2)
    except AttributeError:
        bot.reply_to(message, "Sorry, say that again, please. Use /getquote <quote_id>. \U0001F609")
        return

    quote = get_quote(message, quote_id)
    try:
        bot.send_message(message.chat.id, format_quote(quote))
    except AttributeError:
        bot.reply_to(message, "Sorry, I don’t have a quote with that ID in my database. \U0001F61E")


def search_quote_handler(message):
    match = re.match('/searchquote(@\w+)?\s(.*)', message.text)
    try:
        search_string = match.group(2)
    except AttributeError:
        bot.reply_to(message, "Sorry, say that again, please. Use /searchquote <search_string>. \U0001F609")
        return

    quotes = search_quote(message, search_string)
    if quotes:
        bot.send_message(message.chat.id, format_quotes(quotes))
    else:
        bot.reply_to(message, "Sorry, I don’t have any quotes containing that string. \U0001F61E")


def list_quotes_handler(message):
    quotes = list_quotes(message)
    if quotes:
        bot.send_message(message.chat.id, format_quotes_list(quotes))
    else:
        bot.reply_to(message, "Sorry, I don’t have any quotes for this chat. \U0001F61E")
