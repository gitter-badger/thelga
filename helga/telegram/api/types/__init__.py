"""
    helga.telegram.types
    ~~~~~~~~~~~~~~~~~~~~

    This module defines the Telegram API types as classes.

    :copyright: (c) 2015 by buckket, teddydestodes.
    :license: MIT, see LICENSE for more details.
"""

import asyncio
import datetime


class Reference:
    """This class keeps a reference to another structure."""
    def __init__(self, ref):
        self.ref = ref


class Descriptor(object):
    def __init__(self, name, cls, default=None):
        self.name = name
        self.cls = cls
        self.default = default

    def __set__(self, instance, value):
        # convert the value to `cls` and write to instance dict
        if isinstance(self.cls, Type):
            instance.__dict__[self.name] = self.cls.parse_value(value)
        if isinstance(self.cls, Reference):
            if isinstance(value, dict):
                instance.__dict__[self.name] = instance.registry[self.cls.ref](**value)
            elif isinstance(value, (tuple, list)):
                instance.__dict__[self.name] = instance.registry[self.cls.ref](*value)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        # retrieve the value from instance dict
        return instance.__dict__.get(self.name, self.default)


class StructureMeta(type):
    def __init__(cls, name, bases, nmspc):
        super(StructureMeta, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = dict()
        cls.registry[cls.__name__] = cls

    def __new__(meta, name, bases, clsdict):
        for k, v in clsdict.copy().items():
            if isinstance(v, (Type, Reference)):
                clsdict[k] = Descriptor(k, v)
        return super(StructureMeta, meta).__new__(meta, name, bases, clsdict)

    def resolve_reference(cls, ref):
        return cls.registry[ref]


class Type:
    """Base class for every type returned by the Telegram API."""
    __target__ = 'params'

    def __init__(self, required=True):
        self._required = required

    @property
    def target(self):
        return self.__target__

    def parse_value(self, val):
        return val

    def get_value(self, val):
        return val


class Structure(object, metaclass=StructureMeta):
    """Base class for all structures returned by the Telegram API."""
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            try:
                ce = getattr(self.__class__, k)
            except AttributeError:
                # this is a stupid hack due to my laziness
                # if someone would implement a storage and/or look-up-table we wouldn't rely on the
                # classmembernames directly
                ce = getattr(self.__class__, k+'_')
                k += '_'

            if isinstance(ce, Descriptor):
                setattr(self, k, v)

    def get_value(self):
        """Returns this structure and all substructures as a dict to be fed into some json encoder.

        :return: dict
        """
        data = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, StructureMeta):
                data[k] = v.get_value()
            elif isinstance(v, Type):
                data[k] = v.get_value(getattr(self, k))


class String(Type):
    pass


class Integer(Type):
    pass


class Float(Type):
    pass


class Boolean(Type):
    pass


class Bytes(Type):
    pass


class Date(Type):
    def parse_value(self, val):
        return datetime.datetime.fromtimestamp(int(val))

    def get_value(self, val):
        if isinstance(val, int):
            return int(val)
        elif isinstance(val, datetime.datetime):
            return val.timestamp()


class InputFile(Type):
    """This type represents a file to be uploaded to Telegram."""
    __target__ = 'data'


class File(Structure):
    """File information struct returned by the Telegram API."""
    file_id = String()
    file_size = Integer()
    file_path = String()


class Resource(Structure):
    """Base class for resources posted in chat."""
    file_id = String()
    file_size = Integer()
    contents = Bytes()
    file_path = String()

    @asyncio.coroutine
    def download(self, bot):
        """Downloads this resource.

        Cached data will be returned if available.

        :param bot: helga.Helga
        :return: binary data
        """
        if self.contents is None:
            # if no data cached, download
            self.file_path, self.contents = yield from bot.download(self.file_id)
        return self.contents


class PhotoResource(Resource):
    width = Integer()
    height = Integer()


class PhotoSizes(Structure):
    """List of photo resources.

    This is actually a resource, but since Telegram provides
    multiple sizes for pictures we need to represent them somehow.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.photos = []
        for photo_args in args:
            self.photos.append(PhotoResource(**photo_args))


class AudioResource(Resource):
    duration = Integer()
    performer = String()
    title = String()
    mime_type = String()


class DocumentResource(Resource):
    thumb = Reference("PhotoResource")
    file_name = String()
    mime_type = String()


class StickerResource(PhotoResource):
    thumb = Reference("PhotoResource")


class VideoResource(Resource):
    width = Integer()
    height = Integer()
    duration = Integer()
    thumb = Reference("PhotoResource")
    mime_type = String()


class VoiceResource(Resource):
    duration = Integer()
    mime_type = String()


class Contact(Structure):
    phone_number = String()
    first_name = String()
    last_name = String()
    user_id = Integer()


class Location(Structure):
    longitude = Float()
    latitude = Float()


# TODO: Implement MUltiPhotoSizes
#class UserProfilePhotos(Structure):
    #total_count = Integer()
    #photos = Reference("MultiPhotoSizes")


class User(Structure):
    id = Integer()
    first_name = String()
    last_name = String()
    username = String()


class Chat(Structure):
    id = Integer()
    type = String()
    title = String()
    username = String()
    first_name = String()
    last_name = String()


class Message(Structure):
    message_id = Integer()
    from_ = Reference("User")
    date = Date()
    chat = Reference("Chat")
    forward_from = Reference("User")
    forward_date = Date()
    reply_to_message = Reference("Message")
    text = String()
    audio = Reference("AudioResource")
    document = Reference("DocumentResource")
    photo = Reference("PhotoSizes")
    sticker = Reference("StickerResource")
    video = Reference("VideoResource")
    voice = Reference("VoiceResource")
    caption = String()
    contact = Reference("Contact")
    location = Reference("Location")
    new_chat_participant = Reference("User")
    left_chat_participant = Reference("User")
    new_chat_title = String()
    new_chat_photo = Reference("PhotoSizes")
    delete_chat_photo = Boolean()
    group_chat_created = Boolean()
    supergroup_chat_created = Boolean()
    channel_chat_created = Boolean()
    migrate_to_chat_id = Integer()
    migrate_from_chat_id = Integer()


class Update(Structure):
    update_id = Integer()
    message = Reference("Message")
