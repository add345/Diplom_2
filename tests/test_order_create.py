import pytest
import allure
import requests
import json
import urls
from helpers import OrderHelper


class TestOrderCreate:

    @allure.title("Создание заказа с авторизацией")
    def test_order_create_authorized(self, random_registered_user_data, ingredients_ids):
        request_headers = {
            'authorization': random_registered_user_data['accessToken']
        }

        request_data = {
            'ingredients': ingredients_ids
        }

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(urls.orders_url, headers=request_headers, data=request_data)

        response_json = response.json()
        order_json = response_json['order']

        OrderHelper.orders.append(order_json)

        assert response.status_code == 200
        assert response_json['success'] == True
        assert 'name' in response_json.keys()
        assert 'order' in response_json.keys()

        assert [ingredient['_id'] for ingredient in order_json['ingredients']] == ingredients_ids
        assert '_id' in order_json.keys()
        assert order_json['owner']['name'] == random_registered_user_data['name']
        assert order_json['owner']['email'] == random_registered_user_data['email']
        assert 'status' in order_json.keys()
        assert 'name' in order_json.keys()
        assert 'createdAt' in order_json.keys()
        assert 'updatedAt' in order_json.keys()
        assert 'number' in order_json.keys()
        assert 'price' in order_json.keys()



    @allure.title("Создание заказа без авторизации")
    def test_order_create_unauthorized(self, ingredients_ids):
        request_data = {
            'ingredients': ingredients_ids
        }

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(urls.orders_url, data=request_data)

        response_json = response.json()
        order_json = response_json['order']

        OrderHelper.orders.append(order_json)

        assert response.status_code == 200
        assert response_json['success'] == True
        assert 'name' in response_json.keys()
        assert 'order' in response_json.keys()
        assert 'number' in order_json.keys()

    @allure.title("Создание заказа с ингредиентами")
    def test_order_create_ingredients(self, ingredients_ids):
        request_data = {
            'ingredients': ingredients_ids
        }

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(urls.orders_url, data=request_data)

        response_json = response.json()
        order_json = response_json['order']

        OrderHelper.orders.append(order_json)

        assert response.status_code == 200
        assert response_json['success'] == True
        assert 'name' in response_json.keys()
        assert 'order' in response_json.keys()
        assert 'number' in order_json.keys()

    @allure.title("Создание заказа без ингредиентов")
    def test_order_create_non_ingredients(self):
        request_data = {
            'ingredients': []
        }

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(urls.orders_url, data=request_data)

        response_json = response.json()

        assert response.status_code == 400
        assert response_json['success'] == False
        assert response_json['message'] == 'Ingredient ids must be provided'


    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_order_create_invalid_ingredients(self, ingredients_invalid_ids):
        request_data = {
            'ingredients': ingredients_invalid_ids
        }

        with allure.step('Отправка запроса на создание заказа'):
            response = requests.post(urls.orders_url, data=request_data)

        assert response.status_code == 500
