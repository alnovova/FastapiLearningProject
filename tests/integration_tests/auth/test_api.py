import pytest


@pytest.mark.parametrize("email, password, status_code", [
    ("user_1@test.com", "user_1", 200),
    ("user_2@test.com", "user_2", 200),
    ("user_2@test.com", "user_2", 422),
    ("user_3", "user_3", 422),
])
async def test_register(email: str, password: str, status_code: int, ac):
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
    ("null_user", "12345", 422),
])
async def test_login_logout(email: str, password: str, login_status_code: int, ac):
    response_login = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    assert response_login.status_code == login_status_code

    if response_login.status_code == 200:
        assert ac.cookies["access_token"]
        assert "access_token" in response_login.json()

        response_my_data = await ac.get("/auth/me")
        assert response_my_data.status_code == 200
        my_data = response_my_data.json()
        assert my_data["email"] == email
        assert "id" in my_data
        assert "password" not in my_data
        assert "hashed_password" not in my_data

        response_logout = await ac.post("/auth/logout")
        assert response_logout.status_code == 200
        assert not "access_token" in ac.cookies
