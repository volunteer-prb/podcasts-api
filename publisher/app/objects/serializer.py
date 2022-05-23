import dataclasses
import datetime
import json

from app.objects.Envelope import Envelope, EnvelopeBody
from app.objects.Recipient import Recipient, TelegramRecipient

__dataclasses__ = [Envelope, EnvelopeBody, Recipient, TelegramRecipient]


class DataclassEncoder(json.JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return self._dataclass_encoder(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return {'_type_': '__datetime__', 'value': obj.isoformat()}
        if isinstance(obj, (str, int, float, dict, list, tuple, bool)):
            return obj

        return json.JSONEncoder.default(self, obj)

    def _dataclass_encoder(self, obj):
        d = dict([
            (f.name, self.default(getattr(obj, f.name))) for f in dataclasses.fields(obj)
        ])
        d['_type_'] = type(obj).__name__
        return d


def dataclass_decoder(obj):
    if isinstance(obj, dict) and '_type_' in obj:
        if obj['_type_'] == '__datetime__':
            return datetime.datetime.fromisoformat(obj['value'])
        for cls in __dataclasses__:
            if cls.__name__ == obj['_type_']:
                del obj['_type_']
                return cls(**obj)

    return obj


def dumps(obj):
    return json.dumps(obj, cls=DataclassEncoder)


def loads(obj):
    return json.loads(obj, object_hook=dataclass_decoder)
