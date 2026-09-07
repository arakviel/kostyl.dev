# Кастомні декоратори та метадані

## Короткий зміст

У цій лекції вивчається створення власних декораторів для покращення DX та читабельності коду:

- **Декоратор @CurrentUser()** — витягування автентифікованого користувача з `request.user`, створення parameter decorator через `createParamDecorator()`, використання `ExecutionContext` для доступу до request
- **Декоратор @Public()** — позначення публічних маршрутів, які не потребують автентифікації, використання `SetMetadata('isPublic', true)` для додавання метаданих
- **SetMetadata()** — функція для додавання довільних метаданих до маршрутів, класів, методів, створення власних ключів метаданих
- **Reflector** — сервіс для читання метаданих у Guards та Interceptors, методи `get()`, `getAllAndOverride()`, `getAllAndMerge()` для різних стратегій читання
- **Композиція декораторів** — створення складних декораторів через `applyDecorators()`, комбінація кількох декораторів в один (наприклад, `@Auth()` = `@UseGuards()` + `@ApiBearerAuth()`)
- **Best practices** — іменування декораторів, типізація для TypeScript, документація через JSDoc коментарі

Розглядаються практичні приклади: декоратор `@Roles()` + `@Permissions()` в одному, декоратор `@RequestTimeout()` для налаштування таймауту запитів, декоратор `@RateLimit()` для індивідуального throttling.

---

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати створення кастомних декораторів для покращення читабельності та зручності роботи з кодом.
- Навчитися використовувати метадані для передачі конфігурації між декораторами та Guards/Interceptors.
- Створити бібліотеку reusable декораторів для типових сценаріїв авторизації.
- Зрозуміти внутрішню роботу Reflector API для читання метаданих.
- Опанувати композицію декораторів через `applyDecorators()` для створення складних абстракцій.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Decorator (Декоратор):** функція, що модифікує або додає метадані до класу, методу, властивості або параметра.
- **Metadata (Метадані):** додаткова інформація, прикріплена до елемента коду та доступна під час виконання.
- **Reflector:** сервіс NestJS для читання метаданих з класів та методів.
- **ExecutionContext:** об'єкт, що надає доступ до деталей поточного запиту (HTTP, WebSocket, RPC).
- **Parameter Decorator:** декоратор для параметрів методів контролера (наприклад, `@Body()`, `@Param()`).

::

::

---

## Анатомія декораторів у TypeScript

Декоратори у TypeScript — це спеціальні функції, що дозволяють модифікувати класи, методи, властивості та параметри під час оголошення. Вони є експериментальною функцією (Stage 2 у TC39), але активно використовуються у фреймворках на кшталт NestJS та Angular.

### Типи декораторів

TypeScript підтримує п'ять типів декораторів:

```typescript
// 1. Class Decorator — застосовується до класу
@Controller('users')
export class UsersController {}

// 2. Method Decorator — застосовується до методу
@Get(':id')
getUser() {}

// 3. Property Decorator — застосовується до властивості класу
@ApiProperty()
username: string;

// 4. Parameter Decorator — застосовується до параметра методу
getUser(@Param('id') id: string) {}

// 5. Accessor Decorator — застосовується до getter/setter (рідко використовується)
@Readonly()
get fullName() { return `${this.firstName} ${this.lastName}`; }
```

У контексті NestJS найчастіше використовуються **Method Decorators** (для маршрутів) та **Parameter Decorators** (для витягування даних з запиту).

### Увімкнення декораторів у TypeScript

Декоратори потребують увімкнення у `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2021",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

- **`experimentalDecorators: true`** — дозволяє використання декораторів.
- **`emitDecoratorMetadata: true`** — додає метадані про типи параметрів (потрібно для Dependency Injection).

---

## Метадані у NestJS: SetMetadata та Reflector

Метадані — це механізм збереження додаткової інформації про класи, методи та параметри під час компіляції, що дозволяє читати цю інформацію під час виконання програми.

### SetMetadata: Додавання метаданих

NestJS надає функцію `SetMetadata()` для прикріплення довільних даних до декораторів:

```typescript
import { SetMetadata } from '@nestjs/common';

// Створення декоратора з метаданими
export const Roles = (...roles: string[]) => SetMetadata('roles', roles);

