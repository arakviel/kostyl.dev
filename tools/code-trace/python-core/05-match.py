command = "stop"
match command:
    case "go":
        print("їдемо")
    case "stop" | "halt":  #? Який рядок виконається після цього збігу?
        print("зупиняємось")
    case _:
        print("невідома команда")
print("кінець")
