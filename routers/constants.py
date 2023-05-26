from fastapi import APIRouter, Depends, Request, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from db import get_db
from models import constantPage as ConsP

constant_router = APIRouter()

@constant_router.get("/get-constant")
def get_constant(type: str, db: Session = Depends(get_db)):
    result = db.query(
        ConsP.id,
        ConsP.titletm,
        ConsP.titleru,
        ConsP.titleen,
        ConsP.contenttm,
        ConsP.contentru,
        ConsP.contenten,
    ).filter(ConsP.page_type == type).all()
    if result:
        return {"error" : False, "body" : result}
    else:
        return {"error" : True, "body" : "null"}
