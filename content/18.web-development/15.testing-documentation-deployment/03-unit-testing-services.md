# Unit-тестування сервісів

::card-group

::card{title="🎯 Мета лекції" icon="i-lucide-target"}

- Опанувати техніки ізоляції сервісів від зовнішніх залежностей для швидкого та надійного тестування.
- Навчитися створювати та налаштовувати mock об'єкти через `jest.fn()`, `jest.spyOn()`, `mockResolvedValue()`.
- Освоїти мокування TypeORM репозиторіїв та інших NestJS providers у тестах.
- Зрозуміти різницу між типами test doubles: mocks, stubs, spies та коли використовувати кожен.
- Навчитися перевіряти не лише результати, а й взаємодію між компонентами через assertion на виклики методів.

::

::card{title="🔑 Ключові терміни" icon="i-lucide-key"}

- **Test Double:** загальний термін для об'єктів-замінників у тестах (mocks, stubs, fakes, spies).
- **Mock Object:** об'єкт, що імітує поведінку реальної залежності та дозволяє перевіряти виклики його методів.
- **Stub:** спрощена реалізація залежності, що повертає заздалегідь визначені дані без перевірки викликів.
- **Spy:** обгортка навколо реального методу, що дозволяє відстежувати виклики, зберігаючи оригінальну поведінку.
- **Isolation (Ізоляція):** принцип тестування, коли компонент перевіряється окремо від усіх зовнішніх залежностей.

::

::

---

## Короткий зміст

У цій лекції детально вивчається тестування бізнес-логіки у сервісах з ізоляцією залежностей:

- **Unit-тестування концепція** — тестування smallest testable units (методів сервісу) у повній ізоляції від зовнішніх залежностей (БД, інші сервіси, HTTP), швидкі тести для швидкого feedback
- **Мокування залежностей** — заміна реальних залежностей на mock objects, `jest.fn()` для створення mock функцій, `jest.spyOn()` для шпигунства за викликами методів, налаштування return values через `mockReturnValue()`, `mockResolvedValue()`
- **Мок-репозиторії TypeORM** — створення mock repository через `jest.fn()` для методів find, findOne, save, remove, реєстрація у testing module через custom providers, `getRepositoryToken()` для injection token
- **Testing providers з залежностями** — мокування сервісів у constructor injection, createTestingModule з providers array, overrideProvider() для заміни реальних providers на mocks
- **Isolated testing patterns** — AAA pattern (Arrange-Act-Assert), Given-When-Then, тестування edge cases (null, undefined, empty arrays), error scenarios (throwing exceptions)
- **Assertion на виклики** — перевірка що метод був викликаний: `toHaveBeenCalled()`, `toHaveBeenCalledWith()`, `toHaveBeenCalledTimes()`, важливість verify правильних аргументів
- **Coverage метрики** — statement coverage, branch coverage, function coverage, line coverage, цільові показники для production code

Розглядаються практичні приклади: тестування CRUD методів сервісу, мокування repository для різних scenarios, testing business validation logic, error handling tests.

---

## Концепція ізоляції у Unit тестах

На попередніх лекціях ми розглянули піраміду тестування та базову структуру тестів через Jest. Тепер заглибимося у найважливішу складову Unit тестування — **ізоляцію** (*isolation*). Що це означає практично?

Уявіть типовий NestJS сервіс для роботи з замовленнями:

```typescript
@Injectable()
export class OrderService {
  constructor(
    @InjectRepository(Order)
    private readonly orderRepository: Repository<Order>,
    private readonly userService: UserService,
    private readonly emailService: EmailService,
    private readonly paymentGateway: PaymentGateway,
  ) {}

  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    // 1. Перевірка існування користувача
    const user = await this.userService.findById(userId);
    
    // 2. Валідація товарів та розрахунок суми
    const total = this.calculateTotal(items);
    
    // 3. Обробка платежу через зовнішній шлюз
    const payment = await this.paymentGateway.charge(user.paymentMethod, total);
    
    // 4. Збереження замовлення у БД
    const order = this.orderRepository.create({ userId, items, total, paymentId: payment.id });
    await this.orderRepository.save(order);
    
    // 5. Відправка email-підтвердження
    await this.emailService.sendOrderConfirmation(user.email, order);
    
    return order;
  }
}
```

Цей метод має **п'ять зовнішніх залежностей**: TypeORM репозиторій, три інші сервіси та платіжний шлюз. Якщо ми спробуємо протестувати `createOrder()` без ізоляції — запустивши весь стек залежностей — зіткнемося з проблемами:

**1. Повільність.** Метод виконує реальні запити до БД, викликає зовнішній платіжний API, надсилає справжні email. Один тест може виконуватися 5-10 секунд. Якщо у вас 100 таких тестів, запуск тестового набору займе 10-15 хвилин — це неприйнятно для швидкого feedback loop.

**2. Крихкість.** Тест падатиме при недоступності БД, збої мережі при виклику платіжного API, проблеми з SMTP сервером. Це **false negatives** — тест червоний не через баг у `OrderService`, а через інфраструктурні проблеми.

**3. Складність налаштування.** Щоб тест пройшов, потрібно: запустити БД, створити користувача, налаштувати тестовий акаунт у платіжному шлюзі, підняти SMTP mock. Це вимагає складної інфраструктури для тестів.

**4. Побічні ефекти.** Тест створює реальні записи у БД, виконує платіжні транзакції (навіть у sandbox), надсилає email. Це вимагає cleanup після кожного тесту та може призвести до взаємовпливу тестів.

**Рішення — ізоляція через test doubles.** Замість запуску реальних залежностей ми замінюємо їх на **тестові дублери** (*test doubles*) — спрощені об'єкти, що імітують поведінку оригіналів. У результаті тест перевіряє **лише логіку `OrderService`**, не зачіпаючи БД, мережу чи інші сервіси:

```typescript
describe('OrderService', () => {
  let service: OrderService;
  let orderRepository: jest.Mocked<Repository<Order>>;
  let userService: jest.Mocked<UserService>;
  let emailService: jest.Mocked<EmailService>;
  let paymentGateway: jest.Mocked<PaymentGateway>;

  beforeEach(async () => {
    // Створюємо test doubles для всіх залежностей
    const mockOrderRepo = {
      create: jest.fn(),
      save: jest.fn(),
      findOne: jest.fn(),
    };
    const mockUserService = { findById: jest.fn() };
    const mockEmailService = { sendOrderConfirmation: jest.fn() };
    const mockPaymentGateway = { charge: jest.fn() };

    const module = await Test.createTestingModule({
      providers: [
        OrderService,
        { provide: getRepositoryToken(Order), useValue: mockOrderRepo },
        { provide: UserService, useValue: mockUserService },
        { provide: EmailService, useValue: mockEmailService },
        { provide: PaymentGateway, useValue: mockPaymentGateway },
      ],
    }).compile();

    service = module.get<OrderService>(OrderService);
    orderRepository = module.get(getRepositoryToken(Order));
    userService = module.get(UserService);
    emailService = module.get(EmailService);
    paymentGateway = module.get(PaymentGateway);
  });

  it('should create order with correct total', async () => {
    // Arrange: налаштовуємо поведінку test doubles
    const mockUser = { id: '1', email: 'user@test.com', paymentMethod: 'card_123' };
    const mockPayment = { id: 'pay_456', status: 'success' };
    const mockOrder = { id: 'order_789', userId: '1', total: 100 };

    userService.findById.mockResolvedValue(mockUser);
    paymentGateway.charge.mockResolvedValue(mockPayment);
    orderRepository.create.mockReturnValue(mockOrder as Order);
    orderRepository.save.mockResolvedValue(mockOrder as Order);
    emailService.sendOrderConfirmation.mockResolvedValue(undefined);

    // Act: викликаємо тестований метод
    const result = await service.createOrder('1', [{ productId: 'P1', price: 50, quantity: 2 }]);

    // Assert: перевіряємо результат та взаємодію
    expect(result.total).toBe(100);
    expect(paymentGateway.charge).toHaveBeenCalledWith('card_123', 100);
    expect(orderRepository.save).toHaveBeenCalled();
    expect(emailService.sendOrderConfirmation).toHaveBeenCalledWith('user@test.com', mockOrder);
  });
});
```

