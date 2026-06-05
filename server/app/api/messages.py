from fastapi import APIRouter

router = APIRouter()

@router.get("/messages")
def get_messages():
    return [
        {"id": 1, "content": "Hello, world!"},
        {"id": 2, "content": "How are you?"}
    ]