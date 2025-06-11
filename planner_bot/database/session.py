from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base
from ..config import settings

engine = create_async_engine(settings.database_dsn, echo=False)
async_session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
