from copy import copy, deepcopy
from board import Stone, Status
import random

class Brain:
  def __init__(self):
    pass


  def minimax(self, board, stone, depth):
    if depth is 6:
      return (-1, -1), 5, depth

    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    size = board.size

    possibles = []
    op4moks = []

    for r in range(size):
      for c in range(size):
        if board.status[stone][r][c] is Status.FIVE:
          return (r, c), 10, depth

        if board.status[stone][r][c] is not Status.FORBIDDEN:
          possibles.append((r, c))

        if (
          board.status[opponent][r][c] is Status.STRAIGHT_FOUR or
          board.status[opponent][r][c] is Status.DOUBLE_FOUR or
          board.status[opponent][r][c] is Status.FOUR
        ):
          op4moks.append((r, c))

    for r, c in possibles:
      if board.status[opponent][r][c] is Status.FIVE:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        tmp, val, d = self.minimax(board, opponent, depth + 1)
        board.data[r][c] = 0
        board.status = st
        return (r, c), 10 - val, d

    for r, c in possibles:
      if (
        board.status[stone][r][c] is Status.STRAIGHT_FOUR or
        board.status[stone][r][c] is Status.DOUBLE_FOUR or
        board.status[stone][r][c] is Status.FOUR
      ):
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        tmp, val, d = self.minimax(board, opponent, depth + 1)
        board.data[r][c] = 0
        board.status = st
        if 10 - val == 10:
          return (r, c), 10, d
        if val == 0:
          possibles.remove((r, c))

    if len(op4moks) > 0:
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        isBreak = False
        for r2 in range(size):
          if isBreak:
            break
          for c2 in range(size):
            if (
              board.status[opponent][r2][c2] is Status.STRAIGHT_FOUR or
              board.status[opponent][r2][c2] is Status.DOUBLE_FOUR
            ):
              possibles.remove((r, c))
              isBreak = True
              break
        board.data[r][c] = 0
        board.status = st

    if depth is 0:
      pipeWrite('MESSAGE RANDOM CHOICE = %s' % str(possibles))
    return random.choice(possibles), 5, depth

    #######################################################################
    # backups
    #######################################################################
    opwins = []
    for r, c in op4moks:
      st = deepcopy(board.status)
      board.putStone(r, c, opponent)
      tmp, val, d = self.minimax(board, stone, depth + 1)
      board.data[r][c] = 0
      board.status = st
      if 10 - val == 10:
        opwins.append((r, c, d))

    if len(opwins) > 0:
      if depth is 0:
        pipeWrite('MESSAGE OP4MOKS = %s' % str(op4moks))
        pipeWrite('MESSAGE OPWINS = %s' % str(opwins))
      r, c, d = random.choice(opwins)
      return (r, c), 5, d

    if depth is 0:
      pipeWrite('MESSAGE RANDOM CHOICE = %s' % str(possibles))
    return random.choice(possibles), 5, depth
    #######################################################################


  def predict(self, board, stone):
    pos, val, d = self.minimax(board, stone, 0)
    return pos

    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    size = board.size

    possibles = []
    candies = []
    for r in range(size):
      for c in range(size):
        if board.status[stone][r][c] is Status.FIVE:
          candies.append((r, c))
        if board.status[stone][r][c] is not Status.FORBIDDEN:
          possibles.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE MY FIVE = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[opponent][r][c] is Status.FIVE:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE OP FIVE = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[stone][r][c] is Status.STRAIGHT_FOUR:
        candies.append((r, c))
      if board.status[stone][r][c] is Status.DOUBLE_FOUR:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE MY STRAIGHT_FOUR OR DOUBLE_FOUR = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[opponent][r][c] is Status.STRAIGHT_FOUR:
        candies.append((r, c))
      if board.status[opponent][r][c] is Status.DOUBLE_FOUR:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE OP STRAIGHT_FOUR OR DOUBLE_FOUR = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[stone][r][c] is Status.FOUR:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE MY FOUR = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[opponent][r][c] is Status.FOUR:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE OP FOUR = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[stone][r][c] is Status.DOUBLE_THREE:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE MY DOUBLE_THREE = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[opponent][r][c] is Status.DOUBLE_THREE:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE OP DOUBLE_THREE = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[stone][r][c] is Status.THREE:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE MY THREE = %s' % str(candies))
      return random.choice(candies)

    candies = []
    for r, c in possibles:
      if board.status[opponent][r][c] is Status.THREE:
        candies.append((r, c))
    if len(candies) > 0:
      pipeWrite('MESSAGE OP THREE = %s' % str(candies))
      return random.choice(candies)

    if len(possibles) > 0:
      pipeWrite('MESSAGE RANDOM CHOICE')
      return random.choice(possibles)
    return -1, -1


import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()

