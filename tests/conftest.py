import pytest
import requests

from helpers.api_client import ApiClient
from helpers.data_generator import generate_user_data
from helpers.urls import REGISTER, LOGIN, USER


@pytest.fixture
def api_client():
    """Возвращает экземпляр ApiClient."""
    return ApiClient()


@pytest.fixture
def unique_user():
    """Создаёт уникального пользователя и удаляет его после теста."""
    user_data = generate_user_data()

    # Создаём пользователя
    response = requests.post(REGISTER, json=user_data)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    token = response.json().get("accessToken")

    yield {
        "user_data": user_data,
        "token": token,
        "response": response
    }

    # Удаляем пользователя после теста
    if token:
        requests.delete(USER, headers={"Authorization": token})


@pytest.fixture
def registered_user_token(unique_user):
    """Возвращает токен зарегистрированного пользователя."""
    return unique_user["token"]