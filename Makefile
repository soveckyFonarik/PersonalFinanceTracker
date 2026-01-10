.PHONY: help test test-unit test-integration test-cov lint format clean

help:
	@echo "Доступные команды:"
	@echo "  test        - Запустить все тесты"
	@echo "  test-unit   - Запустить unit-тесты"
	@echo "  test-integration - Запустить интеграционные тесты"
	@echo "  test-cov    - Запустить тесты с покрытием кода"
	@echo "  lint        - Проверить код линтерами"
	@echo "  format      - Отформатировать код"
	@echo "  clean       - Очистить временные файлы"

test:
	pytest tests/ -v

test-unit:
	pytest tests/ -m "unit" -v

test-integration:
	pytest tests/ -m "integration" -v

test-cov:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

lint:
	black --check app/ tests/
	isort --check-only app/ tests/
	flake8 app/ tests/
	mypy app/

format:
	black app/ tests/
	isort app/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +