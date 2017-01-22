from copy import copy, deepcopy
from board import Stone, Status
import random

class Brain:
  MAX_DEPTH = 2

  def __init__(self):
    pass    


  def minimax(self, board, stone, depth=0):
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    needForDefense = False
    needForDefense2 = False
    possibles = []
    op5moks = []
    for r in range(board.size):
      for c in range(board.size):
        if (
          board.status[opponent][r][c] is Status.STRAIGHT_FOUR or
          board.status[opponent][r][c] is Status.DOUBLE_FOUR or
          board.status[opponent][r][c] is Status.FOUR
        ):
          needForDefense = True
        elif board.status[opponent][r][c] is Status.DOUBLE_THREE:
          needForDefense2 = True

        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue
        if board.status[stone][r][c] is Status.FIVE:
          return 10, depth

        possibles.append((r, c))

        if board.status[opponent][r][c] is Status.FIVE:
          op5moks.append((r, c))

    if len(op5moks) >= 2: 
      return 0, depth + 1

    for r, c in op5moks:
      st = deepcopy(board.status)
      board.putStone(r, c, stone)
      score, d = self.minimax(board, opponent, depth + 1)
      board.data[r][c] = 0
      board.status = st
      return 10 - score, d

    for r, c in possibles:
      if (
        board.status[stone][r][c] is Status.STRAIGHT_FOUR or
        board.status[stone][r][c] is Status.DOUBLE_FOUR
      ):
        return 10, depth + 2

    if not needForDefense:
      for r, c in possibles:
        if board.status[stone][r][c] is Status.DOUBLE_THREE:
          return 10, depth + 4

    if depth > self.MAX_DEPTH:
      return (5, depth)
      
    for r, c in possibles:
      if (
        board.status[stone][r][c] is Status.FOUR or
        board.status[stone][r][c] is Status.DOUBLE_THREE # or
        # board.status[stone][r][c] is Status.THREE
      ):
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        score, d = self.minimax(board, opponent, depth + 1)
        board.data[r][c] = 0
        board.status = st
        if score is 0:
          return 10, d

    if needForDefense or needForDefense2:
      canDefense = False
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        score, d = self.minimax(board, opponent, depth + 1)
        board.data[r][c] = 0
        board.status = st
        if score is 0:
          return 10, d
        if score is 5:
          return 5, d
          canDefense = True
      if canDefense:
        return 5, depth

    return 5, depth



  def predict(self, board, stone):
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK

    needForDefense = False
    needForDefense2 = False

    possibles = []
    for r in range(board.size):
      for c in range(board.size):
        if (
          board.status[opponent][r][c] is Status.STRAIGHT_FOUR or
          board.status[opponent][r][c] is Status.DOUBLE_FOUR or
          board.status[opponent][r][c] is Status.FOUR
        ):
          needForDefense = True
        elif board.status[opponent][r][c] is Status.DOUBLE_THREE:
          needForDefense2 = True

        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue
        if board.status[stone][r][c] is Status.FIVE:
          return r, c

        possibles.append((r, c))

    for r, c in possibles:
      if board.status[opponent][r][c] is Status.FIVE:
        return r, c

    for r, c in possibles:
      if (
        board.status[stone][r][c] is Status.STRAIGHT_FOUR or
        board.status[stone][r][c] is Status.DOUBLE_FOUR
      ):
        return r, c

    if not needForDefense:
      for r, c in possibles:
        if board.status[stone][r][c] is Status.DOUBLE_THREE:
          return r, c

    for r, c in possibles:
      if (
        board.status[stone][r][c] is Status.FOUR or
        board.status[stone][r][c] is Status.DOUBLE_THREE # or
        # board.status[stone][r][c] is Status.THREE
      ):
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        score, depth = self.minimax(board, opponent)
        board.data[r][c] = 0
        board.status = st
        if score is 0:
          return r, c

    if needForDefense or needForDefense2:
      canDefense = []
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        score, depth = self.minimax(board, opponent)
        board.data[r][c] = 0
        board.status = st
        if score is 0:
          return r, c
        if score is 5:
          canDefense.append((r, c))
      if len(canDefense) > 0:
        return random.choice(canDefense)

    return random.choice(possibles)



import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()

