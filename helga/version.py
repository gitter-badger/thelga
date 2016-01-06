"""
    helga.version
    ~~~~~~~~~~~~~

    This module retries version information from git tags.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

from subprocess import check_output


command = 'git describe --tags --long --dirty'


def format_version(version, fmt):
    parts = version.split('-')
    assert len(parts) in (3, 4)
    dirty = len(parts) == 4
    tag, count, sha = parts[:3]
    if count == '0' and not dirty:
        return tag
    return fmt.format(tag=tag, commitcount=count, gitsha=sha.lstrip('g'))

try:
    version = check_output(command.split()).decode('utf-8').strip()
    version = format_version(version=version, fmt='{tag}.dev{commitcount}+{gitsha}')
    __version__ = version
except Exception:
    __version__ = 'unknown'
