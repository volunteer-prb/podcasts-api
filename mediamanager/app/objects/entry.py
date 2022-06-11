from dataclasses import dataclass
from typing import List


@dataclass
class Files:
    uri: str


@dataclass
class AudioFile(Files):
    duration: int


@dataclass
class ImageFile(Files):
    pass


@dataclass
class Channel:
    id: str
    title: str
    url: str


@dataclass
class Entry:
    id: str
    title: str
    description: str
    url: str
    tags: List[str]
    channel: Channel
    audio: AudioFile
    image: ImageFile
