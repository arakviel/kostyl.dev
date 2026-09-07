# HTTPS у продакшені

## Короткий зміст

У цій лекції вивчається налаштування HTTPS для безпечної передачі даних у продакшн середовищі:

- **TLS сертифікати** — криптографічні сертифікати для підтвердження ідентичності сервера, структура: public key, private key, certificate chain, CA (Certificate Authority)
- **Let's Encrypt** — безкоштовні TLS сертифікати з автоматичним оновленням, використання Certbot для отримання сертифікатів, wildcards для субдоменів (*.example.com)
- **Reverse proxy (Nginx)** — термінація TLS на рівні reverse proxy замість Node.js застосунку, конфігурація Nginx для HTTPS, проксування до NestJS на localhost, переваги: кращa продуктивність TLS, централізоване керування сертифікатами
- **Reverse proxy (Traefik)** — сучасна альтернатива Nginx з автоматичним отриманням Let's Encrypt сертифікатів, інтеграція з Docker, автоматичне оновлення
- **HTTP → HTTPS редирект** — автоматичне перенаправлення HTTP трафіку на HTTPS, конфігурація на рівні Nginx/Traefik, код відповіді 301 Moved Permanently
- **HSTS (HTTP Strict Transport Security)** — примусове використання HTTPS на рівні браузера після першого відвідування, заголовок Strict-Transport-Security з maxAge, includeSubDomains для всіх субдоменів, preload для включення у браузерні списки
- **Автоматичне оновлення сертифікатів** — cron jobs для Certbot, systemd timers, моніторинг дати закінчення сертифікатів, алерти при проблемах з оновленням
- **Налаштування у NestJS** — HTTPS listener у NestJS (опціонально), використання fs для читання сертифікатів, HTTPSOptions конфігурація

