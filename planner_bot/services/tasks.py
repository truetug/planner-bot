from datetime import datetime
from typing import Any
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import Task, TaskLink, TaskResult
from ..database.schemas import TaskSchema, TaskLinkSchema, TaskResultSchema

async def create_task(
    session: AsyncSession,
    user_id: int,
    title: str,
    description: str | None = None,
    project_id: int | None = None,
    deadline: datetime | None = None,
    estimate_hours: int | None = None,
    priority: str | None = None,
    status: str | None = None,
    parent_id: int | None = None,
) -> TaskSchema:
    task = Task(
        title=title,
        description=description,
        project_id=project_id,
        user_id=user_id,
        deadline=deadline,
        estimate_hours=estimate_hours,
        priority=priority,
        status=status,
        parent_id=parent_id,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return TaskSchema.model_validate(task)

async def list_tasks(session: AsyncSession, user_id: int) -> list[TaskSchema]:
    result = await session.execute(select(Task).where(Task.user_id == user_id))
    tasks = result.scalars().all()
    return [TaskSchema.model_validate(t) for t in tasks]

async def update_task(session: AsyncSession, task_id: int, user_id: int, **fields: Any) -> TaskSchema | None:
    await session.execute(
        update(Task).where(Task.id == task_id, Task.user_id == user_id).values(**fields)
    )
    await session.commit()
    result = await session.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    task = result.scalar_one_or_none()
    return TaskSchema.model_validate(task) if task else None

async def delete_task(session: AsyncSession, task_id: int, user_id: int) -> None:
    await session.execute(delete(Task).where(Task.id == task_id, Task.user_id == user_id))
    await session.commit()

async def add_task_link(session: AsyncSession, task_id: int, related_task_id: int, link_type: str) -> TaskLinkSchema:
    link = TaskLink(task_id=task_id, related_task_id=related_task_id, type=link_type)
    session.add(link)
    await session.commit()
    await session.refresh(link)
    return TaskLinkSchema.model_validate(link)

async def list_task_links(session: AsyncSession, task_id: int) -> list[TaskLinkSchema]:
    result = await session.execute(select(TaskLink).where(TaskLink.task_id == task_id))
    links = result.scalars().all()
    return [TaskLinkSchema.model_validate(l) for l in links]


async def add_task_result(
    session: AsyncSession,
    task_id: int,
    user_id: int,
    result_text: str,
) -> TaskResultSchema:
    result = TaskResult(task_id=task_id, user_id=user_id, result=result_text)
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return TaskResultSchema.model_validate(result)


async def list_task_results(session: AsyncSession, task_id: int) -> list[TaskResultSchema]:
    res = await session.execute(select(TaskResult).where(TaskResult.task_id == task_id))
    results = res.scalars().all()
    return [TaskResultSchema.model_validate(r) for r in results]
