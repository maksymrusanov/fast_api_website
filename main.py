import os
from random import randint

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import db

app = FastAPI()
router = APIRouter()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = db.create_database()
conn.autocommit = True
db_table = db.create_table(conn, "fastapi")


folder = "static/pictures"

for root, dirs, files in os.walk(folder):
    for file in files:
        db.insert_to_db(
            conn=conn,
            table="fastapi",
            path=os.path.join(root, file),
            name=os.path.splitext(file)[0],
            price=randint(50, 200),
        )


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request, name="index.html")


@app.get("/bucket", response_class=HTMLResponse)
async def bucket(request: Request):
    return templates.TemplateResponse(request, name="bucket.html")


@app.get("/contact", response_class=HTMLResponse)
async def contacts(request: Request):
    return templates.TemplateResponse(request, name="contact.html")
