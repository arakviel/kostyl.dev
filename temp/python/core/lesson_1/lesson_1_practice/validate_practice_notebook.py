#!/usr/bin/env python3
"""Валідатор практичного ноутбука Lesson 1.

1. Збирає «розв'язану» версію ноутбука (усі TODO заповнені правильними відповідями).
2. Виконує її через nbclient — жодна клітинка не має впасти з помилкою.
3. Перевіряє, що фінальна таблиця показує 8/8 блоків ✅.
4. Окремо запускає «порожню» версію й перевіряє, що перевірки коректно повідомляють про відсутність розв'язку.

Запуск:  python3 validate_practice_notebook.py
"""

import pathlib
import sys

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

NB = pathlib.Path(__file__).resolve().parent / "01_python_basics_practice.ipynb"

# Ключ — унікальний маркер у клітинці, значення — повний готовий код клітинки.
SOLUTIONS = {
    "# 👤 Впишіть": 'student_name = "Тест Тестович"\ngroup = "IT-99"',
    "# 🛠️ ТЗ-1.": '%%capture cap1\nprint("Python", "урок", "1", sep="-")',
    "# 🛠️ ТЗ-2.": '%%capture cap2\nprint("Ім\'я:", end=" ")\nprint("Олесь")',
    "# 🛠️ ТЗ-3.": '%%capture cap3\nprint("Курс", "Python", "1", sep="-", end="!")',
    "# 🛠️ ТЗ-4.": "num = 42\nratio = 3.14\ntext = \"Python\"\nflag = True",
    "# 🛠️ ТЗ-5.": "hex_num = 0x1F\noct_num = 0o17\nsci_num = 3e3",
    "# 🛠️ ТЗ-6.": 'pred_div = "float"\npred_mul = "int"\npred_concat = "str"',
    "# 🛠️ ТЗ-7.": 'quote_line = \'Він сказав: "Привіт"!\'',
    "# 🛠️ ТЗ-8.": 'card = "Ім\'я: Олесь\\nВік: 30"',
    "# 🛠️ ТЗ-9.": 'first_name = "Олесь"\nlast_name = "Ковальчук"\nfull_name = first_name + " " + last_name',
    "# 🛠️ ТЗ-10.": 'age_line = "Вік: " + str(30)',
    "# 🛠️ ТЗ-11.": (
        "a = 17\nb = 5\ntotal = a + b\npart = a / b\nwhole = a // b\nrest = a % b\n"
        "power = a ** b\npriority = 2 + 3 * 4\nbrackets = (2 + 3) * 4"
    ),
    "# 🛠️ ТЗ-12.": "p_floor = -4\np_mod = -1\np_pow = 512",
    "# 🛠️ ТЗ-13.": 't_mul = "int"\nt_mul_float = "float"\nt_pow = "int"\nt_pow_float = "float"',
    "# 🛠️ ТЗ-14.": "income = 100\nincome += 25\nincome += 10\nincome *= 2\nincome -= 30",
    "# 🛠️ ТЗ-15.": 'valid_names = "user_name, _temp, age2"\ninvalid_names = "1st_place, my var, class"',
    "# 🛠️ ТЗ-16.": "import_is_reserved = False",
    "# 🛠️ ТЗ-17": (
        'set_inputs("30")\n'
        'age_str = input("Скільки вам років? ")\n'
        "age_int = int(age_str)\n"
        "next_year_age = age_int + 1\n"
        'print("Наступного року вам буде " + str(next_year_age))\n'
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-18": (
        'set_inputs("3.5")\n'
        'side_str = input("Введіть сторону: ")\n'
        "side = float(side_str)\n"
        "square_area = side ** 2\n"
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-19": 'concat_result = "5" + "5"\nnumber_result = int("5") + 5',
    "# 🛠️ ТЗ-20.": (
        'set_inputs("4", "5")\n'
        'width_str = input("Введіть ширину прямокутника: ")\n'
        'height_str = input("Введіть висоту прямокутника: ")\n'
        "width = float(width_str)\n"
        "height = float(height_str)\n"
        "area = width * height\n"
        'print("Площа прямокутника: " + str(area))\n'
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-21.": (
        'set_inputs("2500", "41.5")\n'
        'uah_str = input("Введіть суму в UAH: ")\n'
        'rate_str = input("Введіть курс USD: ")\n'
        "uah = float(uah_str)\n"
        "rate = float(rate_str)\n"
        "usd = uah / rate\n"
        'print("Сума в USD: " + str(usd))\n'
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-22.": "a = 3.0\nb = 4.0\nc = (a ** 2 + b ** 2) ** 0.5",
    "# 🛠️ Бліц": (
        "b1 = 2 + 3 * 4\nb2 = (2 + 3) * 4\nb3 = 10 // 3\n"
        'b4 = 10 % 3\nb5 = "str"\nb6 = True'
    ),
}


def build_solved() -> nbformat.NotebookNode:
    nb = nbformat.read(NB, as_version=4)
    used = set()
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = cell.source
        for marker, solution in SOLUTIONS.items():
            if marker in src:
                cell.source = solution
                used.add(marker)
                break
    missing = set(SOLUTIONS) - used
    if missing:
        raise SystemExit(f"❌ Маркери не знайдені в ноутбуці: {missing}")
    return nb


def run(nb: nbformat.NotebookNode, allow_errors: bool):
    client = NotebookClient(
        nb,
        timeout=120,
        kernel_name="python3",
        allow_errors=allow_errors,
        resources={"metadata": {"path": "."}},
    )
    client.execute()
    return nb


def outputs_of(nb: nbformat.NotebookNode, marker: str) -> str:
    for cell in nb.cells:
        if cell.cell_type == "code" and marker in cell.source:
            text = ""
            for out in cell.get("outputs", []):
                text += out.get("text", "") or ""
            return text
    return ""


def main() -> int:
    print("▶ 1/3 Виконую розв'язану версію ноутбука...")
    solved = build_solved()
    try:
        run(solved, allow_errors=False)
    except CellExecutionError as exc:
        print(f"❌ РОЗВ'ЯЗАНА ВЕРСІЯ ВПАЛА:\n{exc}")
        return 1
    print("   ✅ усі клітинки виконалися без помилок")

    final_text = outputs_of(solved, "ФІНАЛЬНА ПЕРЕВІРКА (викладач)")
    print("\n--- Вивід фінальної перевірки (розв'язана версія) ---")
    print(final_text.strip())
    print("--- кінець ---")

    ok = (
        "Пройдено блоків: 8 з 8" in final_text
        and "🎉" in final_text
        and "❌" not in final_text
    )
    if not ok:
        print("❌ Фінальна перевірка показала не всі блоки ✅")
        return 1
    print("   ✅ 8/8 блоків пройдено")

    print("\n▶ 2/3 Виконую порожню (студентську) версію — очікую ввічливі помилки...")
    empty = nbformat.read(NB, as_version=4)
    try:
        run(empty, allow_errors=True)
    except CellExecutionError as exc:
        print(f"❌ Непередбачена помилка в порожній версії:\n{exc}")
        return 1
    print("   ✅ порожня версія не падає непередбачено")

    empty_final = outputs_of(empty, "ФІНАЛЬНА ПЕРЕВІРКА (викладач)")
    print("\n--- Вивід фінальної перевірки (порожня версія) ---")
    print(empty_final.strip())
    print("--- кінець ---")
    if "Пройдено блоків: 0 з 8" not in empty_final:
        print("❌ У порожній версії очікувався результат 0 з 8")
        return 1
    if "❌" not in empty_final:
        print("❌ У порожній версії мають бути помилки по блоках")
        return 1

    print("\n▶ 3/3 Перевіряю, що в коді клітинок з TODO немає готових відповідей")
    bad = []
    for cell in nbformat.read(NB, as_version=4).cells:
        if cell.cell_type != "code" or "# TODO" not in cell.source:
            continue
        # дивимося лише на.robotний код, а не на коментарі-інструкції
        code_lines = [
            line for line in cell.source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        code_only = "\n".join(code_lines)
        for marker in ("num = 42", 'pred_div = "float"', "income = 100",
                       "square_area = side ** 2", "b1 = 2 + 3 * 4",
                       "full_name = first_name"):
            if marker in code_only:
                bad.append((marker, code_only[:70]))
    if bad:
        for m, s in bad:
            print(f"❌ Знайдено готове рішення {m!r} у клітинці: {s!r}")
        return 1
    print("   ✅ у всіх клітинках з TODO немає готових відповідей у коді")

    print("\n🎉 Валідація пройдена: ноутбук готовий до використання.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
