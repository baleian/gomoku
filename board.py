#-*- coding: utf-8 -*-

import copy


class Stone(object):
  NONE = 0
  BLACK = 1
  WHITE = 2
  def __setattr__(self, *_):
    raise TypeError


class Status(object):
  NONE = 0
  FIVE = 1
  FORBIDDEN = 2
  STRAIGHT_FOUR = 3
  DOUBLE_FOUR = 4
  FOUR = 5
  DOUBLE_THREE = 6
  THREE = 7
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
    self.rule = rule if rule is not None else self.size
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


  def popStone(self, r, c):
    if not self.isRange(r, c):
      return -1

    if self.data[r][c] is Stone.NONE:
      return Stone.NONE

    ret = self.data[r][c]
    self.data[r][c] = Stone.NONE
    stone = ret
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    self.updateStatusNearBy(r, c, stone)
    self.updateStatusNearBy(r, c, opponent)

    return ret


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

    return Status.NONE


  
  def debugPrint(self):
    chrs = ['┼', '①', '②', '③', '④', '⑤', '⑥', '⑦']
    for r in range(self.size):
      for c in range(self.size):
        if self.data[r][c] is 1:
          sys.stdout.write('●')
        elif self.data[r][c] is 2:
          sys.stdout.write('○')
        else:
          if self.status[1][r][c] is not Status.NONE:
            sys.stdout.write(chrs[self.status[1][r][c]])
          else:
            sys.stdout.write('┼')
      sys.stdout.write('\t')
      for c in range(self.size):
        if self.data[r][c] is 1:
          sys.stdout.write('●')
        elif self.data[r][c] is 2:
          sys.stdout.write('○')
        else:
          if self.status[2][r][c] is not Status.NONE:
            sys.stdout.write(chrs[self.status[2][r][c]])
          else:
            sys.stdout.write('┼')
      sys.stdout.write('\r\n')
      sys.stdout.flush()
    sys.stdout.write('\r\n')
    sys.stdout.flush()

import sys