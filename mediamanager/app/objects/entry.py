from dataclasses import dataclass


@dataclass
class Files:
    uri: str


@dataclass
class AudioFile(Files):
    pass


@dataclass
class ImageFile(Files):
    pass


@dataclass
class Entry:
    id: str
    author: str
    title: str
    description: str
    url: str
    audio: AudioFile
    image: ImageFile
