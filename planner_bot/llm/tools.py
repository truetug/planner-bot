from datetime import datetime

from langchain_core.tools import tool

from ..database.session import async_session_factory
from ..services.projects import create_project, list_projects, delete_project
from ..services.reminders import create_reminder, list_reminders, delete_reminder
from ..services.tasks import (
    create_task,
    list_tasks,
    update_task,
    delete_task,
    add_task_result,
    list_task_results,
)

@tool("create_task")
async def create_task_tool(
    user_id: int,
    title: str,
    description: str | None = None,
    project_id: int | None = None,
    deadline: str | None = None,
    estimate_hours: int | None = None,
    priority: str | None = None,
    status: str | None = None,
    parent_id: int | None = None,
) -> dict:
    """Create a task for a user."""
    _deadline = datetime.fromisoformat(deadline) if deadline else None
    async with async_session_factory() as session:
        task = await create_task(
            session,
            user_id=user_id,
            title=title,
            description=description,
            project_id=project_id,
            deadline=_deadline,
            estimate_hours=estimate_hours,
            priority=priority,
            status=status,
            parent_id=parent_id,
        )
        return task.dict()


@tool("list_tasks")
async def list_tasks_tool(user_id: int) -> list[dict]:
    """List tasks for the given user."""
    async with async_session_factory() as session:
        tasks = await list_tasks(session, user_id)
        return [t.dict() for t in tasks]


@tool("update_task")
async def update_task_tool(
    user_id: int,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    project_id: int | None = None,
    deadline: str | None = None,
    estimate_hours: int | None = None,
    priority: str | None = None,
    status: str | None = None,
    parent_id: int | None = None,
) -> dict | None:
    """Update a task and return the new values."""
    fields = {}
    if title is not None:
        fields["title"] = title
    if description is not None:
        fields["description"] = description
    if project_id is not None:
        fields["project_id"] = project_id
    if deadline is not None:
        fields["deadline"] = datetime.fromisoformat(deadline)
    if estimate_hours is not None:
        fields["estimate_hours"] = estimate_hours
    if priority is not None:
        fields["priority"] = priority
    if status is not None:
        fields["status"] = status
    if parent_id is not None:
        fields["parent_id"] = parent_id
    async with async_session_factory() as session:
        task = await update_task(session, task_id, user_id, **fields)
        return task.dict() if task else None


@tool("delete_task")
async def delete_task_tool(user_id: int, task_id: int) -> str:
    """Delete a task."""
    async with async_session_factory() as session:
        await delete_task(session, task_id, user_id)
    return "deleted"


@tool("add_task_result")
async def add_task_result_tool(task_id: int, user_id: int, result: str) -> dict:
    """Attach a result text to a task."""
    async with async_session_factory() as session:
        res = await add_task_result(session, task_id, user_id, result)
        return res.dict()


@tool("list_task_results")
async def list_task_results_tool(task_id: int) -> list[dict]:
    """Return all results for a task."""
    async with async_session_factory() as session:
        results = await list_task_results(session, task_id)
        return [r.dict() for r in results]


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
