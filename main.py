# -*- coding: utf8 -*-
import sys
import os
from omok import Omok


def printBoard(board, lr, lc):
  for r in range(15):
    for c in range(15):
      stone = board[r][c]
      if r is lr and c is lc:
        sys.stdout.write("%s" % 
          { 1: '★', 2: '☆' }.get(stone, ' '))
      else:
        sys.stdout.write("%s" % 
          { 0: '┼', 1: '●', 2: '○', 3: 'Ｘ' }.get(stone, ' '))
    sys.stdout.write('\n')
  sys.stdout.flush()


def userMove():
  r, c = raw_input("input row col: ").split()
  return int(r), int(c)


def aiMove():
  r, c = int(raw_input("ai row col: ").split())
  return r, c  


###############################################################################
if __name__ == "__main__":
  omok = Omok()

  while True:
    omok.newGame()
    r, c = 7, 7
    omok.putStone(r, c)

    while not omok.isGameOver():
      board, current = omok.getBoardStat()
      printBoard(board, r, c)
      print {1: 'black', 2: 'white'}.get(current, ' '), 'turn'

      while True:
        r, c = userMove()
        if omok.putStone(r, c): break
        print 'forbidden.'

    board, current = omok.getBoardStat()
    printBoard(board, r, c)
    print 'winner: ', {1: 'black', 2: 'white'}.get(omok.getWinner(), 'draw')
    raw_input()
###############################################################################
