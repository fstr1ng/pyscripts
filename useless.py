def stringSize(inputString):
    size = 0
    while True:
        try:
            c = inputString[size]
            size += 1
        except IndexError:
            return size

print(stringSize('hello'))
