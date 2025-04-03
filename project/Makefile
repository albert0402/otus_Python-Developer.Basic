# Docker Utilities
logs:
	docker-compose logs -f

up:
	docker-compose up -d

down:
	docker-compose down

rebuild:
	docker-compose up -d --build


# Django Management
migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

showmigrations:
	docker-compose exec web python manage.py showmigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

shell:
	docker-compose exec web python manage.py shell

test:
	docker-compose exec web python manage.py test

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput


# Database
db-shell:
	docker-compose exec db psql -U store_user -d store_db


# Redis
redis-ping:
	docker-compose exec redis redis-cli ping
