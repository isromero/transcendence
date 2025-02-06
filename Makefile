# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: samusanc <samusanc@student.42madrid>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/06/24 19:28:25 by samusanc          #+#    #+#              #
#    Updated: 2025/02/06 20:18:02 by samusanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all: build up

build: env						# build the docker image
	docker-compose -f ./docker-compose.yml build	
	docker image prune -f		# delete intermediate images

up:								# up the docker image and rebuilding if it is nescessary
	docker-compose -f ./docker-compose.yml up --build	

down:							# down the docker image
	docker-compose -f ./docker-compose.yml down	

stop:							# stop all containers
	if [ -n "$$(docker ps -aq)" ]; then \
		docker stop $$(docker ps -aq); \
	fi

delvol:
	if [ -n "$$(docker volume ls -qf dangling=true)" ]; then \
		docker volume rm $$(docker volume ls -qf dangling=true); \
	fi

env:
	bash ./srcs/requirements/tools/env.sh

re: fclean all

fclean: down clean delvol
	docker system prune -a -f
	#docker volume prune -a -f

# delete only containers, dont delete images or volumes
clean: stop
	if [ -n "$$(docker ps -aq)" ]; then \
		docker rm $$(docker ps -aq); \
	fi

.PHONY: all clean fclean re stop down up build delvol
