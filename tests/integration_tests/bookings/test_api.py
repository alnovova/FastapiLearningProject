import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 400),
    (1, "2024-09-01", "2024-09-10", 200),
])
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if response.status_code == 200:
        result = response.json()
        assert isinstance(result, dict)
        assert result["status"] == "OK"
        assert "data" in result


@pytest.fixture(scope="module")
async def delete_all_bookings(db):
    await db.bookings.delete()
    await db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, expected_count", [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-01", "2024-08-10", 2),
    (1, "2024-08-01", "2024-08-10", 3),
])
async def test_add_and_get_my_bookings(room_id, date_from, date_to, expected_count, authenticated_ac, delete_all_bookings):
    await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    response = await authenticated_ac.get("/bookings/me")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_count

