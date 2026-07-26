# 🧠 План Навчання: Застосування Штучного Інтелекту в Розробці (від А до Я)

> **Дата створення:** 2026-07-18
> **Цільова аудиторія:** Розробники середнього та вищого рівня, які хочуть максимально ефективно інтегрувати AI у свій робочий процес.
> **Формат:** Послідовний навчальний курс із теорією, практикою, та самостійними дослідженнями.

---

## 📋 Зміст

1. [Модуль 0: Фундамент — Що таке LLM і як вони працюють](#модуль-0-фундамент--що-таке-llm-і-як-вони-працюють)
2. [Модуль 1: Ландшафт AI-моделей для розробки](#модуль-1-ландшафт-ai-моделей-для-розробки)
3. [Модуль 2: AI-асистенти та IDE — інструменти розробника](#модуль-2-ai-асистенти-та-ide--інструменти-розробника)
4. [Модуль 3: Prompt Engineering та Context Engineering](#модуль-3-prompt-engineering-та-context-engineering)
5. [Модуль 4: Конфігурація AI-агентів — AGENTS.md, Rules, Skills](#модуль-4-конфігурація-ai-агентів--agentsmd-rules-skills)
6. [Модуль 5: Model Context Protocol (MCP) — протокол нового покоління](#модуль-5-model-context-protocol-mcp--протокол-нового-покоління)
7. [Модуль 6: Context7 та інші MCP-сервери для розробників](#модуль-6-context7-та-інші-mcp-сервери-для-розробників)
8. [Модуль 7: Smithery — маркетплейс MCP-інструментів](#модуль-7-smithery--маркетплейс-mcp-інструментів)
9. [Модуль 8: Методології розробки з AI](#модуль-8-методології-розробки-з-ai)
10. [Модуль 9: Spec-Driven Development (SDD)](#модуль-9-spec-driven-development-sdd)
11. [Модуль 10: AI + TDD — тестування з AI](#модуль-10-ai--tdd--тестування-з-ai)
12. [Модуль 11: Агентна розробка (Agentic Development)](#модуль-11-агентна-розробка-agentic-development)
13. [Модуль 12: RAG — Retrieval-Augmented Generation](#модуль-12-rag--retrieval-augmented-generation)
14. [Модуль 13: AI у DevOps та CI/CD](#модуль-13-ai-у-devops-та-cicd)
15. [Модуль 14: Безпека, етика та обмеження AI в розробці](#модуль-14-безпека-етика-та-обмеження-ai-в-розробці)
16. [Модуль 15: Побудова AI-powered робочого процесу з нуля](#модуль-15-побудова-ai-powered-робочого-процесу-з-нуля)
17. [Модуль 16: Фреймворки для побудови AI-агентів](#модуль-16-фреймворки-для-побудови-ai-агентів)
18. [Модуль 17: Майбутнє AI в розробці — куди рухається індустрія](#модуль-17-майбутнє-ai-в-розробці--куди-рухається-індустрія)

---

## Модуль 0: Фундамент — Що таке LLM і як вони працюють

### 🎯 Мета модуля

Зрозуміти базову архітектуру Large Language Models, щоб усвідомлено взаємодіяти з AI-інструментами, а не «магічно».

### 📚 Теми

#### 0.1. Що таке Large Language Model (LLM)

- Архітектура Transformer (Attention Is All You Need)
- Токенізація: як текст перетворюється на числа (BPE, SentencePiece)
- Контекстне вікно (context window): чому розмір має значення
- Temperature, top-p, top-k — параметри генерації
- Різниця між base model та instruction-tuned / RLHF-моделями

#### 0.2. Як LLM «думає» при генерації коду

- Autoregressive generation — передбачення наступного токена
- Чому LLM може «галюцинувати» — генерувати правдоподібний, але неправильний код
- Attention mechanism і чому контекст на початку/в кінці промпту «важливіший»
- Кеш KV (Key-Value Cache) та його вплив на продуктивність

#### 0.3. Reasoning-моделі нового покоління

- Що таке «reasoning» / «thinking» моделі (o1, Claude Opus, Gemini Deep Think)
- Chain-of-Thought всередині моделі vs зовнішній CoT
- Коли reasoning-моделі потрібні, а коли зайві (і навіть шкідливі)

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має виконати наступне дослідження для отримання актуальної інформації:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "openai" → `query-docs` "tokenizer tiktoken encoding"
> 2. `resolve-library-id` для "anthropic" → `query-docs` "claude model card specifications"
> 3. `resolve-library-id` для "google gemini" → `query-docs` "model architecture context window"
>
> **Web Search запити:**
>
> - "transformer architecture attention mechanism latest research 2026"
> - "LLM reasoning models comparison o1 claude opus gemini 2026"
> - "context window size impact LLM performance 2026"
>
> **Вимога:** Результати дослідження мають бути інтегровані безпосередньо в текст модуля як актуальні факти, приклади та посилання. Не покладатись лише на тренувальні дані.

### 📖 Ресурси

- [Attention Is All You Need (оригінальна стаття)](https://arxiv.org/abs/1706.03762)
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [Anthropic Model Cards](https://docs.anthropic.com/en/docs/about-claude/models)
- [Google AI — Gemini Overview](https://ai.google.dev/gemini-api/docs)

---

## Модуль 1: Ландшафт AI-моделей для розробки

### 🎯 Мета модуля

Знати всі ключові AI-моделі, їхні сильні/слабкі сторони, та навчитися вибирати правильну модель для конкретної задачі.

### 📚 Теми

#### 1.1. Сімейства моделей (станом на 2026)

| Сімейство       | Флагман                        | Сильні сторони                                                  | Контекст            |
| --------------- | ------------------------------ | --------------------------------------------------------------- | ------------------- |
| **Anthropic**   | Claude Fable 5 / Opus 4.8      | Глибоке планування, довгі агентні сесії, складна логіка         | до 200K токенів     |
| **OpenAI**      | GPT-5.6 Sol / GPT-5.5          | Універсальне reasoning, термінальні агенти, аналітика           | до 128K токенів     |
| **Google**      | Gemini 3.1 Pro                 | Найкраща ціна/якість, мультимодальність, ультра-довгий контекст | до 1M+ токенів      |
| **Open-source** | Llama 4, Qwen 3, Mistral Large | Локальний запуск, кастомізація, конфіденційність                | залежить від моделі |

#### 1.2. Стратегія вибору моделі: «Routing» замість «One Model»

- **Планування та архітектура** → найпотужніша reasoning-модель (Claude Fable 5 / GPT-5.6 Sol)
- **Виконання та генерація коду** → cost-effective «робоча конячка» (Claude Sonnet 4.6 / GPT-5.5)
- **Code Review** → незалежна модель для перевірки коду на баги та вразливості
- **Швидкий autocomplete** → легкі моделі (Codestral, Supermaven, GPT-4o mini)

#### 1.3. Бенчмарки та як їх читати

- SWE-bench Verified/Pro — золотий стандарт для реальної інженерії
- Terminal-Bench 2.0 — для агентних задач
- LiveCodeBench — задачі з реального часу
- Coding Arenas (сліпе голосування) — «як відчувається» модель у щоденній роботі
- Чому HumanEval більше не актуальний (насичення бенчмарку)

#### 1.4. Open-source vs Proprietary

- Коли використовувати відкриті моделі (конфіденційність, кастомізація, fine-tuning)
- Коли використовувати комерційні моделі (якість на frontier, підтримка, SLA)
- Інструменти для локального запуску: Ollama, vLLM, LM Studio

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "anthropic" → `query-docs` "Claude model comparison coding benchmarks"
> 2. `resolve-library-id` для "openai" → `query-docs` "GPT model capabilities coding features"
> 3. `resolve-library-id` для "google gemini" → `query-docs` "Gemini Pro coding features pricing"
>
> **Web Search запити:**
>
> - "AI models comparison coding 2026 Claude GPT Gemini benchmarks"
> - "SWE-bench leaderboard latest results 2026"
> - "open source LLM coding comparison Llama Qwen Mistral 2026"
> - "AI model routing strategy coding task-based selection"
>
> **Вимога:** Автор має знайти актуальні назви моделей, бенчмарки та порівняльні дані. Таблиці порівняння мають базуватися на реальних дослідженнях, а не на припущеннях. Створити практичне завдання для читача на порівняння моделей.

### 📖 Ресурси

- [Anthropic Claude Models](https://docs.anthropic.com/en/docs/about-claude/models)
- [OpenAI Models](https://platform.openai.com/docs/models)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [SWE-bench Leaderboard](https://www.swebench.com/)
- [Ollama](https://ollama.com/)

---

## Модуль 2: AI-асистенти та IDE — інструменти розробника

### 🎯 Мета модуля

Детально вивчити всі основні AI-інструменти для розробників, зрозуміти їхню філософію та навчитися обирати правильний інструмент під задачу.

### 📚 Теми

#### 2.1. Класифікація AI-інструментів для розробників

```
┌─────────────────────────────────────────────────────────────────┐
│                   AI-інструменти розробника                     │
├─────────────────┬────────────────────┬──────────────────────────┤
│ AI App Builders │  AI-Native IDE     │  Terminal-based Agents   │
│                 │                    │                          │
│ • Lovable       │ • Cursor           │ • Claude Code            │
│ • Bolt.new      │ • Windsurf         │ • Aider                  │
│ • v0            │ • Kiro (AWS)       │ • Codex (OpenAI)         │
│ • Replit Agent  │ • Zed              │ • Gemini CLI             │
│                 │ • GitHub Copilot   │                          │
│                 │   (Workspace)      │                          │
├─────────────────┼────────────────────┼──────────────────────────┤
│ Прототипування  │ Щоденна розробка   │ Складний рефакторинг     │
│ MVP             │ Парне програмув.   │ Автономне вирішення      │
│ Швидкий старт   │ Глибока інтеграція │ CI/CD інтеграція         │
└─────────────────┴────────────────────┴──────────────────────────┘
```

#### 2.2. Cursor — професійний стандарт

- Форк VS Code, перебудований для AI
- **Composer** — мульти-файлові зміни з гранулярним контролем
- **Tab autocomplete** — предиктивне автодоповнення
- **Chat + @-mentions** — контекстне спілкування з кодом
- `.cursor/rules/*.mdc` — умовні правила для проєкту
- Вибір моделі (Claude, GPT, Gemini) всередині одного IDE
- **Cursor Agent** — агентний режим для автономних задач

#### 2.3. Windsurf (Codeium) — агентний суперник

- **Cascade** — технологія проактивного аналізу контексту
- **Plan Mode** — автономне планування мульти-крокових задач
- RAG-based context retrieval — автоматичний пошук контексту
- Чому Windsurf кращий за Cursor при роботі з великими кодовими базами
- Коли обрати Windsurf замість Cursor

#### 2.4. Claude Code — термінальний агент від Anthropic

- Філософія: «junior інженер» у вашому терміналі
- Глибоке reasoning для складних архітектурних задач
- Автономне виконання команд, читання кодової бази, створення PR
- `CLAUDE.md` — конфігурація поведінки
- **Sub-agents** — делегування підзадач
- **GitHub інтеграція** — автоматичне створення PR та issues
- Slash-команди: `/goal`, `/learn`, `/schedule`

#### 2.5. GitHub Copilot — екосистемний гравець

- Інтеграція у будь-яке IDE (VS Code, JetBrains, Neovim, Xcode)
- **Copilot Workspace** — агентний режим в GitHub
- **Copilot Chat** — контекстний чат
- Найменш «дизруптивний» інструмент — не вимагає зміни IDE
- Enterprise-рівень: SOC 2, SSO, audit logs

#### 2.6. Kiro (AWS) — spec-driven IDE

- Три фази: Requirements → Design → Tasks
- EARS notation для формалізації вимог
- Agent Hooks та Steering files
- Інтеграція з AWS сервісами
- Паралельне виконання незалежних задач

#### 2.7. Інші інструменти, які варто знати

- **Zed** — високопродуктивний IDE з AI інтеграцією
- **Aider** — open-source термінальний асистент (Git-native)
- **Continue** — open-source AI-автодоповнення для VS Code/JetBrains
- **Cody (Sourcegraph)** — AI з глибоким розумінням кодових баз
- **Tabnine** — enterprise-рішення з підтримкою приватних моделей
- **Gemini Code Assist (Google)** — AI для Google Cloud розробників
- **JetBrains Junie** — вбудований AI у JetBrains IDE

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "cursor" → `query-docs` "cursor rules configuration agent mode"
> 2. `resolve-library-id` для "anthropic claude code" → `query-docs` "CLAUDE.md configuration sub-agents"
> 3. `resolve-library-id` для "github copilot" → `query-docs` "copilot workspace agent features"
> 4. `resolve-library-id` для "aider" → `query-docs` "aider git integration workflow"
> 5. `resolve-library-id` для "windsurf codeium" → `query-docs` "cascade plan mode features"
>
> **Web Search запити:**
>
> - "Cursor vs Windsurf vs Claude Code comparison 2026"
> - "Kiro IDE AWS spec-driven development features 2026"
> - "best AI coding assistant 2026 developer survey"
> - "Zed editor AI integration features 2026"
> - "JetBrains Junie AI assistant features 2026"
>
> **Вимога:** Для кожного інструмента автор має знайти актуальні функції, ціни, обмеження та відгуки. Порівняльна таблиця має базуватися на реальних даних. Створити практичне завдання для читача.

### 📖 Ресурси

- [Cursor Documentation](https://docs.cursor.com/)
- [Windsurf Documentation](https://docs.codeium.com/windsurf/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- [Kiro Documentation](https://kiro.dev/docs)
- [Aider Documentation](https://aider.chat/)

---

## Модуль 3: Prompt Engineering та Context Engineering

### 🎯 Мета модуля

Перейти від «наівного промптінгу» до системного підходу Context Engineering — управління повним контекстом взаємодії з AI.

### 📚 Теми

#### 3.1. Еволюція: від Prompt Engineering до Context Engineering

- **2023:** Prompt Engineering — «магічні слова» для кращих відповідей
- **2024:** Structured Prompting — шаблони, ролі, обмеження
- **2026:** Context Engineering — управління всім, що потрапляє в контекстне вікно

> **Аналогія:** LLM — це CPU, контекстне вікно — це RAM, а ви — операційна система, яка ефективно завантажує лише потрібний код, стан та інструкції у цю пам'ять.

#### 3.2. Техніки промптінгу для розробників

##### Zero-shot Prompting

```
Напиши функцію на Python, яка валідує email-адресу за допомогою regex.
```

##### Few-shot Prompting

```
Ось приклади валідних та невалідних email:
<example>
  <input>user@domain.com</input>
  <output>valid</output>
</example>
<example>
  <input>user@.com</input>
  <output>invalid</output>
</example>

Напиши функцію валідації, яка обробляє подібні випадки.
```

##### Chain-of-Thought (CoT)

```
Проаналізуй цю функцію крок за кроком:
1. Визнач, які вхідні дані вона приймає
2. Прослідкуй потік виконання для кожного edge case
3. Визнач потенційні баги
4. Запропонуй виправлення з поясненням
```

##### Self-Consistency

- Генерація кількох reasoning-шляхів для однієї задачі
- Вибір найконсистентнішої відповіді
- Зменшення галюцинацій для критичного коду

##### Meta-Prompting

- Використання LLM для оптимізації власних промптів
- Automated prompt testing (Promptfoo, Braintrust)

#### 3.3. Структурні елементи промпту

```xml
<!-- Структура ефективного промпту для розробки -->
<system>
  Ти — Senior Python розробник з досвідом у FastAPI та PostgreSQL.
  Дотримуйся PEP 8. Використовуй type hints завжди.
  Не використовуй глобальні змінні.
</system>

<context>
  Проєкт: REST API для управління бібліотекою
  Стек: FastAPI 0.115, SQLAlchemy 2.0, PostgreSQL 16
  Архітектура: Layered (Router → Service → Repository → Model)
</context>

<task>
  Створи endpoint POST /api/v1/books для додавання книги.
  Включи: валідацію через Pydantic, обробку помилок, unit test.
</task>

<constraints>
  - Відповідай лише валідним JSON якщо потрібен вивід
  - Максимум 100 рядків на файл
  - Використовуй async/await
</constraints>

<output_format>
  Надай відповідь у форматі:
  1. Файл моделі (model.py)
  2. Файл сервісу (service.py)
  3. Файл роутера (router.py)
  4. Тест (test_books.py)
</output_format>
```

#### 3.4. Delimiter-и та розмітка

- XML-теги (`<example>`, `<input>`, `<output>`) — найефективніший спосіб
- Markdown заголовки (`### Instruction`, `### Context`)
- Triple backticks для коду
- Чому роздільники обов'язкові для запобігання «змішування» інструкцій із даними

#### 3.5. Constraint-Based Prompting

- **Погано:** «Будь лаконічним»
- **Добре:** «Відповідь має бути менше 100 слів» або «Поверни лише валідний JSON»
- Вимірювані обмеження завжди краще за абстрактні

#### 3.6. Оптимізація контексту

- Статичні інструкції → на початку контексту (для кеш-ефективності)
- Змінні дані (код, запити) → в кінці контексту
- Не перевантажувати контекст — використовувати retrieval або summarization
- **Prompt caching** — як працює і чому економить гроші

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "anthropic" → `query-docs` "prompt engineering best practices system prompt"
> 2. `resolve-library-id` для "openai" → `query-docs` "prompt engineering guide structured output JSON"
> 3. `resolve-library-id` для "langchain" → `query-docs` "prompt template chain of thought few-shot"
>
> **Web Search запити:**
>
> - "context engineering vs prompt engineering 2026 differences"
> - "Promptfoo automated prompt testing setup tutorial 2026"
> - "Braintrust AI evaluation framework prompt testing"
> - "prompt caching Claude OpenAI Gemini how it works 2026"
> - "XML tags vs markdown delimiters prompting effectiveness"
>
> **Вимога:** Автор має знайти актуальні рекомендації від кожного провайдера (Anthropic, OpenAI, Google) та включити реальні приклади промптів для розробників. Включити інформацію про інструменти тестування промптів.

### 📖 Ресурси

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google AI Prompting Guide](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Promptfoo](https://promptfoo.dev/)
- [Braintrust](https://braintrust.dev/)

---

## Модуль 4: Конфігурація AI-агентів — AGENTS.md, Rules, Skills

### 🎯 Мета модуля

Навчитися створювати «операційну систему» для AI-агентів у ваших проєктах: правила, скіли, та конфігурацію, яка забезпечує консистентну роботу AI.

### 📚 Теми

#### 4.1. AGENTS.md — «README для машин»

`AGENTS.md` — це індустріальний стандарт (відкритий формат) для надання персистентного контексту AI-агентам. Це файл у корені репозиторію, який читається автоматично.

**Що включати:**

```markdown
# AGENTS.md

## Project Overview

Бібліотечний API на FastAPI з PostgreSQL.

## Setup

- `pip install -r requirements.txt`
- `docker-compose up -d` для бази даних
- `uvicorn main:app --reload` для dev-сервера

## Architecture

- Layered: Router → Service → Repository → Model
- Кожен endpoint в окремому файлі роутера
- Business logic лише в Service layer

## Coding Standards

- Python 3.12+, PEP 8, type hints обов'язкові
- Async/await для всіх DB операцій
- Pydantic v2 для валідації
- Alembic для міграцій

## Testing

- pytest + pytest-asyncio
- Мінімальне покриття: 80%
- Команда: `pytest tests/ -v --cov=app`

## Rules

- НІКОЛИ не хардкодьте секрети — використовуйте .env
- Не створюйте god-objects — максимум 200 рядків на клас
- Кожна зміна в DB — через міграцію Alembic
```

**Кращі практики:**

- Тримайте файл < 150-200 чітких інструкцій (уникайте «instruction bloat»)
- Оновлюйте разом із кодовою базою
- Тестуйте правила: запитайте агента про щось, що має тригерити правило

#### 4.2. Інструмент-специфічні конфігурації

##### Cursor: `.cursor/rules/*.mdc`

```yaml
# .cursor/rules/api-endpoints.mdc
---
description: 'Rules for API endpoint development'
globs: ['app/routers/**/*.py']
---
- Кожен роутер має приймати Service через Depends()
- Використовуй HTTPException для помилок, не raise напряму
- Кожен endpoint має docstring з OpenAPI description
```

**Потужність:** Правила Cursor — умовні. Вони активуються лише при роботі з файлами, що відповідають `globs` або `description`.

##### Claude Code: `CLAUDE.md`

```markdown
# CLAUDE.md

## Обов'язкові правила

- Перед будь-якою нетривіальною зміною: спочатку PLAN.md
- Після кожної зміни: запусти тести `pytest tests/ -v`
- Комітай часто та з описовими повідомленнями
- Використовуй sub-agents для паралельних задач
```

**Pro tip:** Симлінк для уніфікації: `ln -s AGENTS.md CLAUDE.md`

##### Gemini: `.gemini/` та AGENTS.md

- Gemini ефективно працює з AGENTS.md для project-level persistence
- Підтримує Skills — папки зі спеціалізованими інструкціями
- Конфігурація через `.gemini/config/` для глобальних правил

#### 4.3. Skills — модульне розширення можливостей AI

**Skills** — це папки з інструкціями, скриптами та ресурсами, які розширюють можливості AI для спеціалізованих задач.

**Структура скіла:**

```
.agents/skills/
├── database-migration/
│   ├── SKILL.md           # Головні інструкції (YAML frontmatter + Markdown)
│   ├── scripts/           # Допоміжні скрипти
│   │   └── generate_migration.sh
│   ├── examples/          # Приклади використання
│   │   └── example_migration.py
│   ├── resources/         # Додаткові файли, шаблони
│   │   └── migration_template.mako
│   └── references/        # Додаткова документація
│       └── alembic_patterns.md
```

**SKILL.md формат:**

```yaml
---
name: "Database Migration"
description: "Створення та управління міграціями бази даних через Alembic"
---

## Інструкції

Коли потрібно створити міграцію:
1. Проаналізуй зміни в моделях (app/models/)
2. Запусти `alembic revision --autogenerate -m "опис"`
3. Перевір згенеровану міграцію вручну
4. Запусти `alembic upgrade head` для застосування
5. Перевір, що тести проходять

## Правила
- Ніколи не видаляй колонки без explicit підтвердження
- Завжди додавай downgrade
- Використовуй batch operations для SQLite
```

#### 4.4. Ієрархія контексту

```
Пріоритет (від найвищого до найнижчого):
┌──────────────────────────────┐
│ 1. Inline коментарі/директиви│  ← Файл-рівень
├──────────────────────────────┤
│ 2. Поточний чат/сесія        │  ← Сесія-рівень
├──────────────────────────────┤
│ 3. .cursor/rules/ або Skills │  ← Умовний контекст
├──────────────────────────────┤
│ 4. AGENTS.md / CLAUDE.md     │  ← Проєкт-рівень
├──────────────────────────────┤
│ 5. Глобальні правила         │  ← Користувач-рівень
└──────────────────────────────┘
```

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "cursor" → `query-docs` "cursor rules mdc configuration globs"
> 2. `resolve-library-id` для "anthropic claude code" → `query-docs` "CLAUDE.md project configuration best practices"
>
> **Web Search запити:**
>
> - "AGENTS.md specification standard format 2026"
> - "AGENTS.md vs CLAUDE.md vs cursor rules comparison"
> - "cursor rules mdc examples real world projects github"
> - "AI coding skills custom instructions templates examples"
> - "instruction bloat AI rules best practices limit"
>
> **Вимога:** Автор має знайти реальні приклади AGENTS.md з відкритих репозиторіїв, актуальний формат .mdc правил Cursor, та приклади Skills. Включити практичне завдання для читача.

---

## Модуль 5: Model Context Protocol (MCP) — протокол нового покоління

### 🎯 Мета модуля

Глибоко зрозуміти MCP — відкритий стандарт для з'єднання AI-агентів із зовнішніми даними, інструментами та системами.

### 📚 Теми

#### 5.1. Проблема, яку вирішує MCP

**До MCP (NxM проблема):**

```
Кожна AI-модель ←→ Кожен інструмент = N×M інтеграцій

Claude ←→ GitHub (кастомний код)
Claude ←→ Slack (кастомний код)
Claude ←→ PostgreSQL (кастомний код)
GPT ←→ GitHub (ІНШИЙ кастомний код)
GPT ←→ Slack (ІНШИЙ кастомний код)
...
```

**З MCP (стандартизація):**

```
Будь-який MCP Client ←→ Будь-який MCP Server (єдиний протокол)

Claude ─┐                 ┌─ GitHub MCP Server
GPT    ─┤ ← MCP Protocol → ├─ Slack MCP Server
Gemini ─┘                 └─ PostgreSQL MCP Server
```

> **Аналогія:** MCP — це як USB для AI. До USB кожен пристрій мав свій роз'єм. MCP стандартизує «підключення» AI до будь-якого інструменту.

#### 5.2. Архітектура MCP

```
┌──────────────────────────────────────────────────────────────────┐
│                        MCP Architecture                          │
│                                                                  │
│  ┌──────────┐     ┌────────────────┐     ┌──────────────────┐   │
│  │  Host     │     │  MCP Client    │     │  MCP Server      │   │
│  │ (IDE,     │────→│  (SDK-based    │←──→│  (provides       │   │
│  │  Desktop) │     │   connector)   │     │   tools/data)    │   │
│  └──────────┘     └────────────────┘     └──────────────────┘   │
│                                                                  │
│  Примери Hosts:    Примери Clients:      Примери Servers:        │
│  - Claude Desktop  - Вбудований у IDE    - GitHub Server         │
│  - Cursor          - Anthropic SDK       - PostgreSQL Server     │
│  - VS Code         - OpenAI SDK          - Filesystem Server     │
│  - Windsurf        - Google ADK          - Slack Server          │
│  - CLI agents      - Custom client       - Custom server         │
└──────────────────────────────────────────────────────────────────┘
```

#### 5.3. Три стовпи MCP: Tools, Resources, Prompts

##### Tools — виконуючі функції

```json
{
    "name": "create_github_issue",
    "description": "Створює нову issue в GitHub репозиторії",
    "inputSchema": {
        "type": "object",
        "properties": {
            "repo": { "type": "string" },
            "title": { "type": "string" },
            "body": { "type": "string" }
        },
        "required": ["repo", "title"]
    }
}
```

##### Resources — джерела даних

```json
{
    "uri": "postgres://localhost/mydb",
    "name": "Production Database",
    "description": "Read-only access to application database",
    "mimeType": "application/sql"
}
```

##### Prompts — шаблони взаємодії

```json
{
    "name": "code_review",
    "description": "Шаблон для code review з фокусом на безпеку",
    "arguments": [
        { "name": "code", "required": true },
        { "name": "language", "required": true }
    ]
}
```

#### 5.4. Нові примітиви MCP 2026

| Примітив     | Опис                                              | Статус           |
| ------------ | ------------------------------------------------- | ---------------- |
| **Tasks**    | Довготривалі автономні роботи                     | RC (липень 2026) |
| **Triggers** | Webhook-подібні сповіщення від сервера до клієнта | RC               |
| **Apps**     | Server-rendered UI                                | RC               |
| **Skills**   | Пакети domain-specific знань для серверів         | В розробці       |

#### 5.5. Stateless Architecture (2026)

- Перехід від persistent sessions до stateless core
- Працює на стандартній HTTP інфраструктурі
- Покращена масштабованість для enterprise
- Enhanced Authorization: OAuth + OpenID Connect

#### 5.6. SDK та мови програмування

- **Офіційні:** TypeScript, Python, Java, Kotlin, C#
- **Комʼюніті:** Go, PHP, Ruby, Rust, Swift
- SDK v2 — покращений DX та продуктивність

#### 5.7. Практика: Створення власного MCP Server

```python
# Приклад простого MCP Server на Python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-project-tools")

@server.tool("get_project_stats")
async def get_project_stats(path: str) -> list[TextContent]:
    """Отримує статистику проєкту: кількість файлів, рядків коду, тощо."""
    import os
    file_count = sum(1 for _, _, files in os.walk(path) for f in files)
    return [TextContent(
        type="text",
        text=f"Проєкт містить {file_count} файлів"
    )]

@server.tool("run_tests")
async def run_tests(test_path: str = "tests/") -> list[TextContent]:
    """Запускає тести та повертає результат."""
    import subprocess
    result = subprocess.run(
        ["pytest", test_path, "-v", "--tb=short"],
        capture_output=True, text=True
    )
    return [TextContent(type="text", text=result.stdout + result.stderr)]
```

#### 5.8. MCP Inspector — інструмент дебагу

- Тестування MCP серверів
- Перегляд доступних tools/resources/prompts
- Симуляція запитів від клієнта

#### 5.9. Безпека MCP

- Human-in-the-loop для чутливих tool invocations
- Scoping через «Roots» для обмеження доступу до файлової системи
- Supply chain ризик: обережно з неверифікованими реєстрами
- OAuth/OIDC для enterprise identity management

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "modelcontextprotocol" → `query-docs` "MCP specification tools resources prompts primitives"
> 2. `resolve-library-id` для "mcp python sdk" → `query-docs` "creating MCP server Python tutorial tools"
> 3. `resolve-library-id` для "mcp typescript sdk" → `query-docs` "MCP client server implementation SDK v2"
>
> **Web Search запити:**
>
> - "Model Context Protocol specification stateless July 2026"
> - "MCP new primitives Tasks Triggers Apps 2026"
> - "MCP Inspector tutorial debugging setup"
> - "MCP OAuth OpenID Connect authorization enterprise 2026"
> - "MCP server examples GitHub popular 2026"
> - "Agentic AI Foundation Linux Foundation MCP governance"
>
> **Вимога:** Автор має знайти АКТУАЛЬНУ специфікацію MCP (не застарілу), перевірити нові примітиви (Tasks, Triggers, Apps), та включити робочий приклад створення MCP Server. Включити практичне завдання для читача.

### 📖 Ресурси

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol/modelcontextprotocol)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Agentic AI Foundation (Linux Foundation)](https://agenticai.foundation/)

---

## Модуль 6: Context7 та інші MCP-сервери для розробників

### 🎯 Мета модуля

Навчитися використовувати Context7 та інші MCP-сервери для автоматичного постачання AI-агентів актуальною документацією та даними.

### 📚 Теми

#### 6.1. Context7 — документація бібліотек для AI

**Проблема:** AI-моделі навчені на «замороженому» знімку даних. Якщо ви використовуєте FastAPI 0.115, а модель навчена на FastAPI 0.100, вона генеруватиме неправильний код.

**Рішення:** Context7 — MCP-сервер, який надає AI-агенту on-demand доступ до актуальної, version-specific документації бібліотек.

**Як це працює:**

```
1. AI-агент → запит до Context7 MCP: "Як зробити WebSocket endpoint у FastAPI 0.115?"
2. Context7 → шукає в своїй базі останню документацію FastAPI 0.115
3. Context7 → повертає релевантні сніпети документації
4. AI-агент → генерує код на основі АКТУАЛЬНОЇ документації
```

**Ключові інструменти Context7:**

- `resolve-library-id` — знаходить ID бібліотеки в реєстрі Context7
- `query-docs` — виконує пошук по документації конкретної бібліотеки

**Налаштування:**

```json
// claude_desktop_config.json або аналог для іншого IDE
{
    "mcpServers": {
        "context7": {
            "command": "npx",
            "args": ["-y", "@context7/mcp-server"]
        }
    }
}
```

#### 6.2. Популярні MCP-сервери для розробників

| MCP Server            | Призначення             | Типове використання             |
| --------------------- | ----------------------- | ------------------------------- |
| **Context7**          | Документація бібліотек  | Актуальний API, версійність     |
| **GitHub MCP**        | Репозиторії, Issues, PR | Управління проєктами через AI   |
| **PostgreSQL MCP**    | Бази даних              | Аналіз даних, генерація запитів |
| **Filesystem MCP**    | Локальні файли          | Читання/запис файлів проєкту    |
| **Slack/Discord MCP** | Месенджери              | Автоматизація сповіщень         |
| **Docker MCP**        | Контейнери              | Управління контейнерами         |
| **Sentry MCP**        | Моніторинг              | Аналіз помилок, дебаг           |
| **Figma MCP**         | Дизайн                  | Витягування стилів, компонентів |
| **Linear/Jira MCP**   | Трекери задач           | Управління задачами через AI    |
| **Brave Search MCP**  | Пошук                   | Веб-пошук з AI-агента           |

#### 6.3. Побудова «контекстного стеку» для проєкту

```json
// Приклад конфігурації MCP для повноцінного проєкту
{
    "mcpServers": {
        "context7": {
            "command": "npx",
            "args": ["-y", "@context7/mcp-server"]
        },
        "github": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
        },
        "postgres": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres"],
            "env": { "DATABASE_URL": "${DATABASE_URL}" }
        },
        "filesystem": {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
        }
    }
}
```

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити (продемонструвати роботу Context7 на прикладах):**
>
> 1. `resolve-library-id` для "fastapi" → `query-docs` "websocket endpoint middleware CORS"
> 2. `resolve-library-id` для "react" → `query-docs` "server components hooks useEffect"
> 3. `resolve-library-id` для "nextjs" → `query-docs` "app router server actions middleware"
> 4. `resolve-library-id` для "pydantic" → `query-docs` "model validation v2 features computed"
>
> **Web Search запити:**
>
> - "Context7 MCP setup tutorial Claude Code Cursor 2026"
> - "popular MCP servers list developers 2026"
> - "GitHub MCP server configuration tokens setup"
> - "PostgreSQL MCP server database queries AI"
>
> **Вимога:** Автор має продемонструвати реальну роботу Context7 — показати приклади запитів та відповідей. Таблиця MCP-серверів має базуватися на реальному реєстрі. Включити практичне завдання для читача з налаштування контекстного стеку.

---

## Модуль 7: Smithery — маркетплейс MCP-інструментів

### 🎯 Мета модуля

Навчитися знаходити, встановлювати та керувати MCP-серверами через Smithery — центральний реєстр для MCP-екосистеми.

### 📚 Теми

#### 7.1. Що таке Smithery

- Центральний маркетплейс/реєстр для MCP-серверів
- Пошук серед тисяч серверів за категоріями та тегами
- JSON-based schema для автоматичного виявлення tools/resources/prompts
- Локальний та хмарний хостинг серверів

#### 7.2. Smithery CLI

```bash
# Встановлення
npx -y @anthropic/smithery-cli

# Пошук серверів
smithery search "github"
smithery search "database"
smithery search "monitoring"

# Встановлення сервера
smithery install @modelcontextprotocol/server-github

# Перегляд встановлених серверів
smithery list

# Запуск сервера
smithery run @modelcontextprotocol/server-github
```

#### 7.3. Категорії серверів на Smithery

- **Development Tools:** GitHub, GitLab, Bitbucket, Linear, Jira
- **Databases:** PostgreSQL, MySQL, MongoDB, Redis, Supabase
- **Communication:** Slack, Discord, Email, Teams
- **Cloud:** AWS, GCP, Azure, Cloudflare
- **Monitoring:** Sentry, Datadog, New Relic
- **Design:** Figma, Framer
- **Documentation:** Context7, Notion, Confluence
- **Search:** Brave, Exa, Tavily

#### 7.4. Skill Sets на Smithery

- Високорівневі конфігурації для спеціалізованих задач
- Автоматизований frontend design
- PDF processing
- Складний data retrieval

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "Smithery MCP marketplace registry features 2026"
> - "Smithery CLI installation usage commands tutorial"
> - "best MCP servers web development 2026 top list"
> - "Smithery vs official MCP registry comparison"
>
> **Вимога:** Автор має знайти актуальну інформацію про Smithery CLI (команди, версії), категорії серверів, та включити робочі приклади використання. Створити практичне завдання для читача з пошуку та встановлення серверів.

### 📖 Ресурси

- [Smithery](https://smithery.ai/)
- [MCP Servers Registry](https://github.com/modelcontextprotocol/servers)

---

## Модуль 8: Методології розробки з AI

### 🎯 Мета модуля

Зрозуміти різні підходи до розробки з AI, їхні переваги/недоліки, та навчитися обирати правильний підхід під задачу.

### 📚 Теми

#### 8.1. Спектр підходів

```
←─── Швидкість                                    Контроль ───→

┌────────────┬───────────────┬──────────────┬─────────────────┐
│ Vibe       │ Prompt-       │ Spec-        │ Formal          │
│ Coding     │ Driven Dev    │ Driven Dev   │ Verification    │
│            │               │              │                 │
│ "Просто    │ "Дай мені     │ "Спочатку    │ "Математично    │
│  працює"   │  правильний   │  специфікація│  доведено"      │
│            │  результат"   │  потім код"  │                 │
├────────────┼───────────────┼──────────────┼─────────────────┤
│ Прототипи  │ Feature dev   │ Production   │ Safety-critical │
│ MVPs       │ Daily tasks   │ Enterprise   │ Finance/Medical │
│ Скрипти    │ Bug fixes     │ Teams        │ Infrastructure  │
└────────────┴───────────────┴──────────────┴─────────────────┘
```

#### 8.2. Vibe Coding — «Code by Vibes»

- **Що це:** Розробка через вільні промпти до AI, без формальних специфікацій
- **Коли використовувати:**
    - Прототипування та MVP
    - Одноразові скрипти
    - Навчання новій технології
    - Хакатони
- **Ризики:**
    - «Три-місячна стіна» — технічний борг стає непідʼємним
    - Context decay — AI забуває контекст між сесіями
    - Архітектурна інконсистентність
    - Silent failures — код працює, але порушує бізнес-логіку
- **Як мінімізувати ризики:**
    - Часті коміти (Git як «save points»)
    - Обов'язковий code review
    - Мінімальні тести для критичних шляхів

#### 8.3. Prompt-Driven Development

- Структуровані промпти з чіткими обмеженнями
- Використання AGENTS.md та rules
- Ітеративний підхід: промпт → код → ревʼю → уточнення
- Підходить для щоденної розробки в середніх проєктах

#### 8.4. AI Pair Programming — ефективне парне програмування з AI

**Золоті правила:**

1. **Архітектуй першим, промптуй другим**
    - Визнач проблему → спроєктуй модулі → покроковий план → ПОТІМ промпт

2. **Мислення «Senior Developer»**
    - Ти — lead, AI — assistant
    - Не приймай код, який не можеш пояснити
    - Завжди review, test, validate

3. **Гранулярний version control**
    - Commit рано та часто
    - Кожен commit — це «save point» для відкату
    - AI генерує багато коду швидко → потрібен контроль

4. **Маленькі шматки (Small slices)**
    - Не просіть великих фіч одним промптом
    - Розбивайте на верифіковані чанки
    - Зменшує ризик галюцинацій

5. **Контекстне завантаження**
    - Використовуйте `@-mentions` для файлів/документів
    - MCP для автоматичного контексту
    - Без контексту AI-вивід генеричний та проне до помилок

6. **Multi-Agent Orchestration**
    - Один агент для планування
    - Інший для генерації тестів
    - Третій для рефакторингу

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "vibe coding definition risks technical debt three month wall 2026"
> - "AI pair programming best practices senior developer mindset 2026"
> - "structured vs unstructured AI development methodology comparison"
> - "multi agent orchestration coding workflow examples"
> - "prompt-driven development vs spec-driven comparison"
>
> **Вимога:** Автор має знайти реальні case studies та статистику про наслідки різних підходів. Включити конкретні приклади «трьох-місячної стіни» та способи її уникнення. Створити практичне завдання для читача.

---

## Модуль 9: Spec-Driven Development (SDD)

### 🎯 Мета модуля

Опанувати Spec-Driven Development — парадигму, де специфікація (а не код) є єдиним джерелом правди.

### 📚 Теми

#### 9.1. Чому SDD — це майбутнє

**Фундаментальний зсув:** AI генерує код за секунди. Bottleneck більше не в написанні коду, а у **визначенні, валідації та підтримці наміру (intent)**.

```
Традиційна розробка:     SDD:
Людина пише код      →   Людина пише специфікацію
Людина тестує код     →   AI генерує код
Людина підтримує код  →   AI тестує код проти специфікації
                          Людина підтримує специфікацію
```

#### 9.2. Принципи SDD

1. **«Що» замість «Як»**
    - Визначайте бажані результати, бізнес-логіку, обмеження
    - Залишайте деталі реалізації AI (в межах архітектурних guardrails)

2. **Людська зрозумілість**
    - Якщо специфікацію довго читати — вона liability
    - Модульність: кожна фіча — окрема специфікація

3. **Декомпозиція**
    - Уникайте монолітних специфікацій
    - Розбивайте на незалежно поставлені шматки

4. **Ітеративна еволюція**
    - Специфікація — living document
    - Оновлюється ПЕРЕД регенерацією коду

5. **Validation Gates**
    - Автоматичні перевірки якості між spec → impl → review
    - Валідуйте код проти spec, не проти «відчуттів»

#### 9.3. Рівні зрілості SDD

```
Рівень 1: Spec-First
├── Ad-hoc PRD + AI tool (Cursor, Copilot)
├── Специфікація існує, але не формалізована
└── Вручну перевіряється відповідність

Рівень 2: Spec-Anchored
├── Spec + код еволюціонують разом
├── Інструменти: GitHub Spec Kit, Kiro
└── Часткова автоматизація alignment

Рівень 3: Spec-as-Source
├── Люди редагують ЛИШЕ специфікацію
├── Код повністю генерується та регенерується
└── Інструменти: Tessl, OpenSpec

Рівень 4: Spec-to-Application
├── Специфікація як формальна модель/«геном»
├── Код emitted через детерміністичні компілятори
└── Без LLM на фінальному кроці
```

#### 9.4. Практичний SDD Workflow

##### Крок 1: Requirements (requirements.md)

```markdown
# Feature: Пошук книг за фільтрами

## User Story

Як користувач бібліотеки, я хочу шукати книги за назвою,
автором та жанром, щоб швидко знаходити потрібну літературу.

## Acceptance Criteria (EARS Notation)

- WHEN користувач вводить пошуковий запит довжиною >= 2 символи,
  THE система SHALL повертати результати протягом 500ms
- WHEN результатів більше 20,
  THE система SHALL пагінувати відповідь по 20 елементів
- IF пошуковий запит порожній,
  THEN THE система SHALL повертати HTTP 400 з описом помилки
- THE система SHALL підтримувати часткову відповідність (fuzzy search)

## Non-functional Requirements

- Час відповіді: < 500ms для 95-го перцентиля
- Повинно працювати з 1M+ записів у базі
```

##### Крок 2: Design (design.md)

```markdown
# Design: Пошук книг

## Architecture

- Endpoint: GET /api/v1/books/search
- Query params: q (required), genre (optional), page, per_page
- Full-text search через PostgreSQL tsvector

## Sequence Diagram

(mermaid діаграма)

## Data Flow

Request → Router → SearchService → SearchRepository → PostgreSQL (FTS)

## Considerations

- Індекс GIN на tsvector колонці
- Кешування популярних запитів через Redis (TTL: 5 хвилин)
```

##### Крок 3: Tasks (tasks.md)

```markdown
# Tasks

- [ ] Додати tsvector колонку до моделі Book
- [ ] Створити міграцію Alembic
- [ ] Реалізувати SearchRepository з FTS
- [ ] Реалізувати SearchService з кешуванням
- [ ] Створити endpoint GET /api/v1/books/search
- [ ] Написати unit тести для SearchService
- [ ] Написати integration тести для endpoint
- [ ] Провести навантажувальне тестування
```

#### 9.5. Інструменти для SDD

- **Kiro (AWS)** — IDE з вбудованим SDD workflow
- **GitHub Spec Kit** — GitHub-native spec management
- **Claude Code + PLAN.md** — lightweight SDD через markdown
- **Cursor + .cursor/rules/** — умовні правила для spec alignment

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "kiro" → `query-docs` "spec driven development workflow requirements design tasks EARS"
> 2. `resolve-library-id` для "github" → `query-docs` "GitHub Spec Kit specification management"
>
> **Web Search запити:**
>
> - "spec driven development tutorial step by step 2026"
> - "EARS notation Easy Approach Requirements Syntax examples"
> - "Kiro IDE spec workflow requirements design tasks tutorial"
> - "spec-driven development maturity model levels comparison"
> - "intent-driven development vs spec-driven 2026"
> - "GitHub Spec Kit features usage"
>
> **Вимога:** Автор має знайти актуальну інформацію про Kiro IDE workflow, EARS notation, та рівні зрілості SDD. Приклади requirements.md та design.md мають бути реалістичними. Створити практичне завдання для читача.

---

## Модуль 10: AI + TDD — тестування з AI

### 🎯 Мета модуля

Використовувати AI як потужний інструмент для Test-Driven Development: генерації, виконання та підтримки тестів.

### 📚 Теми

#### 10.1. Ренесанс TDD в епоху AI

**Парадокс:** TDD раніше вважалося «повільним». AI змінив економіку — тепер генерація тестів майже безкоштовна.

**Нова роль TDD:** Тести — це найефективніший «верифікаційний шар» для AI-генерованого коду. Визначаючи, що є «правильним» ПЕРЕД генерацією, ви захищаєте бізнес-логіку від «правдоподібного, але неправильного» коду.

#### 10.2. AI-Assisted TDD Workflow

```
1. 🤔 Розробник визначає BEHAVIOUR (що має робити код)
          ↓
2. 🤖 AI генерує ТЕСТИ на основі behaviour specification
          ↓
3. ❌ Тести FAIL (червоний — коду ще немає)
          ↓
4. 🤖 AI генерує IMPLEMENTATION (мінімальний код для проходження тестів)
          ↓
5. ✅ Тести PASS (зелений)
          ↓
6. 🤖 AI робить REFACTORING (покращення коду без зміни поведінки)
          ↓
7. ✅ Тести все ще PASS (підтвердження правильності рефакторингу)
```

#### 10.3. Типи тестів, які AI генерує ефективно

| Тип тесту         | AI-ефективність | Коментар                                                  |
| ----------------- | --------------- | --------------------------------------------------------- |
| Unit тести        | ⭐⭐⭐⭐⭐      | AI відмінно генерує unit-тести з edge cases               |
| Integration тести | ⭐⭐⭐⭐        | Потребує контексту про зовнішні системи                   |
| Property-based    | ⭐⭐⭐⭐        | AI добре визначає інваріанти                              |
| Snapshot тести    | ⭐⭐⭐          | Корисні для UI, але потребують ручної верифікації         |
| E2E тести         | ⭐⭐            | Потребує значного контексту та часто ручного налаштування |

#### 10.4. Промпти для генерації тестів

```markdown
## Prompt для генерації тестів

Проаналізуй функцію `search_books` у файлі `services/search.py`.

Створи набір тестів, який покриває:

1. Happy path — пошук з валідним запитом повертає результати
2. Edge cases:
    - Порожній запит → помилка
    - Запит < 2 символів → помилка
    - Запит з спецсимволами → коректна обробка
    - Результат = 0 книг → порожній список
3. Boundary conditions:
    - Рівно 20 результатів (гранична пагінація)
    - 21 результат (друга сторінка)
    - Максимально довгий запит (500 символів)
4. Error handling:
    - Database timeout → відповідний HTTP статус
    - Database connection error → graceful degradation

Використовуй pytest, pytest-asyncio, та httpx AsyncClient.
Мокай database через unittest.mock.AsyncMock.
```

#### 10.5. Self-healing тести

- AI автоматично оновлює тести при мінорних змінах UI/структури
- Тести ламаються лише при зміні ПОВЕДІНКИ (не стилю)
- Інструменти: Qodo (раніше CodiumAI), Testim, Katalon

#### 10.6. Mutation Testing з AI

- AI генерує «мутації» коду (навмисні баги)
- Перевірка, чи тести виявляють мутації
- Metric: mutation score = % виявлених мутацій

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "pytest" → `query-docs` "fixtures parametrize async testing mock"
> 2. `resolve-library-id` для "jest" → `query-docs` "mocking testing library async setup"
> 3. `resolve-library-id` для "vitest" → `query-docs` "testing setup configuration mocking"
>
> **Web Search запити:**
>
> - "AI TDD workflow test driven development 2026 tutorial best practices"
> - "Qodo CodiumAI test generation features 2026"
> - "mutation testing AI generated code tools 2026"
> - "self-healing tests AI automated maintenance tools"
> - "AI assisted TDD economics code verification 2026"
>
> **Вимога:** Автор має знайти актуальні інструменти для AI-TDD, приклади self-healing тестів, та конкретні дані про ефективність AI-генерованих тестів. Створити практичне завдання для читача.

---

## Модуль 11: Агентна розробка (Agentic Development)

### 🎯 Мета модуля

Зрозуміти концепцію AI-агентів у розробці: автономні системи, які планують, виконують та верифікують задачі з мінімальним втручанням людини.

### 📚 Теми

#### 11.1. Що таке AI-агент (на відміну від chatbot)

```
Chatbot:                          Agent:
┌────────────┐                    ┌────────────┐
│ User: prompt                    │ User: goal  │
│ AI: response                    │ AI: plan    │
│ User: next prompt               │ AI: execute │
│ AI: response                    │ AI: verify  │
│ ...                             │ AI: adjust  │
│ (людина керує)                  │ AI: report  │
└────────────┘                    │ (AI керує)  │
                                  └────────────┘
```

**Ключові характеристики агента:**

- **Автономність** — працює без постійного втручання
- **Планування** — розбиває задачу на кроки
- **Використання інструментів** — MCP, CLI, файлова система
- **Цикл зворотного зв'язку** — виконує, перевіряє, коригує
- **Довгострокова пам'ять** — зберігає контекст між сесіями

#### 11.2. Agentic Loops

```
        ┌──────────────────────────────────────┐
        │              PLAN                     │
        │  Розбий задачу на підзадачі          │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │              ACT                      │
        │  Виконай наступну підзадачу           │
        │  (edit file, run command, query DB)   │
        └──────────────┬───────────────────────┘
                       ↓
        ┌──────────────────────────────────────┐
        │            OBSERVE                    │
        │  Перевір результат                    │
        │  (run tests, check output, lint)     │
        └──────────────┬───────────────────────┘
                       ↓
                ┌──────────────┐
                │  Все ОК?     │──── Так → Звіт + Commit
                └──────┬───────┘
                       │ Ні
                       ↓
                  Повернись до PLAN
                  (скоригуй підхід)
```

#### 11.3. Multi-Agent Orchestration

```
┌─────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                        │
│            (координація, розподіл задач)                     │
├────────────────┬──────────────────┬─────────────────────────┤
│  Architect     │  Developer       │  Reviewer               │
│  Agent         │  Agent           │  Agent                  │
│                │                  │                         │
│  - Аналіз     │  - Генерація     │  - Code review          │
│    вимог       │    коду          │  - Security audit       │
│  - Дизайн     │  - Тести         │  - Performance check    │
│  - Planning   │  - Рефакторинг   │  - Compliance           │
└────────────────┴──────────────────┴─────────────────────────┘
```

#### 11.4. Human-in-the-Loop патерни

- **Approval gates** — AI зупиняється та чекає схвалення перед критичними діями
- **Review checkpoints** — регулярні точки ревʼю
- **Escalation** — AI розпізнає, коли не може вирішити задачу і запитує допомогу
- **Constraint enforcement** — жорсткі обмеження, які AI не може обійти

#### 11.5. Практичний приклад: Claude Code як агент

```bash
# Запуск Claude Code в агентному режимі
claude "Реалізуй фічу пошуку книг відповідно до spec у requirements.md.
Для кожного кроку:
1. Прочитай відповідну частину специфікації
2. Реалізуй код
3. Напиши та запусти тести
4. Закомітай зміни з описовим повідомленням
Зупинись та запитай, якщо щось неясно."
```

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "agentic development workflow plan act observe loop 2026"
> - "multi agent orchestration coding architect developer reviewer"
> - "Claude Code agent mode autonomous workflow examples 2026"
> - "human in the loop AI agent approval gates patterns"
> - "Cursor Agent vs Claude Code agentic comparison 2026"
>
> **Вимога:** Автор має знайти реальні приклади агентних workflow-ів, паттерни human-in-the-loop, та порівняння агентних режимів різних IDE. Створити практичне завдання для читача.

---

## Модуль 12: RAG — Retrieval-Augmented Generation

### 🎯 Мета модуля

Зрозуміти RAG як архітектурний патерн для «заземлення» AI на ваших даних, та навчитися використовувати його для покращення роботи AI-асистентів.

### 📚 Теми

#### 12.1. Чому RAG необхідний

- LLM навчені на «замороженому» знімку даних
- Ваш проєкт, ваша документація, ваші бізнес-правила — не в training data
- RAG = «дай AI прочитати потрібні документи перед відповіддю»

#### 12.2. Архітектура Production-Ready RAG (2026)

```
┌────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                             │
│                                                            │
│  Query ──→ [Query Rewriting] ──→ [Hybrid Search] ──→      │
│            (перефразування      (Vector + BM25              │
│             для кращого          + Metadata Filters)        │
│             retrieval)                                      │
│                                           ↓                 │
│           [Re-ranking] ←──────────────────┘                │
│           (Cross-encoder scoring,                           │
│            вибір top-K чанків)                               │
│                    ↓                                        │
│           [LLM Generation]                                  │
│           (Відповідь на основі                              │
│            retrieved контексту)                              │
│                    ↓                                        │
│           [Response + Citations]                            │
└────────────────────────────────────────────────────────────┘
```

#### 12.3. Ключові компоненти

##### Chunking — розбиття документів

- **Fixed-size:** 512-1024 токенів (простий, але грубий)
- **Semantic:** розбиття за смислом/темою (кращий для docs)
- **Hierarchical:** зберігає зв'язки (function ↔ imports ↔ module)
- **Для коду:** зберігайте import-и та function signatures разом

##### Embedding — векторне представлення

- text-embedding-3-large (OpenAI)
- Gecko (Google)
- Voyage Code (спеціалізований для коду)

##### Hybrid Search — комбінований пошук

- Dense vector search (семантична подібність)
- Sparse keyword search (BM25 — точна відповідність)
- Reciprocal Rank Fusion (RRF) для злиття результатів

##### Re-ranking — переранжування

- Cross-encoder моделі (Cohere Rerank, BGE Reranker)
- Найвигідніша інвестиція в якість RAG

#### 12.4. Vector Databases

| Database     | Найкраще для                            | Компроміси                                          |
| ------------ | --------------------------------------- | --------------------------------------------------- |
| **pgvector** | Існуючий SQL стек, < 100M векторів      | Просте управління, можливі обмеження продуктивності |
| **Pinecone** | Zero-ops, managed, швидке масштабування | Proprietary, може бути дорогим                      |
| **Qdrant**   | Performance-critical, self-hosted       | Найкращий баланс продуктивність/функціональність    |
| **Weaviate** | Hybrid search, multi-tenant             | Native AI інтеграція                                |
| **ChromaDB** | Прототипування, локальна розробка       | Не для великих production                           |

#### 12.5. Emerging Patterns

- **GraphRAG:** для запитів, що вимагають traversal зв'язків
- **Agentic RAG:** агенти, які самі вирішують де і як шукати
- **Cache-Augmented Generation (CAG):** кешування для зменшення latency

#### 12.6. RAG у контексті AI-розробки

- Cursor та Windsurf використовують RAG для індексації вашого проєкту
- Context7 = RAG для документації бібліотек
- Cody (Sourcegraph) = enterprise RAG для кодових баз
- Як побудувати власний RAG для внутрішньої документації

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "langchain" → `query-docs` "RAG retrieval augmented generation hybrid search"
> 2. `resolve-library-id` для "llama-index" → `query-docs` "RAG pipeline vector store reranker"
> 3. `resolve-library-id` для "chromadb" → `query-docs` "embeddings vector search collection setup"
> 4. `resolve-library-id` для "pinecone" → `query-docs` "vector database index upsert query"
>
> **Web Search запити:**
>
> - "RAG best practices production 2026 hybrid search reranking"
> - "GraphRAG vs vector RAG comparison use cases"
> - "RAGAS evaluation framework RAG pipeline metrics"
> - "hybrid search BM25 vector search reciprocal rank fusion"
> - "agentic RAG multi-hop reasoning 2026"
>
> **Вимога:** Автор має знайти актуальний стек для production-ready RAG, порівняльні дані vector databases, та реальні приклади. Створити практичне завдання для читача з побудови RAG pipeline.

### 📖 Ресурси

- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [RAGAS Evaluation](https://docs.ragas.io/)
- [ChromaDB](https://www.trychroma.com/)
- [Pinecone](https://www.pinecone.io/)

---

## Модуль 13: AI у DevOps та CI/CD

### 🎯 Мета модуля

Інтегрувати AI у весь lifecycle розробки: від коміту до production deployment.

### 📚 Теми

#### 13.1. AI-Driven Code Review

| Інструмент          | Сильні сторони                                      |
| ------------------- | --------------------------------------------------- |
| **CodeRabbit**      | Автоматичне резюме PR, виявлення security issues    |
| **Qodo (CodiumAI)** | Генерація тестів при PR, виявлення missing coverage |
| **Ellipsis**        | Виявлення high-risk логіки (RBAC, auth)             |
| **SonarQube AI**    | Статичний аналіз з AI-підтримкою                    |

#### 13.2. AI у CI/CD Pipeline

```yaml
# Приклад GitHub Actions з AI-powered кроками
name: AI-Enhanced CI

on: [pull_request]

jobs:
    ai-review:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v4

            # AI Code Review
            - name: CodeRabbit Review
              uses: coderabbitai/openai-pr-review@latest

            # AI Test Generation
            - name: Generate Missing Tests
              uses: qodo-ai/generate-tests@v2

            # Standard Tests
            - name: Run Tests
              run: pytest tests/ -v --cov=app

            # AI Security Scan
            - name: Security Analysis
              uses: snyk/actions/python@master
```

#### 13.3. Automated Remediation

- AI генерує PR з виправленнями безпеки
- Self-healing pipelines — AI дебажить failures
- One-click fixes для відомих вразливостей

#### 13.4. Стратегії інтеграції

| Стратегія            | Інструменти                          | Найкраще для                  |
| -------------------- | ------------------------------------ | ----------------------------- |
| **Ecosystem-Native** | GitHub Copilot + Actions, GitLab Duo | Low-friction інтеграція       |
| **Best-of-Breed**    | Qodo + CodeRabbit + Harness + Snyk   | Глибокий аналіз, кастомізація |

#### 13.5. Enforceable Rules

- Перетворюйте повторювані ревʼю-коментарі на автоматичні правила
- AI моніторить їх дотримання в кожному PR

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "CodeRabbit AI code review setup GitHub Actions 2026"
> - "Qodo CodiumAI CI/CD integration test generation PR"
> - "AI code review tools comparison 2026 CodeRabbit Ellipsis"
> - "Snyk AI security scanning CI/CD pipeline integration"
> - "self-healing CI/CD pipeline AI automated remediation 2026"
> - "DevSecOps AI preventive security shift-left 2026"
>
> **Вимога:** Автор має знайти актуальні GitHub Actions приклади з AI-інтеграцією, порівняння інструментів code review, та реальні YAML конфігурації. Створити практичне завдання для читача.

---

## Модуль 14: Безпека, етика та обмеження AI в розробці

### 🎯 Мета модуля

Знати ризики та обмеження AI в розробці, та вміти мінімізувати їх.

### 📚 Теми

#### 14.1. Безпекові ризики

| Ризик                | Опис                                              | Мінімізація                               |
| -------------------- | ------------------------------------------------- | ----------------------------------------- |
| **Hallucination**    | AI генерує правдоподібний, але неправильний код   | Тести, code review, verification          |
| **Data Leakage**     | Чутливі дані в промптах потрапляють до провайдера | Локальні моделі, DLP, .gitignore          |
| **Supply Chain**     | Підроблені MCP-сервери, шкідливі packages         | Верифіковані реєстри, dependency scanning |
| **Prompt Injection** | Маніпуляція AI через шкідливі вхідні дані         | Input sanitization, guardrails            |
| **Over-reliance**    | Сліпа довіра AI без розуміння коду                | «Senior Dev Mindset», обов'язковий review |

#### 14.2. Конфіденційність та compliance

- Розуміння data processing agreements (DPA) з AI-провайдерами
- GDPR/CCPA при використанні хмарних моделей
- Air-gapped deployments для регульованих індустрій
- Opt-out від використання ваших даних для тренування

#### 14.3. Етичні аспекти

- Copyright та ліцензування AI-генерованого коду
- Attribution — коли код «написаний» AI
- Bias у згенерованому коді
- Відповідальність за баги в AI-генерованому коді

#### 14.4. Обмеження AI (чого AI НЕ може)

- Зрозуміти бізнес-контекст без чіткої специфікації
- Гарантувати відсутність багів
- Замінити архітектурне мислення
- Ефективно працювати з дуже великим контекстом (Lost in the Middle)
- Стабільно виконувати задачі, що вимагають «здорового глузду»

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "AI code security risks hallucination mitigation strategies 2026"
> - "prompt injection attacks LLM prevention techniques 2026"
> - "AI generated code copyright legal status jurisdiction 2026"
> - "data privacy AI coding assistants GDPR CCPA compliance"
> - "MCP security best practices supply chain attack prevention"
> - "AI coding data processing agreement DPA providers 2026"
>
> **Вимога:** Автор має знайти актуальні юридичні рішення щодо AI-генерованого коду, реальні приклади prompt injection, та рекомендації з безпеки MCP. Включити конкретні кейси та рішення.

---

## Модуль 15: Побудова AI-powered робочого процесу з нуля

### 🎯 Мета модуля

Синтезувати всі попередні знання та побудувати повноцінний, ефективний робочий процес з AI.

### 📚 Теми

#### 15.1. Повний AI-enhanced Development Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                  AI-Enhanced Development Lifecycle               │
│                                                                 │
│  1. PLAN        2. SPECIFY       3. IMPLEMENT    4. VERIFY      │
│  ┌──────────┐  ┌──────────────┐  ┌────────────┐  ┌──────────┐ │
│  │ AI:      │  │ Human:       │  │ AI:        │  │ AI:      │ │
│  │ Research  │  │ Write spec   │  │ Generate   │  │ Test     │ │
│  │ Architect │  │ Define       │  │ code from  │  │ Review   │ │
│  │ Plan      │  │ acceptance   │  │ spec       │  │ Audit    │ │
│  │          │  │ criteria     │  │            │  │ Bench    │ │
│  └──────────┘  └──────────────┘  └────────────┘  └──────────┘ │
│       ↓              ↓                 ↓              ↓        │
│  5. DEPLOY      6. MONITOR      7. ITERATE                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ AI:      │  │ AI:          │  │ Human: Update spec       │  │
│  │ CI/CD    │  │ Monitoring   │  │ AI: Regenerate code      │  │
│  │ IaC      │  │ Alerting     │  │ AI: Verify               │  │
│  │ Security │  │ Analysis     │  │                          │  │
│  └──────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

#### 15.2. Рекомендований стек для різних рівнів

##### Рівень 1: Початківець

```
IDE: Cursor (безкоштовний план)
Model: Claude Sonnet / GPT-4o
Config: AGENTS.md (базовий)
VCS: Git + GitHub
Tests: AI-generated unit tests
```

##### Рівень 2: Проміжний

```
IDE: Cursor Pro + Claude Code
Models: routing (Opus для планування, Sonnet для виконання)
Config: AGENTS.md + .cursor/rules/ + Skills
MCP: Context7 + GitHub + Filesystem
Workflow: Spec-Driven (requirements.md → design.md → tasks.md)
Tests: AI-TDD + integration tests
CI/CD: GitHub Actions + CodeRabbit
```

##### Рівень 3: Просунутий

```
IDE: Cursor Pro + Claude Code + Kiro (для SDD)
Models: full routing pipeline (plan → execute → review)
Config: AGENTS.md + Skills + custom MCP servers
MCP: Context7 + GitHub + DB + Sentry + Slack + custom
Workflow: Full SDD + multi-agent orchestration
Tests: AI-TDD + mutation testing + property-based
CI/CD: Full AI pipeline + automated security + self-healing
RAG: Custom RAG for internal docs
```

#### 15.3. Чеклист налаштування нового проєкту з AI

```markdown
## Checklist: AI-Ready Project Setup

### Repository Configuration

- [ ] Створити AGENTS.md з правилами проєкту
- [ ] Створити CLAUDE.md (або symlink до AGENTS.md)
- [ ] Налаштувати .cursor/rules/ з conditional rules
- [ ] Створити .gitignore з AI-специфічними виключеннями

### MCP Configuration

- [ ] Встановити Context7 MCP
- [ ] Налаштувати GitHub MCP (якщо потрібно)
- [ ] Налаштувати Database MCP (якщо потрібно)
- [ ] Перевірити всі сервери через MCP Inspector

### Workflow

- [ ] Створити шаблон requirements.md
- [ ] Створити шаблон design.md
- [ ] Налаштувати tasks.md workflow
- [ ] Визначити approval gates

### Testing & CI/CD

- [ ] Налаштувати AI code review (CodeRabbit/Qodo)
- [ ] Додати AI-driven тестування до CI
- [ ] Налаштувати security сканування
- [ ] Визначити мінімальне test coverage

### Security

- [ ] Переконатися, що секрети в .env (не в коді)
- [ ] Налаштувати DLP для промптів (якщо enterprise)
- [ ] Перевірити DPA з AI-провайдерами
```

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "AI enhanced development workflow setup guide 2026"
> - "AI-ready project setup checklist AGENTS.md MCP 2026"
> - "development workflow AI beginner intermediate advanced stack"
>
> **Вимога:** Автор має зібрати та систематизувати всі інструменти з попередніх модулів у єдиний workflow. Чеклист має бути робочим та перевіреним. Створити фінальне практичне завдання для читача з побудови повного AI-workflow.

---

## Модуль 16: Фреймворки для побудови AI-агентів

### 🎯 Мета модуля

Зрозуміти екосистему фреймворків для створення власних AI-агентів та вміти обрати правильний інструмент.

### 📚 Теми

#### 16.1. Ландшафт фреймворків (2026)

| Фреймворк           | Найкраще для                            | Філософія                                  |
| ------------------- | --------------------------------------- | ------------------------------------------ |
| **LangGraph**       | Складні, stateful, production workflows | Граф-based state machine з явним контролем |
| **CrewAI**          | Швидке прототипування role-based команд | Multi-agent orchestration: ролі + задачі   |
| **AutoGen (AG2)**   | Conversational multi-agent системи      | Агенти спілкуються між собою для вирішення |
| **PydanticAI**      | Type-safe Python applications           | Відмінний DX, strict typing                |
| **Google ADK**      | GCP-native production                   | Глибока інтеграція з Google Cloud          |
| **Semantic Kernel** | Azure/Microsoft ecosystem               | Enterprise-grade, інтеграція з Azure       |

#### 16.2. Вибір фреймворку

```
Потрібен explicit контроль    → LangGraph
потоку та стану?

Потрібна швидка команда       → CrewAI
агентів з ролями?

Потрібен type-safe Python     → PydanticAI
з відмінним DX?

Глибоко в Azure/Microsoft?    → Semantic Kernel

Глибоко в Google Cloud?       → Google ADK

Потрібен conversational       → AutoGen
multi-agent?
```

#### 16.3. Огляд ключових патернів

##### LangGraph — граф-based agent

```python
from langgraph.graph import StateGraph, MessagesState

# Визначення стану
class AgentState(MessagesState):
    plan: str
    current_task: str

# Визначення нод графу
def planner(state: AgentState):
    """Планує виконання задачі"""
    ...

def executor(state: AgentState):
    """Виконує поточну підзадачу"""
    ...

def reviewer(state: AgentState):
    """Перевіряє результат"""
    ...

# Побудова графу
graph = StateGraph(AgentState)
graph.add_node("plan", planner)
graph.add_node("execute", executor)
graph.add_node("review", reviewer)
graph.add_edge("plan", "execute")
graph.add_edge("execute", "review")
graph.add_conditional_edges("review", should_continue)
```

##### CrewAI — role-based team

```python
from crewai import Agent, Task, Crew

researcher = Agent(
    role="Senior Researcher",
    goal="Знайти найкращі практики для {topic}",
    backstory="Ти досвідчений дослідник..."
)

writer = Agent(
    role="Technical Writer",
    goal="Створити документацію на основі дослідження",
    backstory="Ти технічний письменник..."
)

research_task = Task(description="Дослідити {topic}", agent=researcher)
write_task = Task(description="Написати документацію", agent=writer)

crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff(inputs={"topic": "FastAPI middleware"})
```

#### 16.4. Production Considerations

- **Durable Execution** — збереження стану, пауза, відновлення
- **Observability** — LangSmith, Braintrust для моніторингу
- **Token Management** — контроль витрат
- **Error Handling** — graceful degradation, retry policies

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Context7 MCP запити:**
>
> 1. `resolve-library-id` для "langgraph" → `query-docs` "StateGraph agent workflow nodes edges conditional"
> 2. `resolve-library-id` для "crewai" → `query-docs` "multi agent team task orchestration crew"
> 3. `resolve-library-id` для "pydantic-ai" → `query-docs` "agent tools structured output type-safe"
> 4. `resolve-library-id` для "autogen" → `query-docs` "conversational agent group chat setup"
>
> **Web Search запити:**
>
> - "LangGraph vs CrewAI vs AutoGen comparison 2026"
> - "PydanticAI agent framework tutorial getting started"
> - "Google Agent Development Kit ADK features 2026"
> - "Semantic Kernel Microsoft agent framework 2026"
> - "LangSmith observability agent monitoring tracing"
> - "durable execution AI agents state persistence 2026"
>
> **Вимога:** Автор має знайти актуальний API кожного фреймворку та створити РОБОЧІ приклади коду (не псевдокод). Порівняльна таблиця має базуватися на реальних можливостях. Створити практичне завдання для читача.

### 📖 Ресурси

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [AutoGen Documentation](https://ag2ai.github.io/ag2/)
- [LangSmith](https://smith.langchain.com/)
- [Google Agent Development Kit](https://google.github.io/adk-docs/)

---

## Модуль 17: Майбутнє AI в розробці — куди рухається індустрія

### 🎯 Мета модуля

Зрозуміти тренди та підготуватися до наступного покоління AI-інструментів.

### 📚 Теми

#### 17.1. Тренди 2026–2027

1. **Від IDE до Agent OS**
    - AI не просто допомагає в IDE — він стає операційною системою розробки
    - Автономні агенти, які працюють 24/7 (Claude Code headless, GitHub Copilot Workspace)

2. **Spec-as-Code**
    - Специфікації стануть «вихідним кодом», а реалізація — артефактом
    - Code generation → Code compilation from specs

3. **Model Routing як стандарт**
    - Автоматичний вибір моделі під задачу
    - Мульти-провайдерні pipeline-и

4. **MCP як USB для AI**
    - Стандартизація з'єднань між AI та всім іншим
    - On-device agent registries (Windows Agent Protocol)

5. **AI-Native Testing**
    - Автоматична генерація та підтримка тестів
    - Self-healing test suites
    - Mutation testing як стандарт

6. **Enterprise AI Governance**
    - Audit trails для AI-генерованого коду
    - Compliance frameworks для AI у розробці
    - SOC 2 / ISO для AI-assisted development

#### 17.2. Навички, які будуть цінними

```
2023: "Знає мову програмування X"
2024: "Вміє ефективно промптити AI"
2025: "Вміє будувати AI-enhanced workflows"
2026: "Вміє архітектурувати AI-native системи"
2027: "Вміє оркеструвати мульти-агентні pipeline-и"
```

#### 17.3. Чого НЕ замінить AI

- Розуміння бізнес-домену
- Стратегічне мислення та product vision
- Комунікація з stakeholders
- Етичні рішення
- Інноваційне мислення (генерація нових ідей, а не паттернів)

### 🔬 Інструкції для автора контенту (дослідження)

> **Перед написанням цього модуля**, автор (AI) **ОБОВ'ЯЗКОВО** має:
>
> **Web Search запити:**
>
> - "future of AI software development 2027 2028 predictions trends"
> - "AI agent operating system development paradigm 2026"
> - "spec as code compilation deterministic generation 2026"
> - "skills developers need AI era 2027 career"
> - "model routing automatic selection AI coding 2026"
> - "enterprise AI governance compliance frameworks 2026"
>
> **Вимога:** Автор має знайти найсвіжіші прогнози від лідерів індустрії та аналітиків. Тренди мають підкріплюватися конкретними фактами та прикладами, а не бути загальними твердженнями.

---

## 📊 Додаток A: Порівняльна таблиця всіх інструментів

| Інструмент         | Тип       | Ціна ($/міс) | Модель | MCP | Агентний режим | SDD           |
| ------------------ | --------- | ------------ | ------ | --- | -------------- | ------------- |
| **Cursor**         | AI IDE    | $20          | Multi  | ✅  | ✅             | Частково      |
| **Windsurf**       | AI IDE    | $15-20       | Multi  | ✅  | ✅             | Частково      |
| **Claude Code**    | Terminal  | $20+         | Claude | ✅  | ✅             | ✅ (через MD) |
| **GitHub Copilot** | Extension | $10-19       | Multi  | ✅  | ✅             | ❌            |
| **Kiro**           | AI IDE    | Free preview | Multi  | ✅  | ✅             | ✅ (нативно)  |
| **Aider**          | Terminal  | Free (OSS)   | Multi  | ❌  | ✅             | ❌            |
| **Zed**            | IDE       | Free         | Multi  | ✅  | Частково       | ❌            |
| **Continue**       | Extension | Free (OSS)   | Multi  | ❌  | ❌             | ❌            |
| **Cody**           | Extension | Free-30      | Multi  | ❌  | Частково       | ❌            |
| **Gemini CLI**     | Terminal  | Free         | Gemini | ✅  | ✅             | ❌            |

---

## 📊 Додаток B: Глосарій

| Термін                  | Визначення                                                       |
| ----------------------- | ---------------------------------------------------------------- |
| **LLM**                 | Large Language Model — велика мовна модель                       |
| **MCP**                 | Model Context Protocol — стандарт з'єднання AI з інструментами   |
| **RAG**                 | Retrieval-Augmented Generation — генерація з доповненням пошуком |
| **SDD**                 | Spec-Driven Development — розробка, керована специфікацією       |
| **TDD**                 | Test-Driven Development — розробка, керована тестами             |
| **CoT**                 | Chain-of-Thought — ланцюг міркувань                              |
| **DX**                  | Developer Experience — досвід розробника                         |
| **EARS**                | Easy Approach to Requirements Syntax — нотація для вимог         |
| **KV Cache**            | Key-Value Cache — кеш для прискорення генерації                  |
| **RLHF**                | Reinforcement Learning from Human Feedback                       |
| **RRF**                 | Reciprocal Rank Fusion — злиття результатів пошуку               |
| **SWE-bench**           | Software Engineering Benchmark — бенчмарк для інженерії          |
| **Vibe Coding**         | Розробка через вільні промпти без формальних специфікацій        |
| **Context Engineering** | Системне управління контекстом для AI                            |
| **Skills**              | Модульні набори інструкцій для розширення можливостей AI         |
| **Agentic Loop**        | Цикл Plan → Act → Observe → Adjust                               |

---

## 📊 Додаток C: Рекомендований порядок проходження

```
Тиждень 1:  Модулі 0-1  (Фундамент, моделі)
Тиждень 2:  Модулі 2-3  (Інструменти, промптінг)
Тиждень 3:  Модулі 4-5  (Конфігурація, MCP)
Тиждень 4:  Модулі 6-7  (Context7, Smithery)
Тиждень 5:  Модулі 8-9  (Методології, SDD)
Тиждень 6:  Модулі 10-11 (TDD, агенти)
Тиждень 7:  Модуль 12   (RAG)
Тиждень 8:  Модулі 13-14 (DevOps, безпека)
Тиждень 9:  Модуль 15   (Побудова workflow)
Тиждень 10: Модулі 16-17 (Фреймворки, майбутнє)
```

> **Принцип:** Кожен тиждень = теорія (40%) + практика (40%) + дослідження (20%).
> Після кожного модуля виконуйте ВСІ практичні завдання та дослідження через Context7 / web search.

---

## 📊 Додаток D: Context7 Quick Reference

```bash
# Швидка довідка по Context7 MCP

# Крок 1: Знайдіть бібліотеку
resolve-library-id("fastapi")
# → Повертає: /fastapi/fastapi

# Крок 2: Запитайте документацію
query-docs("/fastapi/fastapi", "middleware CORS configuration")
# → Повертає: актуальні сніпети документації

# Корисні запити для різних мов/фреймворків:
resolve-library-id("react")       → query-docs("hooks useEffect cleanup")
resolve-library-id("nextjs")      → query-docs("app router server components")
resolve-library-id("django")      → query-docs("ORM queryset filter")
resolve-library-id("spring-boot") → query-docs("REST controller security")
resolve-library-id("express")     → query-docs("middleware error handling")
resolve-library-id("sqlalchemy")  → query-docs("async session relationship")
resolve-library-id("prisma")      → query-docs("schema relations query")
resolve-library-id("tailwindcss") → query-docs("responsive grid layout")
```

---

> **💡 Фінальна порада:** AI — це мультиплікатор ваших навичок, а не замінник. Чим краще ви розумієте архітектуру, патерни та бізнес-домен, тим ефективніше ви використовуватимете AI. Інвестуйте в свої фундаментальні знання паралельно з вивченням AI-інструментів.
