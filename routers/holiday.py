from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, distinct, or_, and_
from db import get_db
from routers import crud, token as tk
from models import holiday, congratulation, holidayList

holiday_router = APIRouter()

@holiday_router.get("/get-holidays")
def get_holidays(db: Session = Depends(get_db)):
    result = db.query(holiday).all()
    if not result:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : result}

@holiday_router.post("/get-congratulations")
def get_congratulations(request: holidayList, db: Session = Depends(get_db)):
    result = db.query(
        congratulation.id,
        congratulation.text,
        congratulation.status,
        congratulation.user_id,
        congratulation.holiday_id,
        congratulation.title
    ).filter(request.holiday_id == congratulation.holiday_id).\
        offset(request.limit * (request.page - 1)).\
            limit(request.limit).all()
    if not result:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : result}
