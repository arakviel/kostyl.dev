def countdown(n):
    while n > 0:
        yield n
        n -= 1

g = countdown(2)
print(next(g))
print(next(g))
for x in g:
    print(x)