Розглядаються практичні сценарії: налаштування HTTPS для VPS через Nginx + Certbot, конфігурація для Docker Compose з Traefik, тестування TLS через ssllabs.com, моніторинг експірації сертифікатів, troubleshooting типових проблем (mixed content, certificate chain issues).

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати налаштування HTTPS для продакшн середовища через Let's Encrypt та reverse proxy.
- Навчитися конфігурувати Nginx та Traefik для термінації TLS з автоматичним оновленням сертифікатів.
- Впровадити HTTP → HTTPS редирект та HSTS для примусового використання захищеного з'єднання.
- Налаштувати моніторинг дати закінчення сертифікатів та автоматичні алерти.
- Вирішувати типові проблеми HTTPS (mixed content, certificate chain, port forwarding).

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **TLS (Transport Layer Security):** криптографічний протокол для безпечної передачі даних через мережу (попередник — SSL).
- **Certificate Authority (CA):** довірена організація, що підписує TLS сертифікати (наприклад, Let's Encrypt, DigiCert).
- **Certificate Chain:** ланцюжок сертифікатів від кореневого CA до кінцевого сертифіката сервера.
- **Reverse Proxy:** проміжний сервер, що приймає клієнтські запити та перенаправляє їх до backend застосунку.
- **TLS Termination:** розшифрування HTTPS трафіку на рівні reverse proxy (backend отримує HTTP).
- **Wildcard Certificate:** сертифікат для всіх субдоменів (*.example.com).

::

::

---

## TLS/HTTPS: Основи безпечного з'єднання

У попередній лекції ми розглянули захист від типових атак на веб-застосунки: XSS, CSRF, SQL Injection та інших. Усі ці заходи захисту **втрачають сенс**, якщо трафік між клієнтом та сервером передається через незахищений HTTP — зловмисник у мережі може перехопити паролі, токени автентифікації, особисті дані користувачів.

**HTTPS (HTTP Secure)** — це HTTP протокол, обгорнутий у шар TLS шифрування. Він гарантує:

1. **Конфіденційність:** дані зашифровані, зловмисник не може прочитати трафік.
2. **Цілісність:** дані не можуть бути змінені під час передачі без детектування.
3. **Автентичність:** клієнт може перевірити, що спілкується саме з легітимним сервером (через TLS сертифікат).

### Чому HTTPS критичний у продакшені?

**Без HTTPS:**

```mermaid
graph LR
    Client[Клієнт<br/>Chrome] -->|HTTP<br/>незашифровано| Attacker[🔴 Зловмисник<br/>перехоплює трафік]
    Attacker -->|Читає:<br/>паролі, токени, дані| Server[Сервер]
    Server -->|HTTP відповідь| Attacker
    Attacker -->|Модифікує відповідь| Client
```

**З HTTPS:**

```mermaid
graph LR
    Client[Клієнт<br/>Chrome] -->|HTTPS<br/>🔒 зашифровано| Attacker[⚪ Зловмисник<br/>бачить лише gibberish]
    Attacker -->|Не може розшифрувати| Server[Сервер]
    Server -->|HTTPS відповідь<br/>🔒 зашифрована| Client
```

**Сценарії атак без HTTPS:**

- **Man-in-the-Middle (MITM):** зловмисник у публічній Wi-Fi мережі (кафе, аеропорт) перехоплює трафік та краде credentials.
- **Session Hijacking:** зловмисник краде session cookie та отримує доступ до акаунту користувача.
- **Content Injection:** зловмисник модифікує HTML відповідь сервера, впроваджуючи зловмисний JavaScript.

::warning
**Увага:** сучасні браузери позначають HTTP сайти як "Not Secure" та блокують багато функцій (Geolocation API, Camera/Microphone access, Service Workers) на HTTP. Google також знижує рейтинг у пошуку для сайтів без HTTPS.
::

### Анатомія TLS сертифіката

**TLS сертифікат** — це цифровий документ, що підтверджує ідентичність сервера та містить публічний ключ для шифрування.

**Структура сертифіката:**

```
Subject: CN=example.com              # Домен, для якого виданий сертифікат
Issuer: CN=Let's Encrypt Authority   # Certificate Authority, що підписала
Valid From: 2024-01-01               # Дата початку дії
Valid To: 2024-04-01                 # Дата закінчення (зазвичай 90 днів для Let's Encrypt)
Public Key: RSA 2048 bits            # Публічний ключ для шифрування
Signature: SHA256withRSA             # Цифровий підпис CA
```

**Три компоненти:**

1. **Public Key (Публічний ключ):** використовується клієнтом для шифрування даних.
2. **Private Key (Приватний ключ):** зберігається на сервері, використовується для розшифрування. **Ніколи не передається клієнту!**
3. **Certificate Chain (Ланцюжок сертифікатів):** послідовність сертифікатів від кореневого CA до кінцевого сертифіката сервера.

**Процес TLS Handshake (спрощено):**

```mermaid
sequenceDiagram
    participant Client as Клієнт (Chrome)
    participant Server as Сервер (Nginx)

    Client->>Server: 1. ClientHello (підтримувані cipher suites)
    Server->>Client: 2. ServerHello (обраний cipher suite)
    Server->>Client: 3. Certificate (TLS сертифікат)
    Client->>Client: 4. Перевірка сертифіката<br/>(підпис CA, термін дії, домен)
    Client->>Server: 5. Key Exchange (генерація session key)
    Server->>Server: 6. Розшифрування session key<br/>(через private key)
    Client->>Server: 7. Encrypted Data (з session key)
    Server->>Client: 8. Encrypted Response
```

**Після успішного handshake:** клієнт та сервер використовують **симетричний session key** для шифрування всього наступного трафіку (значно швидше за асиметричне шифрування).

---

## Let's Encrypt: Безкоштовні TLS сертифікати

**Let's Encrypt** — це некомерційний Certificate Authority, що надає безкоштовні TLS сертифікати з автоматичним оновленням. Це стандарт для малих та середніх проєктів.

### Переваги Let's Encrypt

| Аспект | Let's Encrypt | Комерційні CA (DigiCert, Sectigo) |
|--------|---------------|-----------------------------------|
| **Вартість** | Безкоштовно | $50-$300/рік |
| **Термін дії** | 90 днів (автооновлення) | 1-2 роки |
| **Автоматизація** | Повна (Certbot, ACME protocol) | Частково |
| **Wildcard сертифікати** | Підтримуються (через DNS challenge) | Підтримуються (за додаткову плату) |
| **Рівень валідації** | Domain Validation (DV) | DV, Organization Validation (OV), Extended Validation (EV) |

**Коли використовувати комерційні CA:**

- Потрібен **Extended Validation (EV)** сертифікат (зелений рядок з назвою компанії у браузері).
- Вимоги регулятора або корпоративної політики.
- Потрібна технічна підтримка 24/7.

### Certbot: CLI інструмент для Let's Encrypt

**Certbot** — це офіційний клієнт ACME protocol для отримання та оновлення Let's Encrypt сертифікатів.

**Встановлення Certbot (Ubuntu/Debian):**

```bash
# Оновити package lists
sudo apt update

# Встановити Certbot
sudo apt install certbot python3-certbot-nginx -y

# Перевірка версії
certbot --version
```

**Встановлення (macOS через Homebrew):**

```bash
brew install certbot
```

---

## Nginx як Reverse Proxy з HTTPS

**Reverse Proxy** — це архітектурний патерн, де Nginx приймає всі вхідні HTTPS запити, розшифровує їх (TLS termination) та перенаправляє на backend застосунок через HTTP на localhost.

### Переваги Reverse Proxy підходу

```mermaid
graph LR
    Internet[🌐 Інтернет] -->|HTTPS :443| Nginx[Nginx<br/>Reverse Proxy<br/>TLS Termination]
    Nginx -->|HTTP :3000<br/>localhost| NestJS[NestJS<br/>Application]
```

**Чому не робити TLS безпосередньо у NestJS:**

1. **Продуктивність:** Nginx оптимізований для TLS termination (C++ проти JavaScript).
2. **Централізоване керування:** один конфіг для кількох backend сервісів.
3. **Static files:** Nginx ефективно віддає статичні файли (images, CSS, JS).
4. **Load balancing:** Nginx може розподіляти трафік між кількома інстансами NestJS.
5. **Rate limiting:** Nginx має вбудовані модулі для rate limiting на рівні мережі.

### Налаштування Nginx + Certbot

**Крок 1: Встановлення Nginx**

```bash
# Ubuntu/Debian
sudo apt install nginx -y

# Запустити Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Перевірка статусу
sudo systemctl status nginx
```

**Крок 2: Базова конфігурація для HTTP (тимчасово)**

```nginx
# /etc/nginx/sites-available/example.com
server {
    listen 80;
    server_name example.com www.example.com;

    # Тимчасова конфігурація для верифікації домену Certbot
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Активація конфігурації:**

```bash
# Створити symbolic link
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

# Перевірка синтаксису
sudo nginx -t

# Перезавантажити Nginx
sudo systemctl reload nginx
```

**Крок 3: Отримання Let's Encrypt сертифіката**

```bash
# Автоматична конфігурація Nginx через Certbot
sudo certbot --nginx -d example.com -d www.example.com

# Інтерактивні питання:
# 1. Email для термінових повідомлень: your@email.com
# 2. Згода з Terms of Service: Yes
# 3. Редирект HTTP → HTTPS: Yes (рекомендовано)
```

**Що робить Certbot:**

1. Створює тимчасовий файл у `.well-known/acme-challenge/` для верифікації домену.
2. Let's Encrypt сервер перевіряє, чи файл доступний через HTTP.
3. Якщо успішно — видає сертифікат.
4. Certbot автоматично модифікує Nginx конфіг, додаючи HTTPS блок.

**Крок 4: Перевірка оновленої конфігурації**

```nginx
# /etc/nginx/sites-available/example.com (після Certbot)
server {
    listen 80;
    server_name example.com www.example.com;
    
    # Редирект на HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL сертифікати (додані Certbot)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Проксування до NestJS
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # HSTS (додано вручну)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}
```

**Крок 5: Тестування HTTPS**

```bash
# Перевірка через curl
curl -I https://example.com

# Очікуваний результат:
# HTTP/2 200
# strict-transport-security: max-age=31536000; includeSubDomains; preload
```

### Автоматичне оновлення сертифікатів

Let's Encrypt сертифікати дійсні **90 днів**. Certbot автоматично налаштовує оновлення через **systemd timer** або **cron job**.

**Перевірка автоматичного оновлення:**

```bash
# Systemd timer
sudo systemctl status certbot.timer

# Ручне оновлення (dry-run)
sudo certbot renew --dry-run

# Ручне оновлення (real)
sudo certbot renew
```

**Cron job (якщо systemd timer не налаштований):**

```bash
# Додати до crontab
sudo crontab -e

# Запускати щодня о 03:00
0 3 * * * certbot renew --quiet && systemctl reload nginx
```

**Моніторинг дати закінчення:**

```bash
# Перевірка дати закінчення сертифіката
sudo certbot certificates

# Результат:
# Certificate Name: example.com
#   Domains: example.com www.example.com
#   Expiry Date: 2024-04-01 12:00:00+00:00 (VALID: 89 days)
```




---

## Traefik: Сучасний Reverse Proxy з автоматичним HTTPS

**Traefik** — це cloud-native reverse proxy та load balancer з вбудованою підтримкою Let's Encrypt, автоматичним service discovery для Docker/Kubernetes та динамічною конфігурацією без перезавантаження.

### Переваги Traefik над Nginx

| Аспект | Traefik | Nginx |
|--------|---------|-------|
| **Let's Encrypt** | Автоматично (без Certbot) | Через Certbot |
| **Docker integration** | Native (labels) | Потребує ручної конфігурації |
| **Dashboard** | Вбудований | Потребує Nginx Plus |
| **Конфігурація** | Динамічна (без reload) | Статична (потребує reload) |
| **Складність** | Вища крива навчання | Простіша для базових сценаріїв |

### Docker Compose конфігурація з Traefik

**Структура проєкту:**

```
project/
├── docker-compose.yml
├── traefik.yml          # Статична конфігурація Traefik
└── app/
    └── Dockerfile
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v3.0
    container_name: traefik
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    networks:
      - web
    ports:
      - "80:80"     # HTTP
      - "443:443"   # HTTPS
      - "8080:8080" # Dashboard (лише для dev, видалити у prod)
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro  # Docker API
      - ./traefik.yml:/traefik.yml:ro                 # Статична конфігурація
      - ./acme.json:/acme.json                        # Let's Encrypt сертифікати
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.traefik.entrypoints=http"
      - "traefik.http.routers.traefik.rule=Host(`traefik.example.com`)"
      - "traefik.http.middlewares.traefik-auth.basicauth.users=admin:$$apr1$$H6..." # htpasswd hash
      - "traefik.http.middlewares.traefik-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.traefik.middlewares=traefik-https-redirect"
      - "traefik.http.routers.traefik-secure.entrypoints=https"
      - "traefik.http.routers.traefik-secure.rule=Host(`traefik.example.com`)"
      - "traefik.http.routers.traefik-secure.middlewares=traefik-auth"
      - "traefik.http.routers.traefik-secure.tls=true"
      - "traefik.http.routers.traefik-secure.tls.certresolver=letsencrypt"
      - "traefik.http.routers.traefik-secure.service=api@internal"

  app:
    build: ./app
    container_name: nestjs-app
    restart: unless-stopped
    networks:
      - web
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@postgres:5432/db
    labels:
      - "traefik.enable=true"
      # HTTP → HTTPS редирект
      - "traefik.http.routers.app.entrypoints=http"
      - "traefik.http.routers.app.rule=Host(`example.com`) || Host(`www.example.com`)"
      - "traefik.http.middlewares.app-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.app.middlewares=app-https-redirect"
      # HTTPS
      - "traefik.http.routers.app-secure.entrypoints=https"
      - "traefik.http.routers.app-secure.rule=Host(`example.com`) || Host(`www.example.com`)"
      - "traefik.http.routers.app-secure.tls=true"
      - "traefik.http.routers.app-secure.tls.certresolver=letsencrypt"
      - "traefik.http.routers.app-secure.service=app"
      - "traefik.http.services.app.loadbalancer.server.port=3000"

  postgres:
    image: postgres:16-alpine
    container_name: postgres
    restart: unless-stopped
    networks:
      - web
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=db
    volumes:
      - postgres_data:/var/lib/postgresql/data

networks:
  web:
    external: true

volumes:
  postgres_data:
```

**traefik.yml:**

```yaml
# Статична конфігурація Traefik
api:
  dashboard: true  # Увімкнути dashboard

entryPoints:
  http:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: https
          scheme: https

  https:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false  # Лише контейнери з traefik.enable=true

certificatesResolvers:
  letsencrypt:
    acme:
      email: your@email.com
      storage: acme.json
      httpChallenge:
        entryPoint: http
      # Для wildcard сертифікатів (*.example.com):
      # dnsChallenge:
      #   provider: cloudflare
      #   resolvers:
      #     - "1.1.1.1:53"
      #     - "8.8.8.8:53"
```

**Підготовка та запуск:**

```bash
# Створити acme.json з правильними permissions
touch acme.json
chmod 600 acme.json

# Створити Docker network
docker network create web

# Запустити
docker compose up -d

# Перевірка логів
docker logs traefik -f
```

**Що відбувається:**

1. Traefik автоматично виявляє контейнери з `traefik.enable=true`.
2. При першому HTTPS запиті до `example.com` — отримує Let's Encrypt сертифікат через HTTP-01 challenge.
3. Зберігає сертифікат у `acme.json`.
4. Автоматично оновлює сертифікат за 30 днів до закінчення.

::tip
**Wildcard сертифікати:** для `*.example.com` використовуйте DNS-01 challenge замість HTTP-01. Потребує API доступу до DNS провайдера (Cloudflare, Route53, тощо).
::

---

## Wildcard сертифікати для субдоменів

**Wildcard certificate** дозволяє захистити **всі субдомени** одним сертифікатом: `*.example.com` покриває `api.example.com`, `admin.example.com`, `app.example.com`.

### Отримання wildcard через Certbot + Cloudflare DNS

**Крок 1: Встановлення Cloudflare plugin**

```bash
sudo apt install python3-certbot-dns-cloudflare -y
```

**Крок 2: Створення Cloudflare API token**

1. Увійти у Cloudflare Dashboard
2. My Profile → API Tokens → Create Token
3. Template: **Edit zone DNS**
4. Zone Resources: Include → Specific zone → `example.com`
5. Копіювати згенерований токен

**Крок 3: Налаштування credentials**

```bash
# Створити файл з credentials
sudo nano /etc/letsencrypt/cloudflare.ini

# Вміст:
dns_cloudflare_api_token = YOUR_CLOUDFLARE_API_TOKEN

# Встановити permissions
sudo chmod 600 /etc/letsencrypt/cloudflare.ini
```

**Крок 4: Отримання wildcard сертифіката**

```bash
sudo certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d example.com \
  -d '*.example.com'

# Результат:
# Сertificate: /etc/letsencrypt/live/example.com/fullchain.pem
# Private Key: /etc/letsencrypt/live/example.com/privkey.pem
```

**Nginx конфігурація для кількох субдоменів:**

```nginx
# Основний домен
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}

# API субдомен
server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3001;
    }
}

