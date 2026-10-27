count = 100_000
before = id(count)
count = count + 1  #? Чи зміниться сам об'єкт 100000?
print(before == id(count))
print(count)
