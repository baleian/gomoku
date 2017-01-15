import re

class Rule():
  @staticmethod
  def factory(rule):
    if rule is 'renju': return Renju()
    else: return Renju()


class Valid():
  def __init__(self, isWin, isForbidden):
    self.isWin = isWin
    self.isForbidden = isForbidden


class Renju():
  def verify(self, board, r, c, stone):
    if not board.putStone(r, c, stone):
      return Valid(isWin=False, isForbidden=True)
    patterns = board.getPatterns(r, c)
    board.popStone(r, c)

    return Valid(
      isWin=self._isWin(patterns, stone),
      isForbidden=self._isForbidden(patterns, stone)
    )


  def _isWin(self, patterns, stone):
    rgx = r'[^1]11111[^1]' if stone is 1 else r'22222'
    for i in range(4):
      if re.search(rgx, patterns[i]): 
        return True

    return False


  def _isForbidden(self, patterns, stone):
    if stone is 2:
      return False

    if self._isWin(patterns, stone):
      return False

    if (self._sixmok(patterns) or
      self._check33(patterns) or
      self._check44(patterns)):
      return True

    return False


  def _sixmok(self, patterns):
    for i in range(4):
      if re.search(r'111111', patterns[i]): 
        return True
    return False


  def _check33(self, patterns):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if (re.search(r'001110[^1]', s) or 
        re.search(r'[^1]011100', s) or
        re.search(r'[^1]011010[^1]', s) or 
        re.search(r'[^1]010110[^1]', s)):
        cnt = cnt + 1
    return cnt >= 2


  def _check44(self, patterns):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if (re.search(r'01111[^1]', s) or 
        re.search(r'[^1]11110', s) or
        re.search(r'[^1]10111[^1]', s) or
        re.search(r'[^1]11011[^1]', s) or
        re.search(r'[^1]11101[^1]', s)):
        cnt = cnt + 1
      if (re.search(r'[^1]1011101[^1]', s) or 
        re.search(r'[^1]11011011[^1]', s) or 
        re.search(r'[^1]111010111[^1]', s)):
        cnt = cnt + 2
    return cnt >= 2


