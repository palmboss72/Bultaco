import os
import json
import google.generativeai as genai

# Configure the SDK with the key from Render's environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def analyze_event_with_gemini(source: str, payload: dict) -> str:
    """
    Uses Gemini to read the webhook payload and decide the next action.
    """
    try:
        # Using flash for fast routing decisions
        model = genai.GenerativeModel('gemini-2.5-flash') 
        
        system_instruction = (
            "You are the Cognitive Routing Engine for an autonomous agent. "
            "Analyze the incoming webhook payload. "
            "1. Determine the event type (e.g., push, pull_request, issue) and summarize what happened. "
            "2. Decide which sub-agent should handle it: "
            "   - 'Claude' for complex code generation, refactoring, or reviewing PRs. "
            "   - 'Manus' for external operations, browser tasks, or deployment. "
            "   - 'Gemini' for general reasoning, text processing, or if no action is needed. "
            "Respond in strict JSON format using this schema: "
            "{'event_summary': '...', 'assigned_agent': '...', 'reasoning': '...'}"
        )
        
        # Truncate payload to avoid overloading the context window with massive commits
        prompt = f"Source: {source}\n\nPayload:\n{json.dumps(payload)[:5000]}" 
        
        response = model.generate_content(
            f"{system_instruction}\n\n{prompt}",
            generation_config={"response_mime_type": "application/json"}
        )
        
        return response.text
    except Exception as e:
        return json.dumps({"error": str(e), "assigned_agent": "none"})