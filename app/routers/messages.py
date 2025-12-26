from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import SessionLocal
from app.models import CommMessage, CommThread
from app.services.outbound import send_message
from datetime import datetime
import uuid

router = APIRouter()

class MessageCreate(BaseModel):
    thread_id: uuid.UUID
    sender_type: str
    sender_id: str | None = None
    body: str
    channel: str

@router.post("/")
def create_message(payload: MessageCreate):
    db = SessionLocal()
    try:
        thread = db.query(CommThread).filter(CommThread.id == payload.thread_id).first()
        if not thread:
            raise HTTPException(status_code=404, detail=f"Thread with id {payload.thread_id} not found")
        
        msg = CommMessage(
            thread_id=payload.thread_id,
            sender_type=payload.sender_type,
            sender_id=payload.sender_id,
            body=payload.body,
            direction="outbound",
            channel=payload.channel,
            status="queued",
            message_metadata={},
            created_at=datetime.utcnow()
        )
        db.add(msg)
        db.commit()
        db.refresh(msg)
        
        try:
            send_message(msg)
            msg.status = "sent"
            db.commit()
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            msg.status = "queued"
            db.commit()
        
        return {"id": str(msg.id), "status": msg.status}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERROR IN create_message: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
