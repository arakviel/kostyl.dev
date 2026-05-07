# План курсу: Kubernetes — від Docker до Production Orchestration

## Контекст та логіка побудови

Наявний Docker-курс охоплює 17 статей — від концепції контейнеризації до multi-service Compose. Останні дві статті (`16.docker-compose-basics.md`, `17.compose-multi-service.md`) вже містять явне порівняння Compose ↔ Kubernetes та згадки про обмеження single-host підходу. Це природна точка переходу.

**Принцип побудови курсу Kubernetes:** кожна стаття відповідає на запитання *«Як те, що ми вже знаємо з Docker, трансформується у Kubernetes?»* Читач не вивчає Kubernetes з нуля — він розширює вже сформовану ментальну модель.

---

## Структура курсу (18 статей)

### Модуль 1: Перехід від Docker до Kubernetes (статті 01–03)

Мета: Сформувати розуміння «навіщо Kubernetes», коли Compose недостатньо.

---

#### 01. `01.why-kubernetes.md`
**Назва:** Kubernetes — коли Docker Compose більше не вистачає

**Місток з Docker:**
- Стаття 17 (compose-multi-service) закінчується на `--scale api=3` та Nginx upstream. Читач бачить обмеження: один хост, ручне балансування, немає self-healing.
- Починаємо з того самого прикладу: «ваш Compose-стек із 3 репліками API впав разом із сервером».

**Ключові концепції:**
- Проблеми single-host оркестрації (no HA, no auto-healing, no auto-scaling)
- Що таке Kubernetes і яку проблему він вирішує
- Kubernetes у порівнянні з Docker Swarm
- Огляд екосистеми (managed: GKE, EKS, AKS vs self-hosted: kubeadm, k3s)

**Практика:** Порівняльна таблиця Docker Compose vs Kubernetes для реального сценарію

---

#### 02. `02.kubernetes-architecture.md`
**Назва:** Архітектура Kubernetes — анатомія кластера

**Місток з Docker:**
- Docker: один демон (`dockerd`), один хост. Kubernetes: кластер з control plane та worker nodes.
- Аналогія: Docker Engine → kubelet; Docker registry → container registry; `docker run` → Pod spec.

**Ключові концепції:**
- Control Plane: `kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`
- Worker Node: `kubelet`, `kube-proxy`, Container Runtime (containerd)
- Роль `kubectl` як аналога `docker` CLI
- Архітектурна діаграма (PlantUML: повна UML-діаграма кластера)

**Практика:** Розбір запиту `kubectl apply` — що відбувається всередині кластера

---

#### 03. `03.local-environment.md`
**Назва:** Локальне середовище — minikube, kind та k3s

**Місток з Docker:**
- Аналог `docker run hello-world` у Kubernetes-світі
- Використання Docker Desktop як backend для minikube/kind

**Ключові концепції:**
- Порівняння minikube / kind / k3s / Docker Desktop Kubernetes
- Встановлення kubectl та kubeconfig
- Перша команда: `kubectl get nodes`, `kubectl get pods -A`
- Namespace як аналог Docker project name

**Практика (::steps):** Встановлення minikube, запуск першого кластера, перевірка

---

### Модуль 2: Фундаментальні об'єкти Kubernetes (статті 04–08)

Мета: Вивчити базові ресурси Kubernetes через призму Docker-концепцій.

---

#### 04. `04.pods-and-containers.md`
**Назва:** Pod — атомарна одиниця Kubernetes

**Місток з Docker:**
- `docker run myapp` → Pod з одним контейнером
- Сайдкар-контейнери як аналог `--network container:name`
- Pod spec ≈ `docker run` з усіма прапорцями, але декларативний

**Ключові концепції:**
- Що таке Pod і чому він, а не контейнер, є мінімальною одиницею
- Pod Spec: `containers`, `volumes`, `restartPolicy`
- Init containers (аналог init-контейнера з Compose статті 17)
- Sidecar pattern (logging, proxy)
- Lifecycle Pod: Pending → Running → Succeeded/Failed
- Ефемерність Pod: чому не можна редагувати запущений Pod

**Практика:** Написати перший Pod manifest, запустити, дослідити (`kubectl describe`, `kubectl logs`)

---

#### 05. `05.workloads-deployments.md`
**Назва:** Deployment — декларативне управління репліками

