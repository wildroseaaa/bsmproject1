from fastapi import FastAPI
from routers import authentication_router
from routers import category_router
from routers import home_router
from routers import favorite_router
from routers import product_router
from routers import profile_router
from routers import filter_router
from routers import holiday_router
from routers import constant_router

app = FastAPI()


app.include_router(authentication_router, tags=["Authentication"])
app.include_router(category_router,       tags=["Category"])
app.include_router(home_router,           tags=["Home"])
app.include_router(favorite_router,       tags=["Favorites"])
app.include_router(product_router,        tags=["Products"])
app.include_router(profile_router,        tags=["Profile"])
app.include_router(filter_router,         tags=["Filter"])
app.include_router(holiday_router,        tags=["Holiday"])
app.include_router(constant_router,       tags=["Constant"])
