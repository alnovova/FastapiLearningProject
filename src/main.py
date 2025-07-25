import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.backends.inmemory import InMemoryBackend

from src.config import settings

sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_connector
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.api.dependencies import get_db


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


async def run_send_emails_regularly():
    while True:
        await asyncio.sleep(5)
        await send_emails_bookings_today_checkin()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    asyncio.create_task(run_send_emails_regularly())
    await redis_connector.connect()
    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    yield
    # При выключении/перезагрузке приложения
    await redis_connector.close()


# if settings.MODE == "TEST":
#     FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
