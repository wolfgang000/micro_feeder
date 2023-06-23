[![Backend CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/backend-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/backend-ci.yml?query=branch%3Amain)
[![Frontend CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/frontend-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/frontend-ci.yml?query=branch%3Amain)
[![E2E CI badge](https://github.com/wolfgang000/micro_feeder/actions/workflows/e2e-ci.yml/badge.svg?branch=main)](https://github.com/wolfgang000/micro_feeder/actions/workflows/e2e-ci.yml?query=branch%3Amain)

# Get started

```sh
# Start the containers
docker compose up

# Run the migrations
(cd backend && make db-migrations)
```

Frontend: http://localhost:8000

Backend: http://localhost:8001

DB(Postgres): postgres://test_user:test_password@localhost:8004/postgres_dev

Message Broker(Rabbitmq): localhost:8005

Message Broker Store(Redis): localhost:8006

# Deployment

## Setup server

```
# Install dokku
# wget -NP . https://dokku.com/bootstrap.sh
# sudo DOKKU_TAG=v0.30.7 bash bootstrap.sh
# dokku plugin:install https://github.com/dokku/dokku-postgres.git
# dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
# dokku plugin:install https://github.com/dokku/dokku-redis.git
# dokku plugin:install https://github.com/dokku/dokku-rabbitmq.git

dokku apps:create micro-feeder-back
dokku builder:set micro-feeder-back build-dir backend
dokku config:set micro-feeder-back \
  # Set the variables from backend/.env.example.prod

dokku apps:create micro-feeder-front
dokku builder:set micro-feeder-front build-dir frontend
dokku config:set micro-feeder-front \
  # Set the variables from frontend/.env.example.prod

# Setup database
dokku postgres:create micro-feeder-db
dokku postgres:link micro-feeder-db micro-feeder-back

# Setup redis
dokku redis:create micro-feeder-redis
dokku redis:link micro-feeder-redis micro-feeder-back

# Setup rabbitmq
dokku rabbitmq:create micro-feeder-rabbitmq
dokku rabbitmq:link micro-feeder-rabbitmq micro-feeder-back

# Setup SSL certificate
# Remember to open the 443 port

dokku letsencrypt:set micro-feeder-front email test@mail.com
dokku letsencrypt:enable micro-feeder-front

dokku letsencrypt:set micro-feeder-back email test@mail.com
dokku letsencrypt:enable micro-feeder-back

dokku letsencrypt:cron-job --add

# Setup domain
dokku domains:set micro-feeder-front micro-feeder.example.com
```

## Deploy and push changes

```
git remote add server-backend dokku@example.com:micro-feeder-back
git remote add server-frontend dokku@example.com:micro-feeder-front

git push server-backend
git push server-frontend
```

# Production debugging

## Enter to the container

```
dokku enter micro-feeder-back web /bin/sh
```

## Show logs

```
dokku logs micro-feeder-back
```

## Open a psql terminal

```
dokku postgres:connect micro-feeder-db
```

### Todo

- [ ] Add deployment script
- [ ] Add kubernetes deployment
