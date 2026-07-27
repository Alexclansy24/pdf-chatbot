from core.config import settings

from storage.local import (
    LocalStorageProvider,
)


def get_storage():
    if (
        settings.STORAGE_PROVIDER
        == "local"
    ):
        return LocalStorageProvider(
            settings.UPLOAD_DIR
        )

    raise ValueError(
        "Invalid storage provider"
    )