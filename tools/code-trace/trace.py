#!/usr/bin/env python3
"""Записує покрокове виконання Python-програми у JSON для компонента ::code-trace.

usage:
  uv run --no-project --python 3.15 tools/code-trace/trace.py PROG.py -o OUT.json
      [--input 5 --input abc] [--max-steps 1000] [--name main.py]

Кожен крок — стан *перед* виконанням рядка (як у Python Tutor): стек кадрів
(імена → посилання), купа об'єктів, яких досягають ці імена, і новий вивід.
Дані знімаються з реального CPython, тому id, типи та вивід — справжні.

Розмітка в коді програми:
  x = y  #? Куди тепер вкаже стрілка x?   — питання «передбач» перед цим рядком
                                           (лише при першому проходженні).
"""

import argparse
import builtins
import inspect
import json
import linecache
import re
import sys
import traceback
import types
from pathlib import Path

FORMAT_VERSION = 1
ASK_RE = re.compile(r"\s*#\?\s*(.*)$")

_frozendict = getattr(builtins, "frozendict", None)
PRIMITIVE = (int, float, complex, bool, str, bytes, type(None))
SEQUENCE = (list, tuple)
SETS = (set, frozenset)
MAPPING = (dict,) + ((_frozendict,) if _frozendict else ())
IMMUTABLE = PRIMITIVE + (tuple, frozenset, range) + ((_frozendict,) if _frozendict else ())

GEN_FLAGS = inspect.CO_GENERATOR | inspect.CO_COROUTINE | inspect.CO_ASYNC_GENERATOR
_is_immortal = getattr(sys, "_is_immortal", None)


class StopTracing(BaseException):
    """Ліміт кроків вичерпано. BaseException, щоб `except Exception` у програмі його не зловив."""


