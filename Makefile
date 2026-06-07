.PHONY: install serve test eval demo cli docker

install:
	cd backend && python -m pip install -r requirements.txt

serve:
	cd backend && uvicorn app.main:app --reload

test:
	cd backend && pytest -q

eval:
	python incidentpilot.py eval

demo:
	python incidentpilot.py investigate --ticket "Checkout latency increased for premium users after deploy 4921. p95 went from ~240ms to >1.8s around 14:05 UTC."

cli:
	python incidentpilot.py --help

docker:
	docker compose up --build
