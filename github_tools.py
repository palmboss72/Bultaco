import os
from github import Github

def post_github_comment(repo_name: str, issue_number: int, comment_body: str):
    """
    Allows the agent to post a comment on a GitHub issue or PR.
    repo_name format: 'palmboss72/Bultaco'
    """
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN not found in environment.")
        return
        
    try:
        g = Github(token)
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(number=issue_number)
        issue.create_comment(comment_body)
        print(f"Successfully posted comment to {repo_name} issue #{issue_number}")
    except Exception as e:
        print(f"Failed to post comment: {e}")