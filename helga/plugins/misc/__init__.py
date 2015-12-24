import random

from helga.plugins import Plugin


class MiscPlugin(Plugin):

    def register(self):
        self.bot.register_command('yn', self.yn)
        self.bot.register_command('random', self.random)
        self.bot.register_command('test', self.test)

    def yn(self, msg, *args):
        """ Prints 'yes' or 'no' """
        self.bot.send_reply(msg, random.choice(('Ja', 'Nein')))

    def random(self, msg, *args):
        """ Random number generator :smirk: """
        self.bot.send_reply(msg, "9")

    def test(self, msg, *args):
        self.bot.send_photo(msg.chat.id, photo=open('test.jpg', 'rb'))
