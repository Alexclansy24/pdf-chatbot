from google import genai

from core.config import settings


client = genai.Client(
    api_key=settings.GOOGLE_API_KEY
)
async def stream_text(
    prompt: str,
):
    response = (
        client.models.generate_content_stream(
            model=
                "gemini-3.1-flash-lite",
            contents=prompt,
        )
    )

    for chunk in response:

        if chunk.text:

            yield chunk.text