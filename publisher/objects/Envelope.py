from dataclasses import dataclass
from typing import List

from publisher.objects.Recipient import Recipient


@dataclass
class Envelope:
    title: str  # title for photo and audio
    description: str  # text description (under photo)
    hashtags: List[str]  # separated hashtag for message and audio
    publisher: str  # publisher name for audio
    thumb: str  # path to preview photo file
    audio: str  # path to audio file
    recipients: List[Recipient]  # list of recipients
