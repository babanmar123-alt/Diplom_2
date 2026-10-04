import pytest
import requests

from helpers.urls import ORDERS, INGREDIENTS


class TestCreateOrder:
    """Тесты создания заказа."""

    @staticmethod
    def get_valid_ingredients():
        """Получает валидные ID ингредиентов."""
        response = requests.get(INGREDIENTS)
        assert response.status_code == 200
        data = response.json()["data"]
        return [data[0]["_id"], data[1]["_id"]]

    def test_create_order_with_auth(self, registered_user_token):
        """Создание заказа с авторизацией — 200 OK."""
        ingredients = self.get_valid_ingredients()
        response = requests.post(
            ORDERS,
            json={"ingredients": ingredients},
            headers={"Authorization": registered_user_token}
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @pytest.mark.xfail(reason="Баг API: сервер принимает заказ без авторизации, должен возвращать 401")
    def test_create_order_without_auth(self):
        """Создание заказа без авторизации — 401 Unauthorized."""
        ingredients = self.get_valid_ingredients()
        response = requests.post(ORDERS, json={"ingredients": ingredients})

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "You should be authorised"

    def test_create_order_with_ingredients(self, registered_user_token):
        """Создание заказа с ингредиентами — 200 OK."""
        ingredients = self.get_valid_ingredients()
        response = requests.post(
            ORDERS,
            json={"ingredients": ingredients},
            headers={"Authorization": registered_user_token}
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True

    def test_create_order_without_ingredients(self, registered_user_token):
        """Создание заказа без ингредиентов — 400 Bad Request."""
        response = requests.post(
            ORDERS,
            json={"ingredients": []},
            headers={"Authorization": registered_user_token}
        )

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    def test_create_order_invalid_hash(self, registered_user_token):
        """Создание заказа с неверным хешем — 500 Internal Server Error."""
        response = requests.post(
            ORDERS,
            json={"ingredients": ["invalid_hash_12345"]},
            headers={"Authorization": registered_user_token}
        )

        assert response.status_code == 500