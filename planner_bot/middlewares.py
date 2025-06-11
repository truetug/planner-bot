from typing import Any, Callable, Awaitable, Dict
from uuid import uuid4
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from .logger import request_id

class RequestIdMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        request_id.set(uuid4().hex)
        return await handler(event, data)
