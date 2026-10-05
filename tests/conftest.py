import pytest
import requests

from helpers.data_generator import generate_user_data
from helpers.urls import REGISTER, USER


@pytest.fixture
def unique_user():
    """Создаёт уникального пользователя и удаляет его после теста.

    ВАЖНО: без ассертов — только подготовка и очистка данных.
    """
    user_data = generate_user_data()

    response = requests.post(REGISTER, json=user_data)

    if response.status_code != 200:
        yield {"user_data": user_data, "token": None}
        return

    token = response.json().get("accessToken")

    yield {
        "user_data": user_data,
        "token": token,
        "response": response
    }

    if token:
        requests.delete(USER, headers={"Authorization": token})


@pytest.fixture
def registered_user_token(unique_user):
    """Возвращает токен зарегистрированного пользователя."""
    return unique_user["token"]