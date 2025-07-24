

async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_facility(ac):
    title = "Тренажерный зал"
    response = await ac.post("/facilities", json={"title": title})
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert "data" in result
    assert result["data"]["title"] == title
