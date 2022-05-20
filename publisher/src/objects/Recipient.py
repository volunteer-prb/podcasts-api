from dataclasses import dataclass


@dataclass
class Recipient:
    """Base Recipient class, describe media to publish audio entry"""
    _type_ = 'base'

    @classmethod
    def from_json(cls, json):
        assert '_type_' in json
        _type_ = json['_type_']
        json = dict({k: v for k, v in json.items() if k != '_type_'})
        if _type_ == 'telegram':
            return TelegramRecipient.from_json(json)


@dataclass
class TelegramRecipient(Recipient):
    _type_ = 'telegram'
    channel_id: int  # channel id (must be negative)

    @classmethod
    def from_json(cls, json):
        return cls(**json)