Цей тест виконується за **2-5 мілісекунд** (замість 5-10 секунд), не залежить від зовнішньої інфраструктури та перевіряє саме логіку `OrderService`: чи правильно розраховується total, чи викликається payment gateway з коректними аргументами, чи зберігається замовлення у БД, чи надсилається email-підтвердження.


::note
**Чому це називається Unit тестом?** Ми тестуємо найменшу можливу «одиницю» (*unit*) коду — окремий метод `createOrder()` класу `OrderService` — у повній ізоляції від його залежностей. Навіть якщо `UserService` має баг або `PaymentGateway` недоступний, наш тест продовжує працювати та перевіряти логіку `OrderService`. Це дозволяє швидко локалізувати проблему: якщо тест падає, баг точно у тестованому методі, а не у якійсь із залежностей.
::

---

## Типи test doubles: mocks, stubs, spies

У попередньому прикладі ми використали загальний термін «test double» для об'єктів-замінників. Проте існує кілька різновидів test doubles, кожен із яких має своє призначення. Розуміння відмінностей допоможе вибирати правильний інструмент для конкретної ситуації.

### Mock — перевірка взаємодії

**Mock object** — це об'єкт, який імітує поведінку реальної залежності та **дозволяє перевірити, чи були викликані його методи з правильними аргументами**. Моки використовуються, коли важлива не лише поведінка тестованого коду, а й **як він взаємодіє** з залежностями.

Приклад: ви тестуєте метод `registerUser()`, який має надіслати welcome email після реєстрації. Навіть якщо email не впливає на повернутий результат, ви хочете переконатися, що `emailService.sendWelcomeEmail()` був викликаний із правильною email-адресою:

```typescript
it('should send welcome email after registration', async () => {
  // Arrange
  const mockEmailService = { sendWelcomeEmail: jest.fn() };
  const service = new UserService(mockEmailService);

  // Act
  await service.registerUser('newuser@test.com', 'password123');

  // Assert: перевіряємо, що метод був викликаний
  expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith('newuser@test.com');
  expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledTimes(1);
});
```

У цьому тесті ми використовуємо `emailService` як **mock**: перевіряємо не те, що він повертає (він нічого не повертає), а те, **чи був викликаний** та **з якими параметрами**.

### Stub — повернення заздалегідь визначених даних

**Stub** — це спрощена реалізація залежності, що повертає заздалегідь визначені дані (*canned responses*) без виконання реальної логіки. Стаби використовуються, коли потрібно просто надати тестованому коду необхідні дані, без перевірки взаємодії.

Приклад: метод `calculateDiscount()` отримує користувача від `userService.findById()` та застосовує знижку залежно від кількості замовлень. Нам не важливо, чи викликався `findById()` — важливо лише, щоб він повернув користувача з певною кількістю замовлень:

```typescript
it('should apply 15% discount for users with 5+ orders', async () => {
  // Arrange: створюємо stub
  const stubUserService = {
    findById: jest.fn().mockResolvedValue({ id: '1', orderCount: 7 }),
  };
  const service = new OrderService(stubUserService);

  // Act
  const discount = await service.calculateDiscount('1', 100);

  // Assert: перевіряємо результат, а не виклики
  expect(discount).toBe(15); // 15% від $100
  // НЕ перевіряємо toHaveBeenCalledWith — це stub, не mock
});
```

У цьому тесті `userService` працює як **stub**: він надає заздалегідь визначені дані (користувача із `orderCount: 7`), і нас не цікавить, скільки разів був викликаний `findById()` або з якими аргументами.

::tip
**Практичне правило:** якщо у тесті є assertions на виклики методів (`toHaveBeenCalled`, `toHaveBeenCalledWith`), ви використовуєте **mock**. Якщо є лише assertions на результат тестованого методу — ви використовуєте **stub**. У реальності більшість test doubles поєднують обидві ролі: вони повертають дані (stub) **і** дозволяють перевіряти виклики (mock). Jest не розрізняє ці поняття термінологічно — `jest.fn()` створює універсальний test double.
::

### Spy — відстеження викликів реального методу

**Spy** — це обгортка навколо реального методу, що дозволяє відстежувати виклики, зберігаючи оригінальну поведінку. Використовується, коли потрібно перевірити, чи викликається метод, але без заміни його реалізації.

```typescript
it('should call internal validation method', async () => {
  const service = new UserService();
  
  // Створюємо spy на приватний метод (для демонстрації)
  const validateSpy = jest.spyOn(service as any, 'validatePassword');

  // Act
  await service.registerUser('user@test.com', 'password123');

  // Assert: метод був викликаний, але виконалася реальна логіка
  expect(validateSpy).toHaveBeenCalledWith('password123');
  
  // Очищуємо spy після тесту
  validateSpy.mockRestore();
});
```

**Важлива відмінність:** при використанні `jest.spyOn()` оригінальний метод **виконується**, на відміну від `jest.fn()`, де метод повністю замінюється заглушкою. Spy корисні для перевірки внутрішньої логіки класу без втрати реальної поведінки.

::warning
Уникайте тестування приватних методів через spy — це порушує інкапсуляцію та робить тести крихкими. Якщо приватний метод містить складну логіку, яку важко покрити через публічний API, це сигнал до рефакторингу: можливо, цей метод варто винести у окрему утиліту або сервіс та протестувати окремо.
::

### Fake — робоча реалізація з обмеженнями

**Fake** — це спрощена, але **робоча** реалізація залежності. На відміну від stub, який просто повертає захардкоджені дані, fake містить реальну логіку, але простішу за production версію.

Приклад: замість реального PostgreSQL ви використовуєте in-memory SQLite для Integration тестів — це fake database. Або замість справжнього SMTP сервера використовуєте `nodemailer-mock`, що зберігає відправлені email у масиві в пам'яті — це fake email service.

