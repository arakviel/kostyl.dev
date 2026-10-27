# code-trace

Записує покрокове виконання Python-програми у JSON для компонента `::code-trace`.
Дані знімаються з реального CPython (`sys.settrace`), тому `id`, типи, вивід і traceback — справжні.

```bash
uv run --no-project --python 3.15 tools/code-trace/trace.py examples/03-aliasing.py \
  -o public/traces/python-core/03-aliasing.json [--input 5 --input abc] [--max-steps 1000]
```

- `--input` — рядки для `input()` по черзі (запрошення і введене потрапляють у вивід, як у терміналі). Якщо рядків не вистачить, виникне `EOFError`.
- `#? Питання` у кінці рядка — режим «передбач»: питання ставиться перед першим виконанням цього рядка. Сам коментар у показаному коді прибирається.
- Перегенеровувати JSON при кожній зміні прикладу і при оновленні Python (`python` у JSON показує версію).

## Формат JSON (`format: 1`)

```jsonc
{
  "format": 1, "python": "3.15.0", "implementation": "cpython",
  "name": "03-aliasing.py",          // ім'я файлу в traceback
  "code": "a = [1, 2, 3]\n...",      // показаний код (без #?-питань)
  "inputs": ["abc"],
  "truncated": false,                // true — вичерпано --max-steps (напр., нескінченний цикл)
  "error": null,                     // або {type, message, traceback} — неперехоплений виняток
  "steps": [ /* Step */ ]
}
```

**Step** — стан *перед* виконанням рядка `line`:

| Поле | Значення |
|---|---|
| `i` | номер кроку |
| `event` | `line` — буде виконано рядок · `call` — створено кадр · `return` — кадр повертає `returnValue` · `exception` — у кадрі виник `exception` · `unwind` — кадр зникає через виняток |
| `line` | рядок у поточному кадрі |
| `frames` | стек від `<module>` до поточного: `{id, name, line, vars: [{name, ref, cell?, cellRef?}]}` |
| `heap` | об'єкти, яких досягають імена: `{ "<id>": Object }` |
| `out` | вивід, що з'явився *під час* цього кроку (вивід повністю — конкатенація `out` до поточного кроку) |
| `ask` | питання «передбач» (необов'язкове) |
| `returnValue`, `exception` | ключ у `heap` |
| `heapTruncated` | купу обрізано лімітом `--max-objects` |

`frames[].id` стабільний, поки кадр живий (`f0`, `f1`, …); у генератора він зберігається між `yield`.
Змінна з `cell: true` живе в комірці замикання; `cellRef` — ключ комірки, якщо її вдалося знайти однозначно (інакше стрілка йде прямо на `ref`).

**Object** — ключ це `id(obj)` (те саме число, що друкує `id()`):

| `kind` | Поля |
|---|---|
| `primitive` | `repr` (int, float, complex, bool, str, bytes, None, range) |
| `sequence` | `items: [ref]` (list, tuple) · `more` — скільки елементів не показано |
| `set` | `items: [ref]` (set, frozenset) |
| `mapping` | `entries: [[keyRef, valueRef]]` (dict, frozendict) |
| `function` | `name`, `signature`, `freevars: {name: cellRef}` |
| `cell` | `ref` — вміст комірки (або `null`) |
| `generator` | `name`, `state` (`GEN_CREATED`/`GEN_SUSPENDED`/`GEN_RUNNING`/`GEN_CLOSED`), `frame: {line, vars}` — заморожений кадр (коли генератор не виконується) |
| `exception` | `message` |
| `builtin`, `module`, `class` | `name` |
| `object` | `repr`, `attrs: [{name, ref}]` |

Спільні поля: `type` (ім'я типу), `mutable`, `immortal` (CPython 3.12+: безсмертні об'єкти — `None`, `True`, малі `int` −5…1024 у 3.15), `refs` — **кількість стрілок на схемі**. Це не `sys.getrefcount`: той рахує й внутрішні посилання інтерпретатора, а для безсмертних об'єктів повертає умовне велике число.

## Обмеження

- Трасується лише код самої програми; виклики stdlib виконуються «одним кроком».
- Ключ об'єкта — `id()`. Після звільнення об'єкта CPython може віддати той самий `id` новому об'єкту (це правда і для живого Python).
- Атрибути класів і `__globals__` функцій не розгортаються.
