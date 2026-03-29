import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_database():

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port="5432",
    )
    return conn


conn = create_database()
conn.autocommit = True


def create_table(conn, table):
    with conn.cursor() as cur:
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table} (id serial PRIMARY KEY, name text, path text unique, price int);"
        )
        print(f"Table '{table}' created ")
    return table


def delete_table(conn, table):
    with conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")

    print(f"Table '{table}' deleted ")


def insert_to_db(conn, table, name, path, price):
    with conn.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO {table} (name,path,price) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (name, path, price),
        )


def get_info(conn, table):
    with conn.cursor() as curr:
        curr.execute(f"select path from {table};")
        data = [row[0] for row in curr.fetchall()]
        return data


# ── CART ──────────────────────────────────────────────────────────────────────

def create_cart_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id           SERIAL PRIMARY KEY,
                product_id   TEXT NOT NULL UNIQUE,
                product_name TEXT NOT NULL,
                price        INT  NOT NULL,
                img          TEXT NOT NULL DEFAULT '',
                qty          INT  NOT NULL DEFAULT 1 CHECK (qty >= 1)
            );
        """)


def cart_add(conn, product_id: str, product_name: str, price: int, img: str):
    """Insert new item or increment qty if already present."""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO cart (product_id, product_name, price, img, qty)
            VALUES (%s, %s, %s, %s, 1)
            ON CONFLICT (product_id)
            DO UPDATE SET qty = cart.qty + 1;
        """, (product_id, product_name, price, img))


def cart_get(conn) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("SELECT id, product_id, product_name, price, img, qty FROM cart ORDER BY id;")
        rows = cur.fetchall()
    return [
        {"id": r[0], "product_id": r[1], "name": r[2], "price": r[3], "img": r[4], "qty": r[5]}
        for r in rows
    ]


def cart_update_qty(conn, item_id: int, qty: int):
    with conn.cursor() as cur:
        cur.execute("UPDATE cart SET qty = %s WHERE id = %s;", (qty, item_id))


def cart_remove(conn, item_id: int):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM cart WHERE id = %s;", (item_id,))


def cart_clear(conn):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM cart;")