class Snapshot:
    """Купа об'єктів одного кроку: ключ — id() у вигляді рядка."""

    def __init__(self, max_objects, max_items, max_repr):
        self.heap = {}
        self.max_objects = max_objects
        self.max_items = max_items
        self.max_repr = max_repr
        self.truncated = False
        self.closures = []  # (code функції, ім'я вільної змінної, ключ комірки) — для зв'язку кадрів з комірками

    def ref(self, obj):
        key = str(id(obj))
        if key in self.heap:
            return key
        if len(self.heap) >= self.max_objects:
            self.truncated = True
            return None
        entry = {"type": type(obj).__name__, "mutable": not isinstance(obj, IMMUTABLE)}
        if _is_immortal and _is_immortal(obj):
            entry["immortal"] = True
        self.heap[key] = entry  # до рекурсії — щоб цикли посилань не зациклили обхід
        self._fill(obj, entry)
        return key

    def _short(self, text):
        return text if len(text) <= self.max_repr else text[: self.max_repr - 1] + "…"

    def _items(self, entry, iterable, size):
        items = []
        for i, item in enumerate(iterable):
            if i >= self.max_items:
                entry["more"] = size - self.max_items
                break
            items.append(self.ref(item))
        return items

    def _fill(self, obj, entry):
        if isinstance(obj, PRIMITIVE):
            entry.update(kind="primitive", repr=self._short(repr(obj)))
        elif isinstance(obj, SEQUENCE):
            entry.update(kind="sequence", items=self._items(entry, obj, len(obj)))
        elif isinstance(obj, SETS):
            entry.update(kind="set", items=self._items(entry, obj, len(obj)))
        elif isinstance(obj, MAPPING):
            pairs, size = [], len(obj)
            for i, (k, v) in enumerate(obj.items()):
                if i >= self.max_items:
                    entry["more"] = size - self.max_items
                    break
                pairs.append([self.ref(k), self.ref(v)])
            entry.update(kind="mapping", entries=pairs)
        elif isinstance(obj, range):
            entry.update(kind="primitive", repr=repr(obj))
        elif inspect.isfunction(obj):
            entry.update(kind="function", name=obj.__qualname__, signature=_signature(obj))
            if obj.__closure__:
                free = {}
                for name, cell in zip(obj.__code__.co_freevars, obj.__closure__):
                    free[name] = self.ref(cell)
                    self.closures.append((obj.__code__, name, free[name]))
                entry["freevars"] = free
        elif isinstance(obj, types.CellType):
            try:
                entry.update(kind="cell", ref=self.ref(obj.cell_contents))
            except ValueError:  # комірка ще порожня
                entry.update(kind="cell", ref=None)
        elif inspect.isbuiltin(obj):
            entry.update(kind="builtin", name=obj.__name__)
        elif inspect.ismodule(obj):
            entry.update(kind="module", name=obj.__name__)
        elif inspect.isclass(obj):
            entry.update(kind="class", name=obj.__qualname__)
        elif inspect.isgenerator(obj):
            entry.update(kind="generator", name=obj.__qualname__, state=inspect.getgeneratorstate(obj))
            if entry["state"] in ("GEN_CREATED", "GEN_SUSPENDED"):  # під час роботи кадр уже на стеку
                entry["frame"] = {"line": obj.gi_frame.f_lineno, "vars": self.vars(obj.gi_frame.f_locals)}
        elif isinstance(obj, BaseException):
            entry.update(kind="exception", message=self._short(str(obj)))
        else:
            entry.update(kind="object", repr=self._short(repr(obj)))
            attrs = getattr(obj, "__dict__", None)
            if isinstance(attrs, dict):
                entry["attrs"] = self.vars(attrs)

    def vars(self, namespace, hide_dunder=False):
        out = []
        for name, value in list(namespace.items()):
            if hide_dunder and name.startswith("__") and name.endswith("__"):
                continue
            out.append({"name": name, "ref": self.ref(value)})
        return out

    def link_cells(self, frame, frame_vars):
        """Змінна кадру, що живе в комірці (cell), посилається на комірку, а не прямо на об'єкт.

        CPython не дає дістати комірки з кадру, тому знаходимо їх через замикання функцій
        на схемі: для внутрішнього кадру — функції з тим самим code, для зовнішнього —
        функції, чий code створено в цьому кадрі. Якщо кандидат не один — не вгадуємо.
        """
        code = frame.f_code
        cell_names = set(code.co_cellvars) | set(code.co_freevars)
        for var in frame_vars:
            if var["name"] not in cell_names:
                continue
            var["cell"] = True
            found = {key for fcode, name, key in self.closures
                     if name == var["name"] and (fcode is code or fcode in code.co_consts)}
            if len(found) == 1:
                var["cellRef"] = found.pop()

    def count_arrows(self, frames):
        """refs = кількість стрілок на схемі (не sys.getrefcount: той рахує й внутрішні посилання CPython)."""
        counts = {}

        def hit(ref):
            if ref is not None:
                counts[ref] = counts.get(ref, 0) + 1

        for frame in frames:
            for var in frame["vars"]:
                hit(var.get("cellRef", var["ref"]))
        for entry in self.heap.values():
            for ref in entry.get("items", ()):
                hit(ref)
            for k, v in entry.get("entries", ()):
                hit(k)
                hit(v)
            for ref in entry.get("freevars", {}).values():
                hit(ref)
            if entry.get("kind") == "cell":
                hit(entry["ref"])
            for var in entry.get("attrs", ()):
                hit(var["ref"])
            for var in entry.get("frame", {}).get("vars", ()):
                hit(var["ref"])
        for key, entry in self.heap.items():
            entry["refs"] = counts.get(key, 0)


def _signature(func):
    try:
        return str(inspect.signature(func))
    except (TypeError, ValueError):
        return "(...)"


class Output:
    """Підміна sys.stdout: накопичує вивід, а трасувальник забирає приріст на кожному кроці."""

    def __init__(self):
        self.parts = []

    def write(self, text):
        self.parts.append(text)
        return len(text)

    def flush(self):
        pass

    def take(self):
        text = "".join(self.parts)
        self.parts.clear()
        return text


