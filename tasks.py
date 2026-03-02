import os
import json
from celery import Celery
from agent import analyze_event_with_gemini, call_claude_for_coding
from github_tools import post_github_comment

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("agent_tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task
def process_agent_task(task_id: str, source: str, payload: dict):
    print(f"--- Processing Task {task_id} ---")
    
    # 1. Triage
    decision_str = analyze_event_with_gemini(source, payload)
    print(f"Routing Decision: {decision_str}")
    
    try:
        decision = json.loads(decision_str)
    except:
        decision = {"assigned_agent": "Gemini", "reasoning": "Failed to parse decision."}

    # 2. Identify Target
    repo_name = payload.get("repository", {}).get("full_name")
    issue_number = payload.get("issue", {}).get("number")

    if not repo_name or not issue_number:
        print("Missing repo_name or issue_number. Stopping.")
        return

    # 3. Execution
    if decision.get("assigned_agent") == "Claude":
        issue_body = payload.get("issue", {}).get("body", "No description.")
        response_text = call_claude_for_coding(issue_body)
        final_comment = f"🚀 **Claude 3.5 Sonnet Engineer:**\n\n{response_text}"
    else:
        final_comment = f"🤖 **Gemini Assistant:**\n\n{decision.get('reasoning')}"

    # 4. Post back to GitHub
    print(f"Attempting to post to {repo_name} issue #{issue_number}...")
    post_github_comment(repo_name, issue_number, final_comment)
    
    return {"status": "complete"}