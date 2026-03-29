from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, EmailStr

import database as db
import auth
from dependencies import get_conn

router = APIRouter(prefix="/api/auth")


class RegisterRequest(BaseModel):
    username: str
    email:    EmailStr
    password: str


class LoginRequest(BaseModel):
    email:    EmailStr
    password: str


@router.post("/register", status_code=201)
async def register(body: RegisterRequest, response: Response, conn=Depends(get_conn)):
    if len(body.username.strip()) < 2:
        raise HTTPException(400, "Username must be at least 2 characters")
    if len(body.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    if db.get_user_by_email(conn, body.email):
        raise HTTPException(409, "Email already registered")
    user = db.create_user(conn, body.username.strip(), body.email, body.password)
    auth.set_auth_cookie(response, user["id"])
    return {"id": user["id"], "username": user["username"], "email": user["email"]}


@router.post("/login")
async def login(body: LoginRequest, response: Response, conn=Depends(get_conn)):
    user = db.get_user_by_email(conn, body.email)
    if not user or not db.verify_password(body.password, user["password_hash"]):
        raise HTTPException(401, "Invalid email or password")
    auth.set_auth_cookie(response, user["id"])
    return {"id": user["id"], "username": user["username"], "email": user["email"]}


@router.post("/logout")
async def logout(response: Response):
    from config import COOKIE_NAME
    response.delete_cookie(COOKIE_NAME)
    return {"status": "ok"}


@router.get("/me")
async def me(request: Request, conn=Depends(get_conn)):
    user = auth.get_current_user(request, conn)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user
