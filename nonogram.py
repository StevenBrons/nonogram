import functools
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from nonogram_solver import solve_nonogram
import random

class Nonogram:

	def __init__(self, grid):
		self.HEIGHT = len(grid)
		self.WIDTH = len(grid[0])
		self.grid = grid
		self.col_hints = self.__create_hints(True)
		self.row_hints = self.__create_hints(False)
		self.given = []

	def __create_hints(self, rotated=False):
		def red(acc, cur):
			if cur != acc[0][0]:
				return [(cur, 1)] + acc 
			else:
				return [(cur, acc[0][1] + 1)] + acc[1:]

		hints = map(lambda l: functools.reduce(red,l, [(0,0)]), zip(*self.grid[::-1]) if rotated else self.grid)
		hints = map(lambda l: filter(lambda x: x[0]==1,l), hints)
		hints = map(lambda l: map(lambda x: x[1], l), hints)
		hints = map(list, hints)

		if not rotated:
			hints = map(lambda l: l[::-1], hints)

		return list(hints)
	
	def print_ascii(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[x])):
				if self.grid[x][y] == None:
					print("ERROR")
				print("██" if self.grid[x][y] else "  ", end="")
			print()


	def solve(self):
		solve_nonogram(self.row_hints, self.col_hints)

	def is_unique(self):
		print("Checking uniqueness")
		model = solve_nonogram(self.row_hints, self.col_hints)
		return not solve_nonogram(self.row_hints, self.col_hints, [], [model])

	def find_random_diff(self, grid1, grid2):
		diffs = []
		for x in range(self.WIDTH):
			for y in range(self.HEIGHT):
				if grid1[y][x] != grid2[y][x]:
					diffs = diffs + [(x,y)]
		return random.choice(diffs)

	def create_unique_hints(self):
		given = []
		model = solve_nonogram(self.row_hints, self.col_hints, given, [self.grid])
		while model != False:
			x, y = self.find_random_diff(self.grid, model)
			given = given + [(x, y, self.grid[y][x])]
			print(f"Adding hint: {x},{y}={self.grid[y][x]}")
			model = solve_nonogram(self.row_hints, self.col_hints, given, [self.grid])
		self.given = map(lambda hint: (hint[0],hint[1]), given)
		return self.given


	def visualize(self, show_solution=False):
		fix, ax = plt.subplots()
		plt.xlim(0, self.WIDTH)
		plt.ylim(0, self.HEIGHT)


		col_labels = map(lambda x: "\n".join(map(str, x)), self.col_hints)
		row_labels = list(map(lambda x: "  ".join(map(str, x)), self.row_hints))[::-1]

		ax.set_xticks(np.arange(.5, self.WIDTH + 0.5, 1))
		ax.set_yticks(np.arange(.5, self.HEIGHT + 0.5, 1))

		ax.set_xticklabels(col_labels,linespacing=1.8)
		ax.set_yticklabels(row_labels)

		ax.xaxis.tick_top()
		ax.tick_params(axis=u"both", which=u"both",length=0, labelsize=16)
		ax.set_aspect("equal", adjustable="box")

		for x in range(self.WIDTH):
			rect = Rectangle((x, 0), 1, self.HEIGHT, color="black", alpha=0.2, fill=False)
			ax.add_patch(rect)
		for y in range(self.HEIGHT):
			rect = Rectangle((0, y), self.WIDTH, 1, color="black", alpha=0.2, fill=False)
			ax.add_patch(rect)
		for x in range(0, self.WIDTH, 2):
			rect = Rectangle((x-0.03, 0), 0.06, self.HEIGHT, color="black", alpha=0.4)
			ax.add_patch(rect)
		for y in range(0, self.HEIGHT, 3):
			rect = Rectangle((0, y-0.03), self.WIDTH, 0.06, color="black", alpha=0.4)
			ax.add_patch(rect)


		if show_solution:
			for x in range(self.WIDTH):
				for y in range(self.HEIGHT):
					if (self.grid[y][x]):
						ax.add_patch(Rectangle((x, self.HEIGHT - y - 1), 1, 1, color="black"))
		else: 
			for x, y in self.given:
				if (self.grid[y][x]):
					rect = Rectangle((x, self.HEIGHT - y - 1), 1, 1, color="black")
					ax.add_patch(rect)
				else:
					plt.plot(x + 0.5, self.HEIGHT - (y + 0.5), marker="x", markersize=15, color="grey", dash_capstyle="butt")

		box = ax.get_position()
		ax.set_position([0.2,-0.2,box.width*1.5, box.height*1.5])

		plt.title("Als je blind bent, dan zie je hem niet!", pad=40, fontsize=20, fontweight="bold")
		plt.show()
		
