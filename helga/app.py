"""
    helga.app
    ~~~~~~~~~

    This module implements the main event loop and signal handler.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

import logging
import signal
import asyncio
import functools

from helga import Helga
from helga.config import load_config
from helga.log import init_logging


def main():
    load_config()
    init_logging()

    loop = asyncio.get_event_loop()
    helga = Helga(loop=loop)

    def ask_exit(signal_name):
        logging.info("Got signal {}: exiting…".format(signal_name))
        helga.shutdown()

    for signal_name in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signal_name), functools.partial(ask_exit, signal_name))

    # TODO: Add signal handler for SIGHUP (reload config)

    try:
        loop.run_until_complete(helga.get_updates())
    finally:
        loop.close()
