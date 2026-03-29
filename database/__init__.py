"""
database package — re-exports all public functions so existing
code using `import db` can switch to `import database as db`
with no other changes.
"""

from database.connection import create_database
from database.products import create_table, delete_table, get_info, insert_to_db
from database.cart import (
    cart_add,
    cart_clear,
    cart_get,
    cart_remove,
    cart_update_qty,
    create_cart_table,
)
from database.users import (
    create_user,
    create_users_table,
    get_user_by_email,
    get_user_by_id,
    verify_password,
)

__all__ = [
    # connection
    "create_database",
    # products
    "create_table",
    "delete_table",
    "get_info",
    "insert_to_db",
    # cart
    "create_cart_table",
    "cart_add",
    "cart_get",
    "cart_update_qty",
    "cart_remove",
    "cart_clear",
    # users
    "create_users_table",
    "create_user",
    "get_user_by_email",
    "get_user_by_id",
    "verify_password",
]