**Місток з Docker:**
- `docker compose up --scale api=3` → `replicas: 3` у Deployment
- `docker compose restart` → rolling update у Deployment
- Відсутність self-healing у Compose → ReplicaSet у Kubernetes

**Ключові концепції:**
- ReplicaSet та чому ми не створюємо його напряму
- Deployment як декларація бажаного стану
- `kubectl rollout`: history, undo, status
- Rolling Update strategy vs Recreate
- Pod template labels та selectors

**Практика:** Deployment ASP.NET Core API, оновлення образу, rollback

---

#### 06. `06.services-networking.md`
**Назва:** Service — мережева абстракція для Podʼів

**Місток з Docker:**
- Docker DNS (`db:5432` у Compose) → Kubernetes DNS (`db.default.svc.cluster.local`)
- `ports:` у Compose → Service `nodePort` / `clusterIP`
- Docker networks (frontend/backend ізоляція) → Kubernetes Namespaces + NetworkPolicy

**Ключові концепції:**
- Типи Services: ClusterIP, NodePort, LoadBalancer, ExternalName
- kube-proxy та iptables/IPVS
- CoreDNS та service discovery
- Headless Service для StatefulSet
- Endpoints та EndpointSlices

**Практика:** ClusterIP для внутрішнього API, NodePort для доступу ззовні, тест DNS resolution

---

#### 07. `07.configmaps-secrets.md`
**Назва:** ConfigMap та Secret — управління конфігурацією

**Місток з Docker:**
- `environment:` у Compose → `env` з ConfigMap/Secret
- `.env` файл → Secret (але зашифрований в etcd)
- `volumes: ./config:/app/config` → ConfigMap як volume mount

**Ключові концепції:**
- ConfigMap: як файл та як env змінні
- Secret: base64, opaque, TLS, docker-registry types
- Immutable ConfigMaps/Secrets (Kubernetes 1.21+)
- Проблема безпеки Secret у Git (SOPS, Sealed Secrets, External Secrets)
- `envFrom` vs `env` з `valueFrom`

**Практика:** ConfigMap для конфігурації Nginx, Secret для PostgreSQL credentials

---

#### 08. `08.volumes-persistent-storage.md`
**Назва:** Volumes та PersistentVolume — зберігання даних

**Місток з Docker:**
- `docker volume create` → PersistentVolume
- `volumes: postgres-data:/var/lib/postgresql/data` → PVC у Pod spec
- Named volumes у Compose → StorageClass у Kubernetes

**Ключові концепції:**
- Volume types: emptyDir, hostPath, configMap, secret
- PersistentVolume (PV) та PersistentVolumeClaim (PVC)
- StorageClass та dynamic provisioning
- Access modes: RWO, ROX, RWX
- Reclaim policies: Retain, Delete, Recycle

**Практика:** PostgreSQL із PVC, перевірка персистентності після видалення Pod

---

### Модуль 3: Розширені об'єкти та патерни (статті 09–12)

Мета: Вивчити об'єкти, яких немає у Docker Compose, але які критичні для production.

---

#### 09. `09.statefulsets.md`
**Назва:** StatefulSet — оркестрація stateful-застосунків

**Місток з Docker:**
- У Compose база даних — просто сервіс з named volume. У Kubernetes вона потребує StatefulSet для стабільної ідентичності.
- `depends_on: db: condition: service_healthy` → Init containers + readiness probe

**Ключові концепції:**
- Чим StatefulSet відрізняється від Deployment
- Стабільні мережеві ідентифікатори (`db-0`, `db-1`, `db-2`)
- Ordered deployment та scaling
- VolumeClaimTemplates
- Headless Service для StatefulSet

**Практика:** PostgreSQL як StatefulSet з реплікацією (primary/replica pattern)

---

#### 10. `10.health-probes.md`
**Назва:** Liveness, Readiness та Startup Probes

**Місток з Docker:**
- `healthcheck:` у Compose → три типи probes у Kubernetes
- `condition: service_healthy` у `depends_on` → `readinessProbe` як умова отримання трафіку
- Compose перезапускає контейнер при падінні → `livenessProbe` вбиває та перезапускає Pod

**Ключові концепції:**
- Різниця між liveness, readiness та startup probe
- Типи перевірок: httpGet, tcpSocket, exec, grpc
- Параметри: `initialDelaySeconds`, `periodSeconds`, `failureThreshold`
- Вплив на rolling update: readiness probe блокує трафік до готовності
- Антипатерни: занадто агресивний liveness probe

