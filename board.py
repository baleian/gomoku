import copy

class Board:
  def __init__(self, size):
    self._size = size
    self._board = None
    self._remain = None
    self.init()


  def init(self):
    self._board = [[0 for c in range(self._size)] for r in range(self._size)]
    self._remain = self._size * self._size


  def getStone(self, r, c):
    return self._board[r][c]


  def putStone(self, r, c, stone):
    if not self.isRange(r, c):
      return False

    if self._board[r][c] is not 0:
      return False

    self._board[r][c] = stone
    self._remain = self._remain - 1
    return True


  def popStone(self, r, c):
    ret = self._board[r][c]
    self._board[r][c] = 0

    if ret is not 0:
      self._remain = self._remain + 1
    return ret


  def getSize(self):
    return self._size
    

  def getRemain(self):
    return self._remain


  def getPatterns(self, r, c):
    patterns = ['' for i in range(4)]
    dir = [[1, 0], [0, 1], [1, 1], [1, -1]]
    for i in range(4):
      tr, tc = r - 5*dir[i][0], c - 5*dir[i][1]
      for j in range(11):
        if self.isRange(tr, tc):
          patterns[i] = patterns[i] + str(self._board[tr][tc])
        tr, tc = tr + dir[i][0], tc + dir[i][1]
    return patterns


  def getBoardDump(self):
    return copy.deepcopy(self._board)


  def isRange(self, r, c):
    return r >= 0 and c >= 0 and r < self._size and c < self._size