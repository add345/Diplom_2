from data import generate_random_string, generate_randint_list, STANDARD_PASSWORD_LENGTH, STANDARD_NAME_LENGTH, generate_email
import random
import urls
import allure
import requests
import json

class UserHelper:
    users = {}

    @staticmethod
    @allure.step("Генерация данных пользователя")
    def create_random_user_data():
        user_data = {"email": generate_email(),
                     "password": generate_random_string(STANDARD_PASSWORD_LENGTH),
                     "name": generate_random_string(STANDARD_NAME_LENGTH)}

        return user_data

    @staticmethod
    @allure.step('Регистрация пользователя')
    def register_user(user_data):
        response = requests.post(urls.user_register_url, data=user_data)

        if response.status_code != 200:
           raise Exception("Ошибка регистрации")

        user_data["accessToken"] = response.json()["accessToken"]
        user_data["refreshToken"] = response.json()["refreshToken"]

        UserHelper.users[user_data['email']] = user_data

        return user_data

    @staticmethod
    @allure.step('Логин пользователя на сайте')
    def login_user(self, user_data):

        request_data = {
            'email':  user_data['email'],
            'password': user_data['password']
        }

        response = requests.post(urls.user_login_url, json.dumps(request_data))

        if response.status_code != 200:
           raise Exception("Ошибка логина")

        user_data["accessToken"] = response.json()["accessToken"]
        user_data["refreshToken"] = response.json()["refreshToken"]

        UserHelper.users[user_data['email']] = user_data

        return user_data
        # https://stellarburgers.nomoreparties.site/api/auth/login

    @staticmethod
    @allure.step('Удаление пользователя')
    def delete_user(user_data):
        request_headers = {
            'authorization': user_data['accessToken']
        }

        response = requests.delete(urls.user_login_url, headers=request_headers)

        return user_data

    @staticmethod
    @allure.step('Удаление всех созданных пользователей')
    def delete_all_users():

        for email in UserHelper.users.keys():
            UserHelper.delete_user(UserHelper.users[email])


class OrderHelper:

    orders = []

    @staticmethod
    @allure.step("Запрос данных об ингредиентах")
    def get_ingredients_ids():
        response = requests.get(urls.ingredients_url)

        response_json = response.json()

        result = []

        for ingredient in response_json["data"]:
            result.append(ingredient["_id"])

        return result

    @staticmethod
    @allure.step('Генерация набора ингредиентов')
    def generate_order():
        ingredients_src =  OrderHelper.get_ingredients_ids()
        ingredients_count = random.randint(1, 10)

        ingredients_indexes = generate_randint_list(ingredients_count, len(ingredients_src) - 1)

        result = []

        for i in ingredients_indexes:
            result.append(ingredients_src[i])

        return result
