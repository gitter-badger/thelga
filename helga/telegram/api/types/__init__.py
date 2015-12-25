class reference:
    def __init__(self, ref):
        self._ref = ref


class StructureMeta(type):

    def __init__(cls, name, bases, nmspc):
        super(StructureMeta, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = dict()
        cls.registry[cls.__name__] = cls


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


class Structure(metaclass=StructureMeta):

    def __new__(cls, *args, **kwargs):
        new_cls = super().__new__(cls)
        for k, v in cls.__dict__.items():
            val = kwargs.get(k)
            if k.endswith('_'):
                val = kwargs.get(k[:-1])

            if isinstance(v, StructureMeta):
                if val:
                    setattr(new_cls, k, v(**val))
                else:
                    setattr(new_cls, k, None)
            elif isinstance(v, Type):
                setattr(new_cls, k, v.parse_value(val))
        return new_cls

    def get_value(self):
        data = {}
        for k, v in self.__class__.__dict__.items():
            if isinstance(v, StructureMeta):
                data[k] = v.get_value()
            elif isinstance(v, Type):
                data[k] = v.get_value(getattr(self, k))

    @classmethod
    def finalize(cls):
        for name, klass in cls.registry.items():
            for (k, v) in klass.__dict__.items():
                if isinstance(v, reference):
                    setattr(klass, k, cls.registry[v._ref])


class String(Type):
    pass


class Integer(Type):
    pass


class Float(Type):
    pass


class Boolean(Type):
    pass


class InputFile(Type):
    __target__ = 'data'


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
    date = Integer()
    chat = reference("Chat")
    reply_to_message = reference("Message")
    forward_from = reference("User")
    forward_date = Integer()
    text = String()
    #audio = reference("Audio")


class Update(Structure):
    update_id = Integer()
    message = reference("Message")
