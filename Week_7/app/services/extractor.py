from app.utils.text_extract import extract_text_from_bytes
from app.services.schema import ExtractionResult
from app.services.llm_client import get_client
from app.core.config import OPENAI_MODEL
import json

SYSTEM_PROMPT = """
Extract structured data from the document.
Only use information explicitly present.
If missing, return null or empty list.
"""

def extract_structured_from_text(filename: str, source_type: str, text: str):
    client = get_client()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text[:150000]}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "extraction_result",
                "schema": ExtractionResult.model_json_schema()
            }
        }
    )

    data = response.choices[0].message.content
    parsed = ExtractionResult.model_validate(json.loads(data))
    parsed.source_filename = filename
    parsed.source_type = source_type
    return parsed


async def extract_structured_from_upload(file):
    content = await file.read()
    text, ext = extract_text_from_bytes(file.filename, content)

    return extract_structured_from_text(
        filename=file.filename,
        source_type=ext.replace(".", ""),
        text=text
    )