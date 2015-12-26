import datetime


class reference:
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
        if isinstance(self.cls, reference):
            instance.__dict__[self.name] = instance.registry[self.cls.ref](**value)

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
            if isinstance(v, (Type, reference)):
                clsdict[k] = Descriptor(k, v)
        return super(StructureMeta, meta).__new__(meta, name, bases, clsdict)

    def resolve_reference(cls, ref):
        return cls.registry[ref]

class Type:
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

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            try:
                ce = getattr(self.__class__, k)
            except AttributeError:
                ce = getattr(self.__class__, k+'_')
                k = k+'_'

            if isinstance(ce, Descriptor):
                setattr(self, k, v)

    def get_value(self):
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


class Boolean(Type):
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
    __target__ = 'data'


class Ressource(Structure):
    file_id = String()

    def set_data(self, data):
        self._data = data

    def get_data(self):
        if hasattr(self, '_data'):
            return self._data
        else:
            self._download()

    def del_data(self):
        self._data = None
    data = property(get_data, set_data, del_data)

    def _download(self):
        print('downloading...' + self.file_id)
        pass


class VoiceRessource(Ressource):
    duration = Integer()
    file_size = Integer()
    mime_type = String()


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
    from_ = reference("User")
    date = Date()
    chat = reference("Chat")
    reply_to_message = reference("Message")
    forward_from = reference("User")
    forward_date = Integer()
    text = String()
    voice = reference("VoiceRessource")


class Update(Structure):
    update_id = Integer()
    message = reference("Message")
