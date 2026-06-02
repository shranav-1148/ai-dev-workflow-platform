# Backend Database Setup (PostgreSQL + Docker)

## Overview

This project uses PostgreSQL as the primary database for the backend.  
It runs inside Docker and is accessed via SQLAlchemy and DBeaver.

## Start Database

```bash
docker compose up -d
```

## Docker Compose file:

```yml
services:
postgres:
image: postgres:16
container_name: ai_postgres
restart: always
environment:
POSTGRES_USER: postgres
POSTGRES_PASSWORD: password
POSTGRES_DB: ai_platform
ports: - "5432:5432"
volumes: - pgdata:/var/lib/postgresql/data
```

## Database connection String:

`postgresql://postgres:password@localhost:5432/ai_platform`

# Server setup:

- Create virtual venv `venv` and pip install uvicorn and fastapi
