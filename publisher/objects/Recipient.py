from dataclasses import dataclass


@dataclass
class Recipient:
    """Base Recipient class, describe media to publish audio entry"""
    pass


@dataclass
class TelegramRecipient(Recipient):
    channel_id: int  # channel id (must be negative)
