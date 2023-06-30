format: 
	venv/bin/black src tests

type-check: 
	venv/bin/mypy src tests

pytest:
	docker compose exec backend bash -c "ENV=test pytest"

db-migrations:
	docker compose exec backend bash -c "alembic upgrade head"