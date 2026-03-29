from datetime import datetime, timedelta, timezone

from fastapi import Request, Response
from jose import JWTError, jwt

import database as db
from config import ALGORITHM, COOKIE_NAME, SECRET_KEY, TOKEN_EXPIRE_H


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_H)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def set_auth_cookie(response: Response, user_id: int) -> None:
    token = create_token(user_id)
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        max_age=TOKEN_EXPIRE_H * 3600,
        samesite="lax",
    )


def get_current_user(request: Request, conn) -> dict | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    try:
        payload  = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id  = int(payload["sub"])
        return db.get_user_by_id(conn, user_id)
    except (JWTError, KeyError, ValueError):
        return None
