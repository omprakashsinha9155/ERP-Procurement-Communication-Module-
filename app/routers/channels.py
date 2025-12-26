from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_channels():
    return {"channels": ["email", "sms", "webhook", "portal", "chat"]}

