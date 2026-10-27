for n in range(2, 6):
    if n % 3 == 0:  #? Що станеться, коли n стане 3?
        break
    print(n)
else:
    print("без break")
print("кінець")
