import json
import argparse
from pathlib import Path
from app.utils.text_extract import extract_text_from_bytes
from app.services.extractor import extract_structured_from_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("--out", default="output.json")
    args = parser.parse_args()

    path = Path(args.file_path)
    content = path.read_bytes()
    text, ext = extract_text_from_bytes(path.name, content)

    result = extract_structured_from_text(
        filename=path.name,
        source_type=ext.replace(".", ""),
        text=text
    )

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2)

    print("Saved:", args.out)

if __name__ == "__main__":
    main()