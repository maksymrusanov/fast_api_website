def create_cart_table(conn) -> None:
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


def cart_add(conn, product_id: str, product_name: str, price: int, img: str) -> None:
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


def cart_update_qty(conn, item_id: int, qty: int) -> None:
    with conn.cursor() as cur:
        cur.execute("UPDATE cart SET qty = %s WHERE id = %s;", (qty, item_id))


def cart_remove(conn, item_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM cart WHERE id = %s;", (item_id,))


def cart_clear(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM cart;")
