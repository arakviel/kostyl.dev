def make_counter():
    count = 0
    def step():
        nonlocal count
        count += 1
        return count
    return step

c = make_counter()
c()
c()

def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

print(fact(3))
