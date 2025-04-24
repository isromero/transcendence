# Check if docker-compose or docker compose is available
COMPOSE := $(shell command -v docker-compose || echo "docker compose")

all: apple build up

.apple:
	unzip -qq cli/src/badapple/frames.zip -d cli/src/badapple/
	touch .apple

apple: .apple

build:
	$(COMPOSE) build

up:
	python3 update_env_and_caddy.py
	$(COMPOSE) up

down:
	$(COMPOSE) down -t 1

stop:
	if [ -n "$$(docker ps -aq)" ]; then \
		docker stop $$(docker ps -aq); \
	fi

delvol:
	if [ -n "$$(docker volume ls -qf dangling=true)" ]; then \
		docker volume rm $$(docker volume ls -qf dangling=true); \
	fi

clean-migrations:
	rm -rf be/apps/core/migrations/*_initial.py

# Clean all relationed to the compose file
clean-compose: 
	$(COMPOSE) down --rmi all --volumes

re: clean-compose clean-migrations all

fclean: down clean delvol
	docker system prune -a -f --volumes
	rm -rf cli/src/badapple/frames/
	rm -rf .apple

# Delete only containers, dont delete images or volumes
clean: stop
	if [ -n "$$(docker ps -aq)" ]; then \
		docker rm $$(docker ps -aq); \
	fi

.PHONY: all clean fclean re stop down up build delvol
