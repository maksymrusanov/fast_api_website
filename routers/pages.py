from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.connection import create_database
from database.products import get_info

conn = create_database()
templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    info = get_info(conn, "main")
    return templates.TemplateResponse(
        request, name="index.html", context={"products": info}
    )


@router.get("/bucket", response_class=HTMLResponse)
async def bucket(request: Request):
    return templates.TemplateResponse(request, name="bucket.html")


@router.get("/contact", response_class=HTMLResponse)
async def contacts(request: Request):
    return templates.TemplateResponse(request, name="contact.html")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, name="login.html")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, name="register.html")
