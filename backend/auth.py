from lib import flask_db
import hashlib
import string
import random

class AuthException(Exception):
    pass

def _hash_matches(hashval, password):
    chunks = hashval.split('$')
    if len(chunks) != 3:
        raise AuthException('Wrong password format')

    _, salt, _ = hashval.split('$')
    return hash_password(password, salt) == hashval


def _gen_salt(k=10):
    return ''.join(random.choices(string.printable[:36], k=k))


def hash_password(password, salt=None):
    if salt is None:
        salt = _gen_salt()

    salt_pass = (salt + password).encode('utf-8')
    hashed_pass = hashlib.sha256(salt_pass).hexdigest()
    return '$'.join(('sha256', salt, hashed_pass))


def check_password(email, password):
    match = flask_db.fetch_one(
        'select id, passwd from users where email = %s',
        (email, )
    )

    if not match:
        raise AuthException('User not found')

    if not _hash_matches(match.passwd, password):
        raise AuthException('Wrong credentials')

    return match.id
