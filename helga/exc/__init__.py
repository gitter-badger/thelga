"""
    helga.exc
    ~~~~~~~~~

    This module defines custom exceptions used throughout helga.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""


class MalformedResponseError(Exception):
    pass


class RequestError(Exception):
    pass
