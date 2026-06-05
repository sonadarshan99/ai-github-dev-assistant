from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo("sonadarshan99/ai-productivity-test")


def push_ai_fix_file(content="AI fix commit"):
    branch = "ai-fix-branch"

    try:
        repo.create_file(
            path="ai_fix.txt",
            message="AI generated fix commit",
            content=content,
            branch=branch
        )
        print("✅ Commit pushed to branch")

    except Exception as e:
        print("❌ Commit failed:", e)