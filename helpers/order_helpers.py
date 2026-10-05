import requests

from helpers.urls import INGREDIENTS


def get_valid_ingredients() -> list:
    """Получает валидные ID ингредиентов для заказа."""
    response = requests.get(INGREDIENTS)
    data = response.json()["data"]
    return [data[0]["_id"], data[1]["_id"]]