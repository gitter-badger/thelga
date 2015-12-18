import os
import re
import random

import telebot

import helga.quotes
import helga.helper


if "TELEBOT_BOT_TOKEN" not in os.environ:
    raise AssertionError("Please configure TELEBOT_BOT_TOKEN as environment variable.")
bot = telebot.TeleBot(os.environ["TELEBOT_BOT_TOKEN"])


@bot.message_handler(commands=['start', 'help'])
def send_information(message):
    bot.send_message(message.chat.id, "Hi! I’m Helga! \U0001F61D\nGo ahead, check out my source and contribute. :3\n\n"
                                      "https://github.com/buckket/thelga")


@bot.message_handler(commands=['addquote'], content_types=['text'])
def add_quote_handler(message):
    if hasattr(message, 'reply_to_message'):
        try:
            quote = helga.quotes.add_quote(message)
            bot.reply_to(message, "Quote #{} added successfully. \U0001F60B".format(quote.quote_id))
        except AttributeError:
            bot.reply_to(message, "Sorry, there has been an error. \U0001F622")
    else:
        bot.reply_to(message, "Sorry, don’t know what to add. \U0001F615")


@bot.message_handler(commands=['quote'], content_types=['text'])
def get_random_quote_handler(message):
    quote = helga.quotes.get_random_quote(message)
    try:
        bot.send_message(message.chat.id, helga.helper.format_quote(quote))
    except AttributeError:
        bot.send_message(message.chat.id, "Sorry, I don’t have any quotes for this chat yet. Go add some! \U0001F609")


@bot.message_handler(commands=['getquote'], content_types=['text'])
def get_quote_handler(message):
    match = re.match('/getquote(@\w+)?\s(\d+)', message.text)
    try:
        quote_id = match.group(2)
    except AttributeError:
        bot.reply_to(message, "Sorry, say that again, please. Use /getquote <quote_id>. \U0001F609")
        return

    quote = helga.quotes.get_quote(message, quote_id)
    try:
        bot.send_message(message.chat.id, helga.helper.format_quote(quote))
    except AttributeError:
        bot.reply_to(message, "Sorry, I don’t have a quote with that ID in my database. \U0001F61E")


@bot.message_handler(commands=['searchquote'], content_types=['text'])
def search_quote_handler(message):
    match = re.match('/searchquote(@\w+)?\s(.*)', message.text)
    try:
        search_string = match.group(2)
    except AttributeError:
        bot.reply_to(message, "Sorry, say that again, please. Use /searchquote <search_string>. \U0001F609")
        return

    quotes = helga.quotes.search_quote(message, search_string)
    if quotes:
        bot.send_message(message.chat.id, helga.helper.format_quotes(quotes))
    else:
        bot.reply_to(message, "Sorry, I don’t have any quotes containing that string. \U0001F61E")


@bot.message_handler(commands=['listquotes'], content_types=['text'])
def search_quote_handler(message):
    quotes = helga.quotes.list_quotes(message)
    if quotes:
        bot.send_message(message.chat.id, helga.helper.format_quotes_list(quotes))
    else:
        bot.reply_to(message, "Sorry, I don’t have any quotes for this chat. \U0001F61E")


@bot.message_handler(commands=['jn'], content_types=['text'])
def yn_handler(message):
    bot.reply_to(message, random.choice(('Ja', 'Nein')))


def main():
    helga.quotes.init_db()
    bot.polling()
