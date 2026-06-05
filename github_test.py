from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

g = Github(TOKEN)

repo = g.get_repo(
    "sonadarshan99/ai-productivity-test"
)

print("Connected Successfully!")
print(repo.full_name)