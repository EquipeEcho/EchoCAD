# Docker Command Reference

## Containers
- `docker ps` - list running containers
- `docker ps -a` - list all containers
- `docker run --name <name> -d <image>` - start container in background
- `docker run --rm -it <image> /bin/bash` - run temporary interactive container
- `docker start <container>` - start a stopped container
- `docker stop <container>` - stop a running container
- `docker restart <container>` - restart a container
- `docker rm <container>` - remove a stopped container
- `docker rm $(docker ps -aq)` - remove all containers
- `docker inspect <container>` - inspect low-level container details
- `docker inspect --format='{{json .Config}}' <container>` - inspect container configuration
- `docker exec -it <container> /bin/bash` - open shell inside running container
- `docker exec -it <container> <command>` - execute a command inside a running container
- `docker logs <container>` - view container logs
- `docker logs -f <container>` - follow logs

## Images
- `docker images` - list local images
- `docker pull <image>` - download image
- `docker build -t <tag> .` - build image from Dockerfile
- `docker rmi <image>` - remove image
- `docker rmi $(docker images -q)` - remove all images

## Volumes
- `docker volume ls` - list volumes
- `docker volume create <name>` - create volume
- `docker volume rm <volume>` - remove volume
- `docker volume prune` - remove unused volumes

## Networks
- `docker network ls` - list networks
- `docker network create <name>` - create network
- `docker network rm <name>` - remove network

## Logs and Inspection
- `docker logs <container>` - view container logs
- `docker logs -f <container>` - follow logs
- `docker inspect <container>` - inspect container details
- `docker exec -it <container> /bin/bash` - open shell inside container
- `docker stats` - live container resource usage

## Docker Compose
- `docker compose up` - start services from compose file
- `docker compose up -d` - start services in background
- `docker compose down` - stop and remove services
- `docker compose build` - build services
- `docker compose logs -f` - follow compose logs
- `docker compose ps` - list compose services
- `docker compose exec <service> <command>` - run command in service

## Cleanup
- `docker system prune` - remove stopped containers, unused networks, images, and optionally volumes
- `docker system prune -a` - also remove unused images
- `docker builder prune` - remove build cache

## Useful Tips
- `docker stats --no-stream` - one-time resource usage snapshot
- `docker logs --tail 100 <container>` - show last 100 lines of logs
- `docker inspect --format='{{json .Config}}' <container>` - inspect with custom format
