compose_file := docker-compose.yml
compose := docker-compose -f $(compose_file)

.PHONY: black
black:
	$(compose) exec web black -l 100 . --exclude \env

.PHONY: build
build:
	$(compose) build $(name)

.PHONY: clean
clean:
	rm -rf .docker-data/

.PHONY: create_superuser
create_superuser:
	$(compose) exec web python manage.py createsuperuser

.PHONY: dbfresh
dbfresh: down clean up pg_isready migrate

.PHONY: down
down:
	$(compose) down

.PHONY: exec
exec:
	$(compose) exec $(name) $(c)

.PHONY: refresh
refresh: down clean build up pg_isready migrate

.PHONY: make_migrations
make_migrations:
	$(compose) exec web python manage.py makemigrations

.PHONY: migrate
migrate:
	$(compose) exec web python manage.py migrate

.PHONY: pg_isready
pg_isready:
	$(compose) exec db /bin/bash -c "until pg_isready; do sleep 2 ; done; sleep 2"

.PHONY: up
up:
	$(compose) up -d

.PHONY: pytest
pytest:
ifeq ($(strip $(TEST)),)
	$(compose) exec web pytest
else
	$(compose) exec web pytest -s -k $(TEST)
endif
