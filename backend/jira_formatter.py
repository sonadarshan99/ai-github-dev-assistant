def generate_jira_tasks(analysis_data):

    tasks = []

    for i, analysis in enumerate(analysis_data):

        task = {
            "jira_key": f"AI-{100+i}",
            "summary": analysis.get("summary"),
            "issue_type": analysis.get("category"),
            "priority": analysis.get("priority"),
            "status": "To Do",
            "risk_score": analysis.get("risk_score")
        }

        tasks.append(task)

    return tasks