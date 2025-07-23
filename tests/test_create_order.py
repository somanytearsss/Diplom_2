import allure
import requests
from data import Ingredients, Urls
from helpers import get_access_token
from conftest import registration_and_delete_user


@allure.description('Тестирование класса создания заказа')
class TestCreateOrder:
    @allure.title('Проверяем создание заказа с ингредиентами, когда пользователь авторизован')
    def test_create_order_to_auth_user(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = {'ingredients': Ingredients.ingredients}

        with allure.step("Получаем токен доступа"):
            access_token = get_access_token(response)

        headers = {
            'Authorization': f'{access_token}',
        }

        with allure.step("Отправляем запрос на создание заказа"):
            new_response = requests.post(Urls.url_create_order, json=new_payload, headers=headers)

        with allure.step("Проверяем статус ответа"):
            assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"

        with allure.step("Проверяем наличие ключей 'name' и 'number' в ответе"):
            order = new_response.json()
            assert 'name' in order.keys(), "Ключ 'name' отсутствует в ответе"
            assert 'number' in order['order'].keys(), "Ключ 'number' отсутствует в ответе"

    @allure.title('Проверяем создание заказа с ингредиентами, когда пользователь не авторизован')
    def test_create_order_to_not_auth_user(self):
        payload = {'ingredients': Ingredients.ingredients}
        headers = {
                'Content-Type': 'application/json'
            }
        response = requests.post(Urls.url_create_order, json=payload, headers=headers )
        order = response.json()
        assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}"
        assert 'name' in order.keys()
        assert 'number' in order['order'].keys()

    @allure.title('Проверяем создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        ingredients = {'ingredients': []}
        response = requests.post(Urls.url_create_order, data=ingredients )
        assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}"
        assert response.json()['message'] == "Ingredient ids must be provided"

    @allure.title('Проверяем создание заказа c несуществующим хэш ингредиента и авторизованным пользователем')
    def test_create_order_incorrect_ingredients_auth_user_error(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = {'ingredients': Ingredients.INCORRECT_INGREDIENT_HASH}

        access_token = get_access_token(response)
        headers = {
            'Authorization': f'{access_token}',
        }
        new_response = requests.post(Urls.url_create_order, json=new_payload, headers=headers)

        assert new_response.status_code == 400, f"Ожидался статус 400, но получен {new_response.status_code}"
        assert new_response.json()['message'] == "One or more ids provided are incorrect"
        assert new_response.json()['success'] == False
