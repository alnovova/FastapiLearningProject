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
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_ac):
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
