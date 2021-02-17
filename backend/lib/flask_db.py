import flask
import mysql.connector

def _get_conn():
    if not hasattr(flask.g, 'mysql_conn'):
        conn = mysql.connector.connect(
            user='user',
            database='db_name',
            password='password',
            host='db',
            port=3306
        )
        flask.g.mysql_conn = conn
        conn.autocommit = True

    return flask.g.mysql_conn


def fetch_one(query, params):
    conn = _get_conn()

    with conn.cursor(buffered=True, named_tuple=True) as c:
        c.execute(query, params)
        out = c.fetchone()

    return out


def fetch_all(query, params):
    conn = _get_conn()

    with conn.cursor(buffered=True, named_tuple=True) as c:
        c.execute(query, params)
        out = c.fetchall()

    return out


def insert(query, params):
    conn = _get_conn()
    with conn.cursor() as c:
        c.execute(query, params)
        out = c.lastrowid
    return out


def delete(query, params):
    conn = _get_conn()
    with conn.cursor() as c:
        c.execute(query, params)
        out = c.rowcount
    return out
