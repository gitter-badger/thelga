import os

import telebot
import helga.config

bot = telebot.TeleBot(helga.config.api_token)


@bot.message_handler(commands=['start', 'help'])
def send_information(message):
    bot.send_message(message.chat.id, "Hi! I’m Helga! \U0001F61D\nGo ahead, check out my source and contribute. :3\n\n"
                                      "https://github.com/buckket/thelga")
