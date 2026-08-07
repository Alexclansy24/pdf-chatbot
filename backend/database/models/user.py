from sqlalchemy import String

from database.base import Base
from database.models.base_model import UUIDMixin
from database.models.mixins import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


class User(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
    String(255),
    nullable=False,
)

    conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan",
    )