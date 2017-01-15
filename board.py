import copy


class Stone(object):
  NONE = 0
  BLACK = 1
  WHITE = 2
  def __setattr__(self, *_):
    raise TypeError


class Board:
  Stone = Stone()

  def __init__(self, size=None):
    self._size = None
    self._data = None
    self.init(size)


  def init(self, size=None):
    self._size = size if size is not None else self._size
    self._data = [[Stone.NONE for c in range(self._size)] for r in range(self._size)]


  def getSize(self):
    return self._size
    

  def getData(self):
    return self._data

    
  def putStone(self, r, c, stone):
    if not self.isRange(r, c):
      return False

    if self._data[r][c] is not Stone.NONE:
      return False

    self._data[r][c] = stone
    return True


  def popStone(self, r, c):
    if not self.isRange(r, c):
      return -1

    if self._data[r][c] is Stone.NONE:
      return Stone.NONE

    ret = self._data[r][c]
    self._data[r][c] = Stone.NONE
    return ret
    

  def getPatterns(self, r, c):
    patterns = ['x' for i in range(4)]
    dir = [[1, 0], [0, 1], [1, 1], [1, -1]]
    for i in range(4):
      tr, tc = r - 5*dir[i][0], c - 5*dir[i][1]
      for j in range(11):
        if self.isRange(tr, tc):
          patterns[i] = patterns[i] + str(self._data[tr][tc])
        tr, tc = tr + dir[i][0], tc + dir[i][1]
      patterns[i] = patterns[i] + 'x'
    return patterns


  def isRange(self, r, c):
    return r >= 0 and c >= 0 and r < self._size and c < self._size