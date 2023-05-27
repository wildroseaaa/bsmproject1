from typing import Optional
from pydantic import BaseModel



class phone_verification(BaseModel):
    phone_number : str



class code_verification(BaseModel):
    phone_number : str
    code         : int


class TokenData(BaseModel):
    phone_number: Optional[str] = None


class CreateUser(BaseModel):
    fullname     : str
    phone_number : str

    class Config:
        orm_mode = True

class ListProducts(BaseModel):
    limit          : int
    page           : int
    sort           : int = None
    max            : int = None
    min            : int = None
    color_list     : str = None
    category_list  : str = None
    district_id    : int = None

    class Config:
        orm_mode = True

class addFavorite(BaseModel):
    product_id     : int

    class Config:
        orm_mode = True

class UserList(BaseModel):
    id : int

    class Config:
        orm_mode = True


class holidayList(BaseModel):
    holiday_id     : int
    limit          : int
    page           : int

    class Config:
        orm_mode = True

class updateProfile(BaseModel):
    email          : str
    fullname       : str
    district_id    : int

    class Config:
        orm_mode = True

class addProduct(BaseModel):
    name           : str
    price          : float
    colorID        : int
    subcategoryID  : int
    descriptionName: str
    phoneNumber    : str
    
    class Config:
        orm_mode = True
        
class updateProduct(BaseModel):
    id             : int
    
    class Config:
        orm_mode = True

class deleteProduct(BaseModel):
    id             : int
    
    class Config:
        orm_mode = True
        
