import os
import json
from celery import Celery
from agent import analyze_event_with_gemini
from github_tools import post_github_comment

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "agent_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def process_agent_task(task_id: str, source: str, payload: dict):
    print(f"Executing task {task_id} from {source}")
    
    # 1. Cognitive Routing (Gemini analyzes the payload)
    decision_json_str = analyze_event_with_gemini(source, payload)
    print(f"Gemini Routing Decision: {decision_json_str}")
    
    # 2. Parse the JSON response
    try:
        decision = json.loads(decision_json_str)
    except json.JSONDecodeError:
        print("Error: Gemini did not return valid JSON.")
        return {"status": "failed", "reason": "Invalid JSON from LLM"}

    # 3. Execution: If this is a GitHub Issue, post a comment back
    if "issues" in source and payload.get("action") == "opened":
        repo_name = payload.get("repository", {}).get("full_name")
        issue_number = payload.get("issue", {}).get("number")
        
        if repo_name and issue_number:
            # Construct the reply using Gemini's analysis
            reply_body = (
                f"🤖 **Autonomous Agent Acknowledgment**\n\n"
                f"**Summary:** {decision.get('event_summary')}\n"
                f"**Routing:** I am assigning this to **{decision.get('assigned_agent')}**.\n"
                f"**Reasoning:** {decision.get('reasoning')}"
            )
            
            # Fire the tool
            post_github_comment(repo_name, issue_number, reply_body)

    return {"status": "success", "task_id": task_id}