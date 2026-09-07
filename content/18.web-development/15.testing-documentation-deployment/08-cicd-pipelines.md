# CI/CD pipelines

## Короткий зміст

У цій лекції вивчається автоматизація процесів testing, building та deployment через CI/CD:

- **Концепція CI/CD** — Continuous Integration: автоматичний запуск тестів при кожному commit, early detection проблем; Continuous Deployment: автоматичний deploy після успішних тестів, швидкий delivery features
- **GitHub Actions** — CI/CD платформа інтегрована у GitHub, workflow files у `.github/workflows/`, тригери: push, pull_request, schedule, manual dispatch
- **Workflow синтаксис YAML** — структура: name, on (triggers), jobs (stages), steps (commands), використання actions з marketplace, environment variables та secrets
- **Pipeline stages** — типовий flow: 1) Checkout code, 2) Setup Node.js, 3) Install dependencies, 4) Lint code (ESLint), 5) Run unit tests, 6) Run E2E tests, 7) Build production, 8) Deploy, кожен stage може блокувати наступний при failure
- **Running tests у CI** — setup test database через Docker services, environment variables для test config, parallel test execution через matrix strategy (Node 18/20), artifacts для test reports та coverage
- **Docker build та push** — build Docker image у CI, login до Docker registry (Docker Hub, GitHub Container Registry, AWS ECR), tagging з version/commit SHA, push до registry для deployment
- **Deployment strategies** — Blue-Green deployment: два identичні environments, switch traffic; Rolling updates: поступова заміна instances; Canary releases: поступовий rollout до частини users
- **Environment secrets** — зберігання sensitive data у GitHub Secrets, доступ через `${{ secrets.DATABASE_URL }}`, різні secrets для staging/production environments
- **Notifications** — Slack/Discord/Email notifications при failed builds, integration з issue tracking для auto-creating bugs

Розглядаються практичні приклади: GitHub Actions workflow для NestJS (lint → test → build → deploy), setup PostgreSQL service для E2E тестів, deploy до AWS/DigitalOcean, rollback strategies.
