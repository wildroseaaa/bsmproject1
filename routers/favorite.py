from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from routers import crud, token as tk
from models import banner, category, users, product, product_image, favorite, addFavorite
from sqlalchemy import and_, or_



favorite_router = APIRouter()

@favorite_router.get("/get-favorites")
def get_favorite(header_param: Request, page: int, limit: int, db: Session = Depends(get_db)):

    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)
    user_id = db.query(users.id).filter(users.phone_number == token_dec_phone_number).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    productIDs = db.query(favorite.product_id).filter(favorite.user_id == user_id.id).all()
    if not productIDs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product id not found")
    productIDs = crud.row2dict(productIDs)

    get_Products = db.query(
        product.id,
        product.name,
        product_image.small_image
    ).\
    join(product_image, product_image.product_id == product.id).\
    filter(or_(product.id == el for el in productIDs)).\
    offset(limit * (page - 1)).\
    limit(limit).all()
    get_Products = crud.distinct(get_Products)

    return get_Products


@favorite_router.post("/add-favorite")
def add_favorite(header_param: Request, request: addFavorite, db: Session = Depends(get_db)):

    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)

    user_id = db.query(users.id).filter(users.phone_number == token_dec_phone_number).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    favorite_id = db.query(favorite.id).filter(and_(request.product_id == favorite.product_id,\
        user_id.id == favorite.user_id)).first()
    # return request.product_id

    if not favorite_id:
        new_add = favorite(product_id = request.product_id, user_id = user_id["id"])
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        if new_add:
            return {"error" : "false", "body" : "INSERTED"}
        else:
            return {"error" : "true", "body" : "NOT INSERTED"}


@favorite_router.delete("/delete-favorite")
def destroy_favorite(header_param: Request, request: addFavorite, db: Session = Depends(get_db)):
    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)

    user_id = db.query(users.id).filter(users.phone_number == token_dec_phone_number).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    destroy = db.query(favorite).filter(and_(request.product_id == favorite.product_id,\
        user_id.id == favorite.user_id)).delete(synchronize_session=False)
    db.commit()
    if destroy:
        return {"error" : "false", "body" : "DELETED"}
    else:
        return {"error" : "true", "body" : "NOT DELETED"}
