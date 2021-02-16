from lib import flask_db
import hashlib

class AuthException(Exception):
    pass

def _hash_matches(hashval, password):
    chunks = hashval.split('$')
    if len(chunks) != 3:
        raise AuthException('Wrong password format')

    _, salt, hashpwd = hashval.split('$')
    salt_pass = (salt + password).encode('utf-8')
    return hashlib.sha256(salt_pass).hexdigest() == hashpwd


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