// Використання
@Get('admin')
@Roles('admin', 'moderator')
getAdminPanel() {}
```

**Що відбувається під капотом:**

1. `SetMetadata('roles', ['admin', 'moderator'])` прикріплює масив ролей до методу `getAdminPanel`.
2. Метадані зберігаються під ключем `'roles'`.
3. Пізніше Guard може прочитати ці метадані через `Reflector`.

### Reflector: Читання метаданих

`Reflector` — це сервіс NestJS, що надає API для читання метаданих з класів та методів:

```typescript
import { Injectable, CanActivate, ExecutionContext } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    // Читання метаданих з ключем 'roles'
    const roles = this.reflector.get<string[]>('roles', context.getHandler());
    
    if (!roles) {
      return true; // Якщо ролі не вказані, дозволяємо доступ
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    return roles.includes(user.role);
  }
}
```

**Методи Reflector:**

| Метод | Опис | Приклад використання |
|-------|------|----------------------|
| `get(key, target)` | Читає метадані з одного джерела (метод або клас) | `reflector.get('roles', handler)` |
| `getAll(key, targets)` | Читає метадані з кількох джерел, повертає масив | `reflector.getAll('roles', [handler, class])` |
| `getAllAndOverride(key, targets)` | Читає метадані з кількох джерел, повертає **перше непорожнє** значення | `reflector.getAllAndOverride('roles', [handler, class])` |
| `getAllAndMerge(key, targets)` | Читає метадані з кількох джерел, **об'єднує** у один масив | `reflector.getAllAndMerge('roles', [handler, class])` |

**Приклад різниці між методами:**

```typescript
// Контролер
@Controller('posts')
@Roles('user') // Метадані на рівні класу
export class PostsController {
  @Get()
  @Roles('admin') // Метадані на рівні методу (перевизначають клас)
  getAllPosts() {}

  @Post()
  createPost() {} // Успадковує @Roles('user') з класу
}

// У Guard
// get() — читає лише з одного джерела
const methodRoles = reflector.get('roles', context.getHandler()); // ['admin']
const classRoles = reflector.get('roles', context.getClass()); // ['user']

// getAllAndOverride() — бере перше непорожнє (метод має пріоритет)
const roles = reflector.getAllAndOverride('roles', [
  context.getHandler(), // Спочатку метод
  context.getClass(),   // Потім клас
]); // ['admin'] — перевизначає клас

// getAllAndMerge() — об'єднує обидва джерела
const mergedRoles = reflector.getAllAndMerge('roles', [
  context.getHandler(),
  context.getClass(),
]); // ['admin', 'user'] — об'єднує
```

::tip
**Стратегія вибору методу Reflector:**

- **`getAllAndOverride()`** — використовуйте для випадків, коли метод має перевизначати налаштування класу (наприклад, публічний маршрут у захищеному контролері).
- **`getAllAndMerge()`** — використовуйте для випадків, коли метод має успадковувати налаштування класу та додавати власні (наприклад, додавання додаткових ролей).
::

---

## Декоратор @CurrentUser(): Витягування користувача

Один із найпоширеніших випадків використання — витягування автентифікованого користувача з `request.user`. Замість повторення `@Request() req` та `req.user` у кожному методі, створимо декоратор `@CurrentUser()`.

### Реалізація через createParamDecorator

```typescript
// src/auth/decorators/current-user.decorator.ts
import { createParamDecorator, ExecutionContext } from '@nestjs/common';
import { User } from '../../users/entities/user.entity';

/**
 * Декоратор для витягування автентифікованого користувача з request
 * 
 * @example
 * // Витягування всього об'єкта користувача
 * getProfile(@CurrentUser() user: User) { ... }
 * 
 * @example
 * // Витягування конкретного поля
 * getProfile(@CurrentUser('id') userId: string) { ... }
 */
export const CurrentUser = createParamDecorator(
  (data: keyof User | undefined, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;

    // Якщо вказано конкретне поле, повертаємо лише його
    if (data) {
      return user?.[data];
    }

    // Інакше повертаємо весь об'єкт користувача
    return user;
  },
);
```

**Пояснення реалізації:**

- **`createParamDecorator()`** — фабрика NestJS для створення parameter decorators.
- **Параметр `data`:** дозволяє передавати аргумент у декоратор (наприклад, `@CurrentUser('email')`).
- **`ExecutionContext`:** надає доступ до деталей запиту незалежно від транспорту (HTTP, WebSocket, gRPC).
- **`ctx.switchToHttp().getRequest()`:** витягує HTTP request з контексту.

### Використання у контролері

```typescript
// src/posts/posts.controller.ts
import { Controller, Get, Post, Body, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CurrentUser } from '../auth/decorators/current-user.decorator';
import { User } from '../users/entities/user.entity';

