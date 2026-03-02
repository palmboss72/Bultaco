def analyze_event_with_gemini(source: str, payload: dict) -> str:
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # We add a 'System Instruction' to be extremely strict
        prompt = (
            "SYSTEM: You are a JSON-only response engine. "
            "Analyze this GitHub event. Return ONLY a JSON object. "
            "Do NOT include backticks, markdown, or 'Here is your JSON'.\n"
            f"DATA: Source: {source}, Payload: {json.dumps(payload)[:1500]}\n"
            "JSON STRUCTURE: {'event_summary': '...', 'assigned_agent': 'Claude', 'reasoning': '...'}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Clean up the response just in case Gemini adds markdown backticks
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        return clean_text
    except Exception as e:
        print(f"CRITICAL ROUTING ERROR: {e}")
        return json.dumps({"assigned_agent": "Gemini", "reasoning": "Routing failed."})