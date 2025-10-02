import pytest
import allure
import requests
import json
import urls
from helpers import UserHelper


class TestUserCreate:

    @allure.title('Регистрация нового уникального пользователя')
    def test_new_user_register(self, random_user_data):

        with allure.step('Отправка запроса на регистрацию пользователя'):
            response = requests.post(urls.user_register_url, data=random_user_data)

        response_json = json.loads(response.text)
        response_json_user = response_json['user']

        user_data = random_user_data
        user_data['accessToken'] = response_json['accessToken']
        user_data['refreshToken'] = response_json['refreshToken']
        UserHelper.users[user_data['email']] = user_data

        assert response_json['success'] == True
        assert response_json_user['email'] == random_user_data['email']
        assert response_json_user['name'] == random_user_data['name']
        assert 'accessToken' in response_json.keys()
        assert 'refreshToken' in response_json.keys()
        assert response.status_code == 200

    @allure.title('Регистрация уже зарегистрированного пользователя')
    def test_existing_user_register(self, random_registered_user_data):
        request_data = {
            'email': random_registered_user_data['email'],
            'password': random_registered_user_data['password'],
            "name": random_registered_user_data['name']
        }

        with allure.step('Отправка запроса на регистрацию пользователя'):
            response = requests.post(urls.user_register_url, data=request_data)

        response_json = json.loads(response.text)

        assert response.status_code == 403
        assert response_json['success'] == False
        assert response_json['message'] == 'User already exists'


    @allure.title('Регистрация пользователя незаполненными обязательными полями')
    @pytest.mark.parametrize('excluded_key', ["email", "password", "name"])
    def test_unsufficient_user_register(self, random_user_data, excluded_key):
        request_data = random_user_data
        request_data.pop(excluded_key)

        with allure.step('Отправка запроса на регистрацию пользователя'):
            response = requests.post(urls.user_register_url, data=request_data)

        response_json = json.loads(response.text)

        assert response.status_code == 403
        assert response_json['success'] == False
        assert response_json['message'] == 'Email, password and name are required fields'
