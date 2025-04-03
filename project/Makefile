.PHONY: help logs up down rebuild migrate makemigrations showmigrations \
        createsuperuser shell test collectstatic db-shell redis-ping

# Colors
GREEN := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE := $(shell tput -Txterm setaf 7)
RESET := $(shell tput -Txterm sgr0)

## Help - Show this help message
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-20s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Docker logs - View container logs
logs:
	docker-compose logs -f

## Start containers - Start all services
up:
	docker-compose up

## Stop containers - Stop and remove containers
down:
	docker-compose down -v

## Rebuild containers - Rebuild and start containers
rebuild:
	docker-compose up -d --build

## Apply migrations - Apply database migrations
migrate:
	docker-compose exec web python manage.py migrate

## Create migrations - Create new migration files
makemigrations:
	docker-compose exec web python manage.py makemigrations

## Show migrations - Display migration status
showmigrations:
	docker-compose exec web python manage.py showmigrations

## Create superuser - Create Django superuser
createsuperuser:
	docker-compose exec web python manage.py createsuperuser

## Django shell - Open Django shell
shell:
	docker-compose exec web python manage.py shell

## Run tests - Run Django tests
test:
	docker-compose exec web python manage.py test

## Collect static - Collect static files
collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

## DB shell - Access PostgreSQL shell
db-shell:
	docker-compose exec db psql -U store_user -d store_db

## Redis ping - Test Redis connection
redis-ping:
	docker-compose exec redis redis-cli ping