@Controller('posts')
@UseGuards(JwtAuthGuard)
export class PostsController {
  constructor(private postsService: PostsService) {}

  /**
   * Отримання профілю поточного користувача
   * @CurrentUser() витягує весь об'єкт User з request.user
   */
  @Get('me')
  getMyProfile(@CurrentUser() user: User) {
    return {
      id: user.id,
      email: user.email,
      roles: user.roles,
    };
  }

  /**
   * Створення поста від імені поточного користувача
   * @CurrentUser('id') витягує лише поле id
   */
  @Post()
  createPost(
    @Body() createDto: CreatePostDto,
    @CurrentUser('id') userId: string,
  ) {
    return this.postsService.create({
      ...createDto,
      authorId: userId,
    });
  }

  /**
   * Отримання email поточного користувача
   */
  @Get('my-email')
  getMyEmail(@CurrentUser('email') email: string) {
    return { email };
  }
}
```

**Переваги підходу:**

- **Читабельність:** `@CurrentUser()` явно вказує на джерело даних, на відміну від `req.user`.
- **Типобезпека:** TypeScript знає тип повернутого значення (`User` або конкретне поле).
- **Reusability:** декоратор можна використовувати у всіх контролерах без дублювання коду.
- **Витягування полів:** `@CurrentUser('id')` дозволяє отримувати лише потрібне поле без доступу до всього об'єкта.

::note
**Важливо:** декоратор `@CurrentUser()` працює лише після виконання `JwtAuthGuard` або іншого Guard, що встановлює `request.user`. Якщо Guard не застосовано, `user` буде `undefined`.
::

---

## Декоратор @Public(): Позначення публічних маршрутів

При глобальному застосуванні `JwtAuthGuard` всі маршрути стають захищеними. Для публічних маршрутів (реєстрація, вхід, документація) створимо декоратор `@Public()`, що обходить автентифікацію.

### Реалізація декоратора

```typescript
// src/auth/decorators/public.decorator.ts
import { SetMetadata } from '@nestjs/common';

/**
 * Ключ для збереження метаданих про публічні маршрути
 */
export const IS_PUBLIC_KEY = 'isPublic';

/**
 * Декоратор для позначення публічних маршрутів, що не вимагають автентифікації
 * 
 * @example
 * @Get('public-info')
 * @Public()
 * getPublicInfo() { ... }
 */
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

### Оновлення JwtAuthGuard для підтримки @Public()

```typescript
// src/auth/guards/jwt-auth.guard.ts
import { Injectable, ExecutionContext } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';
import { Reflector } from '@nestjs/core';
import { IS_PUBLIC_KEY } from '../decorators/public.decorator';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {
  constructor(private reflector: Reflector) {
    super();
  }

  canActivate(context: ExecutionContext) {
    // Перевірка метаданих @Public()
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(), // Метод контролера має вищий пріоритет
      context.getClass(),   // Клас контролера
    ]);

    if (isPublic) {
      return true; // Публічний маршрут — пропускаємо автентифікацію
    }

    // Виконуємо стандартну JWT автентифікацію
    return super.canActivate(context);
  }
}
```

### Використання у контролері

```typescript
// src/auth/auth.controller.ts
import { Controller, Post, Body, Get, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from './guards/jwt-auth.guard';
import { Public } from './decorators/public.decorator';
import { CurrentUser } from './decorators/current-user.decorator';

@Controller('auth')
@UseGuards(JwtAuthGuard) // Глобальний Guard для всього контролера
export class AuthController {
  constructor(private authService: AuthService) {}

  /**
   * Реєстрація — публічний маршрут
   */
  @Post('register')
  @Public() // Обходить JwtAuthGuard
  register(@Body() registerDto: RegisterDto) {
    return this.authService.register(registerDto);
  }

  /**
   * Вхід — публічний маршрут
   */
  @Post('login')
  @Public()
  login(@Body() loginDto: LoginDto) {
    return this.authService.login(loginDto);
  }

  /**
   * Профіль — захищений маршрут (без @Public())
   */
  @Get('profile')
  getProfile(@CurrentUser() user: User) {
    return user;
  }
}
```

**Альтернатива: @Public() на рівні класу**

```typescript
@Controller('public')
@Public() // Весь контролер публічний
export class PublicController {
  @Get('info')
  getInfo() {} // Публічний

  @Get('status')
  getStatus() {} // Публічний
}
```



