import asyncio

from services.graph.service import GraphService


async def main():

    service = GraphService()

    async for event in service.stream_answer(
        question="what are the skills?",
        conversation_id=None,
        document_id="294a9221-70c9-48f0-8b97-ec360b20720a",
    ):
        print("\nEVENT:")
        print(event)


if __name__ == "__main__":
    asyncio.run(main())