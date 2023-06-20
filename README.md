[![Backend CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/backend-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/backend-ci.yml?query=branch%3Amain)
[![Frontend CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/frontend-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/frontend-ci.yml?query=branch%3Amain)
[![E2E CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/e2e-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/e2e-ci.yml?query=branch%3Amain)

# Get started

```
# Start the containers
docker compose up

# Run the migrations
(cd backend && make db-migrations)
```

Frontend: http://localhost:8000

Backend: http://localhost:8001

DB: postgres://test_user:test_password@localhost:8004/postgres_dev

### Todo

- [ ] Add deployment script