---

## Композиція декораторів через applyDecorators()

Часто потрібно застосовувати кілька декораторів одночасно. Замість повторення декораторів на кожному маршруті, створимо **композитні декоратори** через `applyDecorators()`.

### Приклад: Декоратор @Auth()

Створимо декоратор `@Auth()`, що комбінує автентифікацію, перевірку ролей та документацію Swagger:

```typescript
// src/auth/decorators/auth.decorator.ts
import { applyDecorators, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiUnauthorizedResponse } from '@nestjs/swagger';
import { JwtAuthGuard } from '../guards/jwt-auth.guard';
import { RolesGuard } from '../guards/roles.guard';
import { Roles } from './roles.decorator';
import { Role } from '../../common/enums/role.enum';

/**
 * Композитний декоратор для автентифікації та авторизації
 * Комбінує JwtAuthGuard, RolesGuard та Swagger документацію
 * 
 * @param roles - Необхідні ролі для доступу до маршруту
 * 
 * @example
 * // Доступ лише для адміністраторів
 * @Get('admin/users')
 * @Auth(Role.ADMIN)
 * getAllUsers() { ... }
 * 
 * @example
 * // Доступ для адміністраторів або редакторів
 * @Put('posts/:id')
 * @Auth(Role.ADMIN, Role.EDITOR)
 * updatePost() { ... }
 */
export function Auth(...roles: Role[]) {
  return applyDecorators(
    // Застосовуємо Guards
    UseGuards(JwtAuthGuard, RolesGuard),
    
    // Додаємо метадані про ролі
    Roles(...roles),
    
    // Swagger документація
    ApiBearerAuth(),
    ApiUnauthorizedResponse({ description: 'Unauthorized' }),
  );
}
```

**Використання у контролері:**

```typescript
// src/users/users.controller.ts
import { Controller, Get, Delete, Param } from '@nestjs/common';
import { Auth } from '../auth/decorators/auth.decorator';
import { Role } from '../common/enums/role.enum';
import { CurrentUser } from '../auth/decorators/current-user.decorator';

@Controller('users')
export class UsersController {
  constructor(private usersService: UsersService) {}

  /**
   * Отримання списку користувачів
   * Доступ: лише адміністратори
   */
  @Get()
  @Auth(Role.ADMIN) // Замість 3 окремих декораторів
  getAllUsers() {
    return this.usersService.findAll();
  }

  /**
   * Видалення користувача
   * Доступ: лише адміністратори
   */
  @Delete(':id')
  @Auth(Role.ADMIN)
  deleteUser(@Param('id') id: string) {
    return this.usersService.delete(id);
  }

  /**
   * Отримання власного профілю
   * Доступ: всі автентифіковані користувачі (без вимог до ролей)
   */
  @Get('me')
  @Auth() // Без аргументів — лише автентифікація без перевірки ролей
  getProfile(@CurrentUser() user: User) {
    return user;
  }
}
```

**Порівняння "До" та "Після":**

```typescript
// ❌ ДО: Багато повторень
@Get('admin/users')
@UseGuards(JwtAuthGuard, RolesGuard)
@Roles(Role.ADMIN)
@ApiBearerAuth()
@ApiUnauthorizedResponse({ description: 'Unauthorized' })
getAllUsers() {}

// ✅ ПІСЛЯ: Один композитний декоратор
@Get('admin/users')
@Auth(Role.ADMIN)
getAllUsers() {}
```

### Приклад: Декоратор @ApiPaginatedResponse()

Створимо декоратор для Swagger документації пагінованих відповідей:

```typescript
// src/common/decorators/api-paginated-response.decorator.ts
import { applyDecorators, Type } from '@nestjs/common';
import { ApiOkResponse, ApiProperty, getSchemaPath } from '@nestjs/swagger';

/**
 * Клас для опису пагінованої відповіді
 */
export class PaginatedDto<T> {
  @ApiProperty({ description: 'Масив результатів', isArray: true })
  data: T[];

  @ApiProperty({ description: 'Загальна кількість записів' })
  total: number;

  @ApiProperty({ description: 'Поточна сторінка' })
  page: number;

  @ApiProperty({ description: 'Кількість записів на сторінці' })
  limit: number;

  @ApiProperty({ description: 'Загальна кількість сторінок' })
  totalPages: number;
}

/**
 * Декоратор для Swagger документації пагінованих відповідей
 * 
 * @param dataDto - DTO клас для елементів масиву
 */
export function ApiPaginatedResponse<TModel extends Type<any>>(
  dataDto: TModel,
) {
  return applyDecorators(
    ApiOkResponse({
      description: 'Пагінована відповідь',
      schema: {
        allOf: [
          {
            properties: {
              data: {
                type: 'array',
                items: { $ref: getSchemaPath(dataDto) },
              },
              total: { type: 'number' },
              page: { type: 'number' },
              limit: { type: 'number' },
              totalPages: { type: 'number' },
            },
          },
        ],
      },
    }),
  );
}
```

