from pathlib import Path

from storage.base import StorageProvider


class LocalStorageProvider(StorageProvider):

    def __init__(
        self,
        upload_dir: str,
    ):
        self.upload_dir = Path(upload_dir)

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def upload(
        self,
        file_bytes: bytes,
        path: str,
    ) -> str:
        destination = self.upload_dir / path

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(
            file_bytes
        )

        return str(destination)

    async def delete(
        self,
        path: str,
    ) -> None:
        file_path = self.upload_dir / path

        if file_path.exists():
            file_path.unlink()

    async def exists(
        self,
        path: str,
    ) -> bool:
        return (
            self.upload_dir / path
        ).exists()