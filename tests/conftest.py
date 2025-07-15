import json
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert

from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        tests_dir = Path(__file__).parent
        hotels_path = tests_dir / "mock_hotels.json"
        rooms_path = tests_dir / "mock_rooms.json"

        hotels_data = json.loads(hotels_path.read_text(encoding="utf-8"))
        rooms_data = json.loads(rooms_path.read_text(encoding="utf-8"))

        await conn.execute(insert(HotelsORM), hotels_data)
        await conn.execute(insert(RoomsORM), rooms_data)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="https://api.example.com/v1") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.ru",
                "password": "1234"
            }
        )