```typescript
// Fake implementation для email service
class FakeEmailService {
  private sentEmails: Array<{ to: string; subject: string; body: string }> = [];

  async send(to: string, subject: string, body: string): Promise<void> {
    this.sentEmails.push({ to, subject, body });
  }

  getSentEmails() {
    return this.sentEmails;
  }

  clear() {
    this.sentEmails = [];
  }
}

it('should send two emails for order confirmation', async () => {
  const fakeEmailService = new FakeEmailService();
  const service = new OrderService(fakeEmailService);

  await service.createOrder('user123', items);

  // Перевіряємо через fake
  expect(fakeEmailService.getSentEmails()).toHaveLength(2);
  expect(fakeEmailService.getSentEmails()[0].to).toBe('user@test.com');
});
```

Fakes частіше використовуються в Integration тестах, ніж у Unit тестах, оскільки вони все ще виконують певну логіку, що сповільнює тести порівняно з простими stubs.

---

## Створення mock об'єктів через jest.fn()

Тепер, коли ми розуміємо різні типи test doubles, розглянемо детально, як створювати їх за допомогою Jest API.

### jest.fn() — базова mock функція

**`jest.fn()`** створює mock функцію — спеціальний об'єкт, що:
1. Може бути викликаний як звичайна функція.
2. Запам'ятовує всі виклики: аргументи, результати, контекст (`this`).
3. Дозволяє налаштувати повернуте значення через `.mockReturnValue()` або `.mockResolvedValue()`.
4. Надає методи для перевірки викликів: `toHaveBeenCalled()`, `toHaveBeenCalledWith()`.

```typescript
// Створення простої mock функції
const mockFunction = jest.fn();

// Виклик функції
mockFunction('hello', 42);
mockFunction('world', 100);

// Перевірка викликів
expect(mockFunction).toHaveBeenCalledTimes(2);
expect(mockFunction).toHaveBeenCalledWith('hello', 42);
expect(mockFunction).toHaveBeenLastCalledWith('world', 100);

// Отримання всіх викликів
console.log(mockFunction.mock.calls);
// [['hello', 42], ['world', 100]]
```

### Налаштування return values

За замовчуванням `jest.fn()` повертає `undefined`. Щоб налаштувати повернуте значення:

**`mockReturnValue(value)`** — для синхронних функцій:

```typescript
const mockGetName = jest.fn().mockReturnValue('John Doe');

console.log(mockGetName()); // 'John Doe'
console.log(mockGetName()); // 'John Doe' (той самий результат)
```

**`mockReturnValueOnce(value)`** — різні значення для послідовних викликів:

```typescript
const mockGetId = jest.fn()
  .mockReturnValueOnce('id-1')
  .mockReturnValueOnce('id-2')
  .mockReturnValue('default-id');

console.log(mockGetId()); // 'id-1'
console.log(mockGetId()); // 'id-2'
console.log(mockGetId()); // 'default-id'
console.log(mockGetId()); // 'default-id'
```

**`mockResolvedValue(value)`** — для асинхронних функцій (повертають Promise):

```typescript
const mockFindUser = jest.fn().mockResolvedValue({ id: '1', email: 'test@test.com' });

await mockFindUser(); // Promise<{ id: '1', email: 'test@test.com' }>

// Еквівалентно:
jest.fn().mockReturnValue(Promise.resolve({ id: '1', email: 'test@test.com' }));
```

**`mockRejectedValue(error)`** — для симуляції помилок:

```typescript
const mockSave = jest.fn().mockRejectedValue(new Error('Database connection failed'));

try {
  await mockSave();
} catch (error) {
  console.log(error.message); // 'Database connection failed'
}
```

### Створення mock об'єкта з кількома методами

Для мокування сервісу або репозиторію з багатьма методами створюємо об'єкт із `jest.fn()` для кожного методу:

```typescript
const mockUserRepository = {
  findOne: jest.fn(),
  find: jest.fn(),
  create: jest.fn(),
  save: jest.fn(),
  remove: jest.fn(),
  count: jest.fn(),
};

// Налаштовуємо поведінку кожного методу
mockUserRepository.findOne.mockResolvedValue({ id: '1', email: 'test@test.com' });
mockUserRepository.find.mockResolvedValue([]);
mockUserRepository.create.mockReturnValue({ id: '2', email: 'new@test.com' });
mockUserRepository.save.mockResolvedValue({ id: '2', email: 'new@test.com' });
```

Цей об'єкт можна передати у `Test.createTestingModule()` як заміну для реального репозиторію.


---

## Мокування TypeORM репозиторіїв

TypeORM репозиторії — найпоширеніша залежність у NestJS сервісах. Розглянемо детально, як правильно їх мокувати для Unit тестів.

### Базовий приклад: мокування Repository<T>

Припустимо, у нас є сервіс для роботи з постами блогу:

```typescript
// post/post.service.ts
@Injectable()
export class PostService {
  constructor(
    @InjectRepository(Post)
    private readonly postRepository: Repository<Post>,
  ) {}

  async findById(id: string): Promise<Post> {
    const post = await this.postRepository.findOne({ where: { id } });
    
    if (!post) {
      throw new NotFoundException(`Post with ID ${id} not found`);
    }
    
    return post;
  }

  async findPublishedPosts(): Promise<Post[]> {
    return this.postRepository.find({
      where: { published: true },
      order: { createdAt: 'DESC' },
    });
  }

  async createPost(title: string, content: string, authorId: string): Promise<Post> {
    const post = this.postRepository.create({ title, content, authorId, published: false });
    return this.postRepository.save(post);
  }

  async publishPost(id: string): Promise<Post> {
    const post = await this.findById(id);
    post.published = true;
    return this.postRepository.save(post);
  }
}
```

Тепер створимо тести:

