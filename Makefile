.PHONY: build up down logs

initialize-network:
	docker network create mcp-database-mvp-network

build:
	docker compose build

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

reset-docker:
	docker stop mcp-database-mvp-app
	docker stop mcp-database-mvp-mysql
	docker stop mcp-database-mvp-qdrant
	docker network rm mcp-database-mvp-network

bash-app:
	docker compose exec app bash
