from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import SessionLocal
from app.models import CommThread
import uuid
import datetime

router = APIRouter()

class ThreadCreate(BaseModel):
    object_type: str
    object_id: str
    supplier_id: uuid.UUID | None = None
    subject: str | None = None
    created_by: uuid.UUID | None = None

@router.post("/", response_model=dict)
def create_thread(payload: ThreadCreate):
    db = SessionLocal()
    try:
        thread = CommThread(
            object_type=payload.object_type,
            object_id=payload.object_id,
            supplier_id=payload.supplier_id,
            subject=payload.subject,
            created_by=payload.created_by,
            status="open",
            created_at=datetime.datetime.utcnow()
        )
        db.add(thread)
        db.commit()
        db.refresh(thread)
        return {"id": str(thread.id)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        db.close()



