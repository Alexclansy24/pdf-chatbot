from database.models.enums import DocumentStatus
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database.base import Base
from database.models.base_model import UUIDMixin
from database.models.mixins import TimestampMixin


class Document(UUIDMixin, TimestampMixin, Base):

    __tablename__ = "documents"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        nullable=False,
        default=DocumentStatus.UPLOADED,
    )

    page_count: Mapped[int]

    chunk_count: Mapped[int]