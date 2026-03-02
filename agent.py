import os
import json
import google.generativeai as genai
import anthropic

# Setup clients
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def analyze_event_with_gemini(source: str, payload: dict) -> str:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash') # Using 1.5 for maximum stability
        system_instruction = (
            "You are a router. Analyze the GitHub payload. "
            "Return ONLY JSON with these keys: 'event_summary', 'assigned_agent', 'reasoning'. "
            "assigned_agent must be either 'Claude' (for code/bugs) or 'Gemini' (for greetings/stars)."
        )
        prompt = f"Source: {source}\nPayload: {json.dumps(payload)[:2000]}"
        
        response = model.generate_content(
            f"{system_instruction}\n\n{prompt}",
            generation_config={"response_mime_type": "application/json"}
        )
        return response.text
    except Exception as e:
        print(f"Gemini Routing Error: {e}")
        return json.dumps({"assigned_agent": "Gemini", "reasoning": "Error in routing, defaulting."})

def call_claude_for_coding(task_description: str):
    try:
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": f"You are a Senior Engineer. Provide a technical solution for: {task_description}"}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Claude API Error: {e}")
        return "I encountered an error while consulting Claude for this technical task."