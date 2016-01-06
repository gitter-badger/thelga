"""
    helga.config
    ~~~~~~~~~~~~

    This module reads and parses the bots configuration file and handles CLI arguments.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

import os
import argparse

import yaml


# TODO: .config is the place to go, see standard
DEFAULT_CONFIG = os.path.expanduser('~/.helga')


# TODO: More specific help texts
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-w', '--workdir', type=str, help='Working Directory for Helga {default} by default'.format(
        default=DEFAULT_CONFIG), default=DEFAULT_CONFIG)


class Config:
    workdir = DEFAULT_CONFIG

    def __init__(self):
        self._config = {}

    def load_config(self):
        args = parser.parse_args()
        self.workdir = os.path.expanduser(args.workdir)
        self.parse_yaml()

    def parse_yaml(self):
        with open(os.path.expanduser(os.path.join(self.workdir, 'config.yml'))) as ch:
            self._config = yaml.load(ch)

    def get(self, key):
        return self._config[key]


config = Config()


def load_config():
    config.load_config()
