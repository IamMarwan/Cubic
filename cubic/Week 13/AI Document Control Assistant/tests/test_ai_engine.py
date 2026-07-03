from app.services.ai_engine import classify_text, extract_metadata

def test_classifies_electrical_drawing():
    result = classify_text("cable routing switchgear panel lighting layout drawing")
    assert result["discipline"] == "Electrical"
    assert result["document_type"] == "Drawing"
    assert result["confidence"] > 0.5

def test_extracts_metadata():
    result = extract_metadata("Title: Pump Datasheet\nDocument Number: CUB-MEC-MAT-002\nRevision: C\npump valve supplier material datasheet")
    assert result.title == "Pump Datasheet"
    assert result.document_number == "CUB-MEC-MAT-002"
    assert result.revision == "C"
