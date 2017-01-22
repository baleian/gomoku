from copy import copy, deepcopy
from board import Stone, Status
import random



class Brain:
  MAX_DEPTH = 2

  def __init__(self):
    pass

  def predict(self, board, stone):
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    
    nears = []
    attacks = []
    defenses = []
    for r in range(board.size):
      for c in range(board.size):
        if board.status[opponent][r][c] >= Status.DOUBLE_THREE:
          defenses.append((r, c, board.status[opponent][r][c]))
        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue
        if board.status[stone][r][c] is Status.FIVE:
          return r, c
        if board.status[stone][r][c] >= Status.THREE:
          attacks.append((r, c, board.status[stone][r][c]))
        if board.status[stone][r][c] >= Status.NEAR:
          nears.append((r, c))
    
    attacks.sort(key=lambda x: x[2], reverse=True)
    defenses.sort(key=lambda x: x[2], reverse=True)

    for r, c, stat in defenses:
      if stat is Status.FIVE:
        return r, c

    for r, c, stat in attacks:
      if stat >= Status.DOUBLE_FOUR:
        return r, c
      elif stat is Status.DOUBLE_THREE:
        if len(defenses) is 0 or defenses[0][2] < Status.FOUR:
          return r, c

    if len(attacks) > 0:
      random.shuffle(attacks)
      alpha, beta = 0, 10
      for r, c, status in attacks:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        pipeWrite('MESSAGE attack suggest: %d,%d' % (r, c))
        val = self.alphaBetaPruning(board, opponent, 0, alpha, beta, False)
        board.data[r][c] = 0
        board.status = st
        pipeWrite('MESSAGE = %d' % val)
        alpha = val if alpha < val else alpha
        if val is 10:
          return r, c

    if len(defenses) > 0:
      matrix = [[0 for r in range(board.size)] for c in range(board.size)]
      possibles = []
      for r, c, status in defenses:
        sr = r - 4 if r - 4 >= 0 else 0
        sc = c - 4 if c - 4 >= 0 else 0
        er = r + 4 if r + 4 < board.size else board.size - 1
        ec = c + 4 if c + 4 < board.size else board.size - 1
        for r2 in range(sr, er + 1):
          for c2 in range(sc, ec + 1):
            if board.status[stone][r2][c2] is not Status.FORBIDDEN:
              matrix[r2][c2] = 1

      for r in range(board.size):
        for c in range(board.size):
          if matrix[r][c] is 1:
            possibles.append((r, c))

      random.shuffle(possibles)
      alpha, beta = 0, 5
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        pipeWrite('MESSAGE defense suggest: %d,%d' % (r, c))
        val = self.alphaBetaPruning(board, opponent, 0, alpha, beta, False)
        board.data[r][c] = 0
        board.status = st
        pipeWrite('MESSAGE = %d' % val)
        alpha = val if alpha < val else alpha
        if val >= 5:
          return r, c

      #pipeWrite('MESSAGE defense possibles: %s' % str(possibles))
      #return random.choice(possibles)

    return random.choice(nears)


  def alphaBetaPruning(self, board, stone, depth=0, alpha=0, beta=10, maxPlayer=True):
    #raw_input()
    #board.debugPrint()
    #pipeWrite('MESSAGE depth=%d' % depth)
    if depth > self.MAX_DEPTH:
      return 5

    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    
    attacks = []
    defenses = []
    for r in range(board.size):
      for c in range(board.size):
        if board.status[opponent][r][c] >= Status.DOUBLE_THREE:
          defenses.append((r, c, board.status[opponent][r][c]))
        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue
        if board.status[stone][r][c] is Status.FIVE:
          return 10 if maxPlayer else 0
        if board.status[stone][r][c] >= Status.THREE:
          attacks.append((r, c, board.status[stone][r][c]))
    
    attacks.sort(key=lambda x: x[2], reverse=True)
    defenses.sort(key=lambda x: x[2], reverse=True)

    if len(defenses) >= 2 and defenses[1][2] is Status.FIVE:
      return 0 if maxPlayer else 10

    if len(defenses) >= 1 and defenses[0][2] is Status.FIVE:
      r, c = defenses[0][0], defenses[0][1]
      st = deepcopy(board.status)
      board.putStone(r, c, stone)
      val = self.alphaBetaPruning(board, opponent, depth, alpha, beta, not maxPlayer)
      board.data[r][c] = 0
      board.status = st
      return val

    for r, c, stat in attacks:
      if stat >= Status.DOUBLE_FOUR:
        return 10 if maxPlayer else 0
      elif stat is Status.DOUBLE_THREE:
        if len(defenses) is 0 or defenses[0][2] < Status.FOUR:
          return 10 if maxPlayer else 0

    if len(attacks) > 0:
      random.shuffle(attacks)
      alpha, beta = 0, 10
      for r, c, status in attacks:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        if status < Status.FOUR:
          val = self.alphaBetaPruning(board, opponent, depth + 1, alpha, beta, not maxPlayer)
        else:
          val = self.alphaBetaPruning(board, opponent, depth, alpha, beta, not maxPlayer)
        board.data[r][c] = 0
        board.status = st
        if maxPlayer:
          alpha = val if alpha < val else alpha
        else:
          beta = val if beta > val else beta
        if alpha >= beta:
          return alpha if maxPlayer else beta

    if len(defenses) > 0:
      matrix = [[0 for r in range(board.size)] for c in range(board.size)]
      possibles = []
      for r, c, status in defenses:
        sr = r - 4 if r - 4 >= 0 else 0
        sc = c - 4 if c - 4 >= 0 else 0
        er = r + 4 if r + 4 < board.size else board.size - 1
        ec = c + 4 if c + 4 < board.size else board.size - 1
        for r2 in range(sr, er + 1):
          for c2 in range(sc, ec + 1):
            if board.status[stone][r2][c2] is not Status.FORBIDDEN:
              matrix[r2][c2] = 1
              
      for r in range(board.size):
        for c in range(board.size):
          if matrix[r][c] is 1:
            possibles.append((r, c))

      random.shuffle(possibles)
      alpha, beta = 0, 5
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        val = self.alphaBetaPruning(board, opponent, depth + 1, alpha, beta, not maxPlayer)
        board.data[r][c] = 0
        board.status = st
        alpha = val if alpha < val else alpha
        if maxPlayer:
          alpha = val if alpha < val else alpha
        else:
          beta = val if beta > val else beta
        if alpha >= beta:
          return alpha if maxPlayer else beta

      #pipeWrite('MESSAGE defense possibles: %s' % str(possibles))
      #return random.choice(possibles)

    return 5



import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()

