import datetime


def format_timestamp(time):
    """
    Return a human-readable timestamp.
    :param time: UNIX timestamp as int.
    :return: Formatted time string as str.
    """
    return datetime.datetime.fromtimestamp(time).strftime('%d.%m.%Y %H:%M')


def format_quote(quote):
    """
    Return a humand-readable string representation of a Quote object.
    :param quote: helga.quotes.Quote
    :return: str
    """
    return "Quote #{quote_id}: „<{author}> {text}“ (added by {added_by} at {date})".format(
            quote_id=quote.quote_id,
            author=quote.author.first_name,
            text=quote.text,
            added_by=quote.added_by.first_name,
            date=format_timestamp(quote.date))
