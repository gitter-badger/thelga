import logging
import logging.handlers
import os

from helga import config


def init_logging():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    fh = logging.handlers.TimedRotatingFileHandler(os.path.join(config.workdir, 'helga.log'), when='midnight')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)


