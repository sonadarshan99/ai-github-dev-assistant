from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_commit(message, files, patch):

    patch = str(patch)[:1500]
    message = str(message)[:1000]

    prompt = f"""
You are a senior software engineer performing code review.

Strict rules:
- Output MUST be valid JSON only
- No markdown, no explanation, no extra text

Risk scoring rules:
- Security / memory leak / crash → 7-10
- Refactor → 3-6
- Minor changes → 0-3

Return format:

{{
  "category": "Bug Fix | Feature | Security | Refactor",
  "priority": "Low | Medium | High",
  "risk_score": 0,
  "security_issues": "",
  "summary": ""
}}

Commit Message:
{message}

Files Changed:
{files}

Code Diff:
{patch}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            return json.loads(content)

        except:
            return {
                "category": "Refactor",
                "priority": "Low",
                "risk_score": 2,
                "security_issues": "",
                "summary": content
            }

    except Exception as e:

        print("Groq Error:", e)

        return {
            "category": "Unknown",
            "priority": "Low",
            "risk_score": 0,
            "security_issues": "",
            "summary": f"Analysis failed: {str(e)}"
        }