# Admin панель
server {
    listen 443 ssl http2;
    server_name admin.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3002;
    }
}
```

---

## HTTPS у NestJS (опціонально)

У більшості випадків TLS termination виконується на рівні reverse proxy (Nginx/Traefik). Проте для локальної розробки або простих single-server setup можна налаштувати HTTPS безпосередньо у NestJS.

### Генерація самопідписного сертифіката для розробки

```bash
# Генерація private key та сертифіката
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes

# Інтерактивні питання (можна залишити порожнім для dev):
# Country Name: UA
# Common Name: localhost
```

### HTTPS listener у NestJS

```typescript
// src/main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import * as fs from 'fs';

async function bootstrap() {
  const httpsOptions = {
    key: fs.readFileSync('./secrets/key.pem'),
    cert: fs.readFileSync('./secrets/cert.pem'),
  };

  const app = await NestFactory.create(AppModule, { httpsOptions });

  await app.listen(3000);
  console.log('Server running on https://localhost:3000');
}
bootstrap();
```

**Для продакшену з Let's Encrypt сертифікатами:**

```typescript
// src/main.ts
import * as fs from 'fs';

async function bootstrap() {
  const isProduction = process.env.NODE_ENV === 'production';

  const httpsOptions = isProduction
    ? {
        key: fs.readFileSync('/etc/letsencrypt/live/example.com/privkey.pem'),
        cert: fs.readFileSync('/etc/letsencrypt/live/example.com/fullchain.pem'),
      }
    : undefined; // HTTP у dev режимі

  const app = await NestFactory.create(AppModule, { httpsOptions });

  await app.listen(3000);
}
bootstrap();
```

::warning
**Увага:** цей підхід **не рекомендується** для продакшену через:
- Гіршу продуктивність TLS у Node.js порівняно з Nginx
- Складніше керування сертифікатами (потрібен перезапуск при оновленні)
- Відсутність centralized rate limiting та load balancing
::

---

## Моніторинг та алерти для сертифікатів

### Script для перевірки дати закінчення

```bash
#!/bin/bash
# check-cert-expiry.sh

