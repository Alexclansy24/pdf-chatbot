from dataclasses import dataclass


@dataclass(slots=True)
class StorageFile:
    path: str
    filename: str
    size: int