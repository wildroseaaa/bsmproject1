from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import subcategory, region, district, imgColor, category

filter_router = APIRouter()

@filter_router.get("/get-filters")
def get_filters(db: Session = Depends(get_db)):

    getColors = db.query(
        imgColor.id,
        imgColor.nametm,
        imgColor.nameru,
        imgColor.nametm,
        imgColor.hexcode
    ).all()
    getCategories = db.query(
        category.id,
        category.categorynametm,
        category.categorynameru,
        category.categorynameen,
    ).all()


    getRegions = db.query(
        region.id,
        region.nametm,
        region.nameru,
        region.nameen,
    ).all()


    newList = []
    for ctg in getCategories:
        ctgDict = dict(ctg)
        sctg = db.query(
            subcategory.id,
            subcategory.nametm,
            subcategory.nameru,
            subcategory.nameen,
        ).filter(ctg.id == subcategory.category_id).all()
        sctg = list(sctg)
        ctgDict["subcategory"] = sctg
        newList.append(ctgDict)

    getCategories = newList

    newList = []
    for reg in getRegions:
        regDict = dict(reg)
        dist = db.query(
            district.id,
            district.nametm,
            district.nameru,
            district.nameen,
        ).filter(reg.id == district.region_id).all()
        dist = list(dist)
        regDict["district"] = dist
        newList.append(regDict)
        
    getRegions = newList

    result = {"colors" : getColors, "category" : getCategories, "regions" : getRegions}
    if not result:
        return {"error" : "True", "body" : "null"}
    else:
        return {"error" : "False", "body" : result}
