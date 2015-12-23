import sys
import importlib

from helga import config
from helga.version import __version__


class Plugin:

    def __init__(self, bot):
        self.bot = bot

    def register(self):
        pass


class PluginRepository:
    def __init__(self, bot):
        self._bot = bot

    def load_plugin(self, classname):

        # Initialize and run the task
        module, classname = classname.split(':')
        importlib.import_module(module)
        pluginclass = getattr(sys.modules[module], classname)
        plugin = pluginclass(self._bot)
        plugin.register()

    def load_all(self):
        for plugin in config.get('plugins'):
            self.load_plugin(plugin)


class HelpPlugin(Plugin):

    def register(self):
        self.bot.register_command('help', self.print_help)
        self.bot.register_command('start', self.print_help)
        self.bot.register_command('list', self.list_commands)
        self.bot.register_command('info', self.show_info)

    def print_help(self, msg, *args):
        """ Shows help and introduction """
        self.bot.make_reply(msg, "Hi! I’m Helga! \U0001F61D\nGo ahead, check out my source and contribute. :3\n"
                                 "https://github.com/buckket/thelga\n\n"
                                 "You can view my commands by typing /list\n\n"
                                 "My owner is: {owner}\n"
                                 "My version is: {version}"
                            .format(owner=config.get('bot')['owner'], version=__version__))

    def list_commands(self, msg, *args):
        """ Lists available commands """
        response = ''
        for command in self.bot.get_commands():
            docstring = self.bot.get_commands()[command][1].__doc__ or "No Docstring"
            response += "{prefix}{command}\t{docstring}\n".format(
                    prefix=self.bot._command_prefix,
                    command=command,
                    docstring=docstring)
        self.bot.make_reply(msg, response)

    def show_info(self, msg, *args):
        """ Shows installed version """
        self.bot.make_reply(msg, 'Hello, I’m Helga version {version}'.format(version=__version__))