**Практика:** ASP.NET Core `/health` endpoint, налаштування всіх трьох probes

---

#### 11. `11.ingress.md`
**Назва:** Ingress — HTTP-маршрутизація та TLS termination

**Місток з Docker:**
- Nginx у Compose як reverse proxy → Ingress Controller
- `nginx.conf` з `upstream` → Ingress rules у YAML
- Ручне налаштування TLS → автоматичний cert-manager + Let's Encrypt

**Ключові концепції:**
- Ingress vs Service LoadBalancer
- Ingress Controller: nginx, traefik, istio
- Path-based та host-based routing
- TLS termination та cert-manager
- Annotations для налаштування nginx ingress

**Практика:** Ingress для двох сервісів (API + frontend), TLS з cert-manager

---

#### 12. `12.resource-management.md`
**Назва:** Resource Requests та Limits — управління ресурсами

**Місток з Docker:**
- `deploy.resources.limits` у Compose (ігнорується локально) → `resources.requests/limits` у Kubernetes (реально працює)
- cgroups, які ми вивчали в статті про контейнеризацію → Kubernetes scheduler використовує requests для планування

**Ключові концепції:**
- Requests vs Limits: різниця та наслідки
- CPU: millicores (250m = 0.25 core)
- Memory: bytes (256Mi, 1Gi)
- QoS classes: Guaranteed, Burstable, BestEffort
- LimitRange та ResourceQuota для namespace
- OOMKilled: як діагностувати та виправити

**Практика:** Встановлення requests/limits для всіх сервісів, ResourceQuota для namespace

---

### Модуль 4: Автоматизація та Production-практики (статті 13–16)

Мета: Вивчити автоматизацію, що недоступна у Docker Compose.

---

#### 13. `13.horizontal-scaling.md`
**Назва:** HorizontalPodAutoscaler — автоматичне масштабування

**Місток з Docker:**
- `docker compose up --scale api=3` — ручне, статичне → HPA — автоматичне, динамічне
- Немає аналога у Compose: Kubernetes сам реагує на навантаження

**Ключові концепції:**
- Metrics Server як джерело метрик
- HPA на основі CPU та Memory
- Custom metrics через Prometheus Adapter
- Scale-up та scale-down cooldown (`stabilizationWindowSeconds`)
- VerticalPodAutoscaler (VPA) як доповнення

**Практика:** HPA для API з навантажувальним тестом (k6 або vegeta)

---

#### 14. `14.jobs-cronjobs.md`
**Назва:** Job та CronJob — пакетні задачі та розклад

**Місток з Docker:**
- Init-контейнер для міграцій у Compose → Kubernetes Job для міграцій
- Немає аналога cron у Compose → CronJob

**Ключові концепції:**
- Job: одноразове виконання задачі (міграції, seed)
- `completions` та `parallelism`
- CronJob: синтаксис cron, `concurrencyPolicy`
- `ttlSecondsAfterFinished` для автоочищення
- Типові use cases: backup, звіти, очищення даних

**Практика:** Job для EF Core міграцій, CronJob для щоденного бекапу PostgreSQL

---

#### 15. `15.namespaces-rbac.md`
**Назва:** Namespaces та RBAC — мультиоренда та безпека

**Місток з Docker:**
- Docker project name (`-p myapp`) як слабка аналогія namespace
- Немає аналога RBAC у Docker Compose

**Ключові концепції:**
- Namespace як логічна ізоляція (dev/staging/prod в одному кластері)
- ServiceAccount, Role, ClusterRole
- RoleBinding та ClusterRoleBinding
- Принцип least privilege для Pod ServiceAccount
- NetworkPolicy: ізоляція трафіку між namespace (аналог Docker networks)

**Практика:** Окремі namespaces для dev/prod, RBAC для CI/CD service account

---

#### 16. `16.helm.md`
**Назва:** Helm — пакетний менеджер для Kubernetes

**Місток з Docker:**
- `docker-compose.yml` — один файл для одного стека → Helm Chart — шаблонізований пакет
- `docker compose -f docker-compose.yml -f docker-compose.prod.yml` → `helm install -f values.prod.yaml`
- Docker Hub → Artifact Hub для Helm charts

**Ключові концепції:**
- Структура Helm Chart: `Chart.yaml`, `values.yaml`, `templates/`
- Go templates: `{{ .Values.image.tag }}`
- `helm install`, `helm upgrade`, `helm rollback`
- Залежності (`Chart.lock`, `charts/`)
- Helmfile для управління кількома release

