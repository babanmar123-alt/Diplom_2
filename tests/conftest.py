import pytest
import requests

from helpers.data_generator import generate_user_data
from helpers.urls import REGISTER, USER


@pytest.fixture
def unique_user():
    """Создаёт уникального пользователя и удаляет его после теста.

    Если пользователь не создался — тест пропускается (pytest.skip).
    """
    user_data = generate_user_data()

    # Создаём пользователя
    response = requests.post(REGISTER, json=user_data)

    # Если пользователь не создался — пропускаем тест
    if response.status_code != 200:
        pytest.skip(f"Не удалось создать пользователя: {response.text}")

    token = response.json()["accessToken"]

    # ОДИН yield — передаём данные в тест
    yield {
        "user_data": user_data,
        "token": token,
        "response": response
    }

    # Очистка: удаляем пользователя после теста
    requests.delete(USER, headers={"Authorization": token})


@pytest.fixture
def registered_user_token(unique_user):
    """Возвращает токен зарегистрированного пользователя."""
    return unique_user["token"]