from fastapi import APIRouter, HTTPException
from app.db import SessionLocal
from app.models import CommMessage
from app.services.events import publish_event

router = APIRouter()

@router.post("/emit/{message_id}")
def emit_message_event(message_id: str):
    db = SessionLocal()
    try:
        msg = db.query(CommMessage).filter(CommMessage.id == message_id).first()
        if not msg:
            raise HTTPException(status_code=404, detail=f"Message with id {message_id} not found")
        
        publish_event("comm.message.sent", {
            "message_id": str(msg.id),
            "thread_id": str(msg.thread_id),
            "channel": msg.channel,
            "body": msg.body
        })
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        db.close()
