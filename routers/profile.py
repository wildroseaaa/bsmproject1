from fastapi import APIRouter, Depends, UploadFile, File, Request
from sqlalchemy.orm import Session
from db import get_db
from models import users, product, UserList, holiday, updateProfile
from routers import crud, token as tk
import os
import sys
import shutil


profile_router = APIRouter()

@profile_router.post("/get-profile")
def get_profile(request: UserList, db: Session = Depends(get_db)):

    getUser = db.query(
        users.id,
        users.fullname,
        users.phone_number,
        users.address,
        users.profile_img,
        users.usertype_id,
        users.district_id,
        users.gender,
        users.email,
        users.status,
        users.token,
        users.notification_token,
        users.created_at,
        users.updated_at
    ).filter(users.id == request.id).first()
    if not getUser:
        return {"error" : "True", "body" : "null"}


    getProducts = db.query(
      product.id,
      product.name,
      product.price,
      product.status,
      product.description_name,
      product.color_id,
      product.subcategory_id,
      product.user_id,
      product.is_popular,
      product.created_at,
      product.updated_at
    ).filter(product.user_id == request.id).all()
    if not getProducts:
        return {"error" : "True", "body" : "null"}


    getHolidays = db.query(
        holiday.id,
        holiday.nametm,
        holiday.nameru,
        holiday.nameen,
    ).all()
    if not getHolidays:
        return {"error" : "True", "body" : "null"}

    getUser = dict(getUser)
    getProducts = list(getProducts)
    getHolidays = list(getHolidays)
    getUser['products'] = getProducts
    getUser['holidays'] = getHolidays

    if not getUser:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : getUser}

@profile_router.put("/update-profile-image")
def update_profile_image(header_param: Request, db: Session = Depends(get_db), file: UploadFile = File(...)):

    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)

    path = sys.path[0] + "\images\profile_img"
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + f"\\{file.filename}"
    
    with open(path,  "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    new_update = db.query(users).filter(users.phone_number == token_dec_phone_number).\
        update({users.profile_img: file.filename}, synchronize_session=False)
    db.commit()
    if new_update:
        return {"error" : "False", "body" : "UPDATED"}
    else:
        return {"error" : "True", "body" : "NOT UPDATED"}

@profile_router.put("/update_profile")
def update_profile(header_param: Request, request: updateProfile, db: Session = Depends(get_db)):

    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)

    new_update = db.query(users).filter(users.phone_number == token_dec_phone_number).\
        update({users.email: request.email, users.fullname: request.fullname,\
            users.district_id: request.district_id}, synchronize_session=False)
    db.commit()
    if new_update:
        return {"error" : "False", "body" : "UPDATED"}
    else:
        return {"error" : "True", "body" : "NOT UPDATED"}
