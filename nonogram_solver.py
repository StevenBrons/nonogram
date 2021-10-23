'''Nonograms solver.
Nonograms is a perfect-information logic puzzle with simple rules.
There is a free online implementation at, for instance,
https://www.puzzle-nonograms.com/.
The rules are as follows: You have a grid of squares, which must be
either filled in black or left white. Beside each row of the grid are
listed the lengths of the runs of black squares on that row. Above
each column are listed the lengths of the runs of black squares in
that column.  The aim is to find all black squares.
This module encodes that puzzle definition as a finite-domain
constraint satisfaction problem and solves it with Z3
(https://github.com/Z3Prover/z3).  In my limited testing, Z3 finds
solutions to puzzles up to 25x25 in a matter of seconds.
For this to work, run it in a virtualenv that has the Z3 python
bindings installed.
'''
import sys

import z3

def solve_nonogram(rows, columns, given = [], not_equal_to = []):
  '''Encode the given Nonograms puzzle as a collection of Z3 constraints.
  Return a 2-tuple of the Z3 Solver object representing the puzzle,
  and the Z3 Bool objects representing whether each square in the grid
  is black.  The squares are indexed row-major.
  This function just encodes the problem; to solve it, invoke
  `.check()` on the returned Solver.
  '''
  width = len(columns)
  height = len(rows)
  s = z3.Solver()
  s.set(unsat_core=True)
  squares = [[z3.Bool('sq %d %d' % (i, j)) for i in range(width)] for j in range(height)]

  # Given
  for i, j, b in given:
    s.assert_and_track(squares[j][i] == b, f"hint {i} {j}")

  # Not equal to
  for model in not_equal_to:
    unique_clause = z3.Not(z3.And([squares[i][j] == model[i][j] for i in range(height) for j in range(width)]))
    s.assert_and_track(unique_clause, "unique")

  # Horizontal block constraints
  horiz_block_positions = {}
  horiz_block_lengths = {}
  for (j, row) in enumerate(rows):
    for (k, block_len) in enumerate(row):
      left_edge = z3.Int('horiz block %d %d' % (k, j))
      horiz_block_positions[(k, j)] = left_edge
      horiz_block_lengths[(k, j)] = block_len
      s.assert_and_track(left_edge >= 0, 'left edge positive %d %d' % (j, k))
      s.assert_and_track(left_edge <= width - block_len, 'left edge in bounds %d %d' % (j, k))
      if k > 0:
        prev_end = horiz_block_positions[(k-1, j)] + horiz_block_lengths[(k-1, j)]
        s.assert_and_track(left_edge >= prev_end + 1, 'horiz block separation %d %d' % (j, k))
      for i in range(width):
        # If the square is in the block, it must be on
        s.assert_and_track(z3.Implies(z3.And(left_edge <= i, left_edge + block_len > i), squares[j][i]),
                           'squares on horiz %d %d %d' % (j, k, i))
        # There are three ways the square might not be in any block in
        # the row, in which case it must be off
        if k > 0:
          s.assert_and_track(z3.Implies(z3.And(left_edge > i, prev_end <= i), z3.Not(squares[j][i])),
                             'gap squares off horiz %d %d %d' % (j, k, i))
        else:
          s.assert_and_track(z3.Implies(left_edge > i, z3.Not(squares[j][i])),
                             'early squares off horiz %d %d %d' % (j, k, i))
        if k == len(row) - 1:
          s.assert_and_track(z3.Implies(left_edge + block_len <= i, z3.Not(squares[j][i])),
                             'late squares off horiz %d %d %d' % (j, k, i))

  # Vertical block positioning and length constraints
  vert_block_positions = {}
  vert_block_lengths = {}
  for (i, col) in enumerate(columns):
    for (k, block_len) in enumerate(col):
      top_edge = z3.Int('vert block %d %d' % (i, k))
      vert_block_positions[(i, k)] = top_edge
      vert_block_lengths[(i, k)] = block_len
      s.assert_and_track(top_edge >= 0, 'top edge positive %d %d' % (i, k))
      s.assert_and_track(top_edge <= height - block_len, 'top edge in bounds %d %d' % (i, k))
      if k > 0:
        prev_end = vert_block_positions[(i, k-1)] + vert_block_lengths[(i, k-1)]
        s.assert_and_track(top_edge >= prev_end + 1, 'vert block separation %d %d' % (i, k))
      for j in range(height):
        # If the square is in the block, it must be on
        s.assert_and_track(z3.Implies(z3.And(top_edge <= j, top_edge + block_len > j), squares[j][i]),
                           'squares on vert %d %d %d' % (i, k, j))
        # There are three ways the square might not be in any block in
        # the column, in which case it must be off
        if k > 0:
          s.assert_and_track(z3.Implies(z3.And(top_edge > j, prev_end <= j), z3.Not(squares[j][i])),
                             'gap squares off vert %d %d %d' % (i, k, j))
        else:
          s.assert_and_track(z3.Implies(top_edge > j, z3.Not(squares[j][i])),
                             'early squares off vert %d %d %d' % (i, k, j))
        if k == len(col) - 1:
          s.assert_and_track(z3.Implies(top_edge + block_len <= j, z3.Not(squares[j][i])),
                             'late squares off vert %d %d %d' % (i, k, j))
  
  res = s.check()
  if res == z3.sat:
    M = s.model()
    return [[True if M[squares[j][i]] else False for i in range(len(squares[0]))] for j in range(len(squares))]
  return False