def parse(text):
    return int(text)

def read_age():
    raw = input("Вік: ")
    try:
        return parse(raw)
    except ValueError as e:
        print("Помилка:", e)
        return None

age = read_age()
parse("x")
