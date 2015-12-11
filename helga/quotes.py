from peewee import *


db = SqliteDatabase('helga_quotes.db')


class QuoteModel(Model):
    class Meta:
        database = db


class Chat(QuoteModel):
    id = IntegerField(primary_key=True)
    type = TextField()

    # optional arguments
    title = TextField(null=True)
    username = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)

    # each chat has it’s own id counter, easier for humans!
    current_quote_id = IntegerField(default=0)


class User(QuoteModel):
    id = IntegerField(primary_key=True)
    first_name = TextField()

    # optional arguments
    username = TextField(null=True)
    last_name = TextField(null=True)


class Quote(QuoteModel):
    # not unique, but unique per chat
    quote_id = IntegerField()

    chat = ForeignKeyField(Chat, related_name='quotes')
    author = ForeignKeyField(User, related_name='quotes')
    added_by = ForeignKeyField(User, related_name='added')

    date = IntegerField()
    text = TextField()


def _get_db_user(user, update=True):
    """
    Return a User object from database or create it, in case it doesnt exist.
    :param user: telebot.types.User
    :param update: Update data according to newest metadata received with the message.
    :return: helga.quotes.User
    """
    db_user, created = User.get_or_create(id=user.id, defaults={'first_name': user.first_name})

    if update:
        db_user.first_name = user.first_name
        db_user.username = user.username
        db_user.last_name = user.last_name
        db_user.save()

    return db_user


def _get_db_chat(chat, update=True):
    """
    Return a Chat object from database or create it, in case it doesnt exist.
    :param chat: telebot.types.Chat
    :param update: Update data according to newest metadata received with the message.
    :return: helga.quotes.Chat
    """
    db_chat, created = Chat.get_or_create(id=chat.id, defaults={'type': chat.type})

    if update:
        db_chat.type = chat.type
        db_chat.title = chat.title
        db_chat.username = chat.username
        db_chat.first_name = chat.first_name
        db_chat.last_name = chat.last_name
        db_chat.save()

    return db_chat


def add_quote(message):
    """
    Add quote to database, return Quote object.
    :param message: telebot.types.Message
    :return: helga.quotes.Quote
    """
    db.connect()

    chat = _get_db_chat(message.chat)
    author = _get_db_user(message.reply_to_message.from_user)
    added_by = _get_db_user(message.from_user)

    quote = Quote.create(quote_id=chat.current_quote_id,
                         chat=chat,
                         author=author,
                         added_by=added_by,
                         date=message.date,
                         text=message.reply_to_message.text)

    chat.current_quote_id += 1
    chat.save()

    db.close()
    return quote


def get_random_quote(message):
    """
    Return random quote for the chat in which message was sent.
    :param message: telebot.types.Message
    :return: helga.quotes.Quote
    """
    db.connect()

    chat = _get_db_chat(message.chat)
    try:
        quote = Quote.select().where(Quote.chat == chat).order_by(fn.Random()).get()
    except DoesNotExist:
        quote = None

    db.close()
    return quote


def get_quote(message, quote_id):
    """
    Return a specific quote by id for the chat in which message was sent.
    :param message: telebot.types.Message
    :param quote_id: Unique ID of quote in chat as int.
    :return: helga.quotes.Quote
    """
    db.connect()

    chat = _get_db_chat(message.chat)
    try:
        quote = Quote.select().where((Quote.chat == chat) & (Quote.quote_id == quote_id)).get()
    except DoesNotExist:
        quote = None

    db.close()
    return quote


def init_db():
    """
    Initialize database, create tables if necessary.
    """
    db.connect()
    db.create_tables([Chat, User, Quote], True)
    db.close()
