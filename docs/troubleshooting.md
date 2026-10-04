# Troubleshooting and Docker analysis

This project intentionally keeps the observability/debugging exercises from the lesson.

## Inspect containers

```bash
docker compose ps
docker inspect docker-microservices-nginx-1
docker inspect docker-microservices-app-1
```

## Logs

```bash
docker compose logs -f nginx
docker compose logs -f app
docker compose logs -f db
```

Generate successful and error traffic:

```bash
./scripts/demo.sh
```

The script produces normal requests plus HTTP 404 and HTTP 500 responses, which can then be found in Nginx logs.

## Network checks

```bash
docker network ls
docker compose exec app getent hosts db
docker compose exec nginx getent hosts app
```

The database is attached only to the backend network. Nginx is attached only to the frontend network. The Flask application connects both layers.

## Volume check

```bash
docker volume ls
docker compose down
docker compose up -d
curl http://localhost:8080/api/messages
```

Messages remain after container recreation because PostgreSQL data is stored in a named Docker volume. Use `docker compose down -v` only when you intentionally want to delete the database data.
