import requests

from helpers.data_generator import generate_user_data
from helpers.urls import LOGIN


class TestLoginUser:
    """Тесты авторизации пользователя."""

    def test_login_existing_user(self, unique_user):
        """Вход под существующим пользователем — 200 OK."""
        user_data = unique_user["user_data"]
        response = requests.post(LOGIN, json={
            "email": user_data["email"],
            "password": user_data["password"]
        })

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body

    def test_login_wrong_password(self, unique_user):
        """Вход с неверным паролем — 401 Unauthorized."""
        user_data = unique_user["user_data"]
        response = requests.post(LOGIN, json={
            "email": user_data["email"],
            "password": "wrong_password"
        })

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"

    def test_login_wrong_email(self):
        """Вход с несуществующим email — 401 Unauthorized."""
        response = requests.post(LOGIN, json={
            "email": "nonexistent_user_12345@yandex.ru",
            "password": "some_password"
        })

        assert response.status_code == 401