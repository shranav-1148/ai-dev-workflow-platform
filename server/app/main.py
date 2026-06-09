from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.repositories import router as repository_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.messages import router as messages_router
from app.api.users import router as users_router
from app.api.workflow import router as workflow_router



app = FastAPI()

app.include_router(health_router)
app.include_router(repository_router)
app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(messages_router)
app.include_router(users_router)
app.include_router(workflow_router)