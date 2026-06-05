from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

g = Github(TOKEN)

repo = g.get_repo("sonadarshan99/ai-productivity-test")


def create_pull_request():
    branch_name = "ai-fix-branch"

    print("📌 Checking existing PRs...")

    pulls = repo.get_pulls(
        state="open",
        head=f"sonadarshan99:{branch_name}"
    )

    if pulls.totalCount > 0:
        print("♻️ PR already exists")
        return pulls[0].html_url

    print("🚀 Creating PR...")

    try:
        pr = repo.create_pull(
            title="AI Generated Fix",
            body="Auto generated PR from AI system",
            head=branch_name,
            base="main"
        )

        print("✅ PR CREATED:", pr.html_url)
        return pr.html_url

    except Exception as e:
        print("❌ PR FAILED:", e)
        return None