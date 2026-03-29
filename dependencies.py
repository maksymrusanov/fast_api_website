"""
Shared FastAPI dependencies.
`get_conn` yields the single psycopg2 connection so routers
never have to import or reference it directly.
"""

_conn = None


def init_conn(connection) -> None:
    global _conn
    _conn = connection


def get_conn():
    return _conn
