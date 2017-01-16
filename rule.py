import re

class Rule():
  @staticmethod
  def factory(rule):
    if rule is 'renju': return Renju()
    else: return Renju()


class Valid():
  def __init__(self, isWin, isForbidden, n3mok, n4mok):
    self.isWin = isWin
    self.isForbidden = isForbidden
    self.n3mok = n3mok
    self.n4mok = n4mok


class Renju():
  def verify(self, board, r, c, stone):
    if not board.putStone(r, c, stone):
      return Valid(isWin=False, isForbidden=True, n3mok=0, n4mok=0)
    patterns = board.getPatterns(r, c)
    board.popStone(r, c)

    isWin = self._isWin(patterns, stone)
    isForbidden = False if isWin else self._isForbidden(patterns, stone)
    n3mok = 0 if isForbidden else self._n3mok(patterns, stone)
    n4mok = 0 if isForbidden else self._n4mok(patterns, stone)
    return Valid(isWin, isForbidden, n3mok, n4mok)


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

    if (self._sixmok(patterns, stone) or
      self._check33(patterns, stone) or
      self._check44(patterns, stone)):
      return True

    return False


  def _sixmok(self, patterns, stone):
    for i in range(4):
      if re.search(r'111111', patterns[i]): 
        return True
    return False


  def _check33(self, patterns, stone):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if (re.search(r'001110[^1]', s) or 
        re.search(r'[^1]011100', s) or
        re.search(r'[^1]011010[^1]', s) or 
        re.search(r'[^1]010110[^1]', s)):
        cnt = cnt + 1
    return cnt >= 2


  def _check44(self, patterns, stone):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if stone is 1:
        if re.search(r'[^1]01111[^1]', s) or re.search(r'[^1]11110[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]10111[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]11011[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]11101[^1]', s): cnt = cnt + 1
      elif stone is 2:
        if re.search(r'02222', s) or re.search(r'22220', s): cnt = cnt + 1
        if re.search(r'20222', s): cnt = cnt + 1
        if re.search(r'22022', s): cnt = cnt + 1
        if re.search(r'22202', s): cnt = cnt + 1

    return cnt >= 2


  def _n3mok(self, patterns, stone):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if stone is 1:
        if re.search(r'001110[^1]', s) or re.search(r'[^1]011100', s): cnt = cnt + 1
        if re.search(r'[^1]011010[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]010110[^1]', s): cnt = cnt + 1
      elif stone is 2:
        if re.search(r'002220[^2]', s) or re.search(r'[^2]022200', s): cnt = cnt + 1
        if re.search(r'020220', s): cnt = cnt + 1
        if re.search(r'022020', s): cnt = cnt + 1
    
    return cnt


  def _n4mok(self, patterns, stone):
    cnt = 0
    for i in range(4):
      s = patterns[i]
      if stone is 1:
        if re.search(r'[^1]01111[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]11110[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]10111[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]11011[^1]', s): cnt = cnt + 1
        if re.search(r'[^1]11101[^1]', s): cnt = cnt + 1
      elif stone is 2:
        if re.search(r'02222', s): cnt = cnt + 1
        if re.search(r'22220', s): cnt = cnt + 1
        if re.search(r'20222', s): cnt = cnt + 1
        if re.search(r'22022', s): cnt = cnt + 1
        if re.search(r'22202', s): cnt = cnt + 1
    
    return cnt
