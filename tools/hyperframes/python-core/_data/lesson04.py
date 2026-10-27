import json, sys, ast
D = {"python": sys.version.split()[0]}
D["expr"] = [2 + 3 * 4, (2 + 3) * 4, 3 * 4]
D["floor"] = [-7 // 2, -7 % 2, 7 // 2, 7 % 2, -7 == 2 * (-4) + 1]
word = "ab"; copy = word; D["id_ab"] = id(word); word += "c"; D["id_abc"] = id(word); D["wc"] = [word, copy]
raw = "41"; D["id_raw"] = id(raw); number = int(raw); D["id_num"] = id(number)
price, n, x = 3.14159, 42, 0.256
D["fmt"] = [f"{price:.2f}", f"{n:05d}", f"{x:.1%}"]
a, b = float("3"), float("4"); c = (a ** 2 + b ** 2) ** 0.5; D["hyp"] = [a, b, c, f"{c:.2f}"]
D["mul"] = "5" * 3
try: "5" + 1
except TypeError as e: D["typeerror"] = str(e)
json.dump(D, open("lesson04.json", "w"), ensure_ascii=False, indent=1); print(json.dumps(D, ensure_ascii=False))
