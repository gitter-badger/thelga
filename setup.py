import os
from os.path import dirname, abspath

# don't try this at home kids

import distutils.command
from distutils.command.sdist import sdist as _sdist

class sdist(_sdist):
    """stuff"""
    def make_release_tree(self, base_dir, files):
        _sdist.make_release_tree(self, base_dir, files)
        print('removing version.py to replace with our own.')
        os.unlink(os.path.join(base_dir, 'helga', 'version.py'))
        print('writing our own version.py with version number "{version}".'.format(version=self.distribution.get_version()))
        with open(os.path.join(base_dir, 'helga', 'version.py'), 'w') as vh:
            vh.write('__version__ = "{version}"\n'.format(version=self.distribution.get_version()))

# overwriting standard sdist command
distutils.command.sdist.sdist = sdist

def get_version():
    with open(os.path.join(dirname(abspath(__file__)), 'helga', 'version.py')) as f:
        local_dict = {}
        exec(f.read(), globals(), local_dict)
        return local_dict['__version__']


__version__ = get_version()


from setuptools import setup

setup(
    name='helga',
    version=__version__,
    long_description=__doc__,
    packages=['helga'],
    install_requires=['pyTelegramBotAPI',
                      'peewee',
                      'pyaml'
                      ],
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['helga=helga.app:main']
    }

)
