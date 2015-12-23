import signal
import asyncio
import functools

from helga import Helga
from helga.config import load_config


def main():
    load_config()

    loop = asyncio.get_event_loop()
    helga = Helga(loop=loop)

    def ask_exit(signal_name):
        print("Got signal {}: exiting…".format(signal_name))
        helga.shutdown()

    for signal_name in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signal_name), functools.partial(ask_exit, signal_name))

    # TODO: Add signal handler for SIGHUP (reload config)

    try:
        loop.run_forever()
    finally:
        loop.close()
