from abc import ABC
from abc import abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    async def upload(
        self,
        file_bytes: bytes,
        path: str,
    ) -> str:
        pass

    @abstractmethod
    async def delete(
        self,
        path: str,
    ) -> None:
        pass

    @abstractmethod
    async def exists(
        self,
        path: str,
    ) -> bool:
        pass