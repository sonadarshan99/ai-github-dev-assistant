import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
print("TOKEN:", GITHUB_TOKEN[:10])
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
print(headers)
def get_commits(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    res = requests.get(
    url,
    headers=headers,
    timeout=30
    )

    print("Status Code:", res.status_code)

    if res.status_code != 200:
        print(res.text)
        return []

    commits = res.json()

    detailed_commits = []

    for c in commits[:3]:

        sha = c["sha"]

        detail_url = (
            f"https://api.github.com/repos/"
            f"{owner}/{repo}/commits/{sha}"
        )

        detail_res = requests.get(
            detail_url,
            headers=headers,
            timeout=30
        )

        if detail_res.status_code == 200:

            commit_data = detail_res.json()

            if "files" in commit_data:
                commit_data["files"] = commit_data["files"][:3]

            detailed_commits.append(commit_data)

    return detailed_commits