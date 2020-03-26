from math import sin 
num = 1000
sin_mult = 100
i_mult = 1
for i in range(num):
	print(str(i) + ' '*int(str(sin(i/10)*sin_mult)) + '#')