```typescript
// post/post.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { getRepositoryToken } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { NotFoundException } from '@nestjs/common';
import { PostService } from './post.service';
import { Post } from './post.entity';

describe('PostService', () => {
  let service: PostService;
  let repository: jest.Mocked<Repository<Post>>;

  beforeEach(async () => {
    // Створюємо mock repository з основними методами
    const mockRepository = {
      findOne: jest.fn(),
      find: jest.fn(),
      create: jest.fn(),
      save: jest.fn(),
      remove: jest.fn(),
      count: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        PostService,
        {
          provide: getRepositoryToken(Post),
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<PostService>(PostService);
    repository = module.get(getRepositoryToken(Post));
  });

  describe('findById', () => {
    it('should return post when found', async () => {
      // Arrange
      const mockPost = {
        id: '123',
        title: 'Test Post',
        content: 'Test content',
        published: false,
      } as Post;
      
      repository.findOne.mockResolvedValue(mockPost);

      // Act
      const result = await service.findById('123');

      // Assert
      expect(result).toEqual(mockPost);
      expect(repository.findOne).toHaveBeenCalledWith({ where: { id: '123' } });
    });

    it('should throw NotFoundException when post not found', async () => {
      // Arrange
      repository.findOne.mockResolvedValue(null);

      // Act & Assert
      await expect(service.findById('nonexistent')).rejects.toThrow(NotFoundException);
      await expect(service.findById('nonexistent')).rejects.toThrow('Post with ID nonexistent not found');
    });
  });

  describe('findPublishedPosts', () => {
    it('should return only published posts ordered by date', async () => {
      // Arrange
      const mockPosts = [
        { id: '1', title: 'Post 1', published: true, createdAt: new Date('2024-01-02') },
        { id: '2', title: 'Post 2', published: true, createdAt: new Date('2024-01-01') },
      ] as Post[];
      
      repository.find.mockResolvedValue(mockPosts);

      // Act
      const result = await service.findPublishedPosts();

      // Assert
      expect(result).toEqual(mockPosts);
      expect(repository.find).toHaveBeenCalledWith({
        where: { published: true },
        order: { createdAt: 'DESC' },
      });
    });

    it('should return empty array when no published posts', async () => {
      // Arrange
      repository.find.mockResolvedValue([]);

      // Act
      const result = await service.findPublishedPosts();

      // Assert
      expect(result).toEqual([]);
      expect(result).toHaveLength(0);
    });
  });

  describe('createPost', () => {
    it('should create and save new post', async () => {
      // Arrange
      const title = 'New Post';
      const content = 'New content';
      const authorId = 'author-123';
      
      const createdPost = { id: '456', title, content, authorId, published: false } as Post;
      
      repository.create.mockReturnValue(createdPost);
      repository.save.mockResolvedValue(createdPost);

      // Act
      const result = await service.createPost(title, content, authorId);

      // Assert
      expect(repository.create).toHaveBeenCalledWith({
        title,
        content,
        authorId,
        published: false,
      });
      expect(repository.save).toHaveBeenCalledWith(createdPost);
      expect(result.published).toBe(false); // За замовчуванням не опубліковано
    });
  });

  describe('publishPost', () => {
    it('should set published flag to true and save', async () => {
      // Arrange
      const postId = '789';
      const unpublishedPost = {
        id: postId,
        title: 'Draft Post',
        published: false,
      } as Post;
      
      const publishedPost = { ...unpublishedPost, published: true } as Post;
      
      repository.findOne.mockResolvedValue(unpublishedPost);
      repository.save.mockResolvedValue(publishedPost);

      // Act
      const result = await service.publishPost(postId);

      // Assert
      expect(result.published).toBe(true);
      expect(repository.save).toHaveBeenCalledWith(
        expect.objectContaining({ id: postId, published: true })
      );
    });

    it('should throw NotFoundException when post does not exist', async () => {
      // Arrange
      repository.findOne.mockResolvedValue(null);

      // Act & Assert
      await expect(service.publishPost('nonexistent')).rejects.toThrow(NotFoundException);
    });
  });
});
```

### Ключові аспекти мокування репозиторіїв

**1. getRepositoryToken(Entity)** — ця утиліта з `@nestjs/typeorm` повертає унікальний injection token для репозиторію. NestJS використовує його для реєстрації та отримання репозиторіїв із DI контейнера. При заміні репозиторію на mock використовуйте цей самий токен.

**2. Часткове мокування** — не обов'язково мокувати всі методи `Repository<T>`. Створюйте лише ті методи, які використовуються у тестованому коді. Якщо ваш сервіс викликає лише `findOne()` та `save()`, не треба додавати моки для `update()`, `delete()` тощо.

**3. Типізація через jest.Mocked<T>** — використання `jest.Mocked<Repository<Post>>` дає TypeScript підказки для mock методів (`.mockResolvedValue`, `.toHaveBeenCalledWith`). Без цієї типізації IDE не підказуватиме доступні mock функції.

```typescript
// ✅ З типізацією
let repository: jest.Mocked<Repository<Post>>;
repository.findOne.mockResolvedValue(/* автокомпліт працює */);

// ❌ Без типізації
let repository: Repository<Post>;
repository.findOne.mockResolvedValue(/* TypeScript помилка: Property 'mockResolvedValue' does not exist */);
```

::tip
Якщо ваш сервіс використовує **QueryBuilder** для складних запитів, мокування стає складнішим, оскільки потрібно імітувати ланцюг методів (`createQueryBuilder().where().andWhere().getMany()`). У таких випадках розгляньте два підходи:

1. **Винесіть логіку побудови запиту в окремий метод** та протестуйте її через Integration тест із реальною БД.
2. **Створіть mock QueryBuilder** з усім ланцюгом методів:

```typescript
const mockQueryBuilder = {
  where: jest.fn().mockReturnThis(),
  andWhere: jest.fn().mockReturnThis(),
  orderBy: jest.fn().mockReturnThis(),
  getMany: jest.fn().mockResolvedValue([]),
  getOne: jest.fn().mockResolvedValue(null),
};

repository.createQueryBuilder.mockReturnValue(mockQueryBuilder as any);
```

Проте це вже сигнал, що Unit тест стає занадто складним — можливо, краще написати Integration тест для цього сценарію.
::

---

## Мокування інших NestJS сервісів

Окрім репозиторіїв, сервіси часто залежать від інших сервісів. Розглянемо детально, як мокувати складні залежності.

### Сервіс із кількома залежностями

```typescript
// order/order.service.ts
@Injectable()
export class OrderService {
  constructor(
    @InjectRepository(Order)
    private readonly orderRepository: Repository<Order>,
    private readonly userService: UserService,
    private readonly productService: ProductService,
    private readonly notificationService: NotificationService,
  ) {}

  async createOrder(userId: string, productIds: string[]): Promise<Order> {
    // 1. Перевірка користувача
    const user = await this.userService.findById(userId);
    if (!user.isActive) {
      throw new BadRequestException('User account is inactive');
    }

    // 2. Перевірка товарів
    const products = await this.productService.findByIds(productIds);
    if (products.length !== productIds.length) {
      throw new BadRequestException('Some products not found');
    }

    // 3. Розрахунок суми
    const total = products.reduce((sum, p) => sum + p.price, 0);

    // 4. Застосування знижки для постійних клієнтів
    const discount = user.orderCount >= 5 ? total * 0.1 : 0;
    const finalTotal = total - discount;

    // 5. Створення замовлення
    const order = this.orderRepository.create({
      userId,
      productIds,
      total: finalTotal,
      discount,
    });
    await this.orderRepository.save(order);

    // 6. Відправка нотифікації
    await this.notificationService.sendOrderCreated(user.email, order.id);

    return order;
  }
}
```

Тест для цього методу:

```typescript
describe('OrderService', () => {
  let service: OrderService;
  let orderRepository: jest.Mocked<Repository<Order>>;
  let userService: jest.Mocked<UserService>;
  let productService: jest.Mocked<ProductService>;
  let notificationService: jest.Mocked<NotificationService>;

  beforeEach(async () => {
    const mockOrderRepo = {
      create: jest.fn(),
      save: jest.fn(),
      findOne: jest.fn(),
    };

    const mockUserService = {
      findById: jest.fn(),
    };

    const mockProductService = {
      findByIds: jest.fn(),
    };

    const mockNotificationService = {
      sendOrderCreated: jest.fn(),
    };

    const module = await Test.createTestingModule({
      providers: [
        OrderService,
        { provide: getRepositoryToken(Order), useValue: mockOrderRepo },
        { provide: UserService, useValue: mockUserService },
        { provide: ProductService, useValue: mockProductService },
        { provide: NotificationService, useValue: mockNotificationService },
      ],
    }).compile();

    service = module.get<OrderService>(OrderService);
    orderRepository = module.get(getRepositoryToken(Order));
    userService = module.get(UserService);
    productService = module.get(ProductService);
    notificationService = module.get(NotificationService);
  });

  describe('createOrder', () => {
    it('should create order with correct total and discount for regular customer', async () => {
      // Arrange
      const userId = 'user-1';
      const productIds = ['prod-1', 'prod-2'];

      const mockUser = {
        id: userId,
        email: 'regular@test.com',
        isActive: true,
        orderCount: 7, // Постійний клієнт
      };

      const mockProducts = [
        { id: 'prod-1', name: 'Product 1', price: 100 },
        { id: 'prod-2', name: 'Product 2', price: 50 },
      ];

      const mockOrder = {
        id: 'order-123',
        userId,
        productIds,
        total: 135, // 150 - 15 (10% знижка)
        discount: 15,
      } as Order;

      userService.findById.mockResolvedValue(mockUser as any);
      productService.findByIds.mockResolvedValue(mockProducts as any);
      orderRepository.create.mockReturnValue(mockOrder);
      orderRepository.save.mockResolvedValue(mockOrder);
      notificationService.sendOrderCreated.mockResolvedValue(undefined);

      // Act
      const result = await service.createOrder(userId, productIds);

      // Assert
      expect(result.total).toBe(135);
      expect(result.discount).toBe(15);
      expect(orderRepository.create).toHaveBeenCalledWith({
        userId,
        productIds,
        total: 135,
        discount: 15,
      });
      expect(notificationService.sendOrderCreated).toHaveBeenCalledWith('regular@test.com', 'order-123');
    });

    it('should create order without discount for new customer', async () => {
      // Arrange
      const mockUser = {
        id: 'user-2',
        email: 'new@test.com',
        isActive: true,
        orderCount: 2, // Менше 5 замовлень
      };

      const mockProducts = [{ id: 'prod-1', price: 100 }];

      userService.findById.mockResolvedValue(mockUser as any);
      productService.findByIds.mockResolvedValue(mockProducts as any);
      orderRepository.create.mockReturnValue({ total: 100, discount: 0 } as Order);
      orderRepository.save.mockResolvedValue({ total: 100, discount: 0 } as Order);

      // Act
      const result = await service.createOrder('user-2', ['prod-1']);

      // Assert
      expect(result.total).toBe(100);
      expect(result.discount).toBe(0); // Без знижки
    });

    it('should throw BadRequestException when user is inactive', async () => {
      // Arrange
      const mockUser = { id: 'user-3', isActive: false };
      userService.findById.mockResolvedValue(mockUser as any);

      // Act & Assert
      await expect(service.createOrder('user-3', ['prod-1']))
        .rejects.toThrow(BadRequestException);
      
      await expect(service.createOrder('user-3', ['prod-1']))
        .rejects.toThrow('User account is inactive');

      // Перевіряємо, що репозиторій НЕ був викликаний
      expect(orderRepository.save).not.toHaveBeenCalled();
    });

    it('should throw BadRequestException when some products not found', async () => {
      // Arrange
      const mockUser = { id: 'user-4', isActive: true, orderCount: 0 };
      userService.findById.mockResolvedValue(mockUser as any);
      
      // Повертаємо лише 1 продукт замість 2
      productService.findByIds.mockResolvedValue([{ id: 'prod-1', price: 100 }] as any);

      // Act & Assert
      await expect(service.createOrder('user-4', ['prod-1', 'prod-2']))
        .rejects.toThrow('Some products not found');

      expect(orderRepository.save).not.toHaveBeenCalled();
    });
  });
});
```

Цей тест демонструє кілька важливих концепцій:

**1. Мокування кількох залежностей одночасно.** Кожен mock налаштовується незалежно через `mockResolvedValue()`.

**2. Перевірка бізнес-логіки.** Ми тестуємо розрахунок знижки (10% для клієнтів із 5+ замовленнями) та коректність підсумкової суми.

**3. Перевірка обробки помилок.** Окремі тести для випадків, коли користувач неактивний або товари не знайдені.

**4. Перевірка side effects.** Assertion на те, що нотифікація була відправлена з правильними параметрами.

**5. Негативні assertions.** `expect(...).not.toHaveBeenCalled()` — перевірка, що певні методи **не були викликані** у сценарії помилки (наприклад, `orderRepository.save()` не має викликатися, якщо валідація провалилася).


---

## Assertions на виклики методів

Перевірка того, **чи був викликаний метод** та **з якими аргументами**, є критично важливою для Unit тестів, що перевіряють взаємодію між компонентами. Jest надає потужний набір matchers для таких перевірок.

### toHaveBeenCalled() — базова перевірка виклику

Найпростіший matcher — перевірка, що функція була викликана принаймні один раз:

```typescript
it('should call repository.save', async () => {
  repository.save.mockResolvedValue({} as Order);
  
  await service.createOrder('user-1', ['prod-1']);
  
  expect(repository.save).toHaveBeenCalled();
});
```

Якщо метод **не був** викликаний, тест провалиться з повідомленням:

```
Expected: "save" to have been called, but it was not called.
```

### toHaveBeenCalledTimes(n) — перевірка кількості викликів

Для перевірки точної кількості викликів використовуйте `toHaveBeenCalledTimes()`:

```typescript
it('should call findById exactly once', async () => {
  userService.findById.mockResolvedValue({ id: '1' } as User);
  
  await service.createOrder('1', ['prod-1']);
  
  expect(userService.findById).toHaveBeenCalledTimes(1);
});

it('should send two notifications for premium order', async () => {
  // ... setup
  await service.createPremiumOrder('user-1', ['prod-1']);
  
  // Преміум замовлення надсилає 2 нотифікації: email + SMS
  expect(notificationService.send).toHaveBeenCalledTimes(2);
});
```

Це особливо корисно для виявлення багів, коли метод викликається більше разів, ніж очікувалося (наприклад, у циклі замість одного разу).

### toHaveBeenCalledWith(...args) — перевірка аргументів

Найважливіший matcher для Unit тестів — перевірка, що метод був викликаний із **правильними аргументами**:

```typescript
it('should pass correct arguments to repository.create', async () => {
  const userId = 'user-123';
  const productIds = ['prod-1', 'prod-2'];
  const total = 150;

  repository.create.mockReturnValue({} as Order);
  repository.save.mockResolvedValue({} as Order);
  // ... інші моки

  await service.createOrder(userId, productIds);

  expect(repository.create).toHaveBeenCalledWith({
    userId: 'user-123',
    productIds: ['prod-1', 'prod-2'],
    total: 150,
    discount: 0,
  });
});
```

Якщо аргументи не співпадають, Jest покаже детальну різницю:

```
Expected: {"userId": "user-123", "productIds": ["prod-1", "prod-2"], "total": 150, "discount": 0}
Received: {"userId": "user-123", "productIds": ["prod-1", "prod-2"], "total": 140, "discount": 10}
```

### expect.objectContaining() — часткове співпадіння

Коли потрібно перевірити лише **частину** аргументів, використовуйте `expect.objectContaining()`:

```typescript
it('should call save with order containing userId', async () => {
  // ... setup
  await service.createOrder('user-1', ['prod-1']);

  expect(repository.save).toHaveBeenCalledWith(
    expect.objectContaining({
      userId: 'user-1', // Перевіряємо лише це поле
      // Інші поля можуть бути будь-якими
    })
  );
});
```

