"""
    (t)helga
    ~~~~~~~~

    A Telegram bot in Python 3.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import logging

import aiohttp

from helga.config import config
from helga.plugins import HelpPlugin, PluginRepository
from helga.plugins.quotes import QuotePlugin
from helga.telegram.api import API_URL, FILE_URL
from helga.telegram.api.commands import GetMe, GetUpdates, SendMessage, ForwardMessage, SendPhoto, SendDocument, GetFile
from helga.version import __version__


logger = logging.getLogger('helga')


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
        self._plugin_repository = PluginRepository(self)
        self._plugin_repository.load_all()
        self.myself = None
        self._run = True

    @asyncio.coroutine
    def update_accountinformation(self):
        try:
            logger.info('Retrieving account information')
            cmd = GetMe()
            self.myself = yield from self._execute_command(cmd)
            logger.info('Successfully loaded account information.'
                        ' Username: {username}'.format(username=self.myself.username))
        except Exception as exc:
            logger.critical('Error retrieving account information')

    @asyncio.coroutine
    def get_updates(self):
        self._run = True
        yield from self.update_accountinformation()

        while self._run:
            try:
                cmd = GetUpdates(timeout=10, offset=self._last_update_id)
                updates = yield from self._execute_command(cmd)
                for update in updates:
                    self._last_update_id = update.update_id + 1
                    self._loop.call_soon(self._handle_update, update)
            except Exception as e:
                logger.exception(e)
                # just sleep a bit, we don't want to accidentially spam the server
                yield from asyncio.sleep(5)

    def shutdown(self):
        self._run = False

    @asyncio.coroutine
    def _execute_command(self, command, headers=None):
        action = {'get': aiohttp.get,
                  'post': aiohttp.post}.get(command.method)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Executing command {command} params={params} data={data}".format(command=command.command,
                                                                                          params=command.get_params(),
                                                                                          data=command.get_data()))
        r = yield from action(API_URL.format(token=config.get('bot')['token'], method=command.command),
                              params=command.get_params(),
                              data=command.get_data(),
                              headers=headers)

        resp = yield from r.json()
        if not resp['ok']:
            logger.debug(resp)
            raise Exception('Error while processing Request')
        return command.parse_result(resp['result'])

    def register_command(self, name, callback, chat_types=("private", "group", "supergroup", "channel")):
        # TODO: Allow name to be a list
        if name in self._command_handlers:
            logger.warning('Possible duplicate command "{command}"'.format(command=name))
        self._command_handlers[name] = (chat_types, callback)

    def register_message_handler(self, callback):
        if callback not in self._message_handlers:
            self._message_handlers.append(callback)

    def get_commands(self):
        return self._command_handlers

    def _handle_update(self, update):
        command = update.message.text or update.message.caption
        if command:
            if command[0] == self._command_prefix:
                args = command[1:].split()
                if '@' in args[0]:
                    # command was directed at a specific bot, check if we are the recipient
                    command, username = args[0].split('@', 2)
                    if username == self.myself.username:
                        args[0] = command
                    else:
                        # not directed at us, goodbye
                        return
                if args[0] in self._command_handlers:
                    if update.message.chat.type not in self._command_handlers[args[0]][0]:
                        return

                    if asyncio.iscoroutinefunction(self._command_handlers[args[0]][1]):
                        asyncio.ensure_future(self._command_handlers[args[0]][1](update.message, *args[1:0]))
                    else:
                        call_args = (self._command_handlers[args[0]][1], update.message) + tuple(args[1:0])
                        self._loop.call_soon(*call_args)

        for handler in self._message_handlers:
            if asyncio.iscoroutinefunction(handler):
                asyncio.ensure_future(handler(update.message))
            else:
                self._loop.call_soon(handler, update.message)

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

    def send_document(self, chat_id, document):
        cmd = SendDocument(chat_id=chat_id, document=document)
        asyncio.ensure_future(self._execute_command(cmd))

    @asyncio.coroutine
    def download(self, file_id):
        """Downloads a file and returns its data.

        :param file_id: Resource by file_id.
        :type file_id: int
        :return: Tuple containing file_path and actual binary data.
        :rtype: tuple
        """
        cmd = GetFile(file_id=file_id)
        file = yield from self._execute_command(cmd)
        logger.debug('Downloading file {path}'.format(path=file.file_path))
        r = yield from aiohttp.get(FILE_URL.format(token=config.get('bot')['token'],
                                                   path=file.file_path))

        data = yield from r.read()
        return file.file_path, data
