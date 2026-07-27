from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.models.base_model import UUIDMixin
from database.models.mixins import TimestampMixin
from sqlalchemy import Enum

from database.models.enums import MessageRole
from sqlalchemy.orm import relationship

class Message(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "messages"

    conversation_id: Mapped[UUID] = mapped_column(
    ForeignKey(
        "conversations.id",
        ondelete="CASCADE",
    ),
    index=True,
    )

    role: Mapped[MessageRole] = mapped_column(
    Enum(MessageRole),
    nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    conversation = relationship(
    "Conversation",
    back_populates="messages",
    )