**Практика:** Власний Helm Chart для ASP.NET Core + PostgreSQL застосунку

---

### Модуль 5: Observability та CI/CD (статті 17–18)

Мета: Завершити цикл: від розробки до production-моніторингу.

---

#### 17. `17.observability.md`
**Назва:** Моніторинг та логування — Prometheus, Grafana, Loki

**Місток з Docker:**
- `docker compose logs -f` → централізований Loki
- Немає вбудованого моніторингу у Compose → Prometheus stack
- Prometheus та Grafana у `profiles: monitoring` з Compose статті 17 → повноцінний production-стек

**Ключові концепції:**
- Prometheus: scraping, PromQL, alerting rules
- Grafana: dashboards, data sources
- Loki + Promtail: агрегація логів
- `kube-state-metrics` та `node-exporter`
- OpenTelemetry як vendor-neutral стандарт

**Практика:** Prometheus stack через Helm, кастомний dashboard для .NET метрик

---

#### 18. `18.cicd-gitops.md`
**Назва:** CI/CD та GitOps — автоматизація деплою

**Місток з Docker:**
- `docker build && docker push` → GitHub Actions pipeline
- `docker compose up` → `kubectl apply` або ArgoCD sync
- Compose як інструмент CI тестів → Kubernetes як production target

**Ключові концепції:**
- GitHub Actions: build → push → deploy pipeline
- GitOps принцип: Git як єдине джерело правди
- ArgoCD: автоматичний sync з Git репозиторію
- Image update automation (Flux ImageAutomationController)
- Стратегії деплою: Rolling, Blue/Green, Canary

**Практика:** Повний CI/CD pipeline: PR → тести в Docker Compose → деплой у Kubernetes через ArgoCD

---

## Педагогічна архітектура курсу

### Наскрізний проєкт

Протягом усього курсу студент розгортає **один і той самий застосунок**, поступово переносячи його з Docker Compose у Kubernetes:

- **Статті 01–03:** Огляд та підготовка середовища
- **Статті 04–08:** Базова версія у Kubernetes (Pod → Deployment → Service → ConfigMap/Secret → PVC)
- **Статті 09–12:** Production-hardening (StatefulSet, probes, Ingress, resource limits)
- **Статті 13–16:** Автоматизація (HPA, Jobs, RBAC, Helm chart)
- **Статті 17–18:** Observability та CI/CD

### Технологічний стек наскрізного проєкту

| Компонент | Docker Compose (наявний) | Kubernetes (новий курс) |
|-----------|--------------------------|------------------------|
| Backend | ASP.NET Core 8 | Deployment + Service |
| База даних | PostgreSQL + named volume | StatefulSet + PVC |
| Кеш | Redis | Deployment + ClusterIP |
| Конфігурація | `.env` файл | ConfigMap + Secret |
| Маршрутизація | Nginx у Compose | Ingress Controller |
| Масштабування | `--scale` (ручне) | HPA (автоматичне) |
| Моніторинг | `profiles: monitoring` | Prometheus + Grafana |
| Деплой | `docker compose up` | ArgoCD + GitOps |

---

## Відповідність стилю `prompt.md`

Кожна стаття будується за структурою:
1. **Hook** — проблема, яку не вирішує Docker Compose
2. **Місток** — явний зв'язок з попереднім Docker-матеріалом
3. **Концепція** — академічне пояснення з аналогіями
4. **Діаграма** — Mermaid (прості) або PlantUML (складні архітектурні)
5. **Код** — YAML-маніфести з детальним розбором рядок за рядком
6. **Практика** — 3 рівні завдань

> [!IMPORTANT]
> **Питання до затвердження:**
> 1. Чи потрібна окрема стаття про `DaemonSet` та `StaticPod` (системні компоненти)? Або вистачить згадки у статті про архітектуру?
> 2. Чи включати статтю про **Service Mesh** (Istio/Linkerd)? Це суттєво збільшить обсяг, але закриє тему mTLS та traffic management.
> 3. Чи потрібна стаття про **Kubernetes Security** (Pod Security Standards, OPA Gatekeeper, Falco) як окремий модуль?
> 4. Фокус наскрізного проєкту: лише .NET/C# (як у Docker-курсі) чи додати паралельні приклади на Node.js?