DOMAIN="example.com"
THRESHOLD_DAYS=30  # Попереджати за 30 днів до закінчення

# Отримати дату закінчення сертифіката
EXPIRY_DATE=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)

# Конвертувати у Unix timestamp
EXPIRY_TIMESTAMP=$(date -d "$EXPIRY_DATE" +%s)
CURRENT_TIMESTAMP=$(date +%s)

# Розрахувати залишок днів
DAYS_LEFT=$(( ($EXPIRY_TIMESTAMP - $CURRENT_TIMESTAMP) / 86400 ))

echo "Certificate for $DOMAIN expires in $DAYS_LEFT days"

if [ $DAYS_LEFT -lt $THRESHOLD_DAYS ]; then
  echo "⚠️ WARNING: Certificate expires soon!"
  # Відправити алерт (Slack, email, тощо)
  curl -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"⚠️ SSL certificate for $DOMAIN expires in $DAYS_LEFT days!\"}" \
    $SLACK_WEBHOOK_URL
fi
```

**Cron job для щоденної перевірки:**

```bash
sudo crontab -e

# Додати:
0 9 * * * /usr/local/bin/check-cert-expiry.sh
```

### Prometheus + Grafana моніторинг

```bash
# Встановити ssl_exporter
docker run -d \
  --name ssl_exporter \
  -p 9219:9219 \
  ribbybibby/ssl-exporter:latest \
  --web.listen-address=:9219