**Використання:**

```typescript
// src/posts/posts.controller.ts
import { Controller, Get, Query } from '@nestjs/common';
import { ApiPaginatedResponse } from '../common/decorators/api-paginated-response.decorator';
import { PostDto } from './dto/post.dto';

@Controller('posts')
export class PostsController {
  /**
   * Отримання пагінованого списку постів
   */
  @Get()
  @ApiPaginatedResponse(PostDto) // Автоматична Swagger документація
  async getPosts(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 10,
  ) {
    const [posts, total] = await this.postsService.findAndCount({ page, limit });

    return {
      data: posts,
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    };
  }
}
```

---

## Практичні декоратори для авторизації

Створимо бібліотеку корисних декораторів для різних сценаріїв авторизації.

### Декоратор @RequireOwnership()

Декоратор для позначення маршрутів, що вимагають власності ресурсу:

```typescript
// src/common/decorators/require-ownership.decorator.ts
import { SetMetadata } from '@nestjs/common';

/**
 * Ключ метаданих для перевірки власності
 */
export const REQUIRE_OWNERSHIP_KEY = 'requireOwnership';

/**
 * Декоратор для позначення маршрутів, що вимагають власності ресурсу
 * Використовується разом з OwnershipGuard
 * 
 * @example
 * @Put('posts/:id')
 * @RequireOwnership()
 * updatePost(@Param('id') id: string) { ... }
 */
export const RequireOwnership = () => SetMetadata(REQUIRE_OWNERSHIP_KEY, true);
```

**Guard для перевірки власності:**

```typescript
// src/common/guards/ownership.guard.ts
import {
  Injectable,
  CanActivate,
  ExecutionContext,
  ForbiddenException,
  NotFoundException,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';
import { REQUIRE_OWNERSHIP_KEY } from '../decorators/require-ownership.decorator';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Post } from '../../posts/entities/post.entity';

@Injectable()
export class OwnershipGuard implements CanActivate {
  constructor(
    private reflector: Reflector,
    @InjectRepository(Post)
    private postRepository: Repository<Post>,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    // Перевірка, чи потрібна перевірка власності
    const requireOwnership = this.reflector.get<boolean>(
      REQUIRE_OWNERSHIP_KEY,
      context.getHandler(),
    );

    if (!requireOwnership) {
      return true;
    }

    const request = context.switchToHttp().getRequest();
    const user = request.user;
    const resourceId = request.params.id;

    if (!user || !resourceId) {
      throw new ForbiddenException('Missing authentication or resource ID');
    }

    // Завантажуємо ресурс (можна зробити більш універсальним)
    const resource = await this.postRepository.findOne({
      where: { id: resourceId },
    });

    if (!resource) {
      throw new NotFoundException('Resource not found');
    }

    // Перевірка власності
    if (resource.authorId !== user.sub) {
      // Перевірка: чи є користувач адміністратором (обхід перевірки власності)
      const isAdmin = user.roles?.includes('admin');
      if (!isAdmin) {
        throw new ForbiddenException('You can only modify your own resources');
      }
    }

    return true;
  }
}
```

### Декоратор @AllowedFor()

Декоратор для гнучкого визначення дозволів з логікою OR/AND:

```typescript
// src/auth/decorators/allowed-for.decorator.ts
import { SetMetadata } from '@nestjs/common';
import { Role } from '../../common/enums/role.enum';

/**
 * Ключ метаданих
 */
export const ALLOWED_FOR_KEY = 'allowedFor';

/**
 * Тип для конфігурації дозволів
 */
export interface AllowedForConfig {
  roles?: Role[];
  permissions?: string[];
  logic?: 'OR' | 'AND'; // Логіка перевірки (за замовчуванням OR)
  allowOwner?: boolean; // Чи дозволити власнику ресурсу
}

/**
 * Декоратор для гнучкого визначення дозволів
 * 
 * @example
 * // Дозволити адміністраторам або редакторам
 * @AllowedFor({ roles: [Role.ADMIN, Role.EDITOR] })
 * 
 * @example
 * // Дозволити власнику ресурсу або модератору
 * @AllowedFor({ roles: [Role.MODERATOR], allowOwner: true })
 * 
 * @example
 * // Потребує ВСІХ вказаних дозволів (логіка AND)
 * @AllowedFor({ 
 *   permissions: ['read:posts', 'write:posts'], 
 *   logic: 'AND' 
 * })
 */
export const AllowedFor = (config: AllowedForConfig) =>
  SetMetadata(ALLOWED_FOR_KEY, config);
```

