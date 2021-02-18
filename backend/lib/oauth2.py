import random
import string


def create_client_id():
    adjective = random.choice(['good', 'new', 'first', 'last', 'long', 'great', 'little'])
    color = random.choice(['red', 'green', 'blue', 'purple', 'magenta', 'lime', 'black', 'gray', 'white'])
    animal = random.choice(['shrimp', 'gorilla', 'lion', 'crockodile', 'panda', 'tiger', 'giraffe'])

    return '-'.join((adjective, color, animal))


def create_client_secret(secret_len=128):
    return ''.join(random.choices(string.printable[:36], k=secret_len))


def _create_jwt_head():
    return {
        'alg': 'RSA256',
        'kid': ''
        'typ': 'JWT',
    }

def _create_jwt_body():
    '''
    {'at_hash': 'Jrbq0PyuRTFWYTZ4z2qjRg',
     'aud': '359913789820-tfbqpn1mpan21vgjb408i42rd1ruc9mv.apps.googleusercontent.com',
     'azp': '359913789820-tfbqpn1mpan21vgjb408i42rd1ruc9mv.apps.googleusercontent.com',
     'email': 'alecrd98@gmail.com',
     'email_verified': True,
     'exp': 1613679310,
     'iat': 1613675710,
     'iss': 'https://accounts.google.com',
     'sub': '102559048848623069948'}
    '''

    iat = time.time()
    exp = iat + 3600
    return {
        'iss': 'https://localhost:8000',
        'sub': flask.session['user_id'],
        'iat': iat,
        'exp': exp,
    }


def _create_checksum():
    return ''

def create_jwt(keypath, claims):
    '''
    '''

    iss = time.time()
    head = _create_jwt_head()
    body = _create_jwt_body()

    checksum = _create_checksum(head, body, keypath)

    return '.'.join((head,body,checksum))
