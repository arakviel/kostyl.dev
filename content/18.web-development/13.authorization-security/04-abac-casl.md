# ABAC та бібліотека CASL

## Короткий зміст

У цій лекції вивчається найскладніша та найгнучкіша модель контролю доступу — ABAC через бібліотеку CASL:

- **Attribute-Based Access Control (ABAC)** — рішення про доступ на основі атрибутів: суб'єкта (userId, role, department), ресурсу (authorId, status, category), дії (read, update, delete), контексту (час доби, IP адреса)
- **Бібліотека CASL** — @casl/ability для визначення правил доступу, інтеграція з NestJS через `@nestjs/casl` або власну імплементацію
- **Визначення abilities** — створення `AbilityFactory` для побудови правил доступу на основі користувача, метод `can(action, subject)` для перевірки дозволів
- **Policy rules** — умовні правила доступу: "користувач може редагувати пост, якщо він є автором", "модератор може видаляти пости зі статусом 'pending'"
- **Інтеграція з TypeORM** — використання CASL з entities, перевірка атрибутів entity для прийняття рішення про доступ, складні умови з joins
- **PoliciesGuard** — створення Guard для перевірки політик, передача entity у Guard для умовної перевірки, обробка відмови у доступі

Розглядаються складні сценарії: multi-tenancy (доступ лише до даних свого tenant), organizational hierarchy (менеджер має доступ до даних підлеглих), time-based access (доступ лише у робочі години).

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати концепцію атрибутивного контролю доступу (ABAC) як найгнучкішу модель авторизації.
- Реалізувати систему ABAC у NestJS через бібліотеку CASL (*CASL — "Castle"*).
- Навчитися визначати складні умовні політики доступу на основі атрибутів ресурсів.
- Створити `AbilityFactory` для динамічної побудови правил на основі контексту користувача.
- Інтегрувати CASL з TypeORM Entity для перевірки дозволів на рівні конкретних об'єктів.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Ability:** об'єкт CASL, що містить набір правил (*rules*) для перевірки дозволів.
- **Subject (Суб'єкт):** ресурс або Entity, над яким виконується дія (наприклад, `Post`, `Comment`, `User`).
- **Action (Дія):** операція, що виконується (`read`, `create`, `update`, `delete`, `manage`).
- **Conditions (Умови):** обмеження доступу на основі атрибутів ресурсу (наприклад, `{ authorId: userId }`).
- **Field-Level Permissions:** гранулярний контроль доступу до окремих полів Entity.

::

::

---

## Обмеження попередніх моделей та необхідність ABAC

У попередніх лекціях ми послідовно розглянули три підходи до авторизації, кожен з яких вирішував проблеми попереднього:

1. **RBAC (Role-Based Access Control):** користувачі отримують ролі, маршрути захищаються перевіркою ролей. Проблема: вибух кількості ролей при складній бізнес-логіці.

2. **Permission-Based Access Control:** ролі стають контейнерами для дозволів, перевірка відбувається на рівні конкретних дій (`create:posts`, `delete:comments`). Проблема: неможливість виразити умовні правила.

3. **ABAC (Attribute-Based Access Control):** рішення про доступ приймається динамічно на основі атрибутів користувача, ресурсу та контексту. Це найгнучкіший підхід, але й найскладніший у реалізації.

### Приклади правил, що неможливо реалізувати у Permission-Based

**Правило 1: Власність ресурсу**
*«Користувач може редагувати пост, лише якщо він є його автором»*

У permission-based системі ми можемо створити дозвіл `update:posts`, але він або дозволяє редагувати **всі** пости, або **жодного**. Для перевірки власності доводиться писати додатковий код у сервісному шарі кожного контролера.

**Правило 2: Статус ресурсу**
*«Модератор може видаляти коментарі, але лише ті, що мають статус `pending` або `flagged`»*

Дозвіл `delete:comments` не може виразити умову на основі поля `status`. Знову потрібна додаткова логіка у сервісі.

**Правило 3: Часові обмеження**
*«Автор може редагувати пост протягом 24 годин після публікації»*

Permission-based не підтримує перевірку на основі різниці між `createdAt` та поточним часом.

**Правило 4: Організаційна ієрархія**
*«Менеджер може переглядати звіти всіх підлеглих у своєму департаменті»*

Потрібна складна перевірка з join-запитом до таблиці організаційної структури.

### ABAC як універсальне рішення

**Attribute-Based Access Control (ABAC)** дозволяє виражати всі ці правила декларативно:

```typescript
// Псевдокод правил ABAC
can('update', 'Post', { authorId: currentUser.id })
can('delete', 'Comment', { status: { $in: ['pending', 'flagged'] } })
can('update', 'Post', { publishedAt: { $gt: new Date(Date.now() - 24 * 60 * 60 * 1000) } })
can('read', 'Report', { departmentId: currentUser.departmentId })
```

Замість написання окремої логіки для кожного випадку, ми визначаємо **політики** (*policies*) один раз, а CASL автоматично перевіряє їх при кожному запиті.

---

## Знайомство з бібліотекою CASL

**CASL** (*Castle*) — це TypeScript/JavaScript бібліотека для декларативного управління дозволами. Вона не прив'язана до жодного фреймворку і може використовуватися у будь-якому застосунку (React, Vue, Angular, Node.js).

### Основні пакети CASL

- **`@casl/ability`** — ядро бібліотеки, визначення та перевірка правил доступу.
- **`@casl/mongoose`** (опційно) — інтеграція з Mongoose для MongoDB.
- **`@casl/prisma`** (опційно) — інтеграція з Prisma ORM.

Для NestJS + TypeORM використовуємо лише базовий пакет `@casl/ability` та створюємо власну інтеграцію.

### Встановлення CASL

```bash
npm install @casl/ability
```

### Базовий приклад CASL

Розглянемо найпростіший приклад використання CASL поза контекстом NestJS для розуміння принципів роботи:

```typescript
import { defineAbility, AbilityBuilder } from '@casl/ability';

// Визначаємо типи для TypeScript
type Actions = 'create' | 'read' | 'update' | 'delete';
type Subjects = 'Post' | 'Comment' | 'User';

// Створюємо ability для звичайного користувача
const userAbility = defineAbility<[Actions, Subjects]>((can, cannot) => {
  // Користувач може читати пости
  can('read', 'Post');

  // Користувач може створювати коментарі
  can('create', 'Comment');

  // Користувач може редагувати та видаляти власні коментарі
  can(['update', 'delete'], 'Comment', { authorId: userId });

  // Користувач НЕ може видаляти пости
  cannot('delete', 'Post');
});

// Перевірка дозволів
userAbility.can('read', 'Post');           // true
userAbility.can('create', 'Comment');      // true
userAbility.can('delete', 'Post');         // false

// Перевірка з конкретним об'єктом
const comment = { id: '1', authorId: userId, text: 'Test' };
userAbility.can('update', comment);        // true, якщо authorId співпадає

const anotherComment = { id: '2', authorId: 'другий-користувач', text: 'Test' };
userAbility.can('update', anotherComment); // false, authorId не співпадає
```

**Ключові концепції:**

- **`can(action, subject, conditions?)`** — визначає правило дозволу.
- **`cannot(action, subject, conditions?)`** — визначає правило заборони (має вищий пріоритет за `can`).
- **`conditions`** — об'єкт з умовами, що повинні виконуватися для застосування правила. Підтримує MongoDB-стиль запитів (`$eq`, `$in`, `$ne`, `$gt`, `$lt`).

---

## Архітектура CASL у NestJS

Для інтеграції CASL у NestJS створимо наступні компоненти:

::mermaid

```mermaid
graph TB
    Request[HTTP Request] --> JwtGuard[JwtAuthGuard]
    JwtGuard --> |встановлює user| PoliciesGuard[PoliciesGuard]
    PoliciesGuard --> |створює| AbilityFactory[AbilityFactory]
    AbilityFactory --> |будує| Ability[Ability Object]
    Ability --> |перевіряє| Rules[Policy Rules]
    Rules --> |PERMIT/DENY| Response[HTTP Response]
    
    Controller[Controller] --> |декоратор| CheckPolicies[@CheckPolicies]
    CheckPolicies --> |метадані| PoliciesGuard
    
    style JwtGuard fill:#3b82f6,stroke:#1d4ed8,color:#ffffff
    style PoliciesGuard fill:#f59e0b,stroke:#b45309,color:#ffffff
    style AbilityFactory fill:#10b981,stroke:#047857,color:#ffffff
    style Ability fill:#8b5cf6,stroke:#6d28d9,color:#ffffff
    style Rules fill:#ef4444,stroke:#b91c1c,color:#ffffff
```

::

**Компоненти системи:**

1. **AbilityFactory** — фабрика для створення об'єкта `Ability` на основі контексту користувача.
2. **Policy Handlers** — класи або функції, що визначають конкретні політики доступу.
3. **@CheckPolicies()** — декоратор для позначення політик на маршрутах.
4. **PoliciesGuard** — Guard, що перевіряє виконання політик перед виконанням обробника.

---

## Визначення типів Actions та Subjects

Створимо типи для дій та суб'єктів системи:

```typescript
// src/casl/casl-ability.types.ts

/**
 * Перелік всіх дій, що можуть виконуватися у системі
 */
export enum Action {
  Manage = 'manage', // Спеціальна дія: дозволяє все
  Create = 'create',
  Read = 'read',
  Update = 'update',
  Delete = 'delete',
  Publish = 'publish',
  Unpublish = 'unpublish',
  Approve = 'approve',
}

/**
 * Перелік всіх ресурсів (суб'єктів), що захищаються
 */
export enum Subjects {
  Post = 'Post',
  Comment = 'Comment',
  User = 'User',
  Report = 'Report',
  Settings = 'Settings',
  All = 'all', // Спеціальний суб'єкт: стосується всіх ресурсів
}

/**
 * Тип для Ability: який тип дій можна виконувати над якими суб'єктами
 */
export type AppAbility = Ability<[Action, Subjects]>;
```

**Пояснення спеціальних значень:**

- **`Action.Manage`** — спеціальна дія, що включає всі інші дії. Якщо користувач має `can('manage', 'Post')`, він автоматично має `can('read', 'Post')`, `can('update', 'Post')`, тощо.

- **`Subjects.All`** — спеціальний суб'єкт, що охоплює всі ресурси. Правило `can('read', 'all')` дозволяє читання всіх ресурсів системи.

---

## Створення AbilityFactory

`AbilityFactory` — це сервіс, що створює об'єкт `Ability` з правилами доступу для конкретного користувача на основі його ролей та атрибутів.

```typescript
// src/casl/casl-ability.factory.ts
import { Injectable } from '@nestjs/common';
import {
  Ability,
  AbilityBuilder,
  AbilityClass,
  ExtractSubjectType,
  InferSubjects,
} from '@casl/ability';
import { Action, Subjects } from './casl-ability.types';
import { User } from '../users/entities/user.entity';
import { Post } from '../posts/entities/post.entity';
import { Comment } from '../comments/entities/comment.entity';

// Тип для всіх можливих суб'єктів (включаючи класи Entity)
type SubjectTypes = InferSubjects<typeof Post | typeof Comment | typeof User> | Subjects;

// Тип Ability з підтримкою всіх суб'єктів
export type AppAbility = Ability<[Action, SubjectTypes]>;

@Injectable()
export class CaslAbilityFactory {
  /**
   * Створює Ability об'єкт для користувача
   * Правила залежать від ролі користувача
   */
  createForUser(user: User): AppAbility {
    const { can, cannot, build } = new AbilityBuilder<AppAbility>(
      Ability as AbilityClass<AppAbility>,
    );

    // Визначаємо правила на основі ролі користувача
    if (user.roles.some(role => role.name === 'admin')) {
      // Адміністратор має повний доступ до всього
      can(Action.Manage, Subjects.All);
    } else if (user.roles.some(role => role.name === 'editor')) {
      // Редактор може керувати постами
      can(Action.Manage, Subjects.Post);

      // Редактор може читати користувачів
      can(Action.Read, Subjects.User);

      // Редактор може затверджувати коментарі
      can(Action.Approve, Subjects.Comment);
      can(Action.Delete, Subjects.Comment, { status: 'pending' }); // Лише pending коментарі
    } else if (user.roles.some(role => role.name === 'author')) {
      // Автор може створювати пости
      can(Action.Create, Subjects.Post);

      // Автор може читати всі пости
      can(Action.Read, Subjects.Post);

      // Автор може редагувати та видаляти лише власні пости
      can([Action.Update, Action.Delete], Subjects.Post, { authorId: user.id });

      // Автор може створювати коментарі
      can(Action.Create, Subjects.Comment);

      // Автор може редагувати власні коментарі
      can([Action.Update, Action.Delete], Subjects.Comment, { authorId: user.id });
    } else {
      // Звичайний користувач (базові права)
      can(Action.Read, Subjects.Post, { status: 'published' }); // Лише опубліковані пости
      can(Action.Read, Subjects.Comment);
      can(Action.Create, Subjects.Comment);
      can([Action.Update, Action.Delete], Subjects.Comment, { authorId: user.id });
    }

    // Заборони (мають пріоритет над can)
    // Ніхто не може видаляти власний обліковий запис
    cannot(Action.Delete, Subjects.User, { id: user.id });

    // Повертаємо побудований Ability об'єкт
    return build({
      // Визначаємо, як CASL має розпізнавати тип суб'єкта
      detectSubjectType: (item) =>
        item.constructor as ExtractSubjectType<SubjectTypes>,
    });
  }
}
```

**Деталі реалізації:**

- **`AbilityBuilder`** — допоміжний клас для зручного визначення правил через `can()` та `cannot()`.
- **`detectSubjectType`** — функція, що повідомляє CASL, як визначати тип суб'єкта. Для класів використовуємо `item.constructor`.
- **Умови у правилах:** `{ authorId: user.id }` означає, що правило застосовується лише до об'єктів, де `authorId` дорівнює `user.id`.
- **Масив дій:** `can([Action.Update, Action.Delete], ...)` — скорочений запис для кількох дій з однаковими умовами.

::note
**Стратегія дозволів:** у прикладі використовується підхід **«Deny by Default»** (*заборонено за замовчуванням*) — якщо правило не визначене явно, доступ автоматично відхиляється. Це безпечніший підхід порівняно з **«Allow by Default»**, де відсутність заборони означає дозвіл.
::



---

## Policy Handlers: Декларативні політики доступу

Замість написання правил перевірки безпосередньо у Guard, створимо систему **Policy Handlers** — окремих класів або функцій, що інкапсулюють логіку перевірки конкретних політик.

### Інтерфейс IPolicyHandler

```typescript
// src/casl/policies/policy-handler.interface.ts
import { AppAbility } from '../casl-ability.factory';

/**
 * Інтерфейс для Policy Handler
 * Кожна політика реалізує метод handle для перевірки дозволу
 */
export interface IPolicyHandler {
  handle(ability: AppAbility): boolean;
}

/**
 * Тип для функції-політики
 */
export type PolicyHandlerCallback = (ability: AppAbility) => boolean;

/**
 * Об'єднаний тип для політик
 */
export type PolicyHandler = IPolicyHandler | PolicyHandlerCallback;
```

### Приклади конкретних Policy Handlers

```typescript
// src/casl/policies/read-post.policy.ts
import { IPolicyHandler } from './policy-handler.interface';
import { AppAbility } from '../casl-ability.factory';
import { Action, Subjects } from '../casl-ability.types';

/**
 * Політика: користувач може читати пости
 */
export class ReadPostPolicyHandler implements IPolicyHandler {
  handle(ability: AppAbility): boolean {
    return ability.can(Action.Read, Subjects.Post);
  }
}
```

```typescript
// src/casl/policies/update-own-post.policy.ts
import { IPolicyHandler } from './policy-handler.interface';
import { AppAbility } from '../casl-ability.factory';
import { Action, Subjects } from '../casl-ability.types';
import { Post } from '../../posts/entities/post.entity';

/**
 * Політика: користувач може редагувати власні пости
 * Приймає конкретний об'єкт Post для перевірки
 */
export class UpdateOwnPostPolicyHandler implements IPolicyHandler {
  constructor(private post: Post) {}

  handle(ability: AppAbility): boolean {
    return ability.can(Action.Update, this.post);
  }
}
```

```typescript
// src/casl/policies/delete-pending-comment.policy.ts
import { IPolicyHandler } from './policy-handler.interface';
import { AppAbility } from '../casl-ability.factory';
import { Action, Subjects } from '../casl-ability.types';
import { Comment } from '../../comments/entities/comment.entity';

/**
 * Політика: модератор може видаляти коментарі зі статусом pending
 */
export class DeletePendingCommentPolicyHandler implements IPolicyHandler {
  constructor(private comment: Comment) {}

  handle(ability: AppAbility): boolean {
    // CASL автоматично перевірить умову { status: 'pending' } з AbilityFactory
    return ability.can(Action.Delete, this.comment);
  }
}
```

### Альтернатива: Функціональні політики

Замість класів можна використовувати прості функції:

```typescript
// src/casl/policies/functional-policies.ts
import { AppAbility } from '../casl-ability.factory';
import { Action, Subjects } from '../casl-ability.types';

/**
 * Перевірка: чи може користувач створювати пости
 */
export const canCreatePost = (ability: AppAbility) =>
  ability.can(Action.Create, Subjects.Post);

/**
 * Перевірка: чи може користувач видаляти коментарі
 */
export const canDeleteComments = (ability: AppAbility) =>
  ability.can(Action.Delete, Subjects.Comment);

/**
 * Перевірка: чи може користувач переглядати налаштування
 */
export const canViewSettings = (ability: AppAbility) =>
  ability.can(Action.Read, Subjects.Settings);
```

::tip
**Вибір між класами та функціями:**

- **Класи:** використовуйте для складних політик, що потребують доступу до конкретного об'єкта (наприклад, перевірка власності ресурсу).
- **Функції:** використовуйте для простих політик без прив'язки до конкретних об'єктів (наприклад, перевірка базового дозволу на дію).

Обидва підходи можна комбінувати у одному проєкті.
::

---

## Декоратор @CheckPolicies()

Створимо декоратор для позначення політик, що мають перевірятися на маршруті:

```typescript
// src/casl/decorators/check-policies.decorator.ts
import { SetMetadata } from '@nestjs/common';
import { PolicyHandler } from '../policies/policy-handler.interface';

/**
 * Ключ для збереження метаданих про політики
 */
export const CHECK_POLICIES_KEY = 'check_policies';

/**
 * Декоратор для позначення політик, що мають перевірятися
 * Приймає класи PolicyHandler або функції
 * 
 * @example
 * // Використання з функціями
 * @CheckPolicies(canCreatePost, canPublishPost)
 * createPost() { ... }
 * 
 * @example
 * // Використання з класами (потребує інстанціювання у Guard)
 * @CheckPolicies(ReadPostPolicyHandler)
 * getPost() { ... }
 */
export const CheckPolicies = (...handlers: PolicyHandler[]) =>
  SetMetadata(CHECK_POLICIES_KEY, handlers);
```

---

## Реалізація PoliciesGuard

Створимо Guard, що перевіряє виконання політик перед доступом до маршруту:

```typescript
// src/casl/guards/policies.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  Logger,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { CaslAbilityFactory, AppAbility } from '../casl-ability.factory';
import { CHECK_POLICIES_KEY } from '../decorators/check-policies.decorator';
import {
  PolicyHandler,
  IPolicyHandler,
  PolicyHandlerCallback,
} from '../policies/policy-handler.interface';

@Injectable()
export class PoliciesGuard implements CanActivate {
  private readonly logger = new Logger(PoliciesGuard.name);

  constructor(
    private reflector: Reflector,
    private caslAbilityFactory: CaslAbilityFactory,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    // Крок 1: Читаємо політики з метаданих
    const policyHandlers =
      this.reflector.get<PolicyHandler[]>(
        CHECK_POLICIES_KEY,
        context.getHandler(),
      ) || [];

    // Крок 2: Якщо політики не вказані, пропускаємо перевірку
    if (policyHandlers.length === 0) {
      return true;
    }

    // Крок 3: Витягуємо користувача з request
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user) {
      this.logger.warn('PoliciesGuard: User is not authenticated');
      throw new ForbiddenException('User is not authenticated');
    }

    // Крок 4: Створюємо Ability об'єкт для користувача
    const ability = this.caslAbilityFactory.createForUser(user);

    // Крок 5: Перевіряємо кожну політику
    const allPoliciesPassed = policyHandlers.every((handler) =>
      this.execPolicyHandler(handler, ability),
    );

    if (!allPoliciesPassed) {
      this.logger.warn(
        `PoliciesGuard: Access denied for user ${user.sub}. Failed policy check.`,
      );
      throw new ForbiddenException('Access denied by policy');
    }

    this.logger.debug(`PoliciesGuard: Access granted for user ${user.sub}`);
    return true;
  }

  /**
   * Виконує перевірку політики (клас або функція)
   */
  private execPolicyHandler(handler: PolicyHandler, ability: AppAbility): boolean {
    if (typeof handler === 'function') {
      // Функціональна політика
      return handler(ability);
    }

    // Класова політика (потребує інстанціювання)
    // У базовій реалізації класи мають бути інстанційовані заздалегідь
    return (handler as IPolicyHandler).handle(ability);
  }
}
```

**Деталі реалізації:**

- **Етап 1–3:** стандартна логіка Guard — читання метаданих, перевірка автентифікації.
- **Етап 4:** створення `Ability` об'єкта через `CaslAbilityFactory.createForUser()`. Цей об'єкт містить всі правила доступу для даного користувача.
- **Етап 5:** перевірка кожної політики через метод `every()` — якщо хоча б одна політика не пройшла, доступ відхиляється.
- **`execPolicyHandler()`:** універсальний метод для виконання як функціональних, так і класових політик.

::warning
**Обмеження базової реалізації:** у наведеному Guard класові політики мають бути інстанційовані до передачі у декоратор. Для політик, що потребують доступу до конкретного об'єкта Entity (наприклад, `UpdateOwnPostPolicyHandler`), потрібна додаткова логіка завантаження об'єкта всередині Guard або сервісу. Розглянемо це у наступному розділі.
::

---

## Застосування PoliciesGuard до маршрутів

### Приклад: Контролер постів з політиками

```typescript
// src/posts/posts.controller.ts
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  UseGuards,
  Request,
} from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { PoliciesGuard } from '../casl/guards/policies.guard';
import { CheckPolicies } from '../casl/decorators/check-policies.decorator';
import { Public } from '../auth/decorators/public.decorator';
import { PostsService } from './posts.service';
import { CreatePostDto, UpdatePostDto } from './dto';

// Імпортуємо функціональні політики
import { canCreatePost } from '../casl/policies/functional-policies';

@Controller('posts')
@UseGuards(JwtAuthGuard, PoliciesGuard) // Порядок: автентифікація → перевірка політик
export class PostsController {
  constructor(private postsService: PostsService) {}

  /**
   * Отримання списку постів
   * Доступ: публічний
   */
  @Get()
  @Public()
  async getAllPosts() {
    return this.postsService.findAll();
  }

  /**
   * Отримання окремого поста
   * Доступ: потрібен дозвіл на читання постів
   */
  @Get(':id')
  @CheckPolicies((ability) => ability.can('read', 'Post'))
  async getPost(@Param('id') id: string) {
    return this.postsService.findById(id);
  }

  /**
   * Створення нового поста
   * Доступ: потрібен дозвіл на створення постів
   */
  @Post()
  @CheckPolicies(canCreatePost) // Використання функціональної політики
  async createPost(@Request() req, @Body() createDto: CreatePostDto) {
    return this.postsService.create({
      ...createDto,
      authorId: req.user.sub,
    });
  }

  /**
   * Оновлення поста
   * Доступ: перевіряється у сервісі через ability.can(update, post)
   */
  @Put(':id')
  async updatePost(
    @Param('id') id: string,
    @Body() updateDto: UpdatePostDto,
    @Request() req,
  ) {
    return this.postsService.update(id, updateDto, req.user);
  }

  /**
   * Видалення поста
   * Доступ: перевіряється у сервісі
   */
  @Delete(':id')
  async deletePost(@Param('id') id: string, @Request() req) {
    return this.postsService.delete(id, req.user);
  }

  /**
   * Публікація поста
   * Доступ: потрібен дозвіл на публікацію
   */
  @Put(':id/publish')
  @CheckPolicies((ability) => ability.can('publish', 'Post'))
  async publishPost(@Param('id') id: string) {
    return this.postsService.publish(id);
  }
}
```

**Аналіз використання політик:**

- **Inline-політики:** `@CheckPolicies((ability) => ability.can('read', 'Post'))` — прості перевірки можна писати безпосередньо у декораторі як стрілкові функції.
- **Функціональні політики:** `@CheckPolicies(canCreatePost)` — для політик, що повторюються у кількох місцях, виносимо логіку у окремі функції.
- **Перевірка у сервісі:** для операцій, що потребують доступу до конкретного об'єкта (оновлення, видалення), перевірку політики виконуємо у сервісі після завантаження Entity.

---

## Перевірка дозволів у сервісному шарі

Для операцій над конкретними об'єктами (оновлення, видалення) необхідно спочатку завантажити об'єкт з бази даних, а потім перевірити політику доступу з урахуванням його атрибутів.

### Сервіс постів з перевіркою через CASL

```typescript
// src/posts/posts.service.ts
import {
  Injectable,
  NotFoundException,
  ForbiddenException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Post } from './entities/post.entity';
import { CreatePostDto, UpdatePostDto } from './dto';
import { CaslAbilityFactory } from '../casl/casl-ability.factory';
import { Action } from '../casl/casl-ability.types';
import { User } from '../users/entities/user.entity';
import { ForbiddenError, subject } from '@casl/ability';

@Injectable()
export class PostsService {
  constructor(
    @InjectRepository(Post)
    private postsRepository: Repository<Post>,
    private caslAbilityFactory: CaslAbilityFactory,
  ) {}

  async findAll(): Promise<Post[]> {
    return this.postsRepository.find({
      where: { status: 'published' },
      order: { publishedAt: 'DESC' },
    });
  }

  async findById(id: string): Promise<Post> {
    const post = await this.postsRepository.findOne({
      where: { id },
      relations: ['author'],
    });

    if (!post) {
      throw new NotFoundException(`Post with ID ${id} not found`);
    }

    return post;
  }

  async create(data: Partial<Post>): Promise<Post> {
    const post = this.postsRepository.create(data);
    return this.postsRepository.save(post);
  }

  /**
   * Оновлення поста з перевіркою дозволів через CASL
   */
  async update(
    id: string,
    updateDto: UpdatePostDto,
    currentUser: User,
  ): Promise<Post> {
    // Крок 1: Завантажуємо пост
    const post = await this.findById(id);

    // Крок 2: Створюємо Ability для поточного користувача
    const ability = this.caslAbilityFactory.createForUser(currentUser);

    // Крок 3: Перевіряємо, чи може користувач редагувати цей конкретний пост
    // subject() — допоміжна функція CASL для явного вказівки типу суб'єкта
    if (ability.cannot(Action.Update, subject('Post', post))) {
      throw new ForbiddenException(
        'You do not have permission to update this post',
      );
    }

    // Крок 4: Виконуємо оновлення
    Object.assign(post, updateDto);
    return this.postsRepository.save(post);
  }

  /**
   * Видалення поста з перевіркою дозволів
   */
  async delete(id: string, currentUser: User): Promise<void> {
    const post = await this.findById(id);

    const ability = this.caslAbilityFactory.createForUser(currentUser);

    if (ability.cannot(Action.Delete, subject('Post', post))) {
      throw new ForbiddenException(
        'You do not have permission to delete this post',
      );
    }

    await this.postsRepository.delete(id);
  }

  /**
   * Публікація поста
   */
  async publish(id: string): Promise<Post> {
    const post = await this.findById(id);
    post.status = 'published';
    post.publishedAt = new Date();
    return this.postsRepository.save(post);
  }
}
```

**Ключові моменти:**

- **`subject('Post', post)`** — функція CASL, що явно позначає об'єкт як екземпляр типу `Post`. Це необхідно, оскільки TypeORM Entity може втрачати інформацію про клас після десеріалізації з бази даних.

- **`ability.cannot()`** — зворотна перевірка до `ability.can()`. Використовується для більш читабельного коду у випадках, коли відсутність дозволу призводить до виключення.

- **Двошарова перевірка:** базовий дозвіл перевіряється у `PoliciesGuard`, а перевірка на основі атрибутів конкретного об'єкта — у сервісі.

::tip
**Альтернатива: ForbiddenError з CASL**

Замість власних виключень можна використовувати вбудований клас `ForbiddenError` з CASL:

```typescript
import { ForbiddenError } from '@casl/ability';

// Замість if + throw
ForbiddenError.from(ability).throwUnlessCan(Action.Update, subject('Post', post));
```

Це автоматично викине виключення з детальним повідомленням про причину відмови.
::


---

## Field-Level Permissions: Гранулярний контроль полів

CASL підтримує контроль доступу не лише на рівні цілих об'єктів, але й на рівні **окремих полів** Entity. Це дозволяє приховувати чутливі дані від користувачів без достатніх прав.

### Визначення правил для полів

```typescript
// src/casl/casl-ability.factory.ts (розширена версія)
createForUser(user: User): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(
    Ability as AbilityClass<AppAbility>,
  );

  if (user.roles.some(role => role.name === 'admin')) {
    can(Action.Manage, Subjects.All);
  } else if (user.roles.some(role => role.name === 'user')) {
    // Користувач може читати пости
    can(Action.Read, Subjects.Post);

    // Але не може бачити поле `analytics` (внутрішня статистика)
    cannot(Action.Read, Subjects.Post, ['analytics']);

    // Користувач може читати профілі інших користувачів
    can(Action.Read, Subjects.User);

    // Але не може бачити поля `email` та `password` чужих профілів
    cannot(Action.Read, Subjects.User, ['email', 'password'], { id: { $ne: user.id } });

    // Користувач може редагувати власний профіль
    can(Action.Update, Subjects.User, { id: user.id });

    // Але не може змінювати поле `role` (лише адміністратор)
    cannot(Action.Update, Subjects.User, ['role']);
  }

  return build({
    detectSubjectType: (item) =>
      item.constructor as ExtractSubjectType<SubjectTypes>,
  });
}
```

### Фільтрація полів при серіалізації

Для автоматичного приховування заборонених полів створимо **Interceptor**, що фільтрує відповідь перед відправкою клієнту:

```typescript
// src/casl/interceptors/casl-serialization.interceptor.ts
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { CaslAbilityFactory } from '../casl-ability.factory';
import { Action } from '../casl-ability.types';
import { subject, Ability } from '@casl/ability';

@Injectable()
export class CaslSerializationInterceptor implements NestInterceptor {
  constructor(private caslAbilityFactory: CaslAbilityFactory) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user) {
      return next.handle(); // Пропускаємо для неавтентифікованих запитів
    }

    const ability = this.caslAbilityFactory.createForUser(user);

    return next.handle().pipe(
      map((data) => this.filterForbiddenFields(data, ability)),
    );
  }

  /**
   * Рекурсивно фільтрує заборонені поля з об'єкта або масиву
   */
  private filterForbiddenFields(data: any, ability: Ability): any {
    if (Array.isArray(data)) {
      return data.map((item) => this.filterForbiddenFields(item, ability));
    }

    if (data && typeof data === 'object' && data.constructor.name !== 'Object') {
      // Це Entity (має constructor, відмінний від чистого Object)
      const subjectType = data.constructor.name;
      const fields = Object.keys(data);

      fields.forEach((field) => {
        // Перевіряємо, чи може користувач читати це поле
        if (ability.cannot(Action.Read, subject(subjectType, data), field)) {
          delete data[field];
        }
      });
    }

    return data;
  }
}
```

**Застосування Interceptor:**

```typescript
// src/users/users.controller.ts
import { Controller, Get, Param, UseInterceptors } from '@nestjs/common';
import { CaslSerializationInterceptor } from '../casl/interceptors/casl-serialization.interceptor';

@Controller('users')
@UseInterceptors(CaslSerializationInterceptor) // Застосовуємо фільтрацію полів
export class UsersController {
  constructor(private usersService: UsersService) {}

  @Get(':id')
  async getUser(@Param('id') id: string) {
    const user = await this.usersService.findById(id);

    // Interceptor автоматично видалить заборонені поля перед відправкою відповіді
    return user;
  }
}
```

**Результат для звичайного користувача:**

```json
// Запит GET /users/другий-користувач
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "firstName": "Іван",
  "lastName": "Петренко",
  // email та password приховані через cannot(Read, User, ['email', 'password'])
  "createdAt": "2026-01-15T10:30:00.000Z"
}
```

::caution
**Обережність з Interceptor:** фільтрація полів через Interceptor є зручною, але не замінює належних практик безпеки:

- **Ніколи не включайте `password` у Entity без явного виключення** — використовуйте декоратор `@Exclude()` з `class-transformer`.
- **Перевіряйте дозволи до завантаження даних** — якщо користувач взагалі не має права переглядати профіль, краще повернути `403 Forbidden` до запиту до бази даних.
- **Уникайте витоку через related entities** — якщо Entity містить зв'язок `posts: Post[]`, потрібна рекурсивна фільтрація.
::

---

## Складні сценарії ABAC

Розглянемо реалізацію декількох складних сценаріїв, що неможливо вирішити через простий RBAC.

### Сценарій 1: Multi-Tenancy (Ізоляція даних за організаціями)

У B2B SaaS-застосунках кожна організація (*tenant*) має власні дані, ізольовані від інших. Користувач може працювати лише з даними своєї організації.

**Entity з tenantId:**

```typescript
// src/posts/entities/post.entity.ts
@Entity('posts')
export class Post {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  title: string;

  @Column()
  authorId: string;

  @Column()
  tenantId: string; // UUID організації

  @Column()
  status: string;

  // ... інші поля
}
```

**Правила у AbilityFactory:**

```typescript
// src/casl/casl-ability.factory.ts
createForUser(user: User): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(
    Ability as AbilityClass<AppAbility>,
  );

  // Користувач може управляти постами лише своєї організації
  can(Action.Manage, Subjects.Post, { tenantId: user.tenantId });

  // Явна заборона доступу до постів інших організацій
  cannot(Action.Manage, Subjects.Post, { tenantId: { $ne: user.tenantId } });

  return build({
    detectSubjectType: (item) =>
      item.constructor as ExtractSubjectType<SubjectTypes>,
  });
}
```

**Перевірка у сервісі:**

```typescript
// src/posts/posts.service.ts
async findAll(currentUser: User): Promise<Post[]> {
  // Завантажуємо лише пости організації користувача
  const posts = await this.postsRepository.find({
    where: { tenantId: currentUser.tenantId },
  });

  const ability = this.caslAbilityFactory.createForUser(currentUser);

  // Додаткова перевірка (для безпеки)
  posts.forEach(post => {
    ForbiddenError.from(ability).throwUnlessCan(Action.Read, subject('Post', post));
  });

  return posts;
}
```

### Сценарій 2: Організаційна ієрархія (Менеджер → Підлеглі)

Менеджер може переглядати звіти всіх підлеглих у своєму департаменті, але не інших департаментів.

**Entity зі зв'язками:**

```typescript
// src/users/entities/user.entity.ts
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  departmentId: string;

  @Column({ nullable: true })
  managerId: string; // UUID менеджера цього користувача

  @ManyToOne(() => User)
  @JoinColumn({ name: 'managerId' })
  manager: User;

  // ... інші поля
}
```

```typescript
// src/reports/entities/report.entity.ts
@Entity('reports')
export class Report {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  authorId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'authorId' })
  author: User;

  @Column()
  content: string;

  // ... інші поля
}
```

**Сервіс для завантаження підлеглих:**

```typescript
// src/users/users.service.ts
/**
 * Отримує список усіх підлеглих користувача (включаючи підлеглих підлеглих)
 */
async getSubordinateIds(userId: string): Promise<string[]> {
  const subordinates = await this.userRepository.find({
    where: { managerId: userId },
    select: ['id'],
  });

  const directIds = subordinates.map(u => u.id);

  // Рекурсивно завантажуємо підлеглих підлеглих
  const nestedIds = await Promise.all(
    directIds.map(id => this.getSubordinateIds(id)),
  );

  return [userId, ...directIds, ...nestedIds.flat()];
}
```

**Правила у AbilityFactory:**

```typescript
// src/casl/casl-ability.factory.ts
async createForUser(user: User, usersService: UsersService): Promise<AppAbility> {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(
    Ability as AbilityClass<AppAbility>,
  );

  if (user.roles.some(role => role.name === 'manager')) {
    // Отримуємо список підлеглих
    const subordinateIds = await usersService.getSubordinateIds(user.id);

    // Менеджер може читати звіти підлеглих
    can(Action.Read, Subjects.Report, { authorId: { $in: subordinateIds } });
  }

  // Користувач завжди може читати власні звіти
  can(Action.Read, Subjects.Report, { authorId: user.id });

  return build({
    detectSubjectType: (item) =>
      item.constructor as ExtractSubjectType<SubjectTypes>,
  });
}
```

::note
**Асинхронність AbilityFactory:** у цьому сценарії `createForUser()` стає асинхронним методом, оскільки завантаження підлеглих вимагає запиту до бази даних. Це вимагає оновлення `PoliciesGuard` для очікування Promise:

```typescript
// У PoliciesGuard
const ability = await this.caslAbilityFactory.createForUser(user, this.usersService);
```
::

### Сценарій 3: Часові обмеження (Time-Based Access)

Автор може редагувати пост лише протягом 24 годин після створення. Після цього потрібна роль `editor`.

**Правила у AbilityFactory:**

```typescript
// src/casl/casl-ability.factory.ts
createForUser(user: User): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(
    Ability as AbilityClass<AppAbility>,
  );

  const now = new Date();
  const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

  if (user.roles.some(role => role.name === 'author')) {
    // Автор може редагувати власні пости, створені менше 24 годин тому
    can(Action.Update, Subjects.Post, {
      authorId: user.id,
      createdAt: { $gt: twentyFourHoursAgo.toISOString() },
    });
  }

  if (user.roles.some(role => role.name === 'editor')) {
    // Редактор може редагувати будь-які пости без часових обмежень
    can(Action.Update, Subjects.Post);
  }

  return build({
    detectSubjectType: (item) =>
      item.constructor as ExtractSubjectType<SubjectTypes>,
  });
}
```

**Перевірка у сервісі:**

```typescript
// src/posts/posts.service.ts
async update(id: string, updateDto: UpdatePostDto, currentUser: User): Promise<Post> {
  const post = await this.findById(id);

  const ability = this.caslAbilityFactory.createForUser(currentUser);

  // CASL автоматично перевірить умову createdAt > 24 години тому
  if (ability.cannot(Action.Update, subject('Post', post))) {
    throw new ForbiddenException(
      'You can only edit your posts within 24 hours of creation. Contact an editor for changes.',
    );
  }

  Object.assign(post, updateDto);
  return this.postsRepository.save(post);
}
```

---

## Тестування CASL Abilities

Написання тестів для політик доступу є критично важливим для гарантії безпеки.

### Unit тестування AbilityFactory

```typescript
// src/casl/casl-ability.factory.spec.ts
import { Test } from '@nestjs/testing';
import { CaslAbilityFactory } from './casl-ability.factory';
import { User } from '../users/entities/user.entity';
import { Post } from '../posts/entities/post.entity';
import { Action, Subjects } from './casl-ability.types';
import { subject } from '@casl/ability';

describe('CaslAbilityFactory', () => {
  let factory: CaslAbilityFactory;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [CaslAbilityFactory],
    }).compile();

    factory = module.get<CaslAbilityFactory>(CaslAbilityFactory);
  });

  describe('Admin role', () => {
    it('should allow admin to manage all subjects', () => {
      const admin: User = {
        id: 'admin-1',
        roles: [{ name: 'admin' }],
      } as User;

      const ability = factory.createForUser(admin);

      expect(ability.can(Action.Manage, Subjects.All)).toBe(true);
      expect(ability.can(Action.Delete, Subjects.Post)).toBe(true);
      expect(ability.can(Action.Update, Subjects.User)).toBe(true);
    });
  });

  describe('Author role', () => {
    it('should allow author to update own posts', () => {
      const authorId = 'author-1';
      const author: User = {
        id: authorId,
        roles: [{ name: 'author' }],
      } as User;

      const ability = factory.createForUser(author);

      const ownPost = { id: 'post-1', authorId, title: 'Test' } as Post;
      expect(ability.can(Action.Update, subject('Post', ownPost))).toBe(true);
    });

    it('should deny author from updating other users posts', () => {
      const authorId = 'author-1';
      const author: User = {
        id: authorId,
        roles: [{ name: 'author' }],
      } as User;

      const ability = factory.createForUser(author);

      const otherPost = { id: 'post-2', authorId: 'other-author', title: 'Test' } as Post;
      expect(ability.can(Action.Update, subject('Post', otherPost))).toBe(false);
    });

    it('should deny author from publishing posts', () => {
      const author: User = {
        id: 'author-1',
        roles: [{ name: 'author' }],
      } as User;

      const ability = factory.createForUser(author);

      expect(ability.can(Action.Publish, Subjects.Post)).toBe(false);
    });
  });

  describe('Editor role', () => {
    it('should allow editor to manage all posts', () => {
      const editor: User = {
        id: 'editor-1',
        roles: [{ name: 'editor' }],
      } as User;

      const ability = factory.createForUser(editor);

      const anyPost = { id: 'post-1', authorId: 'someone-else', title: 'Test' } as Post;
      expect(ability.can(Action.Update, subject('Post', anyPost))).toBe(true);
      expect(ability.can(Action.Delete, subject('Post', anyPost))).toBe(true);
      expect(ability.can(Action.Publish, Subjects.Post)).toBe(true);
    });

    it('should deny editor from managing users', () => {
      const editor: User = {
        id: 'editor-1',
        roles: [{ name: 'editor' }],
      } as User;

      const ability = factory.createForUser(editor);

      expect(ability.can(Action.Delete, Subjects.User)).toBe(false);
    });
  });
});
```

**Покриття тестами:** обов'язково тестуйте:

- Кожну роль окремо
- Позитивні випадки (дозвіл надається)
- Негативні випадки (дозвіл відхиляється)
- Граничні умови (наприклад, роль `author` не може публікувати, але `editor` може)


---

## Оптимізація: Кешування Ability Objects

Створення `Ability` об'єкта при кожному запиті може бути ресурсомістким, особливо якщо `createForUser()` виконує додаткові запити до бази даних (наприклад, завантаження підлеглих). Впровадимо кешування.

### CaslAbilityFactory з кешуванням

```typescript
// src/casl/casl-ability.factory.ts (оптимізована версія)
import { Injectable } from '@nestjs/common';
import {
  Ability,
  AbilityBuilder,
  AbilityClass,
  ExtractSubjectType,
} from '@casl/ability';
import { User } from '../users/entities/user.entity';

@Injectable()
export class CaslAbilityFactory {
  private abilityCache = new Map<string, AppAbility>();
  private readonly CACHE_TTL = 5 * 60 * 1000; // 5 хвилин

  createForUser(user: User): AppAbility {
    // Генеруємо ключ кешу на основі userId та ролей
    const cacheKey = this.generateCacheKey(user);

    // Перевірка кешу
    const cached = this.abilityCache.get(cacheKey);
    if (cached) {
      return cached;
    }

    // Створення нового Ability
    const ability = this.buildAbility(user);

    // Збереження у кеш
    this.abilityCache.set(cacheKey, ability);

    // Автоматичне видалення з кешу через TTL
    setTimeout(() => {
      this.abilityCache.delete(cacheKey);
    }, this.CACHE_TTL);

    return ability;
  }

  /**
   * Генерує унікальний ключ для кешування
   */
  private generateCacheKey(user: User): string {
    const roleNames = user.roles.map(r => r.name).sort().join(',');
    return `${user.id}:${roleNames}`;
  }

  /**
   * Будує Ability об'єкт (винесено у окремий метод для тестування)
   */
  private buildAbility(user: User): AppAbility {
    const { can, cannot, build } = new AbilityBuilder<AppAbility>(
      Ability as AbilityClass<AppAbility>,
    );

    // Логіка визначення правил (як у попередніх прикладах)
    if (user.roles.some(role => role.name === 'admin')) {
      can(Action.Manage, Subjects.All);
    } else if (user.roles.some(role => role.name === 'editor')) {
      can(Action.Manage, Subjects.Post);
      can(Action.Read, Subjects.User);
      can(Action.Approve, Subjects.Comment);
    } else if (user.roles.some(role => role.name === 'author')) {
      can(Action.Create, Subjects.Post);
      can(Action.Read, Subjects.Post);
      can([Action.Update, Action.Delete], Subjects.Post, { authorId: user.id });
      can(Action.Create, Subjects.Comment);
      can([Action.Update, Action.Delete], Subjects.Comment, { authorId: user.id });
    } else {
      can(Action.Read, Subjects.Post, { status: 'published' });
      can(Action.Read, Subjects.Comment);
      can(Action.Create, Subjects.Comment);
      can([Action.Update, Action.Delete], Subjects.Comment, { authorId: user.id });
    }

    cannot(Action.Delete, Subjects.User, { id: user.id });

    return build({
      detectSubjectType: (item) =>
        item.constructor as ExtractSubjectType<SubjectTypes>,
    });
  }

  /**
   * Примусово скидає кеш Ability для користувача
   */
  invalidateUserAbilityCache(userId: string): void {
    // Видаляємо всі ключі, що починаються з userId
    for (const key of this.abilityCache.keys()) {
      if (key.startsWith(userId)) {
        this.abilityCache.delete(key);
      }
    }
  }

  /**
   * Повністю очищає кеш Ability
   */
  clearAbilityCache(): void {
    this.abilityCache.clear();
  }
}
```

**Коли інвалідувати кеш:**

- Після зміни ролей користувача через адміністративний інтерфейс.
- Після зміни дозволів ролі (якщо ви зберігаєте дозволи у БД).
- Після будь-яких змін, що впливають на правила доступу.

---

## Порівняння підходів до авторизації

| Характеристика | RBAC | Permission-Based | ABAC (CASL) |
|----------------|------|------------------|-------------|
| **Гранулярність** | Низька (на рівні ролей) | Середня (на рівні дій) | Висока (на рівні атрибутів) |
| **Умовні правила** | Немає | Немає | Повна підтримка |
| **Складність реалізації** | Низька | Середня | Висока |
| **Продуктивність** | Відмінна | Хороша | Хороша (з кешуванням) |
| **Гнучкість** | Обмежена | Висока | Дуже висока |
| **Підтримуваність** | Проста | Середня | Складна (потребує документації правил) |
| **Власність ресурсу** | Потребує додаткового коду | Потребує додаткового коду | Вбудована підтримка |
| **Тестованість** | Висока | Висока | Висока (unit тести політик) |
| **Аудит** | Простий | Середній | Складний (детальне логування) |

**Рекомендації вибору:**

- **RBAC:** використовуйте для простих систем з кількома ролями та статичними правами (<10 ролей, немає потреби у перевірці власності).

- **Permission-Based:** використовуйте для середніх систем з багатьма ролями та потребою у гранулярному контролі дій (10–50 дозволів, мінімальна перевірка власності).

- **ABAC (CASL):** використовуйте для складних систем з динамічними правилами, перевіркою власності ресурсів, організаційною ієрархією, multi-tenancy (>50 дозволів, складні умови доступу).

**Гібридний підхід:** у більшості реальних проєктів оптимальним є **комбінування підходів**:

- Базові правила через Permission-Based (швидка перевірка на рівні контролера)
- Складні умовні правила через CASL (перевірка у сервісі з урахуванням атрибутів об'єкта)
- Аудит через централізований Interceptor

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ У чому різниця між RBAC та ABAC?" icon="i-lucide-help-circle"}

**RBAC (Role-Based Access Control)** приймає рішення про доступ виключно на основі **ролі** користувача. Правило виду «Користувач має роль `editor` → дозволити редагування постів» не враховує **атрибути конкретного об'єкта**. Усі пости доступні або недоступні для ролі.

**ABAC (Attribute-Based Access Control)** приймає рішення на основі **атрибутів**:
- **Атрибути суб'єкта:** роль, департамент, рівень допуску користувача.
- **Атрибути об'єкта:** власник поста, статус публікації, дата створення.
- **Атрибути контексту:** час доби, IP-адреса, стан сесії.

Правило ABAC: «Користувач може редагувати пост, **якщо** він є його автором **або** має роль `editor` **та** пост створений менше 7 днів тому». Це дозволяє виражати складні умовні політики, що неможливо у чистому RBAC.

::

::accordion-item{label="❓ Чому CASL використовує subject() функцію при перевірці об'єктів?" icon="i-lucide-help-circle"}

Функція `subject('Post', post)` явно вказує CASL, що об'єкт `post` є екземпляром типу `Post`. Це необхідно з двох причин:

1. **Втрата типу після десеріалізації:** коли TypeORM завантажує Entity з бази даних та серіалізує через JSON, об'єкт може втратити інформацію про свій клас-конструктор. CASL потребує цю інформацію для співставлення з правилами.

2. **Явна типізація для TypeScript:** функція `subject()` забезпечує типобезпеку — TypeScript підказує доступні типи суб'єктів та їхні поля.

Без `subject()`:
```typescript
ability.can('update', post); // CASL може не розпізнати тип post
```

З `subject()`:
```typescript
ability.can('update', subject('Post', post)); // CASL точно знає, що це Post
```

::

::accordion-item{label="❓ Як впровадити ABAC для існуючого проєкту з RBAC?" icon="i-lucide-help-circle"}

Міграція з RBAC до ABAC має відбуватися поступово, щоб не зламати існуючу функціональність:

**Крок 1: Встановлення CASL**
```bash
npm install @casl/ability
```

**Крок 2: Створення AbilityFactory**
Спочатку дублюйте існуючу RBAC логіку у CASL:
```typescript
if (user.roles.some(role => role.name === 'editor')) {
  can('manage', 'Post'); // Той самий дозвіл, що був у RBAC
}
```

**Крок 3: Поступова заміна Guards**
Залиште існуючі `RolesGuard` на місці, але для **нових** маршрутів використовуйте `PoliciesGuard`.

**Крок 4: Додавання умовних правил**
Поступово розширюйте правила у `AbilityFactory` умовами:
```typescript
can('update', 'Post', { authorId: user.id }); // Тепер з перевіркою власності
```

**Крок 5: Заміна перевірок у сервісах**
Замість:
```typescript
if (post.authorId !== userId && !user.roles.includes('admin')) {
  throw new ForbiddenException();
}
```

Використовуйте:
```typescript
if (ability.cannot('update', subject('Post', post))) {
  throw new ForbiddenException();
}
```

**Крок 6: Поступове видалення RolesGuard**
Після того, як усі маршрути покриті `PoliciesGuard` та тести проходять, видаліть старі Guards.

::

::accordion-item{label="❓ Чи може CASL працювати з даними з бази даних напряму?" icon="i-lucide-help-circle"}

Частково. CASL має експериментальну підтримку для **побудови SQL-запитів** на основі правил:

**Базовий CASL:** перевіряє дозволи після завантаження об'єкта з БД:
```typescript
const posts = await this.postsRepository.find(); // Завантажує ВСІ пости
const allowedPosts = posts.filter(post => ability.can('read', subject('Post', post)));
```

**Проблема:** неефективно для великих таблиць — завантажуємо всі дані для фільтрації у памяті.

**CASL з інтеграціями (Mongoose, Prisma):** може генерувати запити безпосередньо:
```typescript
// Для Mongoose (MongoDB)
const allowedPosts = await Post.find(ability.conditionForSubject('read', 'Post'));
```

**Для TypeORM** офіційної інтеграції немає, але можна вручну перетворити умови CASL у TypeORM `where`:
```typescript
const conditions = ability.rulesFor('read', 'Post');
// Перетворити conditions у TypeORM QueryBuilder
```

Це складна задача і потребує глибокого розуміння обох бібліотек. У більшості випадків достатньо завантажувати дані з базовою фільтрацією (наприклад, за `tenantId`), а CASL використовувати для фінальної перевірки.

::

::

---

## Підсумок

::card-group

::card{title="🎯 ABAC через CASL" icon="i-lucide-shield-check"}

**Ключові переваги:**
- Умовні правила на основі атрибутів об'єктів
- Вбудована перевірка власності ресурсів
- Гранулярний контроль до рівня окремих полів
- Декларативне визначення політик
- Типобезпека через TypeScript

**Архітектура:** AbilityFactory → Ability Object → Policy Handlers → PoliciesGuard

::

::card{title="✅ Коли використовувати CASL" icon="i-lucide-check-circle"}

**Ідеальні сценарії:**
- Multi-tenancy (ізоляція даних організацій)
- Організаційна ієрархія (менеджер → підлеглі)
- Власність ресурсів (редагування власних постів)
- Статус-залежний доступ (лише `pending` коментарі)
- Часові обмеження (редагування протягом 24 годин)
- Field-level permissions (приховування чутливих полів)

::

::card{title="⚠️ Виклики та рішення" icon="i-lucide-alert-triangle"}

**Складність:**
- Потребує ретельного проєктування правил
- Складніша у налагодженні порівняно з RBAC
- Необхідність детальної документації політик

**Продуктивність:**
- Кешування Ability об'єктів (in-memory або Redis)
- Уникайте завантаження всіх даних для фільтрації у пам'яті
- Базова фільтрація на рівні БД + CASL для фінальної перевірки

::

::card{title="🔄 Інтеграція з екосистемою" icon="i-lucide-git-merge"}

**Гібридний підхід:**
- Permission-Based для базових перевірок (швидко)
- CASL для складних умовних правил (гнучко)
- Interceptor для фільтрації полів (безпечно)
- Unit тести для кожної політики (надійно)

**Результат:** максимальна гнучкість з прийнятною складністю

::

::

---

У цій лекції ми реалізували повноцінну систему атрибутивного контролю доступу через бібліотеку CASL. Цей підхід є найскладнішим серед розглянутих моделей авторизації, але й найгнучкішим — він дозволяє виражати складні багатофакторні правила доступу декларативним способом.

CASL особливо корисна для:
- **B2B SaaS-застосунків** з multi-tenancy та організаційною ієрархією.
- **Платформ з користувацьким контентом**, де автори управляють власними публікаціями.
- **Корпоративних систем** з складними політиками доступу на основі ролей, департаментів та рівнів підпорядкування.

Наступні лекції розгляну практичні аспекти безпеки веб-застосунків: налаштування CORS, Helmet для security headers, rate limiting, захист від поширених атак (XSS, CSRF, SQL Injection) та розгортання у production з HTTPS.
