from sqlalchemy import Column, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from .db import Base

class CommThread(Base):
    __tablename__ = "comm_threads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_type = Column(String, nullable=False)
    object_id = Column(String, nullable=False)
    supplier_id = Column(UUID(as_uuid=True), nullable=True)
    subject = Column(Text, nullable=True)
    status = Column(String, default="open")
    created_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(TIMESTAMP)

class CommMessage(Base):
    __tablename__ = "comm_messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("comm_threads.id", ondelete="CASCADE"))
    sender_type = Column(String, nullable=False)
    sender_id = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    direction = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    status = Column(String, default="queued")
    message_metadata = Column("metadata", JSONB)
    created_at = Column(TIMESTAMP)