### Декоратор @RateLimit()

Декоратор для індивідуального налаштування rate limiting на маршруті:

```typescript
// src/common/decorators/rate-limit.decorator.ts
import { SetMetadata } from '@nestjs/common';

/**
 * Ключ метаданих для rate limiting
 */
export const RATE_LIMIT_KEY = 'rateLimit';

/**
 * Конфігурація rate limiting
 */
export interface RateLimitConfig {
  points: number; // Кількість дозволених запитів
  duration: number; // Часове вікно у секундах
  blockDuration?: number; // Час блокування після перевищення ліміту (секунди)
}

/**
 * Декоратор для індивідуального налаштування rate limiting
 * 
 * @example
 * // Дозволити 5 запитів за 60 секунд
 * @Post('send-email')
 * @RateLimit({ points: 5, duration: 60 })
 * sendEmail() { ... }
 * 
 * @example
 * // Суворий ліміт для критичних операцій
 * @Post('transfer-money')
 * @RateLimit({ points: 3, duration: 300, blockDuration: 900 })
 * transferMoney() { ... }
 */
export const RateLimit = (config: RateLimitConfig) =>
  SetMetadata(RATE_LIMIT_KEY, config);
```

---

## Декоратори для валідації та трансформації

Створимо декоратори для спрощення валідації параметрів запиту.

### Декоратор @ParseUUID()

Декоратор-обгортка для автоматичної валідації UUID параметрів:

```typescript
// src/common/decorators/parse-uuid.decorator.ts
import { Param, ParseUUIDPipe } from '@nestjs/common';

/**
 * Декоратор для витягування та валідації UUID параметра
 * Автоматично кидає BadRequestException якщо параметр не є валідним UUID
 * 
 * @example
 * @Get('users/:id')
 * getUser(@ParseUUID('id') id: string) { ... }
 */
export const ParseUUID = (property: string) =>
  Param(property, new ParseUUIDPipe({ version: '4' }));
```

### Декоратор @ValidatedBody()

Декоратор для комбінації валідації та трансформації тіла запиту:

```typescript
// src/common/decorators/validated-body.decorator.ts
import { Body, ValidationPipe } from '@nestjs/common';

/**
 * Декоратор для валідації тіла запиту з налаштуваннями за замовчуванням
 * 
 * @example
 * @Post('users')
 * createUser(@ValidatedBody() createDto: CreateUserDto) { ... }
 */
export const ValidatedBody = () =>
  Body(
    new ValidationPipe({
      whitelist: true, // Видаляє властивості, що не входять у DTO
      forbidNonWhitelisted: true, // Кидає помилку при зайвих полях
      transform: true, // Трансформує plain objects у class instances
      transformOptions: {
        enableImplicitConversion: true, // Автоматична конвертація типів
      },
    }),
  );
```

---

## Best Practices для кастомних декораторів

### 1. Іменування декораторів

**Дотримуйтесь конвенцій іменування:**

- Використовуйте `PascalCase` для назв декораторів: `@CurrentUser()`, `@Auth()`, `@Public()`.
- Використовуйте префікси для групування: `@Api...` для Swagger, `@Validate...` для валідації.
- Уникайте занадто загальних назв: замість `@Check()` використовуйте `@CheckPolicies()`.

**Приклади хороших назв:**

```typescript
✅ @CurrentUser() — зрозуміло, що витягує поточного користувача
✅ @RequirePermissions() — явно вказує на перевірку дозволів
✅ @ApiPaginatedResponse() — чітко позначає API документацію для пагінації

❌ @User() — занадто загальне, не зрозуміло, чи це декоратор параметра чи метадані
❌ @Check() — не зрозуміло, що перевіряється
❌ @Data() — надмірно абстрактне
```

### 2. Типізація для TypeScript

**Завжди вказуйте типи для параметрів та повернутих значень:**

