from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from .database.session import async_session_factory
from .services.projects import create_project, list_projects, delete_project
from .services.reminders import create_reminder, list_reminders, delete_reminder
from .llm.client import ask
from .logger import logger

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    logger.info("Received start command")
    await message.answer("Hello! I'm planner bot")

@router.message(Command("project_create"))
async def handle_create_project(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /project_create <title>")
        return
    title = parts[1]
    async with async_session_factory() as session:
        project = await create_project(session, message.from_user.id, title)
    await message.answer(f"Project created with id {project.id}")

@router.message(Command("projects"))
async def handle_list_projects(message: Message) -> None:
    async with async_session_factory() as session:
        projects = await list_projects(session, message.from_user.id)
    text = "\n".join(f"{p.id}: {p.title}" for p in projects) or "No projects"
    await message.answer(text)

@router.message(Command("project_delete"))
async def handle_delete_project(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /project_delete <id>")
        return
    pid = int(parts[1])
    async with async_session_factory() as session:
        await delete_project(session, pid, message.from_user.id)
    await message.answer("Project deleted")

@router.message(Command("reminder_create"))
async def handle_create_reminder(message: Message) -> None:
    parts = message.text.split(maxsplit=4)
    if len(parts) < 4:
        await message.answer("Usage: /reminder_create <project_id> <YYYY-MM-DD> <HH:MM> <text>")
        return
    project_id = int(parts[1])
    date = parts[2]
    time = parts[3]
    description = parts[4] if len(parts) > 4 else ""
    remind_at = datetime.fromisoformat(f"{date}T{time}")
    async with async_session_factory() as session:
        reminder = await create_reminder(session, project_id, description, remind_at)
    await message.answer(f"Reminder created with id {reminder.id}")

@router.message(Command("reminders"))
async def handle_list_reminders(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /reminders <project_id>")
        return
    pid = int(parts[1])
    async with async_session_factory() as session:
        reminders = await list_reminders(session, pid)
    text = "\n".join(f"{r.id}: {r.description} at {r.remind_at}" for r in reminders) or "No reminders"
    await message.answer(text)

@router.message(Command("reminder_delete"))
async def handle_delete_reminder(message: Message) -> None:
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /reminder_delete <id>")
        return
    rid = int(parts[1])
    async with async_session_factory() as session:
        await delete_reminder(session, rid)
    await message.answer("Reminder deleted")

@router.message()
async def handle_chat(message: Message) -> None:
    response = await ask(message.text)
    await message.answer(response)
