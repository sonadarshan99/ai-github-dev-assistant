def compute_risk(analysis):

    score = analysis.get("risk_score", 0)
    category = analysis.get("category", "").lower()
    summary = analysis.get("summary", "").lower()

    if "memory leak" in summary:
        score = max(score, 9)

    if "security" in category:
        score = max(score, 8)

    if "crash" in summary:
        score = max(score, 8)

    if "refactor" in category:
        score = min(score, max(score, 3))

    if score >= 7:
        return "High"

    elif score >= 4:
        return "Medium"

    return "Low"