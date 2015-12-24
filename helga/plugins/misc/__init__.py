import random

from helga.plugins import Plugin


class MiscPlugin(Plugin):

    def register(self):
        self.bot.register_command('yn', self.yn)
        self.bot.register_command('random', self.random)
        self.bot.register_command('test', self.test)
        self.bot.register_command('dice', self.dice)

    def yn(self, msg, *args):
        """ Prints 'yes' or 'no' """
        self.bot.send_reply(msg, random.choice(('Ja', 'Nein')))

    def random(self, msg, *args):
        """ Random number generator :smirk: """
        self.bot.send_reply(msg, "9")

    def test(self, msg, *args):
        self.bot.send_photo(msg.chat.id, photo=open('test.jpg', 'rb'))

    def dice(self, msg, *args):
        """rolls a dice, format <rolls>d<sides>"""
        if (len(args) == 0):
            args = ['1d6']
        try:
            rolls, maxint = args[0].split('d')
            rolls = int(rolls)
            maxint = int(maxint)
            results = []
            for roll in range(rolls):
                results.append(str(random.randint(1, maxint+1)))
            self.bot.send_reply(msg, ' '.join(results))
        except Exception as e:
            self.bot.send_reply(msg, 'Please use Format <numrolls>d<sides>')