Це корисно, коли об'єкт містить поля, які важко передбачити (наприклад, автоматично згенеровані `id` або `createdAt`), але ви хочете перевірити ключові поля.

### expect.any(Constructor) — перевірка типу

Для перевірки типу аргументу без точного значення:

```typescript
it('should call logger with string message', () => {
  logger.log.mockReturnValue(undefined);
  
  service.logOrderCreation('order-123');

  expect(logger.log).toHaveBeenCalledWith(
    expect.any(String), // Будь-який рядок
    expect.objectContaining({ orderId: 'order-123' })
  );
});

it('should call repository.save with Date timestamp', async () => {
  await service.createOrderWithTimestamp('user-1', ['prod-1']);

  expect(repository.save).toHaveBeenCalledWith(
    expect.objectContaining({
      createdAt: expect.any(Date), // Будь-який Date об'єкт
    })
  );
});
```

### toHaveBeenLastCalledWith() та toHaveBeenNthCalledWith()

Для перевірки останнього виклику або конкретного виклику за номером:

```typescript
it('should update progress after each step', async () => {
  const progressCallback = jest.fn();
  
  await service.processOrderInSteps('order-1', progressCallback);

  // Перевірка першого виклику
  expect(progressCallback).toHaveBeenNthCalledWith(1, 'Step 1: Validating');
  
  // Перевірка другого виклику
  expect(progressCallback).toHaveBeenNthCalledWith(2, 'Step 2: Processing payment');
  
  // Перевірка останнього виклику
  expect(progressCallback).toHaveBeenLastCalledWith('Step 3: Complete');
});
```

### not.toHaveBeenCalled() — негативна перевірка

Іноді важливо переконатися, що метод **не був викликаний** у певному сценарії:

```typescript
it('should not send notification when user has disabled notifications', async () => {
  const mockUser = { id: '1', notificationsEnabled: false };
  userService.findById.mockResolvedValue(mockUser as User);
  
  await service.createOrder('1', ['prod-1']);

  // Нотифікація НЕ має відправлятися
  expect(notificationService.send).not.toHaveBeenCalled();
});

it('should not save order when validation fails', async () => {
  userService.findById.mockResolvedValue({ id: '1', isActive: false } as User);
  
  await expect(service.createOrder('1', ['prod-1'])).rejects.toThrow();

  // Репозиторій НЕ має викликатися при провалі валідації
  expect(repository.save).not.toHaveBeenCalled();
});
```

::tip
**Коли використовувати assertions на виклики?**

