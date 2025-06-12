from datetime import datetime
from langchain_core.tools import tool

from ..database.session import async_session_factory
from ..services.projects import create_project, list_projects, delete_project
from ..services.reminders import create_reminder, list_reminders, delete_reminder


@tool
async def create_project_tool(user_id: int, title: str, description: str | None = None) -> str:
    """Create a new project for the user and return its id."""
    async with async_session_factory() as session:
        project = await create_project(session, user_id, title, description)
        return str(project.id)


@tool
async def list_projects_tool(user_id: int) -> str:
    """List all projects for the given user."""
    async with async_session_factory() as session:
        projects = await list_projects(session, user_id)
        return "\n".join(f"{p.id}: {p.title}" for p in projects)


@tool
async def delete_project_tool(user_id: int, project_id: int) -> str:
    """Delete a project by id for the given user."""
    async with async_session_factory() as session:
        await delete_project(session, project_id, user_id)
        return "deleted"


@tool
async def create_reminder_tool(project_id: int, when: str, description: str = "") -> str:
    """Create a reminder for a project.

    Args:
        project_id: target project id
        when: ISO datetime string
        description: reminder text
    """
    remind_at = datetime.fromisoformat(when)
    async with async_session_factory() as session:
        reminder = await create_reminder(session, project_id, description, remind_at)
        return str(reminder.id)


@tool
async def list_reminders_tool(project_id: int) -> str:
    """List all reminders for the project."""
    async with async_session_factory() as session:
        reminders = await list_reminders(session, project_id)
        return "\n".join(f"{r.id}: {r.description} at {r.remind_at}" for r in reminders)


@tool
async def delete_reminder_tool(reminder_id: int) -> str:
    """Delete reminder by id."""
    async with async_session_factory() as session:
        await delete_reminder(session, reminder_id)
        return "deleted"
