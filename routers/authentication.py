from datetime import datetime
from fastapi import APIRouter, Depends, Request
from models import sign_up, users, CreateUser
from sqlalchemy.orm import Session
from db import get_db
from routers import token as tk
import random
import models


authentication_router = APIRouter()


@authentication_router.post('/phone-verification')
def post_phone_verification(request: models.phone_verification, db: Session = Depends(get_db)):
    check = db.query(sign_up).filter(sign_up.phone_number == request.phone_number).all()
    generated_code = random.randint(1000, 9999)

    if not check:
        new_add = sign_up(phone_number = request.phone_number, code = generated_code, time = datetime.now())
        db.add(new_add)
        db.commit()
        db.refresh(new_add)
        if new_add:
            return {"error" : "false", "body" : "new"}
        else:
            return {"error" : "true", "body" : "null"}
    else:
        new_update = db.query(sign_up).filter(sign_up.phone_number == request.phone_number).\
            update({sign_up.code: generated_code, sign_up.time: datetime.now()}, \
                synchronize_session=False)
        db.commit()
        if new_update:
            return {"error" : "false", "body" : "update"}
        else:
            return {"error" : "true", "body" : "null"}


@authentication_router.post('/code-verification')
def post_code_verification(request: models.code_verification, db: Session = Depends(get_db)):

    # check spelling of phone number and verification code
    check_ver_code     = db.query(sign_up.phone_number).filter(sign_up.code == request.code).first()
    check_phone_number = db.query(sign_up.code).filter(sign_up.phone_number == request.phone_number).first()
    if not check_phone_number:
        return {"error" : "true", "body" : "Incorrect phone number"}
    elif not check_ver_code:
        return {"error" : "true", "body" : "Incorrect verification code"}
    elif (not check_ver_code)and(not check_phone_number):
        return {"error" : "true", "body" : "Incorrect phone number and verification code"}


    # check request time less than 3 minutes
    check_time = db.query(sign_up.time).filter(sign_up.phone_number == request.phone_number, \
        sign_up.code == request.code).first()
    h_table   = check_time.time.hour
    min_table = check_time.time.minute
    sec_table = check_time.time.second
    h_now     = datetime.now().hour
    min_now   = datetime.now().minute
    sec_now   = datetime.now().second
    all_of_minute_table = h_table * 60 + min_table + (sec_table / 60)
    all_of_minute_now   = h_now   * 60 + min_now   + (sec_now   / 60)
    diff = abs(all_of_minute_now - all_of_minute_table)
    if diff >= 3:
        return {"error" : "true", "body" : "TIMEOUT"}


    # check user have in the table users
    check_user = db.query(users).filter(users.phone_number == request.phone_number).all()
    if not check_user:

        access_token = tk.create_access_token(data={"sub": request.phone_number})

        return {"error" : "false", "body" : {"sign_in" : "false", "user" : {"token" : access_token}}}
    else:
        return {"error" : "false", "body" : {"sign_in" : "false", "user" : check_user[0]}}



@authentication_router.post('/create_user')
def create_user(header_param: Request, request: CreateUser, db: Session = Depends(get_db)):


    token_data = tk.get_token(header_param)
    token_dec_phone_number = tk.decode_token(token_data)

    if token_dec_phone_number == request.phone_number:
        new_add = users(fullname = request.fullname,
                        token = token_data,
                        phone_number = request.phone_number)
        if new_add:
            db.add(new_add)
            db.commit()
            db.refresh(new_add)
            return {"error" : "false", "body" : "INSERTED"}
        else:
            return {"error" : "true", "body" : "null"}
    else:
        return {"error" : "true", "body" : "null"}


@authentication_router.get('/phone-verification')
def get_phone_verification(db: Session = Depends(get_db)):
    return db.query(sign_up).all()
