import json
from unittest import mock
from pathlib import Path

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session")
async def db(check_test_mode):
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac(check_test_mode):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://api.example.com") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        tests_dir = Path(__file__).parent
        hotels_path = tests_dir / "mock_hotels.json"
        rooms_path = tests_dir / "mock_rooms.json"
        facilities_path = tests_dir / "mock_facilities.json"

        hotels_data = json.loads(hotels_path.read_text(encoding="utf-8"))
        rooms_data = json.loads(rooms_path.read_text(encoding="utf-8"))
        facilities_data = json.loads(facilities_path.read_text(encoding="utf-8"))

        await conn.execute(insert(HotelsORM), hotels_data)
        await conn.execute(insert(RoomsORM), rooms_data)
        await conn.execute(insert(FacilitiesORM), facilities_data)


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    response = await ac.post(
        "/auth/register",
        json={
            "email": "test@test.ru",
            "password": "1234"
        }
    )


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "test@test.ru",
            "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac
