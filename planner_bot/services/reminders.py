from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..database.models import Reminder
from ..database.schemas import ReminderSchema

async def create_reminder(session: AsyncSession, project_id: int, description: str, remind_at: datetime, cron: str | None = None) -> ReminderSchema:
    reminder = Reminder(project_id=project_id, description=description, remind_at=remind_at, cron=cron)
    session.add(reminder)
    await session.commit()
    await session.refresh(reminder)
    return ReminderSchema.model_validate(reminder)

async def list_reminders(session: AsyncSession, project_id: int) -> list[ReminderSchema]:
    result = await session.execute(select(Reminder).where(Reminder.project_id == project_id))
    reminders = result.scalars().all()
    return [ReminderSchema.model_validate(r) for r in reminders]

async def delete_reminder(session: AsyncSession, reminder_id: int) -> None:
    await session.execute(delete(Reminder).where(Reminder.id == reminder_id))
    await session.commit()

async def due_reminders(session: AsyncSession, now: datetime) -> list[ReminderSchema]:
    stmt = select(Reminder).where(Reminder.remind_at <= now).options(selectinload(Reminder.project))
    result = await session.execute(stmt)
    reminders = result.scalars().all()
    return [ReminderSchema.model_validate(r) for r in reminders]
