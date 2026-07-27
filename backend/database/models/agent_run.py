from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base
from database.models.base_model import UUIDMixin
from database.models.mixins import TimestampMixin
from sqlalchemy import Enum

from database.models.enums import AgentRunStatus
from datetime import datetime
from sqlalchemy import DateTime

class AgentRun(
    UUIDMixin,
    TimestampMixin,
    Base,
):
    __tablename__ = "agent_runs"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id"),
        index=True,
    )

    status: Mapped[AgentRunStatus] = mapped_column(
    Enum(AgentRunStatus),
    default=AgentRunStatus.RUNNING,
    )

    started_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )