import os

SECRET_KEY     = os.getenv("SECRET_KEY", "nike-secret-change-in-production")
ALGORITHM      = "HS256"
TOKEN_EXPIRE_H = 24
COOKIE_NAME    = "nike_token"