class Tracer:
    def __init__(self, filename, asks, args, out):
        self.filename = filename
        self.asks = dict(asks)
        self.args = args
        self.out = out
        self.steps = []
        self.frame_ids = {}
        self.next_frame = 0
        self.unwinding = set()
        self.truncated = False

    def _frame_id(self, frame):
        key = id(frame)
        if key not in self.frame_ids:
            self.frame_ids[key] = f"f{self.next_frame}"
            self.next_frame += 1
        return self.frame_ids[key]

    def _stack(self, frame):
        stack = []
        while frame is not None:
            if frame.f_code.co_filename == self.filename:
                stack.append(frame)
            frame = frame.f_back
        return stack[::-1]

    def record(self, frame, event, arg=None):
        if len(self.steps) >= self.args.max_steps:
            self.truncated = True
            raise StopTracing
        snap = Snapshot(self.args.max_objects, self.args.max_items, self.args.max_repr)
        frames = []
        stack = self._stack(frame)
        for f in stack:
            is_module = f.f_code.co_name == "<module>"
            frames.append({
                "id": self._frame_id(f),
                "name": f.f_code.co_qualname,
                "line": f.f_lineno,
                "vars": snap.vars(f.f_locals, hide_dunder=is_module),
            })
        for f, data in zip(stack, frames):
            snap.link_cells(f, data["vars"])
        step = {"event": event, "line": frame.f_lineno, "frames": frames}
        if event == "return":
            step["returnValue"] = snap.ref(arg)
        elif event == "exception":
            step["exception"] = snap.ref(arg[1])
        snap.count_arrows(frames)
        step["heap"] = snap.heap
        if snap.truncated:
            step["heapTruncated"] = True
        if event == "line" and frame.f_lineno in self.asks:
            step["ask"] = self.asks.pop(frame.f_lineno)
        self.steps.append(step)

    def flush_output(self):
        text = self.out.take()
        if text and self.steps:
            self.steps[-1]["out"] = self.steps[-1].get("out", "") + text

    def trace(self, frame, event, arg):
        if frame.f_code.co_filename != self.filename:
            return None
        if event == "call" and frame.f_code.co_name == "<module>":
            return self.trace
        self.flush_output()  # вивід, зроблений до цього кроку, належить попередньому кроку
        fid = self._frame_id(frame)
        if event == "line":
            self.unwinding.discard(fid)
        if event == "exception":
            self.unwinding.add(fid)
        if event == "return" and fid in self.unwinding:
            event, arg = "unwind", None
            self.unwinding.discard(fid)
        self.record(frame, event, arg)
        if event in ("return", "unwind") and not frame.f_code.co_flags & GEN_FLAGS:
            del self.frame_ids[id(frame)]  # кадр зникає; його id() може дістатися новому кадру
        return self.trace


def parse_asks(source):
    asks, clean = {}, []
    for lineno, line in enumerate(source.splitlines(), 1):
        match = ASK_RE.search(line)
        if match:
            asks[lineno] = match.group(1).strip()
            line = line[: match.start()].rstrip()
        clean.append(line)
    return asks, "\n".join(clean) + "\n"


def make_input(inputs, out):
    queue = list(inputs)

    def fake_input(prompt=""):
        out.write(str(prompt))
        if not queue:
            raise EOFError("EOF when reading a line")
        value = queue.pop(0)
        out.write(value + "\n")  # як у терміналі: введене видно у виводі
        return value

    return fake_input


def format_uncaught(exc, filename):
    frames = [fs for fs in traceback.extract_tb(exc.__traceback__) if fs.filename == filename]
    lines = []
    if frames:
        lines.append("Traceback (most recent call last):\n")
        lines.extend(traceback.StackSummary.from_list(frames).format())
    lines.extend(traceback.format_exception_only(exc))
    return "".join(lines)


def run(path, args):
    source = Path(path).read_text(encoding="utf-8")
    asks, display_code = parse_asks(source)
    filename = args.name or Path(path).name
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    code = compile(source, filename, "exec")

    out = Output()
    tracer = Tracer(filename, asks, args, out)
    user_globals = {"__name__": "__main__", "__builtins__": builtins}
    real_stdout, real_input = sys.stdout, builtins.input
    error = None
    sys.stdout, builtins.input = out, make_input(args.input, out)
    sys.settrace(tracer.trace)
    try:
        exec(code, user_globals)
    except StopTracing:
        pass
    except BaseException as exc:  # noqa: BLE001 — неперехоплений виняток програми є частиною трасування
        error = {"type": type(exc).__name__, "message": str(exc), "traceback": format_uncaught(exc, filename)}
    finally:
        sys.settrace(None)
        sys.stdout, builtins.input = real_stdout, real_input
    tracer.flush_output()

    for i, step in enumerate(tracer.steps):
        step["i"] = i
    return {
        "format": FORMAT_VERSION,
        "python": sys.version.split()[0],
        "implementation": sys.implementation.name,
        "name": filename,
        "code": display_code,
        "inputs": args.input,
        "steps": tracer.steps,
        "truncated": tracer.truncated,
        "error": error,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("program")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--name", help="ім'я файлу в traceback (типово — ім'я програми)")
    parser.add_argument("--input", action="append", default=[], help="рядок для input(), можна кілька")
    parser.add_argument("--max-steps", type=int, default=1000)
    parser.add_argument("--max-objects", type=int, default=200)
    parser.add_argument("--max-items", type=int, default=50)
    parser.add_argument("--max-repr", type=int, default=120)
    args = parser.parse_args()

    result = run(args.program, args)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    status = f"error: {result['error']['type']}" if result["error"] else "ok"
    print(f"{args.output}: {len(result['steps'])} steps, python {result['python']}, {status}"
          + (" (truncated)" if result["truncated"] else ""))


if __name__ == "__main__":
    main()
