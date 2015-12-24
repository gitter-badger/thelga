from helga.telegram.api.types import Type, InputFile, String, Boolean, Integer, Update, Structure


class TelegramCommand(Structure):
    __command__ = None
    __method__ = 'get'

    def get_params(self):
        return {k: v.get_value(getattr(self, k)) for k, v in self.__class__.__dict__.items() if isinstance(v, Type)}

    def get_data(self):
        return {k: v.get_value(getattr(self, k)) for k, v in self.__class__.__dict__.items() if isinstance(v, InputFile)}

    def parse_result(self, result):
        return result

    @property
    def method(self):
        return self.__method__

    @property
    def command(self):
        return self.__command__


class GetMe(TelegramCommand):
    __command__ = 'getMe'


class SendMessage(TelegramCommand):
    __command__ = 'sendMessage'
    __method__ = 'post'

    chat_id = String()
    text = String()
    parse_mode = String()
    disable_web_page_preview = Boolean()
    reply_to_message_id = Integer()


class ForwardMessage(TelegramCommand):
    __command__ = 'forwardMessage'
    __method__ = 'post'

    chat_id = String()
    from_chat_id = String()
    message_id = Integer()


class SendPhoto(TelegramCommand):
    __command__ = 'sendPhoto'
    __method__ = 'post'

    chat_id = String()
    photo = InputFile()


class GetUpdates(TelegramCommand):
    __command__ = 'getUpdates'
    __method__ = 'get'
    timeout = Integer()
    limit = Integer()
    offset = Integer()

    def parse_result(self, result):
        updates = []
        for item in result:
            update = Update(**item)
            updates.append(update)
        return updates


