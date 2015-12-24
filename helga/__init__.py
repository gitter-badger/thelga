"""
    (t)helga
    ~~~~~~~~

    A Telegram bot in Python 3.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

import asyncio

import aiohttp

from helga.config import config
from helga.plugins import HelpPlugin, PluginRepository
from helga.plugins.quotes import QuotePlugin
from helga.telegram.api import API_URL
from helga.telegram.api.commands import GetMe, GetUpdates, SendMessage, ForwardMessage, SendPhoto
from helga.version import __version__


class Helga:

    def __init__(self, loop=None):
        """
        :param loop: BaseEventLoop
        """
        self._loop = loop
        self._last_update_id = None
        self._command_handlers = {}
        self._message_handlers = []
        self._command_prefix = '/'
        asyncio.ensure_future(self._init())
        self._plugin_repository = PluginRepository(self)
        self._plugin_repository.load_all()
        self.myself = None

    @asyncio.coroutine
    def _init(self):
        try:
            cmd = GetMe()
            self.myself = yield from self._execute_command(cmd)
            asyncio.ensure_future(self._poll_updates())
        except Exception as exc:
            self.shutdown(exc=exc)

    @asyncio.coroutine
    def _poll_updates(self):
        try:
            cmd = GetUpdates(timeout=10, offset=self._last_update_id)
            updates = yield from self._execute_command(cmd)
            for update in updates:
                self._last_update_id = update.update_id + 1
                self._loop.call_soon(self._handle_update, update)
        finally:
            asyncio.ensure_future(self._poll_updates())

    def shutdown(self, exc=None):
        if exc:
            print('Exception'+str(exc))
        self._loop.stop()

    @asyncio.coroutine
    def _execute_command(self, command):
        action = {'get': aiohttp.get,
                  'post': aiohttp.post}.get(command.method)

        r = yield from action(API_URL.format(token=config.get('bot')['token'], method=command.command),
                              params=command.get_params(),
                              data=command.get_data())

        resp = yield from r.json()
        if not resp['ok']:
            raise Exception('Error while processing Request')
        return command.parse_result(resp['result'])

    def register_command(self, name, callback, chat_types=("private", "group", "supergroup", "channel")):
        # TODO: Allow name to be a list
        if name in self._command_handlers:
            print('possible duplicate command')
        self._command_handlers[name] = (chat_types, callback)

    def register_message_handler(self, callback):
        if callback not in self._message_handlers:
            self._message_handlers.append(callback)

    def get_commands(self):
        return self._command_handlers

    def _handle_update(self, update):
        if update.message.text:
            if update.message.text[0] == self._command_prefix:
                args = update.message.text[1:].split()
                if '@' in args[0]:
                    # command was directed at a specific bot, check if we are the recipient
                    command, username = args[0].split('@', 2)
                    if username == self.myself.username:
                        args[0] = command
                    else:
                        #no directed at me, goodbye
                        return
                if args[0] in self._command_handlers:
                    if update.message.chat.type not in self._command_handlers[args[0]][0]:
                        return
                    self._command_handlers[args[0]][1](update.message, args[1:])
            else:
                for handler in self._message_handlers:
                    handler(update.message)

    def send_message(self, chat_id, text, **kwargs):
        cmd = SendMessage(chat_id=chat_id, text=text, **kwargs)
        asyncio.ensure_future(self._execute_command(cmd))

    def send_reply(self, message, text, as_reply=False):
        reply_to_message_id = message.message_id if as_reply else None
        self.send_message(message.chat.id, text, reply_to_message_id=reply_to_message_id)

    def forward_message(self, chat_id, from_chat_id, message_id):
        cmd = ForwardMessage(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
        asyncio.ensure_future(self._execute_command(cmd))

    def send_photo(self, chat_id, photo):
        cmd = SendPhoto(chat_id=chat_id, photo=photo)
        asyncio.ensure_future(self._execute_command(cmd))
