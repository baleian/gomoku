from board import Board
from rule import Rule

class Omok:
  def __init__(self):
    self._size = 15
    self._current = None
    self._winner = None
    self._rule = Rule.factory('renju')
    self._board = Board(self._size)


  def newGame(self):
    self._current = 1
    self._winner = None
    self._board.init()


  def isGameOver(self):
    return self._winner is not None or self._board.getRemain() is 0
    

  def putStone(self, r, c):
    if self.isGameOver():
      return False
    
    valid = self._rule.verify(self._board, r, c, self._current)

    if valid.isForbidden:
      return False

    if valid.isWin:
      self._winner = self._current

    self._board.putStone(r, c, self._current)    
    self._current = 2 if self._current is 1 else 1
    return True


  def getWinner(self):
    return self._winner


  def whoseTurn(self):
    return self._current


  def getBoardStat(self):
    board = self._board.getBoardDump()
    current = self._current

    for r in range(self._size):
      for c in range(self._size):
        if board[r][c] is 0:
          valid = self._rule.verify(self._board, r, c, current)
          if valid.isForbidden and not valid.isWin:
            board[r][c] = 3
    
    return board, current