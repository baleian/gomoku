from board import Stone, Status
import random

class Brain:
  def __init__(self):
    pass

  def predict(self, board, stone):
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

