import dataclasses
from dataclasses import dataclass
from typing import List, Optional

from app.objects.Recipient import Recipient


@dataclass
class EnvelopeBody:
    title: str  # title for photo and audio
    description: str  # text description (under photo)
    hashtags: List[str]  # separated hashtag for message and audio
    publisher: str  # publisher name for audio
    audio: str  # path or url to audio file
    photo: Optional[str] = None  # path or url to preview photo file


@dataclass
class Envelope:
    body: EnvelopeBody
    recipients: List[Recipient]
