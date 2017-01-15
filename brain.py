import random

class Brain:
  def __init__(self):
    pass

  def predict(self, board, stone, rule):
    data = board.getData()
    size = board.getSize()
    opponent = 2 if stone is 1 else 1

    possibles = []
    ret = None

    for r in range(size):
      for c in range(size):
        valid = rule.verify(board, r, c, stone)
        
        if valid.isForbidden:
          continue

        if valid.isWin:
          ret = (r, c)
          break

        opvalid = rule.verify(board, r, c, opponent)
        if opvalid.isWin:
          ret = (r, c)

        possibles.append((r, c))

    return ret if ret is not None else random.choice(possibles)