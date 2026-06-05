from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def safe_parse_json(text):
    """
    Extract and parse JSON safely from model output
    """
    if not text:
        raise ValueError("Empty response from model")

    text = text.strip()

    # remove markdown wrappers if model adds them
    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(text)


def generate_fix(commit_message, summary, file_context=""):
    """
    REAL AI CODE FIX GENERATOR (NO DUMMY TEXT)
    Produces structured patch that can be applied directly to code.
    """

    prompt = f"""
You are an expert software engineer and debugging assistant.

Your job is to generate a REAL code fix that can be directly applied.

STRICT RULES:
- Output ONLY valid JSON
- No explanation
- No markdown
- No extra text

You must return a real patch-like fix.

If possible, ensure:
- old_code exists in real code
- new_code is corrected version

FORMAT:

{{
  "file_path": "exact/file/path.py",
  "old_code": "exact buggy code snippet",
  "new_code": "fixed correct code snippet",
  "reason": "why this fix is needed"
}}

=====================
Commit Message:
{commit_message}

Bug / Analysis Summary:
{summary}

Optional File Context:
{file_context}
=====================

IMPORTANT:
- Do NOT return dummy placeholders like "example.py"
- Try to infer realistic code fixes
- Keep code snippets minimal but real
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2  # lower = more deterministic fixes
        )

        content = response.choices[0].message.content

        try:
            return safe_parse_json(content)

        except Exception as e:
            print("❌ JSON PARSE ERROR:", e)
            print("RAW OUTPUT:", content)

            return {
                "file_path": "",
                "old_code": "",
                "new_code": "",
                "reason": "Parse failed - invalid model output"
            }

    except Exception as e:
        print("❌ GROQ API ERROR:", e)

        return {
            "file_path": "",
            "old_code": "",
            "new_code": "",
            "reason": f"API failure: {str(e)}"
        }