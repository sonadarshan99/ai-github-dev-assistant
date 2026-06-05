from github_service import get_commits
from ai_service import analyze_commit
from risk_engine import compute_risk

def analyze_repository(owner, repo):

    commits = get_commits(owner, repo)

    print("COMMITS FETCHED:", len(commits))

    results = []

    for commit in commits[:3]:

        print("PROCESSING COMMIT")

        message = commit["commit"]["message"]

        try:

            files = commit.get("files", [])

            patch = ""

            for f in files[:3]:

                if "patch" in f:
                    patch += f["patch"][:500]

            analysis = analyze_commit(
                message,
                len(files),
                patch
            )

            print("AI SUCCESS")

            risk = compute_risk(analysis)

            analysis["risk_level"] = risk

            results.append({
                "message": message,
                "analysis": analysis
            })

        except Exception as e:

            print("AI ERROR:", e)

    print("RESULTS GENERATED:", len(results))

    return results