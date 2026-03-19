import json
from pathlib import Path


def read_text_file(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")


def save_json(data: dict, output_path: str) -> None:
    path = Path(output_path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def extract_json_from_text(raw_text: str) -> dict:
    """
    Safely extract a JSON object from model output.
    """
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    start = raw_text.find("{")
    end = raw_text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model did not return valid JSON.")

    json_text = raw_text[start:end + 1]
    return json.loads(json_text)