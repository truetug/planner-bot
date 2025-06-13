import pytest
from datetime import datetime

from planner_bot.services.tasks import (
    create_task,
    list_tasks,
    update_task,
    delete_task,
    add_task_link,
    list_task_links,
    add_task_result,
    list_task_results,
)


@pytest.mark.asyncio
async def test_task_crud(session):
    task = await create_task(session, user_id=1, title="t1")
    assert task.id is not None
    assert task.title == "t1"

    tasks = await list_tasks(session, user_id=1)
    assert len(tasks) == 1

    updated = await update_task(session, task.id, 1, title="new")
    assert updated.title == "new"

    await delete_task(session, task.id, 1)
    tasks = await list_tasks(session, user_id=1)
    assert tasks == []


@pytest.mark.asyncio
async def test_task_links_and_results(session):
    t1 = await create_task(session, user_id=1, title="t1")
    t2 = await create_task(session, user_id=1, title="t2")

    link = await add_task_link(session, t1.id, t2.id, "related")
    links = await list_task_links(session, t1.id)
    assert links == [link]

    res = await add_task_result(session, t1.id, 1, "done")
    results = await list_task_results(session, t1.id)
    assert results == [res]
