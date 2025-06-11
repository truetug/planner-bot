import asyncio
import aioschedule
from datetime import datetime
from aiogram import Bot
from ..database.session import async_session_factory
from ..services.reminders import due_reminders
from ..llm.client import ask
from ..logger import logger

async def reminder_job(bot: Bot) -> None:
    async with async_session_factory() as session:
        now = datetime.utcnow()
        reminders = await due_reminders(session, now)
        for reminder in reminders:
            try:
                text = await ask(f"Напомни: {reminder.description}")
                await bot.send_message(reminder.project.user_id, text)
            except Exception as e:
                logger.exception("Failed to send reminder: %s", e)

async def scheduler_loop(bot: Bot, interval: int) -> None:
    aioschedule.every(interval).seconds.do(reminder_job, bot)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
