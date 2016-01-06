import os
import random
import asyncio
import logging

from io import BytesIO

from helga import config
from helga.plugins import Plugin


logger = logging.getLogger('plugins.evil')


class PictureGrabber(Plugin):
    """A demo plugin to show how to abuse a bot."""

    def register(self):
        if not os.path.exists(os.path.join(config.workdir, 'picturedump')):
            os.makedirs(os.path.join(config.workdir, 'picturedump'))
        self.bot.register_message_handler(self.dump_picture)
        self.bot.register_command('random_pic', self.post_random)
        self.bot.register_command('stolen_pics', self.stats)

    @asyncio.coroutine
    def dump_picture(self, msg):
        """Dump every picture the bot get’s to see"""
        if msg.photo:
            photo = msg.photo.photos[-1]
            data = yield from photo.download(self.bot)
            filename = photo.file_path.split('/')[-1]
            with open(os.path.join(config.workdir, 'picturedump', filename), 'wb') as fh:
                fh.write(data)

    def post_random(self, msg, *args):
        """Posts a random picture. Where they are from?! Who knows… :3"""
        rand_filename = random.choice(os.listdir(os.path.join(config.workdir, 'picturedump')))
        with open(os.path.join(config.workdir, 'picturedump', rand_filename), 'rb') as fh:
            data = BytesIO(fh.read())
            # rather stupid hack below to convince aiohttp to set the right content mimetype
            data.name = rand_filename
            self.bot.send_photo(msg.chat.id, photo=data)

    def stats(self, msg, *args):
        """Shows stats about picturedump"""
        self.bot.send_message(msg.chat.id, str(len(os.listdir(os.path.join(config.workdir, 'picturedump')))))