```typescript
// ❌ Погано: без типів
export const CurrentUser = createParamDecorator((data, ctx) => {
  const request = ctx.switchToHttp().getRequest();
  return data ? request.user[data] : request.user;
});

// ✅ Добре: з типами
export const CurrentUser = createParamDecorator(
  (data: keyof User | undefined, ctx: ExecutionContext): User | User[keyof User] => {
    const request = ctx.switchToHttp().getRequest();
    const user: User = request.user;
    return data ? user[data] : user;
  },
);
```

### 3. Документація через JSDoc

**Додавайте JSDoc коментарі до всіх декораторів:**

```typescript
/**
 * Декоратор для витягування автентифікованого користувача з request
 * 
 * @param data - (Опційно) Назва поля User Entity для витягування конкретного значення
 * @returns Повний об'єкт User або значення конкретного поля
 * 
 * @example
 * // Витягування всього об'єкта користувача
 * getProfile(@CurrentUser() user: User) { ... }
 * 
 * @example
 * // Витягування лише ID користувача
 * createPost(@CurrentUser('id') userId: string) { ... }
 * 
 * @throws {ForbiddenException} Якщо користувач не автентифікований (request.user відсутній)
 */
export const CurrentUser = createParamDecorator(...);
```

### 4. Константи для ключів метаданих

**Виносьте ключі метаданих у константи:**

```typescript
// ❌ Погано: магічні рядки
export const Public = () => SetMetadata('isPublic', true);
// У Guard
const isPublic = this.reflector.get('isPublic', handler); // Легко помилитися

// ✅ Добре: константи
export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
// У Guard
const isPublic = this.reflector.get(IS_PUBLIC_KEY, handler); // Типобезпечно
```

### 5. Валідація параметрів декоратора

**Перевіряйте вхідні дані:**

```typescript
// src/common/decorators/timeout.decorator.ts
import { SetMetadata } from '@nestjs/common';

export const TIMEOUT_KEY = 'timeout';

/**
 * Декоратор для налаштування таймауту запиту
 * @param milliseconds - Таймаут у мілісекундах (має бути > 0)
 */
export const Timeout = (milliseconds: number) => {
  if (milliseconds <= 0) {
    throw new Error('Timeout must be greater than 0');
  }

  if (milliseconds > 60000) {
    throw new Error('Timeout cannot exceed 60 seconds');
  }

  return SetMetadata(TIMEOUT_KEY, milliseconds);
};
```

### 6. Переви usage над реалізацією

**Проєктуйте API декоратора з погляду користувача:**

```typescript
// ❌ Складний у використанні
@CheckAccess({ 
  strategy: 'role-based', 
  config: { roles: ['admin'] },
  fallback: 'deny'
})

// ✅ Інтуїтивно зрозумілий
@Auth(Role.ADMIN)
```

::tip
**Правило золотої середини:** декоратор має бути максимально простим у використанні, навіть якщо це вимагає складнішої реалізації. Developer Experience (DX) важливіше за внутрішню елегантність коду.
::

---

## Інтерактивні запитання для самоперевірки

::accordion

::accordion-item{label="❓ Яка різниця між SetMetadata() та createParamDecorator()?" icon="i-lucide-help-circle"}

**`SetMetadata()`** створює **method decorator** або **class decorator**, що прикріплює метадані до методу або класу. Ці метадані читаються пізніше у Guards, Interceptors або Pipes через `Reflector`.

**Приклад:** `@Roles('admin')` додає метадані про необхідні ролі, які Guard читає для прийняття рішення про доступ.

**`createParamDecorator()`** створює **parameter decorator**, що витягує дані з контексту запиту (HTTP request, WebSocket message, gRPC context) та передає їх як параметр методу контролера.

**Приклад:** `@CurrentUser()` витягує `request.user` та передає його як параметр методу, щоб уникнути повторення `@Request() req` та `req.user`.

**Ключова відмінність:** `SetMetadata()` НЕ змінює параметри методу, лише додає інформацію для Guards/Interceptors. `createParamDecorator()` безпосередньо надає дані методу контролера.

::

::accordion-item{label="❓ Коли використовувати getAllAndOverride() замість getAllAndMerge()?" icon="i-lucide-help-circle"}

**`getAllAndOverride()`** використовуйте, коли метод має **перевизначати** налаштування класу:

```typescript
@Controller('posts')
@Roles('user') // Базова вимога для всього контролера
export class PostsController {
  @Delete(':id')
  @Roles('admin') // Перевизначає 'user' → потрібен 'admin'
  deletePost() {}
}

// У Guard
const roles = reflector.getAllAndOverride('roles', [handler, class]);
// Результат: ['admin'] — метод перевизначає клас
```

