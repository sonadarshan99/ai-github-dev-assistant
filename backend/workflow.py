from github_service import get_commits
from ai_service import analyze_commit

print("\nFetching commits...\n")

commits = get_commits(
    "microsoft",
    "vscode"
)

latest_commit = commits[0]["commit"]["message"]

print("LATEST COMMIT:")
print(latest_commit)

print("\nAnalyzing commit...\n")

analysis = analyze_commit(
    latest_commit
)

print(analysis)