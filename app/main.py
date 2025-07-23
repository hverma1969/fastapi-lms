import os

from fastapi import Depends, FastAPI, Form, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.auth.auth_router import router as auth_router
from app.db_connection import Base, engine, get_db
from app.models.user import User
from app.routes import (course_router, dashboard_routes, progress_routes,
                        user_routes)
from app.routes.lesson_routes import router as lesson_router
from app.routes.quiz_router import router as quiz_router

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Base.metadata.create_all(bind=engine)


app.include_router(progress_routes.router,
                   prefix="/progress", tags=["Progress"])

app.include_router(user_routes.router)
app.include_router(auth_router)
app.include_router(dashboard_routes.router)
app.include_router(course_router.router)
app.include_router(lesson_router)
app.include_router(quiz_router)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR,
          "../static")), name="static")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FanTV AI",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/register")
async def register_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(
        User.email == email).first()
    if existing_user:
        return HTMLResponse(content="<h3>Email already registered. Please login.</h3>", status_code=400)

    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse(url="/static/login.html", status_code=status.HTTP_302_FOUND)
