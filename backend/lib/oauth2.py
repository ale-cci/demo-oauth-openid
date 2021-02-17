import random
import string


def create_client_id():
    adjective = random.choice(['good', 'new', 'first', 'last', 'long', 'great', 'little'])
    color = random.choice(['red', 'green', 'blue', 'purple', 'magenta', 'lime', 'black', 'gray', 'white'])
    animal = random.choice(['shrimp', 'gorilla', 'lion', 'crockodile', 'panda', 'tiger', 'giraffe'])

    return '-'.join((adjective, color, animal))


def create_client_secret(secret_len=128):
    return ''.join(random.choices(string.printable[:36], k=secret_len))
