from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from sqlalchemy import desc
from routers import crud
from models import category
from models import subcategory
from models import  product
from models import product_image


category_router = APIRouter()

@category_router.get("/get-categories")
def get_categories(page: int, limit: int, db: Session = Depends(get_db)):
    category_json = db.query(
                        category.id,
                        category.categorynametm,
                        category.categorynameru,
                        category.categorynameen,
                        category.status
                    ).order_by(desc(category.order_by)).\
                            offset(limit * (page - 1)).\
                                limit(limit).all()
    category_json = crud.category_image(db, category_json)
    if not category_json:
        category_list = {'error' : 'true', 'body' : None}
    else:
        category_list = {'error' : 'false', 'body' : {'category' : category_json}}
    return category_list

