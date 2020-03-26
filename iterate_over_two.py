letters = 'A B C D'.split()
numbers = '1 2 4 5 6 7 8 9'.split()

out = [(l, n) for l in letters for n in numbers]
print(out)
