from sqlalchemy.orm import Session
from models import category
from models import favorite
from models import subcategory
from models import product
from models import product_image


def check(db: Session, json, user_id):
    newList = []
    user_id = dict(user_id)
    for i in json:
        newD = dict(i)
        getF = db.query(favorite.id).filter(favorite.product_id == newD["id"], favorite.user_id == user_id["id"]).first()
        if getF:
            newD["is_favorite"] = 1
        else:
            newD["is_favorite"] = 0
        newList.append(newD)
    return newList

def distinct(json):
    newList = []
    for i in json:
        if i in newList:
            continue
        else:
            newList.append(i)
    return newList

def row2dict(json):
    newList = []
    for i in json:
        newD = dict(i)
        newList.append(newD["product_id"])
    return newList


def category_image(db: Session, json):
    result_joins = db.query(category.id.label("category"), subcategory.id.label("subcategory"), 
                      product.id.label("product"), product_image.id.label("product_image")).\
        join(subcategory, subcategory.category_id == category.id).\
            join(product, product.subcategory_id == subcategory.id).\
            join(product_image, product_image.product_id == product.id).all()
    newList = []
    for elem in json:
        newD = dict(elem)
        imgList = []
        k = 0
        for result in result_joins:
            if  k == 3:
                break
            if result.category != newD["id"]:
                continue
            id = result.product_image
            getIMG = db.query(product_image.small_image).filter(product_image.id == id).first()
            getIMG = dict(getIMG)
            imgList.append(getIMG["small_image"])
            k = k + 1
        newD["images"] = imgList
        newList.append(newD)
    return newList