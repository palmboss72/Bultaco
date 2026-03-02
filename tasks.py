# ... (inside your process_agent_task function) ...
    decision = json.loads(decision_json_str)
    
    if decision.get("assigned_agent") == "Claude":
        # Ask Claude to solve the problem described in the payload
        issue_body = payload.get("issue", {}).get("body", "No description provided.")
        claude_response = call_claude_for_coding(f"Analyze this GitHub issue and provide a technical solution: {issue_body}")
        
        reply_body = f"🚀 **Claude 3.5 Sonnet Analysis:**\n\n{claude_response}"
    else:
        # Default Gemini reply
        reply_body = f"🤖 **Gemini Routing:** {decision.get('reasoning')}"

    # Fire the tool to post the comment
    post_github_comment(repo_name, issue_number, reply_body)