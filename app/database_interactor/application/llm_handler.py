from app.shared.infrastructure.settings import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

settings = get_settings()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    google_api_key=settings.google_api_key,
)


def process_with_gemini(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content
