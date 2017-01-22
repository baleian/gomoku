#-*- coding: utf-8 -*-

import copy


class Stone(object):
  NONE = 0
  BLACK = 1
  WHITE = 2
  def __setattr__(self, *_):
    raise TypeError


class Status(object):
  FORBIDDEN = -1
  NONE = 0
  NEAR = 1
  TWO = 2
  THREE = 3
  DOUBLE_THREE = 4
  FOUR = 5
  DOUBLE_FOUR = 6
  STRAIGHT_FOUR = 7
  FIVE = 8
  def __setattr__(self, *_):
    raise TypeError


class Board:
  def __init__(self, size=None, rule=None):
    self.size = None
    self.rule = None
    self.data = None
    self.status = {
      Stone.BLACK: None,
      Stone.WHITE: None
    }
    self.init(size, rule)


  def init(self, size=None, rule=None):
    self.size = size if size is not None else self.size
    self.rule = rule if rule is not None else self.rule
    self.data = [
      [Stone.NONE for c in range(self.size)] 
      for r in range(self.size)
    ]
    
    self.status[Stone.BLACK] = [
      [Status.NONE for c in range(self.size)]
      for r in range(self.size)
    ]

    self.status[Stone.WHITE] = [
      [Status.NONE for c in range(self.size)]
      for r in range(self.size)
    ]


  def putStone(self, r, c, stone):
    if not self.isRange(r, c):
      return False

    if self.data[r][c] is not Stone.NONE:
      return False

    if self.status[stone][r][c] is Status.FORBIDDEN:
      return False

    self.data[r][c] = stone
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    self.updateStatusNearBy(r, c, stone)
    self.updateStatusNearBy(r, c, opponent)

    return True


  def isRange(self, r, c):
    return r >= 0 and c >= 0 and r < self.size and c < self.size


  def updateStatusNearBy(self, r, c, stone):
    sr = r - 4 if r - 4 >= 0 else 0
    sc = c - 4 if c - 4 >= 0 else 0
    er = r + 4 if r + 4 < self.size else self.size - 1
    ec = c + 4 if c + 4 < self.size else self.size - 1
    
    for r in range(sr, er + 1):
      for c in range(sc, ec + 1):
        if self.data[r][c] is not Stone.NONE:
          self.status[stone][r][c] = Status.FORBIDDEN
          continue
        rows = self.getPatterns(r, c, stone)
        if self.rule.isForbidden(rows, stone):
          self.status[stone][r][c] = Status.FORBIDDEN
        else:
          self.status[stone][r][c] = Status.NEAR
        
    for r in range(sr, er + 1):
      for c in range(sc, ec + 1):
        if self.status[stone][r][c] is Status.FORBIDDEN:
          continue
        rows = self.getPatterns(r, c, stone)
        self.status[stone][r][c] = self.getOrderStatus(rows, stone)


  def getPatterns(self, r, c, stone):
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    patterns = ['x' for i in range(4)]
    dir = [[1, 0], [0, 1], [1, 1], [1, -1]]
    for i in range(4):
      tr, tc = r - 5*dir[i][0], c - 5*dir[i][1]
      for j in range(11):
        if j is 5:
          patterns[i] = patterns[i] + str(stone)
        elif self.isRange(tr, tc):
          if self.data[tr][tc] is not Stone.NONE:
            patterns[i] = patterns[i] + str(self.data[tr][tc])
          elif self.status[stone][tr][tc] is Status.FORBIDDEN:
            patterns[i] = patterns[i] + str(opponent)
          else:  
            patterns[i] = patterns[i] + str(self.data[tr][tc])
        else:
          patterns[i] = patterns[i] + str(opponent)
        tr, tc = tr + dir[i][0], tc + dir[i][1]
      patterns[i] = patterns[i] + 'x'
    return patterns


  def getOrderStatus(self, rows, stone):
    for row in rows:
      if self.rule.isFiveInRow(row, stone):
        return Status.FIVE

    if self.rule.isForbidden(rows, stone):
      return Status.FORBIDDEN

    for row in rows:
      if self.rule.isStraightFour(row, stone):
        return Status.STRAIGHT_FOUR

    if self.rule.isDoubleFour(rows, stone):
      return Status.DOUBLE_FOUR

    for row in rows:
      if self.rule.isFour(row, stone):
        return Status.FOUR

    if self.rule.isDoubleThree(rows, stone):
      return Status.DOUBLE_THREE

    for row in rows:
      if self.rule.isThree(row, stone):
        return Status.THREE

    for row in rows:
      if self.rule.isTwo(row, stone):
        return Status.TWO

    return Status.NEAR

  
  def debugPrint(self):
    chrs = ['┼', '╋', '＋', '③', '④', '⑤', '⑥', '⑦', '⑧', '×']
    for c in range(self.size):
      for r in range(self.size):
        if self.data[r][c] is 1:
          sys.stdout.write('●')
        elif self.data[r][c] is 2:
          sys.stdout.write('○')
        else:
          sys.stdout.write(chrs[self.status[1][r][c]])
      sys.stdout.write('\t')
      for r in range(self.size):
        if self.data[r][c] is 1:
          sys.stdout.write('●')
        elif self.data[r][c] is 2:
          sys.stdout.write('○')
        else:
          sys.stdout.write(chrs[self.status[2][r][c]])
      sys.stdout.write('\r\n')
      sys.stdout.flush()
    sys.stdout.write('\r\n')
    sys.stdout.flush()

import sys