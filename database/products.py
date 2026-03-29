def create_table(conn, table: str) -> str:
    with conn.cursor() as cur:
        cur.execute(
            f"CREATE TABLE IF NOT EXISTS {table} "
            f"(id serial PRIMARY KEY, name text, path text unique, price int);"
        )
        print(f"Table '{table}' created ")
    return table


def delete_table(conn, table: str) -> None:
    with conn.cursor() as cur:
        cur.execute(f"DROP TABLE IF EXISTS {table};")
    print(f"Table '{table}' deleted ")


def insert_to_db(conn, table: str, name: str, path: str, price: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO {table} (name, path, price) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            (name, path, price),
        )


def get_info(conn, table: str) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, path, price FROM {table};")
        rows = cur.fetchall()
        return [{"id": r[0], "name": r[1], "path": r[2], "price": r[3]} for r in rows]
