format: 
	venv/bin/black src tests

type-check: 
	venv/bin/mypy src tests

pytest:
	docker compose exec backend sh -c "ENV=test FAKE_SERVER_URL=http://fake_server:9000 pytest --cov=backend -vv"

db-migrations:
	docker compose exec backend sh -c "alembic upgrade head"