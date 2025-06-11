from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from ..config import settings

llm = ChatOpenAI(
    base_url=settings.openai_api_url,
    api_key=settings.openai_api_key,
    model=settings.openai_model,
)

async def ask(prompt: str, history: list[tuple[str, str]] | None = None) -> str:
    messages = []
    if history:
        for human, ai in history:
            messages.append(HumanMessage(content=human))
            messages.append(SystemMessage(content=ai))
    messages.append(HumanMessage(content=prompt))
    result = await llm.apredict_messages(messages)
    return result.content
