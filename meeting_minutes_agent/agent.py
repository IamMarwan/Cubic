import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL")

def extract_meeting_minutes(text: str):
    prompt = f"""
Return ONLY JSON:

{{
  "decisions": [],
  "action_items": [
    {{
      "task": "",
      "responsible_person": "",
      "deadline": ""
    }}
  ]
}}

Meeting notes:
{text}
"""

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    output = response.output_text

    try:
        return json.loads(output)
    except:
        start = output.find("{")
        end = output.rfind("}")
        return json.loads(output[start:end+1])