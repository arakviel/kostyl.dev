import sys, struct, json, decimal
from decimal import Decimal
D = {}
D["python"] = sys.version.split()[0]
x = 42
D["type_id"] = {"42": [type(42).__name__, id(42), sys.getrefcount(42)], "3.14": [type(3.14).__name__], "'hi'": [type('hi').__name__], "True": [type(True).__name__], "None": [type(None).__name__]}
D["bases"] = {"int": 42, "bin": bin(42), "oct": oct(42), "hex": hex(42), "bin255": bin(255), "hex255": hex(255), "million": 1_000_000}
D["int_info"] = {"bits_per_digit": sys.int_info.bits_per_digit, "sizeof_digit": sys.int_info.sizeof_digit}
n = 2**100
digits, v = [], n
while v: digits.append(v & (2**30 - 1)); v >>= 30
D["pow100"] = {"value": n, "digits_le": digits, "getsizeof": sys.getsizeof(n), "getsizeof_42": sys.getsizeof(42), "bit_length": n.bit_length()}
def f64(x):
    b = struct.unpack(">Q", struct.pack(">d", x))[0]
    s = format(b, "064b"); return {"sign": s[0], "exp": s[1:12], "mant": s[12:], "exp_int": int(s[1:12], 2)}
D["float"] = {"0.1": f64(0.1), "0.2": f64(0.2), "0.3": f64(0.3), "0.5": f64(0.5), "1.0": f64(1.0)}
decimal.getcontext().prec = 60
D["dec"] = {"0.1": str(Decimal(0.1)), "0.2": str(Decimal(0.2)), "0.3": str(Decimal(0.3)), "sum": repr(0.1 + 0.2), "eq": 0.1 + 0.2 == 0.3, "sum_exact": str(Decimal(0.1) + Decimal(0.2))}
D["bool"] = {"True+True": True + True, "isint": isinstance(True, int), "True==1": True == 1, "mro": [c.__name__ for c in bool.__mro__], "int(True)": int(True), "sum": sum([True, True, False, True])}
a, b = None, None
D["none"] = {"is": a is b, "id_same": id(None) == id(None), "type": type(None).__name__, "print": repr(print() ) if False else "None"}
D["round"] = {"round(0.1+0.2,2)": round(0.1 + 0.2, 2), "isclose": __import__("math").isclose(0.1 + 0.2, 0.3)}
json.dump(D, open("lesson02.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(D, ensure_ascii=False, indent=1))
