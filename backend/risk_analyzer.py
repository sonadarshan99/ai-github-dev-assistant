def get_risk_level(risk_score):

    try:
        risk_score = int(risk_score)
    except:
        risk_score = 0

    if risk_score >= 7:
        return "High"
    elif risk_score >= 4:
        return "Medium"
    else:
        return "Low"