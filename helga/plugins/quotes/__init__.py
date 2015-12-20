import re

from helga.plugins import Plugin

from .helper import format_quote, format_quotes, format_quotes_list
from .database import add_quote, get_random_quote, get_quote, search_quote, list_quotes, init_db

class QuotePlugin(Plugin):

    def register(self):
        init_db()
        self.bot.register_command('addquote', self.add_quote_handler)
        self.bot.register_command('quote', self.get_random_quote_handler)
        self.bot.register_command('getquote', self.get_quote_handler)
        self.bot.register_command('searchquote', self.search_quote_handler)
        self.bot.register_command('listquotes', self.list_quotes_handler)

    def add_quote_handler(self, message, *args):
        if hasattr(message, 'reply_to_message'):
            try:
                quote = add_quote(message)
                self.bot.make_reply(message, "Quote #{} added successfully. \U0001F60B".format(quote.quote_id))
            except AttributeError as e:
                self.bot.make_reply(message, "Sorry, there has been an error. \U0001F622")
                print(e)
        else:
            self.bot.make_reply(message, "Sorry, don’t know what to add. \U0001F615")


    def get_random_quote_handler(self, message, *args):
        quote = get_random_quote(message)
        try:
            self.bot.make_reply(message, format_quote(quote))
        except AttributeError:
            self.bot.make_reply(message, "Sorry, I don’t have any quotes for this chat yet. Go add some! \U0001F609")


    def get_quote_handler(self, message, *args):
        match = re.match('/getquote(@\w+)?\s(\d+)', message.text)
        try:
            quote_id = match.group(2)
        except AttributeError:
            self.bot.make_reply(message, "Sorry, say that again, please. Use /getquote <quote_id>. \U0001F609")
            return

        quote = get_quote(message, quote_id)
        try:
            self.bot.make_reply(message, format_quote(quote))
        except AttributeError:
            self.bot.make_reply(message, "Sorry, I don’t have a quote with that ID in my database. \U0001F61E")


    def search_quote_handler(self, message, *args):
        match = re.match('/searchquote(@\w+)?\s(.*)', message.text)
        try:
            search_string = match.group(2)
        except AttributeError:
            self.bot.make_reply(message, "Sorry, say that again, please. Use /searchquote <search_string>. \U0001F609")
            return

        quotes = search_quote(message, search_string)
        if quotes:
            self.bot.make_reply(message, format_quotes(quotes))
        else:
            self.bot.make_reply(message, "Sorry, I don’t have any quotes containing that string. \U0001F61E")


    def list_quotes_handler(self, message, *args):
        quotes = list_quotes(message)
        if quotes:
            self.bot.make_reply(message, format_quotes_list(quotes))
        else:
            self.bot.make_reply(message, "Sorry, I don’t have any quotes for this chat. \U0001F61E")
