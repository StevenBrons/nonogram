from nonogram import Nonogram

braille = {
	" " : [
		[0,0],
		[0,0],
		[0,0]
	],
	"a" : [
		[1,0],
		[0,0],
		[0,0]
	],
	"b" : [
		[1,0],
		[1,0],
		[0,0]
	],
	"c" : [
		[1,1],
		[0,0],
		[0,0]
	],
	"d" : [
		[1,1],
		[0,1],
		[0,0]
	],
	"e" : [
		[1,0],
		[0,1],
		[0,0]
	],
	"f" : [
		[1,1],
		[1,0],
		[0,0]
	],
	"g" : [
		[1,1],
		[1,1],
		[0,0]
	],
	"h" : [
		[1,0],
		[1,1],
		[0,0]
	],
	"i" : [
		[0,1],
		[1,0],
		[0,0]
	],
	"j" : [
		[0,1],
		[1,1],
		[0,0]
	],
	"k" : [
		[1,0],
		[0,0],
		[1,0]
	],
	"l" : [
		[1,0],
		[1,0],
		[1,0]
	],
	"m" : [
		[1,1],
		[0,0],
		[1,0]
	],
	"n" : [
		[1,1],
		[0,1],
		[1,0]
	],
	"o" : [
		[1,0],
		[0,1],
		[1,0]
	],
	"p" : [
		[1,1],
		[1,0],
		[1,0]
	],
	"q" : [
		[1,1],
		[1,1],
		[1,0]
	],
	"r" : [
		[1,0],
		[1,1],
		[1,0]
	],
	"s" : [
		[0,1],
		[1,0],
		[1,0]
	],
	"t" : [
		[0,1],
		[1,1],
		[1,0]
	],
	"u" : [
		[1,0],
		[0,0],
		[1,1]
	],
	"v" : [
		[1,0],
		[1,0],
		[1,1]
	],
	"w" : [
		[0,1],
		[1,1],
		[0,1],
	],
	"x" : [
		[1,1],
		[0,0],
		[1,1]
	],
	"y" : [
		[1,1],
		[0,1],
		[1,1]
	],
	"z" : [
		[1,0],
		[0,1],
		[1,1]
	]
}

text = "never gonna give you up never gonna let you down never gonna run around and desert you"

text_grid = [
	"never gonn",
	"a give you",
	" up never ",
	"gonna let ",
	"you down n",
	"ever gonna",
	" run aroun",
	"d and dese",
	"rt you    ",
]

WIDTH = 10
HEIGHT = 9

text_array = list(map(list, text_grid))
grid = [[None for x in range(WIDTH * 2)]  for y in range(HEIGHT * 3)]

def paste_character(c, x, y):
	ch = braille[c]
	for dx in range(2):
		for dy in range(3):
			grid[y*3 + dy][x*2 + dx] = ch[dy][dx] == 1

for x in range(WIDTH):
	for y in range(HEIGHT):
		paste_character(text_array[y][x], x, y)


prev_best = 1000
while True:
	N = Nonogram(grid)
	N.create_unique_hints()
	if len(list(N.given)) < prev_best:
		prev_best = len(list(N.given))
		N.visualize(False)
		print(prev_best)
