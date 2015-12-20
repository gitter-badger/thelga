import argparse
import yaml
import os

DEFAULT_CONFIG = '~/.helga'


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-w', '--workdir', type=str, help='Working Directory for Helga {default} by default'.format(default=DEFAULT_CONFIG), default=DEFAULT_CONFIG)

class Config:
    workdir = DEFAULT_CONFIG

    def __init__(self):
        self._config = {}

    def load_config(self):
        args = parser.parse_args()
        self.workdir = args.workdir
        self.parse_yaml()


    def parse_yaml(self):
        with open(os.path.expanduser(os.path.join(self.workdir, 'config.yml'))) as ch:
            self._config = yaml.load(ch)

    def get(self, key):
        return self._config[key]


config = Config()

def load_config():
    config.load_config()



