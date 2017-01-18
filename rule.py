from abc import ABCMeta, abstractmethod
import re


class Rule():
  __metaclass__ = ABCMeta

  @abstractmethod
  def isFiveInRow(self, row, stone): pass

  @abstractmethod
  def isOverLine(self, row, stone): pass

  @abstractmethod
  def isFour(self, row, stone): pass

  @abstractmethod
  def isStraightFour(self, row, stone): pass

  @abstractmethod
  def isThree(self, row, stone): pass

  @abstractmethod
  def isDoubleFour(self, rows, stone): pass

  @abstractmethod
  def isDoubleThree(self, rows, stone): pass

  @abstractmethod
  def isForbidden(self, rows, stone): pass



class BasicRule(Rule):
  def isFiveInRow(self, row, stone):
    if stone is 1:
      return re.search(r'[^1]11111[^1]', row)
    if stone is 2:
      return re.search(r'22222', row)
    return False


  def isOverLine(self, row, stone):
    if stone is 1:
      return re.search(r'111111', row)
    return False


  def isFour(self, row, stone):
    if stone is 1:
      return (
        self.isStraightFour(row, stone) or
        re.search(r'211110[^1]', row) or
        re.search(r'[^1]011112', row) or
        re.search(r'[^1]10111[^1]', row) or
        re.search(r'[^1]11011[^1]', row) or
        re.search(r'[^1]11101[^1]', row)
      )
    if stone is 2:
      return (
        self.isStraightFour(row, stone) or
        re.search(r'122220', row) or
        re.search(r'022221', row) or
        re.search(r'20222', row) or
        re.search(r'22022', row) or
        re.search(r'22202', row)
      )
    return False


  def isStraightFour(self, row, stone):
    if stone is 1:
      return re.search(r'[^1]011110[^1]', row)
    if stone is 2:
      return re.search(r'022220', row)
    return False


  def isThree(self, row, stone):
    if stone is 1:
      return (
        re.search(r'[^1]001110[^1]', row) or
        re.search(r'[^1]010110[^1]', row) or
        re.search(r'[^1]011010[^1]', row) or
        re.search(r'[^1]011100[^1]', row)
      )
    if stone is 2:
      return (
        re.search(r'002220', row) or
        re.search(r'020220', row) or
        re.search(r'022020', row) or
        re.search(r'022200', row)
      )
    return False


  def isDoubleFour(self, rows, stone):
    cnt = 0
    for row in rows:
      if self.isFour(row, stone):
        cnt = cnt + 1
    return cnt >= 2


  def isDoubleThree(self, rows, stone):
    cnt = 0
    for row in rows:
      if self.isThree(row, stone):
        cnt = cnt + 1
    return cnt >= 2


  def isForbidden(self, rows, stone):
    return False



class Renju(BasicRule):
  # override
  def isForbidden(self, rows, stone):
    if stone is 2:
      return False

    for row in rows:
      if self.isFiveInRow(row, stone):
        return False

    for row in rows:
      if self.isOverLine(row, stone):
        return True

    if self.isDoubleFour(rows, stone):
      return True

    if self.isDoubleThree(rows, stone):
      return True

    return False