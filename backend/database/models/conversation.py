from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.models.base_model import UUIDMixin
from database.models.mixins import TimestampMixin
from sqlalchemy.orm import relationship

class Conversation(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "conversations"

    user_id: Mapped[UUID] = mapped_column(
    ForeignKey("users.id", ondelete="CASCADE"),
    index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    user = relationship(
    "User",
    back_populates="conversations",
    )

    messages = relationship(
    "Message",
    back_populates="conversation",
    cascade="all, delete-orphan",
    )