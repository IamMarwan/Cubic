# End-to-End Demonstration Script

1. Install dependencies with `pip install -r requirements.txt`.
2. Seed the demo records with `python scripts/seed_demo.py`.
3. Start the web application with `uvicorn app.main:app --reload`.
4. Open the dashboard and show lifecycle KPIs.
5. Open the document register and select a sample document.
6. Demonstrate AI-extracted metadata, document classification, confidence, and risk score.
7. Move a document through Draft, In Review, Approved, Issued, and Archived states.
8. Show the audit trail for traceability.
9. Open `/api/analytics/summary` to show reporting output.
10. Run `pytest -q` and `python scripts/evaluate_ai.py` to show testing and performance results.
