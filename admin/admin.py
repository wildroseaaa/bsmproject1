from fastapi_admin.app import app as admin_app
from fastapi_admin.template import templates
from starlette.requests import Request
from fastapi import Depends
from fastapi_admin.depends import get_current_admin


@admin_app.get("/", dependencies=[Depends(get_current_admin)])
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", context={"request": request})
