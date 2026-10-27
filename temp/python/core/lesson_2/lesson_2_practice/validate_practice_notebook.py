#!/usr/bin/env python3
"""Валідатор практичного ноутбука Lesson 2.

1. Збирає «розв'язану» версію ноутбука (усі TODO заповнені еталонними розв'язками).
2. Виконує її через nbclient — жодна клітинка не має впасти з помилкою.
3. Перевіряє, що фінальна таблиця показує 8/8 блоків ✅.
4. Окремо запускає «порожню» версію й перевіряє, що перевірки коректно сигналізують про відсутність розв'язку.

Запуск:  python3 validate_practice_notebook.py
"""

import pathlib
import sys
import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

NB = pathlib.Path(__file__).resolve().parent / "02_python_core_practice.ipynb"

SOLUTIONS = {
    "# 👤 Впишіть": 'student_name = "Олесь Шевченко"\ngroup = "IT-21"',
    "# 🛠️ ТЗ-1.": "ukraine_population = 38_000_000\nearth_to_moon_km = 384_400",
    "# 🛠️ ТЗ-2.": (
        "num_bin = 0b101010\n"
        "num_oct = 0o52\n"
        "num_hex = 0x2A\n"
        "s_bin = bin(42)\n"
        "s_oct = oct(42)\n"
        "s_hex = hex(42)"
    ),
    "# 🛠️ ТЗ-3.": (
        "speed_of_light = 3e8\n"
        "planck_const = 6.626e-34\n"
        "type_speed = type(speed_of_light).__name__"
    ),
    "# 🛠️ ТЗ-4.": (
        'dialog_escaped = \'Він сказав: "Python — це чудово!" \\\\ Корисна мова\'\n'
        'tabbed_table = "Мова:\\tPython\\nВерсія:\\t3.11"'
    ),
    "# 🛠️ ТЗ-5.": 'win_path = r"C:\\new_folder\\scripts\\test.py"',
    "# 🛠️ ТЗ-6.": (
        'receipt_card = """=== ЧЕК ===\\n'
        'Товар: Ноутбук\\n'
        'Ціна: 25000 грн\\n'
        'Дякуємо за покупку!"""'
    ),
    "# 🛠️ ТЗ-7.": (
        "calc_sum = 0.1 + 0.2\n"
        "check_imprecise = (calc_sum == 0.3)\n"
        "fixed_sum = round(calc_sum, 2)\n"
        "check_precise = (fixed_sum == 0.3)"
    ),
    "# 🛠️ ТЗ-8.": (
        "bool_math = True + True + True + False\n"
        "bool_mult = (5 > 2) * 10\n"
        "eq_true_one = (True == 1)\n"
        "eq_false_zero = (False == 0)"
    ),
    "# 🛠️ ТЗ-9.": (
        "user_avatar = None\n"
        "is_avatar_missing = (user_avatar is None)\n"
        "is_avatar_present = (user_avatar is not None)\n"
        "none_eq_zero = (None == 0)\n"
        "none_eq_empty_str = (None == \"\")\n"
        "none_eq_false = (None == False)"
    ),
    "# 🛠️ ТЗ-10.": (
        "b_zero = bool(0)\n"
        "b_empty_str = bool(\"\")\n"
        "b_none = bool(None)\n"
        "b_num = bool(-15)\n"
        "b_str = bool(\"Python\")"
    ),
    "# 🛠️ ТЗ-11.": (
        "SPEED_OF_SOUND = 343\n"
        "PI = 3.14159\n"
        "student_score = 95\n"
        'course_title = "Python Core"'
    ),
    "# 🛠️ ТЗ-12.": (
        "score_a = score_b = score_c = 0\n"
        "box_length, box_width, box_height = 50, 30, 20"
    ),
    "# 🛠️ ТЗ-13.": 'cup_left = "кава"\ncup_right = "чай"\ncup_left, cup_right = cup_right, cup_left',
    "# 🛠️ ТЗ-14.": (
        "player_balance = 1000\n"
        "player_balance += 250\n"
        "player_balance -= 50\n"
        "player_balance *= 2\n"
        "player_balance //= 100\n"
        "player_balance %= 7"
    ),
    "# 🛠️ ТЗ-15.": (
        "dynamic_holder = 100\n"
        "is_int_step = isinstance(dynamic_holder, int)\n"
        'dynamic_holder = "Сто"\n'
        "is_str_step = isinstance(dynamic_holder, str)\n"
        "dynamic_holder = 100.0\n"
        "is_float_step = isinstance(dynamic_holder, float)"
    ),
    "# 🛠️ ТЗ-16.": (
        "import keyword\n"
        'is_pass_kw = keyword.iskeyword("pass")\n'
        'is_var_kw = keyword.iskeyword("my_variable")\n'
        "kw_count = len(keyword.kwlist)"
    ),
    "# 🛠️ ТЗ-17.": (
        'parsed_bin = int("1100100", 2)\n'
        'parsed_hex = int("2A", 16)\n'
        'parsed_oct = int("755", 8)'
    ),
    "# 🛠️ ТЗ-18.": (
        'box_border = "+" + "-" * 18 + "+"\n'
        'box_content = "|  PYTHON COURSE   |"\n'
        'banner = box_border + "\\n" + box_content + "\\n" + box_border'
    ),
    "# 🛠️ ТЗ-19.": (
        "demo_num = 254\n"
        "demo_ratio = 12.34567\n"
        'fmt_bin = f"{demo_num:b}"\n'
        'fmt_hex = f"{demo_num:X}"\n'
        'fmt_float = f"{demo_ratio:.2f}"'
    ),
    "# 🛠️ ТЗ-20.": (
        'set_inputs("3665")\n'
        'total_sec = int(input("Введіть кількість секунд: "))\n'
        "hours = total_sec // 3600\n"
        "rem_sec = total_sec % 3600\n"
        "minutes = rem_sec // 60\n"
        "seconds = rem_sec % 60\n"
        'time_formatted = f"{hours} год {minutes} хв {seconds} с"\n'
        "print(time_formatted)\n"
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-21.": (
        'set_inputs("Ноутбук", "25000", "2", "10")\n'
        'item_name = input("Назва товару: ")\n'
        'unit_price = float(input("Ціна: "))\n'
        'quantity = int(input("Кількість: "))\n'
        'discount_pct = float(input("Знижка (%): "))\n'
        "subtotal = unit_price * quantity\n"
        "discount_val = round(subtotal * (discount_pct / 100), 2)\n"
        "total_to_pay = round(subtotal - discount_val, 2)\n"
        'summary_line = f"Товар: {item_name} | До сплати: {total_to_pay:.2f} грн (знижка {discount_val:.2f} грн)"\n'
        "print(summary_line)\n"
        "reset_inputs()"
    ),
    "# 🛠️ ТЗ-22.": (
        'set_inputs("6", "8")\n'
        'leg_a = float(input("Введіть перший катет: "))\n'
        'leg_b = float(input("Введіть другий катет: "))\n'
        "hypo = round((leg_a ** 2 + leg_b ** 2) ** 0.5, 2)\n"
        "perimeter = round(leg_a + leg_b + hypo, 2)\n"
        "area = round(0.5 * leg_a * leg_b, 2)\n"
        'print(f"Гіпотенуза: {hypo}, Периметр: {perimeter}, Площа: {area}")\n'
        "reset_inputs()"
    ),
    "# 🛠️ Бліц": (
        "b1 = False\n"
        "b2 = 2\n"
        "b3 = False\n"
        "b4 = 10\n"
        'b5 = "float"\n'
        "b6 = True"
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
    print("   ✅ Усі клітинки виконалися без помилок")

    final_text = outputs_of(solved, "ФІНАЛЬНА ПЕРЕВІРКА (викладач)")
    print("\n--- Вивід фінальної перевірки (розв'язана версія) ---")
    print(final_text.strip())
    print("--- кінець ---")

    ok = (
        "успішно складено 8 з 8 блоків" in final_text
        and "🎉" in final_text
        and "❌" not in final_text
    )
    if not ok:
        print("❌ Фінальна перевірка показала не всі блоки ✅")
        return 1
    print("   ✅ 8/8 блоків пройдено успішно!")

    print("\n▶ 2/3 Виконую порожню (студентську) версію — очікую ввічливі помилки...")
    empty = nbformat.read(NB, as_version=4)
    try:
        run(empty, allow_errors=True)
    except CellExecutionError as exc:
        print(f"❌ Непередбачена помилка в порожній версії:\n{exc}")
        return 1
    print("   ✅ Порожня версія не падає фатально")

    empty_final = outputs_of(empty, "ФІНАЛЬНА ПЕРЕВІРКА (викладач)")
    print("\n--- Вивід фінальної перевірки (порожня версія) ---")
    print(empty_final.strip())
    print("--- кінець ---")
    if "успішно складено 0 з 8 блоків" not in empty_final:
        print("❌ У порожній версії очікувався результат 0 з 8")
        return 1
    if "❌" not in empty_final:
        print("❌ У порожній версії мають бути повідомлення про невиконані блоки")
        return 1
    print("   ✅ Порожня версія коректно фіксує 0/8 блоків з детальними підказками")

    print("\n▶ 3/3 Перевіряю, що в коді студентських клітинок з TODO немає передчасних готових відповідей...")
    bad = []
    for cell in nbformat.read(NB, as_version=4).cells:
        if cell.cell_type != "code" or "# TODO" not in cell.source:
            continue
        code_lines = [
            line for line in cell.source.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        code_only = "\n".join(code_lines)
        for marker in ("ukraine_population = 38_000_000", "num_bin = 0b101010",
                       "speed_of_light = 3e8", "calc_sum = 0.1 + 0.2",
                       "player_balance = 1000", "b1 = False"):
            if marker in code_only:
                bad.append((marker, code_only[:70]))
    if bad:
        for m, s in bad:
            print(f"❌ Знайдено завчасно заповнене рішення {m!r} у клітинці: {s!r}")
        return 1
    print("   ✅ Клітинки завдань чисті від готових відповідей")

    print("\n🎉 ВАЛІДАЦІЯ УСПІШНА! Ноутбук повністю готовий до роздачі студентам.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
