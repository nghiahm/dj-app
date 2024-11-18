.SILENT:

COMPOSE = docker compose -f docker-compose.yml

destroy:
	@$(COMPOSE) down --rmi all --volumes --remove-orphans

build:
	@$(COMPOSE) build ${img}

remove:
	@make destroy
	docker system prune -a

start:
	@$(COMPOSE) up -d

stop:
	@$(COMPOSE) down

logs:
	@$(COMPOSE) logs -f $(img)

migrate:
	@$(COMPOSE) run --rm app python manage.py migrate

makemigrations:
	@$(COMPOSE) run --rm app python manage.py makemigrations ${app}

collectstatic:
	@$(COMPOSE) run --rm app python manage.py collectstatic --no-input

createsuperuser:
	@$(COMPOSE) run --rm app python manage.py createsuperuser

startapp:
	@$(COMPOSE) run --rm app python manage.py startapp ${app}

poetry_add:
	@$(COMPOSE) run --rm app poetry add ${cmd}

run_app:
	@$(COMPOSE) run --rm app ${cmd}

app_schema:
	@$(COMPOSE) run --rm app python manage.py spectacular --color --file schema.yml

app_test:
	@$(COMPOSE) run --rm app pytest -s ${path}
