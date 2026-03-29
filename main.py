import os
from contextlib import asynccontextmanager
from random import randint

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import database as db
import dependencies
from routers import auth, cart, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────────────────────
    conn = db.create_database()
    conn.autocommit = True
    dependencies.init_conn(conn)

    db.create_table(conn, "main")
    db.create_cart_table(conn)
    db.create_users_table(conn)

    for root, dirs, files in os.walk("static/pictures"):
        for file in files:
            db.insert_to_db(
                conn=conn,
                table="main",
                path=os.path.join(root, file),
                name=os.path.splitext(file)[0],
                price=randint(50, 200),
            )

    yield  # app is running

    # ── Shutdown ──────────────────────────────────────────────────────────────
    conn.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(cart.router)
app.include_router(auth.router)
