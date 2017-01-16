import random

class Brain:
  def __init__(self):
    pass

  def _predict(self, board, stone, rule, depth):
    opponent = 2 if stone is 1 else 1
    size = board.getSize()

    tr, tc = -1, -1
    moreThink = False
    possibles = []
    list10 = []

    for r in range(size):
      for c in range(size):
        valid = rule.verify(board, r, c, stone)
        valid2 = rule.verify(board, r, c, opponent)

        if valid.isForbidden:
          continue
        
        possibles.append((r, c))

        if valid.isWin:
          if depth is 2:
            pipeWrite('MESSAGE valid iswin!(%d, %d, %d) = %d' % (r, c, 10, depth))
          return r, c, 10
        if valid2.isWin:
          tr, tc = r, c
          moreThink = True
        if valid.n4mok >= 2:
          list10.append((r, c))
          moreThink = True
        if valid.n4mok > 0 or valid2.n4mok > 0:
          moreThink = True

    if tr is not -1 and tc is not -1:
      if depth is 2:
        pipeWrite('MESSAGE valid2 iswin!(%d, %d, %d) = %d' % (tr, tc, 5, depth))
      return tr, tc, 5

    if len(list10) > 0:
      r, c = random.choice(list10)
      if depth is 2:
        pipeWrite('MESSAGE valid n4mok >= 2!(%d, %d, %d) = %d' % (r, c, 10, depth))
      return r, c, 10

    if not moreThink:
      r, c = random.choice(possibles)
      return r, c, 5

    if depth is 1:
      r, c = random.choice(possibles)
      return r, c, 5

    list5 = []
    list0 = []
    for r, c in possibles:
      board.putStone(r, c, stone)
      rr, cc, ww = self._predict(board, opponent, rule, depth - 1)
      board.popStone(r, c)

      ww = 10 - ww
      if ww is 10:
        return r, c, 10
      elif ww is 5:
        list5.append((r, c))
      else:
        list0.append((r, c))
        

    if len(list5) > 0:
      r, c = random.choice(list5)
      return r, c, 5

    r, c = random.choice(list0)
    return r, c, 0


  def predict(self, board, stone, rule):
    r, c, w = self._predict(board, stone, rule, 2)
    if w is not 5:
      pipeWrite('MESSAGE predict!(%d, %d, %d)' % (r, c, w))
    return r, c


  def _minimax(self, board, stone, rule, depth):
    if depth is 0:
      return 5
    
    opponent = 2 if stone is 1 else 1
    size = board.getSize()
    isMinimax = False
    possibles = []

    retMax = 0
    for r in range(size):
      for c in range(size):
        valid = rule.verify(board, r, c, stone)
        if valid.isWin:
          return 10
        valid2 = rule.verify(board, r, c, opponent)
        if valid2.isWin:
          return 10
        if valid.n4mok > 0:
          isMinimax = True
        if valid2.n4mok > 0:
          isMinimax = True

        if not valid.isForbidden:
          possibles.append((r, c))
    
    if isMinimax:
      for r, c in possibles:
        board.putStone(r, c, stone)
        ret = 10 - self._minimax(board, opponent, rule, depth - 1)
        board.popStone(r, c)
        if retMax < ret:
          retMax = ret

    return retMax


  def minimax(self, board, stone, rule, depth=2):
    opponent = 2 if stone is 1 else 1
    size = board.getSize()

    possibles = []
    list10 = []
    list5 = []
    list0 = []

    isMinimax = False

    for r in range(size):
      for c in range(size):
        valid = rule.verify(board, r, c, stone)
        if valid.isWin:
          return r, c
        valid2 = rule.verify(board, r, c, opponent)
        if valid2.isWin:
          return r, c
        if valid.n4mok > 0:
          isMinimax = True
        if valid2.n4mok > 0:
          isMinimax = True

        if not valid.isForbidden:
          possibles.append((r, c))

    if isMinimax:
      pipeWrite("MESSAGE IsMINIMAX!!!!")
      for r, c in possibles:
        board.putStone(r, c, stone)
        ret = 10 - self._minimax(board, opponent, rule, depth - 1)
        board.popStone(r, c)

        if ret is 10:
          list10.append((r, c))
        elif ret is 5:
          list5.append((r, c))
        else:
          list0.append((r, c))
              
      if len(list10) > 0:
        return random.choice(list10)

      if len(list5) > 0:
        return random.choice(list5)

      if len(list0) > 0:
        return random.choice(list0)        

    return random.choice(possibles)



import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()

