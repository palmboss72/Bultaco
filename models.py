from sqlalchemy import Column, String, Integer, DateTime
from database import Base
from datetime import datetime
import uuid

class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    source = Column(String, index=True) # e.g., 'github', 'heartbeat'
    status = Column(String, default="queued") # 'queued', 'processing', 'completed', 'failed'
    raw_payload = Column(String) 
    created_at = Column(DateTime, default=datetime.utcnow)