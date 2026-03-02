import os
from celery import Celery
from agent import analyze_event_with_gemini

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "agent_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def process_agent_task(task_id: str, source: str, payload: dict):
    print(f"Executing task {task_id} from {source}")
    
    # 1. Cognitive Routing
    decision_json = analyze_event_with_gemini(source, payload)
    
    # Log the output so we can see Gemini's decision in the Render dashboard
    print(f"Gemini Routing Decision: {decision_json}")
    
    # 2. (Future) Execute the tool or API call for the assigned_agent
    
    return {"status": "success", "task_id": task_id, "decision": decision_json}