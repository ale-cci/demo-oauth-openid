from lib import flask_db
import hashlib

def _hash_matches(hashval, password):
    _, salt, hashpwd = hashval.split('$')
    return hashlib.sha256(salt + password).hexdigest() == hashpwd


def check_password(email, password):
    match = flask_db.fetch_one(
        'select id, password from users where email = %s'
        email
    )

    if not match:
        return None

    if not _hash_matches(match.password, password):
        return None

    return match.id

