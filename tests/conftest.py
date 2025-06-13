import os
import sys
import pathlib
import asyncio
import pytest
import pytest_asyncio

# Setup environment variables for config
os.environ.setdefault("BOT_TOKEN", "test-token")
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("DATABASE_DSN", "sqlite+aiosqlite:///./test.db")

# ensure project root on path
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from planner_bot.database.session import async_session_factory, init_db

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    await init_db()
    yield
    if os.path.exists("./test.db"):
        os.remove("./test.db")

@pytest_asyncio.fixture()
async def session():
    async with async_session_factory() as s:
        yield s
        await s.rollback()
