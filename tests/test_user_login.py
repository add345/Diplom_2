import pytest
import allure
import requests
import json
import urls

class TestUserLogin:

    @allure.title("Вход под существующим пользователем")
    def test_existing_user_login(self, random_registered_user_data):
        request_data = {
            'email': random_registered_user_data['email'],
            'password': random_registered_user_data['password']
        }
        with allure.step('Отправка запроса на логин пользователя'):
            response = requests.post(urls.user_login_url, data=request_data)

        response_json = json.loads(response.text)
        response_json_user = response_json['user']

        assert response_json['success'] == True
        assert response_json_user['email'] == random_registered_user_data['email']
        assert response_json_user['name'] == random_registered_user_data['name']
        assert 'accessToken' in response_json.keys()
        assert 'refreshToken' in response_json.keys()
        assert response.status_code == 200


    @allure.title("Вход с неверным логином и паролем")
    @pytest.mark.parametrize('invalid_key', ["email", "password"])
    def test_invalid_user_login(self, random_registered_user_data, invalid_key, random_user_data):

        request_data = {
            'email': random_registered_user_data['email'],
            'password': random_registered_user_data['password']
        }
        request_data[invalid_key] = random_user_data[invalid_key]

        with allure.step('Отправка запроса на логин пользователя'):
            response = requests.post(urls.user_login_url, data=request_data)

        response_json = json.loads(response.text)

        assert response.status_code == 401
        assert response_json['success'] == False
        assert response_json['message'] == 'email or password are incorrect'

