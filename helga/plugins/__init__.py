class PluginRepository:
    def __init__(self):
        pass

    def load_plugin(self, classname, options):
        pass


class Plugin:

    def __init__(self, bot):
        self.bot = bot

    def register(self):
        pass

class HelpPlugin(Plugin):

    def register(self):
        self.bot.register_command('help', self.print_help, ('private',))
        self.bot.register_command('list', self.list_commands, ('private',))

    def print_help(self, msg, *args):
        """ Just a dummy function """
        self.bot.make_reply(msg, 'help is here')

    def list_commands(self, msg, *args):
        """ Lists available commands """
        response = ''
        for command in self.bot.get_commands():
            response += self.bot._command_prefix+command + '\t' + (self.bot.get_commands()[command][1].__doc__ or 'No Docstring') + '\n'
        self.bot.make_reply(msg, response)
