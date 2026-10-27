import sys, json, io, contextlib, dis
D = {"python": sys.version.split()[0]}
x = 5; D["id5"] = id(5); y = x
D["globals"] = repr({k: v for k, v in globals().items() if k in ("x", "y")})
D["xy_same"] = [x is y, x == y, id(x) == id(y)]
x = 7; D["id7"] = id(7); D["after_x7"] = [x, y]
count = 100000; D["count_id_before"] = id(count); before = id(count); count = count + 1
D["count_id_after"] = id(count); D["count_ne"] = before != id(count)
a = [1, 2]; D["list_id"] = id(a); b = a
D["ab"] = [a is b, id(a) == id(b)]
D["rc_a"] = sys.getrefcount(a) - 1
D["rc_ab"] = sys.getrefcount(a) - 1
del b; D["rc_del_b"] = sys.getrefcount(a) - 1
c = [1, 2]
D["eq"] = {"a==c": a == c, "a is c": a is c, "a==b": True}
def mk(s): return int(s)
a1, b1 = int("1000"), int("1000"); c1, d1 = int("100000"), int("100000")
D["cache"] = {"1000": [a1 is b1, a1 == b1], "100000": [c1 is d1, c1 == d1]}
l, r = "ліво", "право"; D["str_ids"] = [id(l), id(r)]
l, r = r, l
D["swapped"] = [l, r]
buf = io.StringIO()
with contextlib.redirect_stdout(buf): dis.dis('a, b = b, a')
D["dis_swap"] = buf.getvalue()
json.dump(D, open("lesson03b.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(D, ensure_ascii=False, indent=1))
