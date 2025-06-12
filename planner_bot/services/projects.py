from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import Project
from ..database.schemas import ProjectSchema

async def create_project(session: AsyncSession, user_id: int, title: str, description: str | None = None) -> ProjectSchema:
    project = Project(title=title, description=description, user_id=user_id)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectSchema.model_validate(project)

async def list_projects(session: AsyncSession, user_id: int) -> list[ProjectSchema]:
    result = await session.execute(select(Project).where(Project.user_id == user_id))
    projects = result.scalars().all()
    return [ProjectSchema.model_validate(p) for p in projects]

async def delete_project(session: AsyncSession, project_id: int, user_id: int) -> None:
    await session.execute(delete(Project).where(Project.id == project_id, Project.user_id == user_id))
    await session.commit()
