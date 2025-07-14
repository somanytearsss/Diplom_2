import allure
import requests
from data import Urls
from conftest import registration_and_delete_user


@allure.description('Тестирование класса авторизации пользователя')
class TestLoginUser:
    @allure.title('Проверяем успешную авторизацию зарегистрированного пользователя')
    def test_success_login_user(self, registration_and_delete_user):
        payload, response  = registration_and_delete_user
        new_payload = {
			"email": payload["email"],
			"password": payload["password"]
		}
        new_response  = requests.post(Urls.url_user_login, data=new_payload)
        assert new_response.status_code == 200, f"Ожидался статус 200, но получен {new_response.status_code}"
        assert new_response.json()['user']['email'] == payload['email']
        assert new_response.json()['user']['name'] == payload['name']

    @allure.title('Проверяем появление ошибки при авторизации с некорректным email')
    def test_login_error_to_auth_incorrect_email(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = {
            "email": 'uncorrect@email',
            "password": payload["password"]
        }
        new_response = requests.post(Urls.url_user_login, data=new_payload)
        assert new_response.status_code == 401, f"Ожидался статус 401, но получен {new_response.status_code}"
        assert new_response.json()['message'] == "email or password are incorrect", \
            f"Ожидалось сообщение 'email or password are incorrect', но получен ответ {new_response.json()['message']}"
        assert new_response.json()['success'] == False, \
            f"Ожидался ответ False, но получен ответ {new_response.json()['success']}"

    @allure.title('Проверяем появление ошибки при авторизации с некорректным password')
    def test_login_error_to_auth_incorrect_email(self, registration_and_delete_user):
        payload, response = registration_and_delete_user
        new_payload = {
            "email": payload["email"],
            "password": 'incorrect password'
        }
        new_response = requests.post(Urls.url_user_login, data=new_payload)
        assert new_response.status_code == 401, f"Ожидался статус 401, но получен {new_response.status_code}"
        assert new_response.json()['message'] == "email or password are incorrect", \
            f"Ожидалось сообщение 'email or password are incorrect', но получен ответ {new_response.json()['message']}"
        assert new_response.json()['success'] == False, \
            f"Ожидался ответ False, но получен ответ {new_response.json()['success']}"
