import mysql.connector

def _get_conn():
    pass


def fetch_one(query):
    conn = _get_conn()

    with conn.cursor(buffered=True, namedtuple=True) as c:
        c.execute(query)
        out = c.fetchone()

    return out
