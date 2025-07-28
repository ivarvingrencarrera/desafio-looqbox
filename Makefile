lint:
	@echo
	ruff format .
	@echo
	ruff check --silent --exit-zero --fix .
	@echo
	ruff check .
	@echo
	mypy .


test:
	pytest --cov-report=term-missing --cov-report=html --cov-report=xml --cov-branch --cov src/


local/start: check_env
	uvicorn src.main:app --port 8008 --reload


check_env:
	@ if [ ! -f ".env" ]; then cp sample.env .env; fi