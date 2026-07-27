from sqlalchemy.ext.asyncio import AsyncSession

from database.models.agent_run import AgentRun
from repositories.base import BaseRepository


class AgentRunRepository(
    BaseRepository[AgentRun]
):
    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            AgentRun,
            db,
        )