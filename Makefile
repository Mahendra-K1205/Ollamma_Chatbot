.PHONY: help install test lint docker-build docker-run deploy-vercel clean

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linter"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run with Docker Compose"
	@echo "  make deploy-vercel - Deploy to Vercel"
	@echo "  make clean         - Clean build artifacts"

install:
	pip install -r requirements.txt
	cd web && npm install

test:
	pytest tests/ -v --cov=.

lint:
	flake8 . --max-line-length=127 --exclude=web,venv

docker-build:
	docker build -t ollama-chatbot .

docker-run:
	docker-compose up -d

deploy-vercel:
	cd web && npx vercel --prod

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
	cd web && rm -rf .next node_modules
