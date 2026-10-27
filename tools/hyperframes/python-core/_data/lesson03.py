import sys, dis, json, io, contextlib
D = {"python": sys.version.split()[0]}
# globals as a table
x = 10; y = x
D["globals"] = {k: repr(v) for k, v in globals().items() if k in ("x", "y")}
D["same_id"] = [id(x), id(y), id(x) == id(y)]
# rebinding
n = 5; i5 = id(n); n = n + 1; i6 = id(n)
D["rebind"] = {"id5": i5, "id6": i6, "ne": i5 != i6}
# refcount of a list
a = [1, 2, 3]
D["refcount"] = {"a": sys.getrefcount(a) - 1}
b = a; D["refcount"]["a_b"] = sys.getrefcount(a) - 1
del b; D["refcount"]["after_del_b"] = sys.getrefcount(a) - 1
# is vs ==
p = [1, 2]; q = [1, 2]
D["is_eq"] = {"p==q": p == q, "p is q": p is q}
def mk(s): return int(s)
D["cache"] = {s: (mk(s) is mk(s)) for s in ["-5", "-6", "256", "257", "1024", "1025"]}
D["tuple_swap"] = None
buf = io.StringIO()
with contextlib.redirect_stdout(buf): dis.dis("a, b = b, a")
D["dis_swap"] = buf.getvalue()
buf = io.StringIO()
with contextlib.redirect_stdout(buf): dis.dis("y = x + 1")
D["dis_assign"] = buf.getvalue()
json.dump(D, open("lesson03.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(D, ensure_ascii=False, indent=1))
