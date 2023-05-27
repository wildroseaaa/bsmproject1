from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from db.database_conn import Base


class category(Base):
    __tablename__  = "category"
    id             = Column(Integer, primary_key=True, index=True)
    categorynametm = Column(String)
    categorynameru = Column(String)
    categorynameen = Column(String)
    status         = Column(Integer)
    category_image = Column(String)
    order_by       = Column(Integer)

class sign_up(Base):
    __tablename__ = "sign_up"
    id            = Column(Integer, primary_key=True, index=True)
    phone_number  = Column(Integer)
    code          = Column(Integer)
    time          = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class users(Base):
    __tablename__      = "users"
    id                 = Column(Integer, primary_key=True, index=True)
    fullname           = Column(String)
    address            = Column(String)
    phone_number       = Column(String)
    profile_img        = Column(String)
    usertype_id        = Column(Integer, default=1)
    district_id        = Column(Integer)
    gender             = Column(Integer, default=1)
    email              = Column(String)
    status             = Column(Integer, default=1)
    notification_token = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    token              = Column(String)

class banner(Base):
    __tablename__      = "banner"
    id                 = Column(Integer, primary_key=True, index=True)
    imagetm            = Column(String)
    imageru            = Column(String)
    imageen            = Column(String)
    order_by           = Column(Integer)
    status             = Column(Integer)
    product_id         = Column(Integer)
    category_id        = Column(Integer)
    user_id            = Column(Integer)
    site_url           = Column(String)
    product_url        = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class product(Base):
    __tablename__      = "product"
    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String)
    price              = Column(Float)
    status             = Column(Integer, default=0)
    description_name   = Column(String)
    color_id           = Column(Integer)
    subcategory_id     = Column(Integer, ForeignKey("sub_category.id"))
    phone_number       = Column(String)
    user_id            = Column(Integer)
    is_popular         = Column(Boolean, default=False)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class product_image(Base):
    __tablename__      = "product_image"
    id                 = Column(Integer, primary_key=True, index=True)
    small_image        = Column(String)
    medium_image       = Column(String)
    large_image        = Column(String)
    product_id         = Column(Integer, ForeignKey("product.id"))



class favorite(Base):
    __tablename__      = "favorite"
    id                 = Column(Integer, primary_key=True, index=True)
    product_id         = Column(Integer)
    user_id            = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())


class holiday(Base):
    __tablename__      = "holiday"
    id                 = Column(Integer, primary_key=True, index=True)
    nametm             = Column(String)
    nameru             = Column(String)
    nameen             = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class subcategory(Base):
    __tablename__      = "sub_category"
    id                 = Column(Integer, primary_key=True, index=True)
    nametm             = Column(String)
    nameru             = Column(String)
    nameen             = Column(String)
    category_id        = Column(Integer, ForeignKey("category.id"))
    status             = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class region(Base):
    __tablename__      = "region"
    id                 = Column(Integer, primary_key=True, index=True)
    nametm             = Column(String)
    nameru             = Column(String)
    nameen             = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class district(Base):
    __tablename__      = "district"
    id                 = Column(Integer, primary_key=True, index=True)
    nametm             = Column(String)
    nameru             = Column(String)
    nameen             = Column(String)
    region_id          = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class imgColor(Base):
    __tablename__      = "image_color"
    id                 = Column(Integer, primary_key=True, index=True)
    nametm             = Column(String)
    nameru             = Column(String)
    nameen             = Column(String)
    hexcode            = Column(Integer)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class congratulation(Base):
    __tablename__      = "congratulation"
    id                 = Column(Integer, primary_key=True, index=True)
    text               = Column(String)
    status             = Column(Integer)
    user_id            = Column(Integer)
    holiday_id         = Column(Integer)
    title              = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())

class constantPage(Base):
    __tablename__      = "constant_page"
    id                 = Column(Integer, primary_key=True, index=True)
    titletm            = Column(String)
    titleru            = Column(String)
    titleen            = Column(String)
    contenttm          = Column(String)
    contentru          = Column(String)
    contenten          = Column(String)
    page_type          = Column(String)
    created_at         = Column(DateTime, default=datetime.now())
    updated_at         = Column(DateTime, default=datetime.now())
    