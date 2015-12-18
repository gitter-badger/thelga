import os

import telebot


if "TELEBOT_BOT_TOKEN" not in os.environ:
    raise AssertionError("Please configure TELEBOT_BOT_TOKEN as environment variable.")

bot = telebot.TeleBot(os.environ["TELEBOT_BOT_TOKEN"])


@bot.message_handler(commands=['start', 'help'])
def send_information(message):
    bot.send_message(message.chat.id, "Hi! I’m Helga! \U0001F61D\nGo ahead, check out my source and contribute. :3\n\n"
                                      "https://github.com/buckket/thelga")