# Prometheus конфігурація
# prometheus.yml
scrape_configs:
  - job_name: 'ssl'
    metrics_path: /probe
    params:
      module: [https]
    static_configs:
      - targets:
        - example.com:443
        - api.example.com:443
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: ssl_exporter:9219
```

**Grafana Alert:**

```promql
# Alert коли залишилось < 30 днів
ssl_cert_not_after - time() < 2592000
```

---

## Troubleshooting типових проблем

### Проблема 1: Mixed Content (HTTP ресурси на HTTPS сторінці)

**Симптом:** браузер блокує завантаження images/scripts через HTTP на HTTPS сторінці.

```
Mixed Content: The page at 'https://example.com' was loaded over HTTPS,
but requested an insecure resource 'http://cdn.example.com/image.jpg'.
This request has been blocked; the content must be served over HTTPS.
```

**Рішення:**

```html
<!-- ❌ Хардкод HTTP -->
<img src="http://cdn.example.com/image.jpg">

<!-- ✅ Protocol-relative URL -->
<img src="//cdn.example.com/image.jpg">

<!-- ✅ HTTPS -->
<img src="https://cdn.example.com/image.jpg">
```

**Content Security Policy для автоматичного upgrade:**

```typescript
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      upgradeInsecureRequests: [], // Автоматично HTTP → HTTPS
    },
  })
);
```

### Проблема 2: Certificate Chain Issues

**Симптом:** деякі браузери/клієнти не довіряють сертифікату.

**Причина:** неповний certificate chain (відсутній intermediate certificate).

**Рішення:** використовуйте `fullchain.pem` замість `cert.pem`:

```nginx
# ❌ Неправильно
ssl_certificate /etc/letsencrypt/live/example.com/cert.pem;

