from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class ReminderSchema(BaseModel):
    id: int
    project_id: int
    description: Optional[str] = None
    remind_at: datetime
    cron: Optional[str] = None
    created_at: datetime
    project: Optional[ProjectSchema] = None

    class Config:
        orm_mode = True
