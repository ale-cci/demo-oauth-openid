# Signing using rsa
# https://stackoverflow.com/questions/49116579/sign-a-byte-string-with-sha256-in-python
import random
import string
import time
import flask
import cryptography
import json
import base64

# Required for jwt signature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def create_client_id():
    adjective = random.choice(['good', 'new', 'first', 'last', 'long', 'great', 'little'])
    color = random.choice(['red', 'green', 'blue', 'purple', 'magenta', 'lime', 'black', 'gray', 'white'])
    animal = random.choice(['shrimp', 'gorilla', 'lion', 'crockodile', 'panda', 'tiger', 'giraffe'])

    return '-'.join((adjective, color, animal))


def create_client_secret(secret_len=128):
    return ''.join(random.choices(string.printable[:36], k=secret_len))


def _create_jwt_head():
    return {
        'alg': 'HS256',
        'kid': '1',
        'typ': 'JWT',
    }

def _create_jwt_body(claims):
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

    reserved_claims = {
        'at_hash', 'aud', 'azp', 'exp', 'iat', 'iss', 'sub', 'nbf'
    }
    token_claims = claims - reserved_claims

    iat = time.time()
    exp = iat + 3600

    token_claims.update({
        'iss': 'https://localhost:8000',
        'sub': flask.session['user_id'],
        'iat': iat,
        'exp': exp,
    })
    return token_claims


def _create_checksum(message, keypath):
    # Read private key
    with open(keypath, "rb") as key_file:
        private_key = serialization.load_ssh_private_key(
            key_file.read(),
            None,
            default_backend()
        )

    # Sign a message using the key
    signature = private_key.sign(
        message,
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA256()
    )

    return base64.b64encode(signature).rstrip(b'=')


def create_jwt(keypath, claims):
    '''
    '''

    iss = time.time()
    head = _create_jwt_head()
    body = _create_jwt_body(claims)

    b64_head = base64.b64encode(json.dumps(head).encode('utf-8')).rstrip(b'=')
    b64_body = base64.b64encode(json.dumps(body).encode('utf-8')).rstrip(b'=')

    message = b'.'.join((b64_head, b64_body))
    checksum = _create_checksum(message, keypath)

    output = b'.'.join((b64_head, b64_body, checksum))
    return output.replace(b'+', b'-').replace(b'/', b'_')


def pubkey_info(keypath):
    with open(keypath, 'rb') as pubkey:
        public_key = serialization.load_ssh_public_key(pubkey.read())

    pn = public_key.public_numbers()
    n = base64.b64encode(str(pn.n).encode('utf-8')).decode('utf-8').rstrip('=').replace('+', '-').replace('/', '_')
    e = base64.b64encode(str(pn.e).encode('utf-8')).decode('utf-8').rstrip('=').replace('+', '-').replace('/', '_')

    return {
        'kty': 'RSA',
        'alg': '',
        'use': 'sig',
        'kid': '1',
        'n': n,
        'e': e,
    }