**`getAllAndMerge()`** використовуйте, коли метод має **успадковувати та додавати** налаштування класу:

```typescript
@Controller('posts')
@Roles('user') // Базова вимога
export class PostsController {
  @Delete(':id')
  @Roles('moderator') // Додає додаткову роль
  deletePost() {}
}

// У Guard
const roles = reflector.getAllAndMerge('roles', [handler, class]);
// Результат: ['user', 'moderator'] — об'єднує обидва
```

**Правило вибору:** якщо наявність метаданих на методі означає «замість» класу — `getAllAndOverride()`. Якщо «разом з» класом — `getAllAndMerge()`.

::

::accordion-item{label="❓ Чи можна використовувати декоратори для асинхронних операцій?" icon="i-lucide-help-circle"}

Так, але з обмеженнями. **Parameter decorators** створені через `createParamDecorator()` можуть виконувати асинхронні операції, але це погана практика:

```typescript
// ❌ Антипатерн: асинхронність у декораторі
export const CurrentUserWithPosts = createParamDecorator(
  async (data, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    const user = request.user;
    
    // Асинхронний запит до БД у декораторі — погана ідея!
    user.posts = await postRepository.find({ authorId: user.id });
    
    return user;
  },
);
```

**Проблеми підходу:**
- Декоратор викликається кожного разу при виконанні методу → додаткові запити до БД.
- Складно кешувати результат.
- Порушує Single Responsibility Principle — декоратор має лише витягувати дані, а не завантажувати їх.

**✅ Правильний підхід:** завантажуйте дані у сервісному шарі:

```typescript
@Get('my-posts')
async getMyPosts(@CurrentUser('id') userId: string) {
  return this.postsService.findByAuthor(userId);
}
```

Декоратор має бути **синхронним витягувачем** існуючих даних з request/context, а не **асинхронним завантажувачем** нових даних.

::

::

---

## Підсумок

::card-group

::card{title="🎨 Переваги кастомних декораторів" icon="i-lucide-sparkles"}

**Developer Experience:**
- Зменшення boilerplate коду
- Підвищення читабельності контролерів
- Типобезпека через TypeScript
- Реюзабельність логіки

**Приклади:** `@CurrentUser()`, `@Public()`, `@Auth()`, `@RequireOwnership()`

::

::card{title="🔧 Інструменти створення" icon="i-lucide-wrench"}

**NestJS надає:**
- `SetMetadata()` — додавання метаданих
- `createParamDecorator()` — витягування даних з request
- `applyDecorators()` — композиція декораторів
- `Reflector` — читання метаданих у Guards/Interceptors

**Результат:** потужний інструментарій для створення абстракцій

::

::card{title="📚 Best Practices" icon="i-lucide-book-open"}

**Рекомендації:**
- Константи для ключів метаданих (уникайте магічних рядків)
- JSDoc документація для кожного декоратора
- Типізація параметрів та повернутих значень
- Інтуїтивні назви з префіксами (`@Api...`, `@Require...`)
- Валідація вхідних параметрів

::

::card{title="⚠️ Антипатерни" icon="i-lucide-alert-triangle"}

**Уникайте:**
- Асинхронних операцій у parameter decorators
- Магічних рядків замість констант
- Надмірно складних декораторів (порушення KISS)
- Відсутності типів та документації
- Дублювання логіки (винесіть у реюзабельні декоратори)

::

::

---

У цій лекції ми опанували створення кастомних декораторів для покращення Developer Experience у NestJS застосунках. Декоратори дозволяють абстрагувати складну логіку авторизації, валідації та витягування даних у простий та виразний API.

**Ключові висновки:**

- **Parameter decorators** (`@CurrentUser()`) витягують дані з контексту запиту.
- **Method decorators** (`@Public()`, `@Roles()`) додають метадані для Guards.
- **Композитні декоратори** (`@Auth()`) комбінують кілька декораторів для зручності.
- **Reflector** дозволяє Guards читати метадані для прийняття рішень.

Створена бібліотека декораторів стане основою для всіх майбутніх проєктів, зменшуючи кількість boilerplate коду та підвищуючи читабельність застосунків.

У наступній лекції розглянемо практичні аспекти безпеки веб-застосунків: налаштування CORS, Helmet для security headers, та захист від поширених атак.
