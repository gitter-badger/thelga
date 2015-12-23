import random

from helga.plugins import Plugin


class MiscPlugin(Plugin):

    def register(self):
        self.bot.register_command('yn', self.yn)
        self.bot.register_command('random', self.random)

    def yn(self, msg, *args):
        """ Prints 'yes' or 'no' """
        self.bot.make_reply(msg, random.choice(('Ja', 'Nein')))

    def random(self, msg, *args):
        """ Random number generator :smirk: """
        self.bot.make_reply(msg, "9")
