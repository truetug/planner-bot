from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class ProjectSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ReminderSchema(BaseModel):
    id: int
    project_id: int
    description: Optional[str] = None
    remind_at: datetime
    cron: Optional[str] = None
    created_at: datetime
    project: Optional[ProjectSchema] = None

    model_config = ConfigDict(from_attributes=True)


class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    user_id: int
    deadline: Optional[datetime] = None
    estimate_hours: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class TaskLinkSchema(BaseModel):
    id: int
    task_id: int
    related_task_id: int
    type: str

    model_config = ConfigDict(from_attributes=True)


class TaskResultSchema(BaseModel):
    id: int
    task_id: int
    user_id: int
    result: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