✅ **Використовуйте**, коли:
- Тестуєте side effects (надсилання email, логування, метрики).
- Перевіряєте, що метод викликається з коректними параметрами (особливо для складних об'єктів).
- Тестуєте умовну логіку (метод має викликатися у одному випадку та не викликатися у іншому).

❌ **Не використовуйте**, коли:
- Тестуєте результат обчислень (краще перевірити результат, а не виклики).
- Перевіряєте деталі реалізації (порядок внутрішніх викликів у приватних методах).
- Дублюєте перевірку поведінки, яка вже покрита assertion на результат.

Загальне правило: якщо тест падає при зміні **внутрішньої реалізації** (але не контракту), він занадто прив'язаний до деталей. Фокусуйтеся на перевірці поведінки, а не реалізації.
::

---

## Тестування edge cases та помилок

Хороший Unit тест перевіряє не лише «happy path» (коли все працює як очікується), а й **граничні випадки** (*edge cases*) та обробку помилок.

### Edge cases: null, undefined, порожні колекції

```typescript
describe('OrderService edge cases', () => {
  it('should handle empty product list', async () => {
    userService.findById.mockResolvedValue({ id: '1', isActive: true } as User);
    productService.findByIds.mockResolvedValue([]);

    // Порожній масив продуктів — валідна помилка
    await expect(service.createOrder('1', [])).rejects.toThrow('Product list cannot be empty');
  });

  it('should handle null user', async () => {
    userService.findById.mockResolvedValue(null);

    await expect(service.createOrder('nonexistent-user', ['prod-1']))
      .rejects.toThrow(NotFoundException);
  });

  it('should handle undefined product prices', async () => {
    userService.findById.mockResolvedValue({ id: '1', isActive: true } as User);
    
    // Продукт без ціни — некоректні дані
    productService.findByIds.mockResolvedValue([{ id: 'prod-1', price: undefined }] as any);

    await expect(service.createOrder('1', ['prod-1']))
      .rejects.toThrow('Invalid product data');
  });

  it('should handle very large order totals', async () => {
    userService.findById.mockResolvedValue({ id: '1', isActive: true, orderCount: 10 } as User);
    
    // Продукти з дуже високою ціною
    const expensiveProducts = Array(100).fill({ id: 'prod', price: 1000000 });
    productService.findByIds.mockResolvedValue(expensiveProducts);

    const result = await service.createOrder('1', Array(100).fill('prod'));

    // Перевіряємо, що знижка правильно застосована навіть для великої суми
    expect(result.discount).toBe(10000000); // 10% від 100 млн
    expect(result.total).toBe(90000000);
  });
});
```

### Тестування асинхронних помилок

Коли метод викликає асинхронні залежності, які можуть викинути помилку:

```typescript
it('should handle database connection errors gracefully', async () => {
  userService.findById.mockResolvedValue({ id: '1', isActive: true } as User);
  productService.findByIds.mockResolvedValue([{ id: 'prod-1', price: 100 }] as any);
  
  // Симулюємо помилку БД
  repository.save.mockRejectedValue(new Error('Database connection timeout'));

  await expect(service.createOrder('1', ['prod-1']))
    .rejects.toThrow('Database connection timeout');
});

it('should retry payment on temporary failure', async () => {
  // Перший виклик падає, другий успішний
  paymentGateway.charge
    .mockRejectedValueOnce(new Error('Payment gateway timeout'))
    .mockResolvedValueOnce({ id: 'pay-123', status: 'success' });

  const result = await service.createOrderWithRetry('user-1', ['prod-1']);

  // Перевіряємо, що метод викликався двічі (retry логіка)
  expect(paymentGateway.charge).toHaveBeenCalledTimes(2);
  expect(result.paymentId).toBe('pay-123');
});
```

### Тестування умовної логіки та branch coverage

Переконайтеся, що всі **гілки** (*branches*) коду покриті тестами:

```typescript
// Метод із складною умовною логікою
async applyDiscount(userId: string, total: number): Promise<number> {
  const user = await this.userService.findById(userId);
  
  // Гілка 1: Новий користувач
  if (user.orderCount === 0) {
    return total * 0.05; // 5% знижка для нових
  }
  
  // Гілка 2: Постійний клієнт
  if (user.orderCount >= 10) {
    return total * 0.2; // 20% знижка
  }
  
  // Гілка 3: Звичайний клієнт
  if (user.orderCount >= 5) {
    return total * 0.1; // 10% знижка
  }
  
  // Гілка 4: Без знижки
  return 0;
}

// Тести для всіх гілок
describe('applyDiscount', () => {
  it('should apply 5% discount for new customers', async () => {
    userService.findById.mockResolvedValue({ id: '1', orderCount: 0 } as User);
    expect(await service.applyDiscount('1', 100)).toBe(5);
  });

  it('should apply 10% discount for customers with 5-9 orders', async () => {
    userService.findById.mockResolvedValue({ id: '1', orderCount: 7 } as User);
    expect(await service.applyDiscount('1', 100)).toBe(10);
  });

  it('should apply 20% discount for loyal customers with 10+ orders', async () => {
    userService.findById.mockResolvedValue({ id: '1', orderCount: 15 } as User);
    expect(await service.applyDiscount('1', 100)).toBe(20);
  });

  it('should apply no discount for customers with 1-4 orders', async () => {
    userService.findById.mockResolvedValue({ id: '1', orderCount: 3 } as User);
    expect(await service.applyDiscount('1', 100)).toBe(0);
  });
});
```

Ці чотири тести покривають **всі чотири гілки** умовної логіки, забезпечуючи 100% branch coverage для цього методу.

::note
**Branch coverage** — це метрика, що показує відсоток покритих гілок коду (if/else, switch cases, тернарні оператори). Вона часто важливіша за **line coverage**, оскільки може бути ситуація, коли рядок коду виконується, але не всі його гілки перевірені:

```typescript
const result = user.isActive ? doSomething() : doOther(); // Один рядок, дві гілки

// Тест, що викликає лише одну гілку:
userService.findById.mockResolvedValue({ isActive: true }); // Покрито лише doSomething()
```

Цей тест досягне 100% line coverage, але лише 50% branch coverage. Додайте другий тест для `isActive: false`, щоб покрити обидві гілки.
::


---

## Code Coverage метрики

Після написання Unit тестів важливо оцінити якість покриття коду. Jest автоматично збирає метрики coverage при запуску з прапором `--coverage`.

### Запуск coverage звіту

```bash
npm run test:cov

# Або напряму через Jest
jest --coverage
```

Результат у терміналі:

::terminal-preview{title="npm run test:cov" :cursor="false"}

<div class="line"><span class="opacity-40">$</span> <strong class="font-bold">npm run test:cov</strong></div>
<div class="line"></div>
<div class="line"> PASS  src/order/order.service.spec.ts</div>
<div class="line"> PASS  src/user/user.service.spec.ts</div>
<div class="line"> PASS  src/post/post.service.spec.ts</div>
<div class="line"></div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line"><span class="text-blue-400 font-bold">File             | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s</span></div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line">All files        |   <span class="text-green-400 font-bold">92.5</span>   |   <span class="text-green-400 font-bold">87.3</span>    |  <span class="text-green-400 font-bold">95.2</span>   |  <span class="text-green-400 font-bold">93.1</span>   |</div>
<div class="line"> order           |   <span class="text-green-400 font-bold">95.0</span>   |   <span class="text-green-400 font-bold">90.0</span>    |  <span class="text-green-400 font-bold">100</span>    |  <span class="text-green-400 font-bold">96.0</span>   |</div>
<div class="line">  order.service  |   <span class="text-green-400 font-bold">95.0</span>   |   <span class="text-green-400 font-bold">90.0</span>    |  <span class="text-green-400 font-bold">100</span>    |  <span class="text-green-400 font-bold">96.0</span>   | 45,67</div>
<div class="line"> user            |   <span class="text-green-400 font-bold">88.5</span>   |   <span class="text-yellow-400 font-bold">75.0</span>    |  <span class="text-green-400 font-bold">90.0</span>   |  <span class="text-green-400 font-bold">89.2</span>   |</div>
<div class="line">  user.service   |   <span class="text-green-400 font-bold">88.5</span>   |   <span class="text-yellow-400 font-bold">75.0</span>    |  <span class="text-green-400 font-bold">90.0</span>   |  <span class="text-green-400 font-bold">89.2</span>   | 23,56-58</div>
<div class="line"> post            |   <span class="text-green-400 font-bold">94.2</span>   |   <span class="text-green-400 font-bold">92.5</span>    |  <span class="text-green-400 font-bold">100</span>    |  <span class="text-green-400 font-bold">95.0</span>   |</div>
<div class="line">  post.service   |   <span class="text-green-400 font-bold">94.2</span>   |   <span class="text-green-400 font-bold">92.5</span>    |  <span class="text-green-400 font-bold">100</span>    |  <span class="text-green-400 font-bold">95.0</span>   | 78</div>
<div class="line"><span class="text-blue-400 font-bold">-----------------|---------|----------|---------|---------|-------------------</span></div>
<div class="line"></div>
<div class="line"><span class="text-green-400 font-bold">Test Suites: 3 passed</span>, 3 total</div>
<div class="line"><span class="text-green-400 font-bold">Tests:       24 passed</span>, 24 total</div>
<div class="line">Coverage report generated in <span class="text-blue-400">coverage/lcov-report/index.html</span></div>

::

### Типи coverage метрик

Jest вимірює чотири типи покриття:

**1. Statement Coverage (% Stmts)** — відсоток виконаних **інструкцій** (*statements*) коду. Інструкція — це будь-який рядок коду, що виконує дію: присвоєння значення, виклик функції, return тощо.

```typescript
const total = price * quantity; // Statement 1
return total;                   // Statement 2
```

Якщо тест викликає цю функцію, обидві інструкції виконаються → 100% statement coverage.

**2. Branch Coverage (% Branch)** — відсоток виконаних **гілок** умовної логіки (if/else, switch, тернарні оператори, логічні оператори `&&`/`||`).

```typescript
if (user.isActive) {        // Branch 1: true
  return 'Active';
} else {                    // Branch 2: false
  return 'Inactive';
}
```

Якщо тест покриває лише випадок `isActive === true`, branch coverage буде 50%. Для 100% потрібен тест для обох гілок.

**3. Function Coverage (% Funcs)** — відсоток викликаних **функцій** або методів класу.

```typescript
class UserService {
  findById() { /* ... */ }      // Function 1
  createUser() { /* ... */ }    // Function 2
  deleteUser() { /* ... */ }    // Function 3
}
```

Якщо тести викликають лише `findById()` та `createUser()`, function coverage = 66.7% (2 з 3 функцій).

**4. Line Coverage (% Lines)** — відсоток виконаних **рядків** коду. Подібна до statement coverage, але вимірює саме рядки, а не логічні інструкції.

```typescript
const result = calculateTotal(items); // Line 1
return result;                        // Line 2
```

### Інтерпретація coverage звіту

**Непокриті рядки** (*Uncovered Line #s*) — номери рядків, які не виконувалися під час тестів:

```
user.service.ts | 88.5 | 75.0 | 90.0 | 89.2 | 23,56-58
```

Це означає: у файлі `user.service.ts` рядки **23, 56, 57, 58** не покриті тестами. Відкрийте файл, знайдіть ці рядки та додайте тести для цих сценаріїв.

### HTML звіт

Jest генерує детальний HTML звіт у директорії `coverage/lcov-report/`:

```bash
open coverage/lcov-report/index.html  # macOS
xdg-open coverage/lcov-report/index.html  # Linux
start coverage/lcov-report/index.html  # Windows
```

HTML звіт показує кожен файл з підсвіткою:
- 🟢 **Зелені рядки** — покриті тестами.
- 🔴 **Червоні рядки** — не покриті тестами.
- 🟡 **Жовті рядки** — частково покриті (наприклад, лише одна гілка if/else).

### Цільові показники coverage

Які відсотки coverage вважаються хорошими для production застосунків?

::card-group

::card{title="✅ Оптимальні цільові показники" icon="i-lucide-target"}

- **Statement Coverage:** 80-90%
- **Branch Coverage:** 75-85%
- **Function Coverage:** 85-95%
- **Line Coverage:** 80-90%

Це реалістичні цілі для backend проєктів із хорошою якістю тестів.

::

::card{title="⚠️ Що не варто покривати" icon="i-lucide-alert-triangle"}

- Геттери/сеттери без логіки
- Конструктори класів (якщо вони лише присвоюють параметри)
- DTO класи (прості data transfer objects)
- Auto-generated code (міграції БД, Swagger схеми)
- Trivial mappers (прості перетворення об'єктів)

::

::

::warning
**Coverage метрики — це не ціль, а індикатор.** Досягнення 100% coverage не гарантує відсутність багів. Можна мати 100% покриття з тестами, що нічого не перевіряють:

```typescript
it('should create order', async () => {
  await service.createOrder('user-1', ['prod-1']); // Викликаємо код
  // Немає assertions! 100% coverage, 0% цінності
});
```

Фокусуйтеся на **якості** тестів (чи перевіряють вони значущу поведінку), а не на кількості покритих рядків. Краще 70% coverage із якісними тестами, ніж 95% coverage із формальними тестами без assertions.
::

### Налаштування thresholds у Jest

Ви можете налаштувати мінімальні пороги coverage, нижче яких Jest повертатиме помилку:

```json
// package.json або jest.config.js
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 75,
        "functions": 85,
        "lines": 80,
        "statements": 80
      },
      "./src/order/": {
        "branches": 90,
        "functions": 95,
        "lines": 90,
        "statements": 90
      }
    }
  }
}
```

Якщо coverage падає нижче цих порогів, `npm test -- --coverage` завершиться з помилкою, що дозволяє блокувати PR у CI/CD pipeline до досягнення необхідного рівня покриття.

---

## Висновки та best practices

У цій лекції ми детально розглянули Unit тестування NestJS сервісів з ізоляцією залежностей. Підсумуємо ключові принципи:

::card-group

::card{title="✅ Ізолюйте тестований код" icon="i-lucide-shield"}

Замінюйте всі зовнішні залежності (репозиторії, інші сервіси, HTTP клієнти) на test doubles. Unit тест має перевіряти **лише логіку тестованого компонента**, не залежачи від БД, мережі або інших модулів.

::

::card{title="✅ Використовуйте правильні test doubles" icon="i-lucide-wrench"}

- **Mock** — коли важлива взаємодія (перевірка викликів методів).
- **Stub** — коли потрібно просто надати дані без перевірки викликів.
- **Spy** — коли потрібно відстежити виклики, зберігши оригінальну поведінку.

::

::card{title="✅ Тестуйте edge cases" icon="i-lucide-alert-circle"}

Не обмежуйтеся happy path. Перевіряйте поведінку при:
- Null/undefined значеннях
- Порожніх колекціях
- Граничних числових значеннях
- Помилках від залежностей
- Умовній логіці (всі гілки if/else)

::

::card{title="✅ Перевіряйте взаємодію через assertions" icon="i-lucide-check-circle"}

Використовуйте `toHaveBeenCalledWith()` для перевірки правильності аргументів, `toHaveBeenCalledTimes()` для кількості викликів, `not.toHaveBeenCalled()` для перевірки, що метод не викликався у певному сценарії.

::

::

**Практичне завдання:** Створіть сервіс `TaskService` для управління задачами, який залежить від `TaskRepository`, `UserService` та `NotificationService`. Реалізуйте методи:
- `createTask(userId, title, description)` — створює задачу, перевіряє існування користувача, надсилає нотифікацію.
- `assignTask(taskId, userId)` — призначає задачу користувачеві, перевіряє, що задача ще не призначена.
- `completeTask(taskId, userId)` — позначає задачу виконаною, перевіряє, що користувач — власник задачі.

Напишіть Unit тести для всіх методів, перевірте edge cases (неіснуючий користувач, вже призначена задача, спроба виконати чужу задачу), досягніть 90%+ coverage для сервісу. Використайте моки для всіх залежностей.

::accordion

::accordion-item{label="❓ Чи потрібно мокувати TypeORM QueryBuilder?" icon="i-lucide-help-circle"}

**Це залежить від складності запиту.** Якщо ваш сервіс використовує простий QueryBuilder для одного методу:

```typescript
async findActiveUsers(): Promise<User[]> {
  return this.userRepository
    .createQueryBuilder('user')
    .where('user.isActive = :active', { active: true })
    .getMany();
}
```

Мокувати весь ланцюг методів (`createQueryBuilder().where().getMany()`) може бути занадто громіздким для Unit тесту. У такому випадку **краще написати Integration тест** із реальною БД, який перевірить коректність SQL запиту.

Проте якщо QueryBuilder використовується для складної бізнес-логіки, яку важко протестувати через Integration тест (наприклад, динамічна побудова запиту залежно від фільтрів), можна створити mock QueryBuilder:

```typescript
const mockQueryBuilder = {
  where: jest.fn().mockReturnThis(),
  andWhere: jest.fn().mockReturnThis(),
  orderBy: jest.fn().mockReturnThis(),
  skip: jest.fn().mockReturnThis(),
  take: jest.fn().mockReturnThis(),
  getMany: jest.fn().mockResolvedValue([]),
  getOne: jest.fn().mockResolvedValue(null),
};

repository.createQueryBuilder.mockReturnValue(mockQueryBuilder as any);
```

Але пам'ятайте: чим більше ланцюгів викликів ви мокуєте, тим крихкішим стає тест. Він буде падати при кожній зміні структури запиту.

::

::accordion-item{label="❓ Як тестувати приватні методи класу?" icon="i-lucide-help-circle"}

**Короткаповідь: не треба.** Приватні методи — це деталь реалізації. Їх коректність має перевірятися через тестування **публічних методів**, що їх викликають.

Якщо приватний метод містить складну логіку, яку важко покрити через публічний API, це сигнал до рефакторингу:

1. **Зробіть метод публічним**, якщо він містить корисну бізнес-логіку.
2. **Винесіть логіку у окрему утиліту** або сервіс та протестуйте його окремо.
3. **Спростіть приватний метод**, розбивши складну логіку на простіші частини.

Якщо ви все ж таки хочете протестувати приватний метод (наприклад, для legacy коду, який важко рефакторити), використовуйте type assertion:

```typescript
it('should validate email format (private method)', () => {
  const service = new UserService();
  
  // Обходимо TypeScript захист через 'as any'
  expect((service as any).validateEmail('test@test.com')).toBe(true);
  expect((service as any).validateEmail('invalid')).toBe(false);
});
```

Проте це порушує інкапсуляцію та робить тест крихким до рефакторингу.

::

::
