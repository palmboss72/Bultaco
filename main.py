from fastapi import FastAPI, Request, BackgroundTasks, Header, HTTPException
from tasks import process_agent_task
from database import engine, Base
import models
import uuid

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autonomous Agent Gateway")

@app.post("/webhook/github")
async def github_webhook(request: Request, x_github_event: str = Header(None)):
    """Receives events from GitHub (e.g., PRs, issue comments)."""
    payload = await request.json()
    task_id = str(uuid.uuid4())
    
    # Push to Celery for background processing
    process_agent_task.delay(
        task_id=task_id, 
        source=f"github_{x_github_event}", 
        payload=payload
    )
    
    # Instantly return 200 so GitHub doesn't timeout
    return {"status": "queued", "task_id": task_id}

@app.post("/internal/heartbeat")
async def system_heartbeat(authorization: str = Header(None)):
    """Triggered by a Render Cron Job to wake the agent."""
    # Add a simple secret check here later
    task_id = str(uuid.uuid4())
    
    process_agent_task.delay(
        task_id=task_id, 
        source="heartbeat", 
        payload={"action": "check_system_state"}
    )
    
    return {"status": "heartbeat_acknowledged"}