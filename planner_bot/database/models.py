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
