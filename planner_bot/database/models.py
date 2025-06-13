from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reminders = relationship("Reminder", back_populates="project", cascade="all, delete-orphan")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    description = Column(Text)
    remind_at = Column(DateTime, nullable=False)
    cron = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="reminders")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, nullable=False)
    deadline = Column(DateTime)
    estimate_hours = Column(Integer)
    priority = Column(String(50))
    status = Column(String(50))
    parent_id = Column(Integer, ForeignKey("tasks.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project")
    parent = relationship("Task", remote_side=[id])
    links = relationship(
        "TaskLink",
        back_populates="task",
        cascade="all, delete-orphan",
        foreign_keys="TaskLink.task_id",
    )
    results = relationship(
        "TaskResult",
        back_populates="task",
        cascade="all, delete-orphan",
    )


class TaskLink(Base):
    __tablename__ = "task_links"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    type = Column(String(50), nullable=False)

    task = relationship("Task", foreign_keys=[task_id], back_populates="links")
    related_task = relationship("Task", foreign_keys=[related_task_id])


class TaskResult(Base):
    __tablename__ = "task_results"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    task = relationship("Task", back_populates="results")
