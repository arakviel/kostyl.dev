it = iter("кіт")
print(next(it))
print(next(it))
print(next(it))
print(next(it, "кінець")) #? Що поверне next, коли символи закінчились?
