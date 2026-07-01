# Support Context Budget Lab — dev convenience targets.
# `./run.sh` is the one-command path; these are granular helpers.

.DEFAULT_GOAL := help
.PHONY: help install backend frontend dev test check clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install backend (uv) and frontend (npm) dependencies
	cd backend && uv sync
	cd frontend && npm install

backend: ## Run the FastAPI backend (reload)
	cd backend && uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000

frontend: ## Run the Next.js frontend
	cd frontend && npm run dev

dev: ## Install + run both servers (delegates to run.sh)
	./run.sh

test: ## Run backend unit tests
	cd backend && uv run pytest -q

check: ## Verify prerequisites and .env
	./run.sh --check

clean: ## Remove build/venv/cache artifacts
	rm -rf backend/.venv backend/.pytest_cache frontend/.next frontend/node_modules
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
