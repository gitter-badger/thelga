"""
    (t)helga
    ~~~~~~~~

    A Telegram bot in Python 3.

    :copyright: (c) 2015 by buckket.
    :license: MIT, see LICENSE for more details.
"""
import asyncio

from helga.config import config
from helga.telegram.api import API_URL
from helga.telegram.api.commands import GetMe, GetUpdates
from helga.version import __version__

import aiohttp


class Helga:

    def __init__(self, loop=None):
        """
        :param loop: BaseEventLoop
        """
        self._loop = loop
        self._last_update_id = None
        asyncio.ensure_future(self._init())

    @asyncio.coroutine
    def _init(self):
        try:
            cmd = GetMe()
            yield from self._execute_command(cmd)
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
                print(update)
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

        r = yield from action(API_URL.format(token=config.get('bot')['token'],
                                             method=command.command), params=command.get_params())

        resp = yield from r.json()
        if not resp['ok']:
            raise Exception('Error while processing Request')
        return command.parse_result(resp['result'])



