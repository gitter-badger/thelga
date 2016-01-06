import datetime
import textwrap

from functools import partial


def format_timestamp(time):
    """Returns a human-readable timestamp.

    :param time: UNIX timestamp as int.
    :return: Formatted time string as str.
    """
    return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M')


def format_quote(quote, short=False):
    """Returns a human-readable string representation of a Quote object.

    :param quote: helga.plugins.quotes.Quote
    :param short: bool
    :return: str
    """
    if short:
            return "#{quote_id}: „<{author}> {text}“".format(
                    quote_id=quote.quote_id,
                    author=quote.author.first_name,
                    text=textwrap.shorten(quote.text, 50))
    else:
            return "Quote #{quote_id}: „<{author}> {text}“ (added by {added_by} at {date})".format(
                    quote_id=quote.quote_id,
                    author=quote.author.first_name,
                    text=quote.text.replace('\n', ' '),
                    added_by=quote.added_by.first_name,
                    date=format_timestamp(quote.date))


def format_quotes(quotes):
    """Returns a human-readable string representation of multiple Quote objects.

    :param quotes: iterable of helga.plugins.quotes.Quote
    :return: str
    """
    format_quote_short = partial(format_quote, short=True)
    return ', '.join(map(format_quote_short, quotes))


def format_quotes_list(quotes):
    """Returns a human-readable list representation of multiple Quote objects, one line for each.

    :param quotes: iterable of helga.plugins.quotes.Quote
    :return: str
    """
    return '\n'.join(map(format_quote, quotes))