# ✅ Правильно
ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
```

**Перевірка chain:**

```bash
openssl s_client -connect example.com:443 -showcerts
```

### Проблема 3: Port 80/443 вже зайнятий

**Симптом:**

```
Error: bind() to 0.0.0.0:443 failed (98: Address already in use)
```

**Діагностика:**

```bash
# Знайти процес, що використовує порт
sudo lsof -i :443

# Альтернативно
sudo netstat -tulpn | grep :443
```

**Рішення:**

```bash
# Зупинити конфліктуючий процес
sudo systemctl stop apache2  # Якщо Apache

# Або змінити порт у конфігурації
```

### Проблема 4: Certbot не може верифікувати домен

**Симптом:**

```
Failed authorization procedure. example.com (http-01):
Fetching http://example.com/.well-known/acme-challenge/XXX: Connection refused
```

**Причини:**

1. **Firewall блокує порт 80**
2. **DNS не вказує на ваш сервер**
3. **Nginx не проксує `.well-known/`**

**Рішення:**

```bash
# 1. Перевірка DNS
dig example.com +short
# Має повернути IP вашого сервера

# 2. Перевірка firewall
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 3. Nginx конфігурація
location /.well-known/acme-challenge/ {
    root /var/www/html;
}
```

### Проблема 5: ERR_CERT_COMMON_NAME_INVALID

**Симптом:** браузер показує помилку "Your connection is not private".

**Причина:** сертифікат виданий для іншого домену (наприклад, для `www.example.com`, а відкривається `example.com`).

**Рішення:** включити обидва домени при отриманні сертифіката:

```bash
sudo certbot --nginx -d example.com -d www.example.com
```



---

## Тестування TLS конфігурації

### SSL Labs Test

**Qualys SSL Labs** — найавторитетніший інструмент для аналізу TLS конфігурації.

**Тестування:**

1. Відкрийте [https://www.ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/)
2. Введіть ваш домен: `example.com`
3. Натисніть **Submit**

**Очікуваний результат:** оцінка **A або A+**

**Критерії оцінки:**

- **Certificate:** валідність, ланцюжок, алгоритм підпису
- **Protocol Support:** TLS 1.2, TLS 1.3 (без SSLv3, TLS 1.0, TLS 1.1)
- **Key Exchange:** міцність ключа (мінімум RSA 2048 або ECDSA 256)
- **Cipher Strength:** підтримка сучасних cipher suites

### Покращення оцінки до A+

**Nginx конфігурація для A+ рейтингу:**

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    # Сертифікати
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS протоколи (лише 1.2 та 1.3)
    ssl_protocols TLSv1.2 TLSv1.3;

    # Cipher suites (пріоритет сучасним)
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # HSTS (строгий)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # OCSP Stapling (покращує швидкість handshake)
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 1.1.1.1 8.8.8.8 valid=300s;
    resolver_timeout 5s;

    # Session cache
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # Diffie-Hellman parameter
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

**Ключові покращення:**

- **TLS 1.3:** найшвидший та найбезпечніший протокол
- **OCSP Stapling:** браузер не робить зайвий запит до CA для перевірки сертифіката
- **Session cache:** повторні з'єднання швидші
- **HSTS preload:** максимальний рівень захисту

### Тестування через CLI

```bash
# Перевірка TLS версій
nmap --script ssl-enum-ciphers -p 443 example.com

# Детальна інформація про сертифікат
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -text

# Перевірка HSTS header
curl -I https://example.com | grep -i strict
```

---

## Best Practices для продакшену

### 1. Використовуйте Reverse Proxy

```
✅ Рекомендовано: Internet → Nginx/Traefik (TLS) → NestJS (HTTP)
❌ Не рекомендовано: Internet → NestJS (TLS)
```

**Причини:** продуктивність, централізоване керування, статичні файли, load balancing.

### 2. Автоматизуйте оновлення сертифікатів

```bash
# Systemd timer (автоматично налаштований Certbot)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Моніторинг
sudo systemctl status certbot.timer
```

### 3. Завжди редіректьте HTTP → HTTPS

```nginx
# Nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### 4. Увімкніть HSTS з preload

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

