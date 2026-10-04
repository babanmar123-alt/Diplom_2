import requests

from helpers.data_generator import generate_user_data
from helpers.urls import REGISTER


class TestCreateUser:
    """Тесты создания пользователя."""

    def test_create_unique_user(self):
        """Создание уникального пользователя — 200 OK."""
        user_data = generate_user_data()
        response = requests.post(REGISTER, json=user_data)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == user_data["email"]
        assert body["user"]["name"] == user_data["name"]

        # Удаляем созданного пользователя
        token = body["accessToken"]
        requests.delete(
            "https://stellarburgers.education-services.ru/api/auth/user",
            headers={"Authorization": token}
        )

    def test_create_duplicate_user(self, unique_user):
        """Создание дубликата пользователя — 403 Forbidden."""
        user_data = unique_user["user_data"]
        response = requests.post(REGISTER, json=user_data)

        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "User already exists"

    def test_create_user_without_email(self):
        """Создание пользователя без email — 403 Forbidden."""
        user_data = generate_user_data()
        del user_data["email"]
        response = requests.post(REGISTER, json=user_data)

        assert response.status_code == 403, f"Ожидался 403, получен {response.status_code}"
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"

    def test_create_user_without_password(self):
        """Создание пользователя без password — 403 Forbidden."""
        user_data = generate_user_data()
        del user_data["password"]
        response = requests.post(REGISTER, json=user_data)

        assert response.status_code == 403

    def test_create_user_without_name(self):
        """Создание пользователя без name — 403 Forbidden."""
        user_data = generate_user_data()
        del user_data["name"]
        response = requests.post(REGISTER, json=user_data)

        assert response.status_code == 403