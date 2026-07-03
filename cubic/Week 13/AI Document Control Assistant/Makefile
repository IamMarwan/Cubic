install:
	pip install -r requirements.txt

seed:
	python scripts/seed_demo.py

test:
	pytest -q

run:
	uvicorn app.main:app --reload

evaluate:
	python scripts/evaluate_ai.py
