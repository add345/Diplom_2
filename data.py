import random
import string

STANDARD_PASSWORD_LENGTH = 10
STANDARD_NAME_LENGTH = 10

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_randint_list(length, max_value):
    result = []
    for _ in range(length):
        result.append(random.randint(0, max_value))

    return result

def generate_email():
    email = f'{generate_random_string(5)}@{generate_random_string(5)}.{generate_random_string(2)}'
    return email
