# recreate_tables.py
import asyncio
from database.base import Base
from database.session import engine

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(main())