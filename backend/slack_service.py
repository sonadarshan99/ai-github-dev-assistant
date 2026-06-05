import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

def send_slack(message, risk, jira=None):

    text = f"""
🚨 *DevOps Alert*

Commit: {message}
Risk: {risk}
"""

    if jira:
        text += f"\nJira: {jira}"

    requests.post(WEBHOOK, json={"text": text})