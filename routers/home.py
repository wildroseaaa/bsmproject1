from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, distinct, func
from db import get_db
from sqlalchemy import or_
from models import banner, category, users, product, product_image, favorite
from routers import crud, token as tk



home_router = APIRouter()

@home_router.get('/get-home')
def home(header_param: Request, db: Session = Depends(get_db)):

    user_id = {"id" : -1}
    header = header_param.headers.get('WWW-Authentication')
    if header:
        token_data = tk.get_token(header_param)
        if token_data != '':
            token_dec_phone_number = tk.decode_token(token_data)
            user_id = db.query(users.id).filter(users.phone_number == token_dec_phone_number).first()
            if not user_id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


    banner_get = db.query(banner.id,
                          banner.status,
                          banner.product_id,
                          banner.category_id,
                          banner.user_id).all()
    for i in range(len(banner_get)):
        i_dict = dict(banner_get[i])
        product_url = "product?"
        for j in i_dict.keys():
            if i_dict[j]:
                product_url = product_url + j + '=' + str(i_dict[j]) + '&'
        product_url = product_url[:-1]
        db.query(banner).filter(banner.id == i+1).\
            update({banner.product_url: product_url}, synchronize_session=False)
        db.commit()
    banner_json = db.query(banner.id,
                           banner.imagetm,
                           banner.imageru,
                           banner.imageen,
                           banner.product_url,
                           banner.site_url).all()

    category_json = db.query(category.id,
                             category.categorynametm,
                             category.categorynameru,
                             category.categorynameen,
                             category.category_image).filter(or_(category.id == 1, category.id == 15,
                                                             category.id == 22, category.id == 25)).all()

    vipUsers_json = db.query(users.id, users.fullname, users.profile_img).\
        filter(users.usertype_id == 3).all()

    newProducts_json = db.query(
                                product.id,
                                product.name,
                                product.price,
                                product_image.small_image).\
                                    join(product_image, product.id == product_image.product_id).\
                                        order_by(desc(product.updated_at)).\
                                                limit(20).all()
    newProducts_json = crud.check(db, newProducts_json, user_id)
    newProducts_json = crud.distinct(newProducts_json)

    trendProducts_json = db.query(product.id,
                                  product.name,
                                  product.price,
                                  product_image.small_image).\
                                    join(product_image, product_image.product_id == product.id).\
                                      filter(product.is_popular == True).all()
    trendProducts_json = crud.check(db, trendProducts_json, user_id)
    trendProducts_json = crud.distinct(trendProducts_json)

    json = {"error" : "false", "body" : {"banner" : banner_json, "static_category" : category_json,
                                         "vip_users" : vipUsers_json, "new_products" : newProducts_json,
                                         "trend_products" : trendProducts_json}}
    if not json:
        return {"error" : "true", "body" : "null"}
    else:
        return json
