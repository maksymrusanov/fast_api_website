import bcrypt


def create_users_table(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT to_regclass('public.users');")
        exists = cur.fetchone()[0]
        if not exists:
            cur.execute("DROP SEQUENCE IF EXISTS users_id_seq CASCADE;")
            cur.execute("""
                CREATE TABLE users (
                    id            SERIAL PRIMARY KEY,
                    username      TEXT NOT NULL,
                    email         TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at    TIMESTAMPTZ DEFAULT NOW()
                );
            """)


def create_user(conn, username: str, email: str, password: str) -> dict:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) "
            "VALUES (%s, %s, %s) RETURNING id, username, email;",
            (username, email, hashed),
        )
        row = cur.fetchone()
    return {"id": row[0], "username": row[1], "email": row[2]}


def get_user_by_email(conn, email: str) -> dict | None:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, username, email, password_hash FROM users WHERE email = %s;",
            (email,),
        )
        row = cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "username": row[1], "email": row[2], "password_hash": row[3]}


def get_user_by_id(conn, user_id: int) -> dict | None:
    with conn.cursor() as cur:
        cur.execute("SELECT id, username, email FROM users WHERE id = %s;", (user_id,))
        row = cur.fetchone()
    if not row:
        return None
    return {"id": row[0], "username": row[1], "email": row[2]}


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())
