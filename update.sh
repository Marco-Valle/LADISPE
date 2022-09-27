#!/bin/bash

docker-compose --file docker-compose.prod.yml down

nginx_id=$(docker container ls --all | grep nginx | cut -d' ' -f1)
backend_id=$(docker container ls --all | grep backend | cut -d' ' -f1)
postgres_id=$(docker container ls --all | grep postgres | cut -d' ' -f1)

nginx_image_id=$(docker image ls | grep nginx |  cut -d' ' -f14)
backend_image_id=$(docker image ls | grep backend |  cut -d' ' -f12)
postgres_image_id=$(docker image ls | grep postgres |  cut -d' ' -f14)

docker container rm ${nginx_id}
docker container rm ${backend_id}
docker container rm ${postgres_id}

docker image rm ${nginx_image_id}
docker image rm ${backend_image_id}
docker image rm ${postgres_image_id}

git pull
docker-compose --file docker-compose.prod.yml up -d --force-recreate