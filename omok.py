from board import Board
from rule import Rule


class Omok:
  def __init__(self):
    self._rule = Rule.factory('renju') # default renju rule
    self._board = Board(size=15) # default board size
    self._myStone = 1 # default my stone is black


  def getRule(self):
    return self._rule


  def getBoard(self):
    return self._board


  def newGame(self, size=None, myStone=1):
    self._board.init(size)
    self._myStone = myStone
    

  def putStone(self, r, c, who):
    stone = self._myStone

    if who is not 1: # not my turn
      stone = 2 if stone is 1 else 1

    return self._board.putStone(r, c, stone)

