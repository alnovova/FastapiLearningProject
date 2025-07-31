import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("user_1@test.com", "user_1", 200),
    ("user_2@test.com", "user_2", 200),
    ("user_2@test.com", "user_3", 422),
])
async def test_register(email, password, status_code, ac):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, login_status_code", [
    ("user_1@test.com", "user_1", 200),
    ("user_2@test.com", "user_2", 200),
    ("user_2@test.com", "wrong_password", 401),
    ("null_user@test.com", "12345", 401),
])
async def test_login_logout(email, password, login_status_code, ac):
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == login_status_code

    if response_login.status_code == 200:
        assert response_login.cookies.get("access_token")

        response_my_data = await ac.get("/auth/me")
        assert response_my_data.status_code == 200
        my_data = response_my_data.json()
        assert my_data["email"] == email

        response_logout = await ac.post("/auth/logout")
        assert response_logout.status_code == 200
        assert not response_logout.cookies.get("access_token")
