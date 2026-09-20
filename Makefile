.PHONY: backend frontend setup test

setup:
	pip install -r backend/requirements.txt
	cd frontend && npm install

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -q