# Docker та контейнеризація

## Короткий зміст

У цій лекції вивчається упаковка NestJS застосунку у Docker контейнери для reproducible deployments:

- **Docker концепція** — контейнеризація для ізоляції застосунків, образи (images) як templates, контейнери (containers) як running instances, переваги: consistency across environments, easy scaling, dependency isolation
- **Dockerfile для NestJS** — інструкції для побудови image: FROM node:18-alpine базовий образ, WORKDIR для робочої директорії, COPY для файлів, RUN для команд (npm install), CMD для запуску застосунку, EXPOSE для порту
- **Multi-stage build** — оптимізація розміру образу: stage 1 (builder) для npm install та build, stage 2 (production) лише з dist/ та production dependencies, копіювання артефактів між stages, зменшення final image size з ~1GB до ~200MB
- **.dockerignore** — виключення файлів з build context: node_modules/, .git/, .env, *.md, зменшення build time та розміру image
- **Docker Compose** — оркестрація multi-container застосунків, docker-compose.yml з services: app (NestJS), db (PostgreSQL), redis, networks для communication, volumes для persistence
- **Volumes** — персистентність даних БД через named volumes, bind mounts для development (live reload), anonymous volumes для node_modules
- **Networking** — communication між контейнерами через service names, environment variables для connection strings (DATABASE_HOST=db), port mapping для доступу ззовні (-p 3000:3000)
- **Best practices** — використання .dockerignore, multi-stage builds, non-root user для security, health checks, minimal base images (alpine), layer caching optimization

Розглядаються практичні приклади: Dockerfile для NestJS з multi-stage, docker-compose.yml для dev environment (NestJS + PostgreSQL + Redis), production-ready setup, debugging у контейнері.
