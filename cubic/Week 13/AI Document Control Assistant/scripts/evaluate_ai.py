from pathlib import Path
import sys, time, json
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.services.ai_engine import classify_text

CASES = [
    ("Civil", "Method Statement", "concrete foundation rebar method statement inspection quality"),
    ("Electrical", "Drawing", "cable lighting switchgear panel layout drawing"),
    ("HSE", "Specification", "safety hazard permit risk standard requirements specification"),
    ("Mechanical", "Material Submittal", "pump valve pipe supplier datasheet material submittal"),
    ("QA/QC", "Inspection Report", "inspection test report itr checklist quality nonconformance"),
]
start = time.perf_counter()
correct_discipline = 0
correct_type = 0
results = []
for expected_discipline, expected_type, text in CASES:
    prediction = classify_text(text)
    correct_discipline += prediction["discipline"] == expected_discipline
    correct_type += prediction["document_type"] == expected_type
    results.append({"expected_discipline": expected_discipline, "expected_type": expected_type, **prediction})
elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
report = {
    "test_cases": len(CASES),
    "discipline_accuracy": round(correct_discipline / len(CASES), 2),
    "type_accuracy": round(correct_type / len(CASES), 2),
    "average_latency_ms_per_document": round(elapsed_ms / len(CASES), 2),
    "results": results,
}
out = ROOT / "reports" / "accuracy_performance_results.json"
out.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
