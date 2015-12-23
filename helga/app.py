import asyncio
import functools

import signal

from helga import Helga
from helga.config import load_config


def main():
    load_config()
    loop = asyncio.get_event_loop()
    helga = Helga(loop=loop)

    def ask_exit(signame):
        print("got signal %s: exit" % signame)
        helga.shutdown()

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), functools.partial(ask_exit, signame))
    try:
        loop.run_forever()
    finally:
        loop.close()
