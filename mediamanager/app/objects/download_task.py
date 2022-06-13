from dataclasses import dataclass


@dataclass
class DownloadTask:
    url: str
    channel_id: str
