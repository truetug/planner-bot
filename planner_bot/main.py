import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import web
from .config import settings
from .handlers import router
from .middlewares import RequestIdMiddleware
from .database.session import init_db
from .logger import logger
from .scheduler.tasks import scheduler_loop

async def main() -> None:
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    dp.message.middleware(RequestIdMiddleware())
    dp.include_router(router)

    async def health_handler(_: web.Request) -> web.Response:
        return web.Response(text="ok")

    app = web.Application()
    app.add_routes([web.get("/health", health_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_loop(bot, settings.scheduler_interval))
    logger.info("Starting bot")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