**Подайте домен до HSTS Preload List:** [hstspreload.org](https://hstspreload.org)

### 5. Моніторьте дату закінчення сертифікатів

```bash
# Prometheus + ssl_exporter
# Grafana alert коли < 30 днів
```

### 6. Використовуйте HTTP/2

```nginx
listen 443 ssl http2;  # Додати http2
```

**Переваги:** multiplexing (кілька запитів через одне з'єднання), server push, header compression.

### 7. Налаштуйте правильні DNS записи

```
# A record
example.com.        300  IN  A  203.0.113.10

# AAAA record (IPv6, опціонально)
example.com.        300  IN  AAAA  2001:db8::1

# WWW subdomain
www.example.com.    300  IN  CNAME  example.com.
```

### 8. Firewall налаштування

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP (для Certbot challenge)
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable

# Перевірка
sudo ufw status
```

### 9. Регулярні security audits

```bash
# Щомісячний аудит
npm audit
sudo apt update && sudo apt upgrade -y
sudo certbot renew --dry-run
```

### 10. Backup сертифікатів

```bash
# Backup Let's Encrypt директорії
sudo tar -czf letsencrypt-backup-$(date +%F).tar.gz /etc/letsencrypt

# Копіювання на remote сервер
scp letsencrypt-backup-*.tar.gz user@backup-server:/backups/
```

---

## Повна конфігурація для production

### Nginx production config

```nginx
# /etc/nginx/sites-available/example.com

# HTTP → HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # Для Certbot challenge
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # Всі інші запити → HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    # SSL сертифікати
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL протоколи та cipher suites
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 1.1.1.1 8.8.8.8 valid=300s;

    # Session
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;

    # DH params
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers (додатково до Helmet у NestJS)
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json;

    # Статичні файли (якщо є)
    location /static/ {
        alias /var/www/example.com/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy до NestJS
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;

        # Headers
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Cache bypass
        proxy_cache_bypass $http_upgrade;
    }

    # Logging
    access_log /var/log/nginx/example.com.access.log;
    error_log /var/log/nginx/example.com.error.log;
}
```

### Systemd service для NestJS

```ini
# /etc/systemd/system/nestjs-app.service
[Unit]
Description=NestJS Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/example.com
ExecStart=/usr/bin/node dist/main.js
Restart=always
RestartSec=10

Environment=NODE_ENV=production
Environment=PORT=3000

# Логування
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Запуск:**

```bash
# Перезавантажити systemd
sudo systemctl daemon-reload

# Увімкнути автозапуск
sudo systemctl enable nestjs-app

# Запустити
sudo systemctl start nestjs-app

# Перевірка статусу
sudo systemctl status nestjs-app

# Логи
sudo journalctl -u nestjs-app -f
```

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чому Let's Encrypt сертифікати дійсні лише 90 днів?" icon="i-lucide-help-circle"}

**Let's Encrypt навмисно встановила короткий термін дії (90 днів) з кількох причин:**

**1. Автоматизація як норма**

Короткий термін **примушує** адміністраторів налаштувати автоматичне оновлення сертифікатів. Це зменшує ймовірність забути оновити сертифікат та отримати downtime.

```bash
# Автоматичне оновлення через systemd timer (налаштований Certbot)
sudo systemctl status certbot.timer
```

**2. Безпека при компрометації**

Якщо приватний ключ було скомпрометовано (витік, хакерська атака), сертифікат **автоматично стане недійсним через 90 днів**, навіть якщо компрометація не була виявлена.

Для порівняння: комерційні CA видають сертифікати на 1-2 роки — компрометований ключ може використовуватися зловмисником значно довше.

**3. Швидше впровадження змін**

Короткий термін дозволяє Let's Encrypt швидше впроваджувати зміни у політиках безпеки (наприклад, заборона застарілих алгоритмів), без необхідності чекати закінчення багаторічних сертифікатів.

**Висновок:** 90 днів — це баланс між безпекою та зручністю. Автоматичне оновлення через Certbot робить цей термін непомітним для адміністраторів.

::

::accordion-item{label="❓ Чи можна використовувати один Let's Encrypt сертифікат для кількох серверів?" icon="i-lucide-help-circle"}

**Так, але з обережністю.**

**Технічно можливо:** сертифікат (`.pem` файли) можна скопіювати на кілька серверів:

```bash
# На сервері 1 (де отримано сертифікат)
sudo tar -czf cert-backup.tar.gz /etc/letsencrypt/live/example.com/

# Копіювання на сервер 2
scp cert-backup.tar.gz user@server2:/tmp/

# На сервері 2
sudo tar -xzf /tmp/cert-backup.tar.gz -C /etc/letsencrypt/
```

**Проблеми:**

1. **Синхронізація оновлень:** коли сервер 1 оновить сертифікат (через 60 днів), потрібно **вручну** скопіювати новий сертифікат на сервер 2. Якщо забути — сервер 2 матиме expired сертифікат.

2. **Безпека приватного ключа:** копіювання приватного ключа між серверами збільшує ризик компрометації.

**Рекомендовані альтернативи:**

**1. Окремі сертифікати на кожному сервері:**

```bash
# Сервер 1
sudo certbot --nginx -d server1.example.com

# Сервер 2
sudo certbot --nginx -d server2.example.com
```

**2. Wildcard сертифікат з централізованим оновленням:**

```bash
# Отримати wildcard на одному сервері
sudo certbot certonly --dns-cloudflare -d '*.example.com'

# Налаштувати автоматичну синхронізацію через rsync cron job
0 4 * * * rsync -avz /etc/letsencrypt/live/example.com/ user@server2:/etc/letsencrypt/live/example.com/
```

**3. Load Balancer з TLS termination:**

Використовуйте один reverse proxy (Nginx/Traefik) для TLS termination, який проксує на кілька backend серверів через HTTP.

**Висновок:** для production краще використовувати окремі сертифікати або централізований TLS termination.

::

::accordion-item{label="❓ Що робити, якщо Certbot не може оновити сертифікат автоматично?" icon="i-lucide-help-circle"}

**Діагностика та рішення:**

**Крок 1: Перевірка логів**

```bash
sudo journalctl -u certbot.timer -n 50

# Або
sudo cat /var/log/letsencrypt/letsencrypt.log
```

**Типові причини помилок:**

**1. Firewall блокує порт 80**

Let's Encrypt потребує доступу до `.well-known/acme-challenge/` через HTTP (порт 80).

```bash
# Перевірка firewall
sudo ufw status

# Дозволити порт 80
sudo ufw allow 80/tcp
```

**2. Nginx конфігурація блокує challenge**

```nginx
# Додати у HTTP server block
location /.well-known/acme-challenge/ {
    root /var/www/html;
    allow all;
}
```

**3. DNS записи змінилися**

```bash
# Перевірка DNS
dig example.com +short

# Має повертати IP вашого сервера
```

**4. Rate Limiting від Let's Encrypt**

Let's Encrypt обмежує кількість запитів:
- **50 сертифікатів на домен за тиждень**
- **5 невдалих спроб за годину**

Рішення: почекати годину або день перед повторною спробою.

**Крок 2: Ручне оновлення з діагностикою**

```bash
# Verbose режим для детального виводу
sudo certbot renew --dry-run --verbose

# Якщо dry-run успішний — реальне оновлення
sudo certbot renew --force-renewal
```

**Крок 3: Перезапуск Nginx після оновлення**

```bash
# Додати post-hook до Certbot
sudo certbot renew --deploy-hook "systemctl reload nginx"
```

**Крок 4: Налаштування алертів**

Щоб не пропустити проблеми з оновленням, налаштуйте моніторинг:

```bash
# Script для перевірки та відправки алерту
#!/bin/bash
EXPIRY=$(sudo certbot certificates | grep "Expiry Date" | head -n1 | awk '{print $3}')
DAYS_LEFT=$(( ($(date -d "$EXPIRY" +%s) - $(date +%s)) / 86400 ))

if [ $DAYS_LEFT -lt 15 ]; then
  echo "⚠️ Certificate expires in $DAYS_LEFT days!" | mail -s "SSL Alert" admin@example.com
fi
```

**Висновок:** більшість проблем з оновленням пов'язані з firewall або DNS. Регулярна перевірка логів та налаштування алертів допоможуть виявити проблеми завчасно.

::

::

---

## Підсумок

::card-group

::card{title="🔒 HTTPS у продакшені" icon="i-lucide-lock"}

**Критичні компоненти:**
- **TLS сертифікати** від Let's Encrypt (безкоштовно)
- **Reverse Proxy** (Nginx/Traefik) для TLS termination
- **HTTP → HTTPS редирект** (301 Moved Permanently)
- **HSTS** для примусового використання HTTPS
- **Автоматичне оновлення** сертифікатів через Certbot

**HTTPS — обов'язкова вимога для production**

::

::card{title="⚙️ Рекомендована архітектура" icon="i-lucide-settings"}

**Best practice setup:**
```
Internet → Nginx (TLS termination)
         → NestJS (HTTP localhost:3000)
```

**Переваги:**
- Кращa продуктивність TLS
- Централізоване керування сертифікатами
- Static files та load balancing
- Rate limiting на мережевому рівні

**Альтернатива для Docker: Traefik з автоматичним Let's Encrypt**

::

::card{title="✅ Checklist для production" icon="i-lucide-check-square"}

**Перед запуском:**
- [ ] Отримати TLS сертифікат (Let's Encrypt)
- [ ] Налаштувати HTTP → HTTPS редирект
- [ ] Увімкнути HSTS з preload
- [ ] Налаштувати автоматичне оновлення (Certbot timer)
- [ ] Тестування через SSL Labs (A/A+ рейтинг)
- [ ] Налаштувати моніторинг експірації сертифікатів
- [ ] Firewall правила (80, 443 відкриті)
- [ ] Backup сертифікатів

**Регулярні перевірки: `sudo certbot renew --dry-run`**

::

::

Цим завершується модуль **"Авторизація та безпека серверних застосунків"**. Ми розглянули повний цикл захисту веб-застосунків: від моделей авторизації (RBAC, ABAC) через практичну імплементацію у NestJS (Guards, Decorators), налаштування security headers (Helmet), захист від rate limiting та типових атак (XSS, CSRF, SQL Injection) до фінального кроку — безпечної передачі даних через HTTPS у продакшн середовищі.
