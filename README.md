# Docker Microservices

Multi-container application built with Docker Compose. The stack consists of an Nginx reverse proxy, Flask API running with Gunicorn, and PostgreSQL database with persistent storage.

## Architecture

```text
Client / curl
     |
     | localhost:8080
     v
+-----------+       frontend network       +----------------+
|   Nginx   | ----------------------------> | Flask/Gunicorn |
|  port 80  |                               |   port 5000    |
+-----------+                               +----------------+
                                                   |
                                                   | backend network
                                                   v
                                            +---------------+
                                            | PostgreSQL 16 |
                                            |   port 5432   |
                                            +---------------+
                                                   |
                                             postgres_data
                                              Docker volume
```

Nginx is the public entry point to the application.

PostgreSQL is not exposed to the host. The database is accessible only through the backend Docker network.

The Flask application is connected to both frontend and backend networks and handles communication between Nginx and PostgreSQL.

## Stack

- Docker
- Docker Compose
- Nginx
- Python / Flask
- Gunicorn
- PostgreSQL 16
- GitHub Actions

## Features

- Multi-container architecture
- Nginx reverse proxy
- Flask REST API
- Gunicorn WSGI server
- PostgreSQL database
- Persistent Docker volume
- Isolated frontend and backend networks
- Docker DNS service discovery
- Container health checks
- Environment-based configuration
- Non-root application container
- HTTP health endpoint
- Centralized access through Nginx
- Docker logs and container inspection
- GitHub Actions CI

## Requirements

- Docker Engine or Docker Desktop
- Docker Compose v2
- `curl`

## Installation

Clone the repository:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd docker-microservices
```

Create the environment file:

```bash
cp .env.example .env
```

Build and start the containers:

```bash
docker compose up -d --build
```

Check container status:

```bash
docker compose ps
```

## API

Check the main endpoint:

```bash
curl http://localhost:8080/
```

Health check:

```bash
curl http://localhost:8080/health
```

Create a message:

```bash
curl -X POST http://localhost:8080/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"content":"My first Docker message"}'
```

Get stored messages:

```bash
curl http://localhost:8080/api/messages
```

## Demo

Run the demo script:

```bash
./scripts/demo.sh
```

Check service status and logs:

```bash
docker compose ps

docker compose logs --tail=30 nginx

docker compose logs --tail=30 app
```

Verify Docker DNS resolution:

```bash
docker compose exec app getent hosts db

docker compose exec nginx getent hosts app
```

## Data Persistence

PostgreSQL data is stored in the `postgres_data` named volume.

Create a record:

```bash
curl -X POST http://localhost:8080/api/messages \
  -H 'Content-Type: application/json' \
  -d '{"content":"Persistent message"}'
```

Stop and remove the containers:

```bash
docker compose down
```

Start them again:

```bash
docker compose up -d
```

Verify the stored data:

```bash
curl http://localhost:8080/api/messages
```

The data remains available after container recreation because the PostgreSQL data directory is stored in a persistent Docker volume.

To remove the containers together with the database volume:

```bash
docker compose down -v
```

## Networking

The stack uses two Docker networks:

```text
frontend
backend
```

The `frontend` network connects:

```text
nginx <-> app
```

The `backend` network connects:

```text
app <-> db
```

PostgreSQL is not connected to the frontend network and does not expose port `5432` to the host.

Docker's internal DNS is used for service discovery:

```text
nginx -> app:5000
app   -> db:5432
```

## Health Checks

The stack includes health checks for the application and database.

Check their current state:

```bash
docker compose ps
```

Detailed container health information can also be inspected with:

```bash
docker inspect <container-name>
```

## Logs

View logs from all services:

```bash
docker compose logs -f
```

Application logs:

```bash
docker compose logs -f app
```

Nginx logs:

```bash
docker compose logs -f nginx
```

PostgreSQL logs:

```bash
docker compose logs -f db
```

## Troubleshooting

Check running containers:

```bash
docker compose ps
```

Check Docker networks:

```bash
docker network ls
```

Check Docker volumes:

```bash
docker volume ls
```

Check service name resolution:

```bash
docker compose exec app getent hosts db
docker compose exec nginx getent hosts app
```

Inspect a container:

```bash
docker inspect <container-name>
```

Validate the Compose configuration:

```bash
docker compose config
```

Additional troubleshooting examples are available in [`docs/troubleshooting.md`](docs/troubleshooting.md).

## CI

GitHub Actions configuration is located in:

```text
.github/workflows/docker-ci.yml
```

The workflow runs on pushes and pull requests and performs Compose configuration validation and application image build.

## Security

The application container runs as a non-root user.

PostgreSQL is isolated from the host and is accessible only through the internal backend network.

Runtime configuration is passed through environment variables.

The `.env` file is excluded from Git and `.env.example` contains the required variable names without runtime credentials.

For external deployment, secrets management, TLS, monitoring, backups, centralized logging, and container image scanning should be configured according to the target environment.

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── docker-ci.yml
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── db/
│   └── init.sql
├── docs/
│   └── troubleshooting.md
├── nginx/
│   └── default.conf
├── scripts/
│   └── demo.sh
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

## Stop

Stop and remove the containers:

```bash
docker compose down
```

Remove containers and persistent data:

```bash
docker compose down -v
```
