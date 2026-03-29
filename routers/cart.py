from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import database as db
from dependencies import get_conn

router = APIRouter(prefix="/api/cart")


class CartAddRequest(BaseModel):
    product_id:   str
    product_name: str
    price:        int
    img:          str = ""


class CartUpdateRequest(BaseModel):
    qty: int


@router.get("")
async def cart_get(conn=Depends(get_conn)):
    return JSONResponse(db.cart_get(conn))


@router.post("", status_code=201)
async def cart_add(body: CartAddRequest, conn=Depends(get_conn)):
    db.cart_add(conn, body.product_id, body.product_name, body.price, body.img)
    return JSONResponse({"status": "ok"})


@router.patch("/{item_id}")
async def cart_update(item_id: int, body: CartUpdateRequest, conn=Depends(get_conn)):
    if body.qty < 1:
        raise HTTPException(400, "qty must be >= 1")
    db.cart_update_qty(conn, item_id, body.qty)
    return JSONResponse({"status": "ok"})


@router.delete("/{item_id}")
async def cart_remove(item_id: int, conn=Depends(get_conn)):
    db.cart_remove(conn, item_id)
    return JSONResponse({"status": "ok"})


@router.delete("")
async def cart_clear(conn=Depends(get_conn)):
    db.cart_clear(conn)
    return JSONResponse({"status": "ok"})
