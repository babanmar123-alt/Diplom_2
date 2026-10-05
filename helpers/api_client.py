import requests

from helpers.urls import REGISTER, LOGIN, USER, ORDERS, INGREDIENTS


class ApiClient:
    """Обёртка над requests для работы с API Stellar Burgers."""

    def register(self, email: str, password: str, name: str) -> requests.Response:
        """Регистрация пользователя."""
        return requests.post(REGISTER, json={
            "email": email,
            "password": password,
            "name": name
        })

    def login(self, email: str, password: str) -> requests.Response:
        """Авторизация пользователя."""
        return requests.post(LOGIN, json={
            "email": email,
            "password": password
        })

    def delete_user(self, token: str) -> requests.Response:
        """Удаление пользователя."""
        return requests.delete(USER, headers={"Authorization": token})

    def create_order(self, ingredients: list, token: str = None) -> requests.Response:
        """Создание заказа."""
        headers = {}
        if token:
            headers["Authorization"] = token
        return requests.post(ORDERS, json={"ingredients": ingredients}, headers=headers)

    def get_ingredients(self) -> requests.Response:
        """Получение списка ингредиентов."""
        return requests.get(INGREDIENTS)