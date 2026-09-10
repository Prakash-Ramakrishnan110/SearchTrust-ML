.PHONY: install test run

install:
	pip install -r requirements.txt

test:
	pytest backend/tests/

run:
	uvicorn backend.app.main:app --reload
