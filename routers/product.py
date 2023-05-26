from fastapi import APIRouter, Depends, Request, HTTPException, status, File, UploadFile, Response
from sqlalchemy.orm import Session, query
from sqlalchemy import desc, asc, or_, and_
from datetime import datetime
from db import get_db
from routers import crud, token as tk
from models import (users, product, product_image, favorite, ListProducts, 
                    subcategory, district, region, addProduct, updateProduct, deleteProduct)
import shutil
import os
import sys

product_router = APIRouter()

@product_router.post('/get-products')
def get_products(header_param: Request, request: ListProducts, db: Session = Depends(get_db)):
    if request.max is None:
        request.max = 999999999
    if request.min is None:
        request.min = 0

    user_id = {"id" : -1}
    header = header_param.headers.get('WWW-Authentication')
    if header:
        token_data = tk.get_token(header_param)
        if token_data != '':
            token_dec_phone_number = tk.decode_token(token_data)
            user_id = db.query(users.id).filter(token_dec_phone_number == users.phone_number).first()

    # COLOR LIST
    if request.color_list != None:
        color_list = list(request.color_list.split(","))
        color_list = list(map(int, color_list))
    else:
        color_list = []
        for i in range(1, 100):
            color_list.append(i)
    # CATEGORY LIST
    if request.category_list != None:
        category_list = list(request.category_list.split(","))
        category_list = list(map(int, category_list))
    else:
        category_list = []
        for i in range(1, 100):
            category_list.append(i)

    # SORTING
    if request.sort == 1:
        sorting = desc(product.updated_at)
    elif request.sort == 2:
        sorting = asc(product.updated_at)
    elif request.sort == 3:
        sorting = asc(product.price)
    elif request.sort == 4:
        sorting = desc(product.price)
    else:
        sorting = asc(product.id)

    result = db.query(
        product.id,
        product.name,
        product.price,
        product_image.small_image
    ).\
    join(
        product_image, product.id == product_image.product_id
    ).\
    filter(
        or_(product.color_id == el for el in color_list),
        or_ (product.subcategory_id == el for el in category_list),
        and_(request.max>=product.price, request.min<=product.price)
    ).\
    order_by(sorting).\
    offset(
        request.limit * (request.page - 1)
    ).\
    limit(request.limit).all()

    result = crud.check(db, result, user_id)
    result = crud.distinct(result)

    if not result:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : result}

@product_router.get("/get-product-by-id")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    getProduct = db.query(
        product.id,
        product.name,
        product.description_name,
        product.price,
        product.color_id,
        product.phone_number,
        product.user_id
    ).filter(product.id == id).first()
    getCatName = db.query(
        subcategory.nametm,
        subcategory.nameru,
        subcategory.nameen
    ).filter(product.subcategory_id == id).first()

    getIsFav = db.query(
        favorite.id
    ).filter(id == favorite.product_id, getProduct.user_id == favorite.user_id).first()

    getProduct = dict(getProduct)
    getCatName = dict(getCatName)
    getProduct["category_name_tm"] = getCatName["nametm"]
    getProduct["category_name_ru"] = getCatName["nameru"]
    getProduct["category_name_en"] = getCatName["nameen"]
    if getIsFav:
        getProduct["is_favorite"] = 1
    else:
        getProduct["is_favorite"] = 0

    getProductImages = db.query(
        product_image.small_image,
        product_image.medium_image,
        product_image.large_image,
    ).filter(product_image.product_id == id).all()
    getProductImages = list(getProductImages)
    getProduct["images"] = getProductImages

    getUser = db.query(
        users.id,
        users.fullname,
        users.profile_img,
        users.phone_number,
    ).filter(getProduct["user_id"] == users.id).first()

    getDistrictID = db.query(
        users.district_id
    ).filter(getProduct["user_id"] == users.id).first()
    getRegionID = db.query(
        district.region_id
    ).filter(getDistrictID.district_id == district.id).first()

    getDistrict = db.query(
        district.nametm,
        district.nameru,
        district.nameen
    ).filter(getDistrictID.district_id == district.id).first()

    getRegion = db.query(
        region.nametm,
        region.nameru,
        region.nameen
    ).filter(getRegionID.region_id == region.id).first()
    getUser = dict(getUser)
    getDistrict = dict(getDistrict)
    getRegion = dict(getRegion)
    getUser["region"] = getRegion
    getUser["district"] = getDistrict
    getProduct["user"] = getUser
    if not getProduct:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : getProduct}

@product_router.post("/add-product")
def add_product(header_param: Request, req: addProduct, db: Session = Depends(get_db)):
    
    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)
    
    userID = db.query(
        users.id
    ).filter(users.phone_number == token_dec_phone_number).first()
    
    if not userID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_add = product(
        name = req.name,
        price = req.price,
        color_id = req.colorID,
        subcategory_id = req.subcategoryID,
        description_name = req.descriptionName,
        phone_number = req.phoneNumber,
        user_id = userID.id,
    )
    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return {"error" : False, "body" : "INSERTED"}
    else:
        return {"error" : True, "body" : "null"}
    


@product_router.post("/upload-image")
def upload_image(header_param: Request, id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)
    userID = db.query(users.id).filter(users.phone_number == token_dec_phone_number).first()
    if not userID:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    path = sys.path[0] + "\images\product_img"
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + f"\\{file.filename}"
    
    with open(path,  "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    new_add = product_image(
        small_image = file.filename,
        medium_image = file.filename,
        large_image = file.filename,
        product_id = id
    )

    if new_add:
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        return {"error" : False, "body" : "Success"}
    else:
        return {"error" : True, "body" : "NOT UPLOADED"}
    
@product_router.put("/update-product")
def update_product(req: updateProduct, db: Session = Depends(get_db)):
    result = db.query(product).filter(req.id == product.id).\
        update({product.updated_at: datetime.now()}, synchronize_session=False)
    
    db.commit()
    if result:
        return {"error" : False, "body" : "UPDATED"}
    else:
        return {"error" : True, "body" : "NOT UPDATED"}
        
@product_router.delete("/delete-product")
def delete_product(req: deleteProduct, db: Session = Depends(get_db)):
    destroy_product = db.query(product).filter(product.id == req.id).\
        delete(synchronize_session=False)
    db.commit()
    
    get_product_imgs = db.query(
        product_image.id,
        product_image.small_image,
        product_image.medium_image,
        product_image.large_image
    ).filter(product_image.product_id == req.id).all()
    
    destroy_product_img = db.query(product_image).filter(product_image.product_id == req.id).\
        delete(synchronize_session=False)
    db.commit()
    
    path = sys.path[0] + "\images\product_img"
    for img in get_product_imgs:
        path = path + f"\{img.small_image}"
        if os.path.exists(path):
            os.remove(path)
        else:
            continue
    if destroy_product_img or destroy_product:
        return {"error" : False, "body" : "DELETED"}
    else:
        return {"error" : True, "body" : "NOT DELETED"}
