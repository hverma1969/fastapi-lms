from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# ✅ Correctly import routers from their location
from app.auth.auth_router import router as auth_router
from app.database import Base, engine
from app.models import course
from app.routes import user_routes
# If you have course_router.py inside routes (create it if missing):
from app.routes.course_router import router as course_router
from app.routes.lesson_routes import router as lesson_router
from app.routes.question_router import router as question_router
from app.routes.quiz_router import router as quiz_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_routes.router)
app.include_router(auth_router, prefix="/auth")
app.include_router(course_router, prefix="/courses")
app.include_router(lesson_router, prefix="/lesson")
app.include_router(quiz_router, prefix="/quiz")
app.include_router(question_router, prefix="/question")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="LMS API",
        version="1.0.0",
        description="Secure LMS with Auth",
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
