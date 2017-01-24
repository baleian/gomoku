#-*- coding: utf-8 -*-
from board import Stone, Status
from threading import Timer
import subprocess
import re
import random

class Brain:
  @property
  def xl_path(self):
    return self._xl_path

  @xl_path.setter
  def xl_path(self, value):
    self._xl_path = value


  def __init__(self):
    self._xl_path = 'D:\\Beom\\workspace\\gomoku'
    pass

  def predict(self, board, stone):
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK

    # 내가 공격으로 잡을 수 있거나 어쩔수 없이 수가 정해지는 경우는 
    # xl-engine이 해결해 줄 거다
    r, c = self._predict(board, stone, timeout=1)
    if r is not -1 and c is not -1:
      pipeWrite('MESSAGE PREDICT!!!')
      return r, c

    # 방어가 필요한 경우는
    # 상대방의 공격 수 근처에서 상대방 eveluate가 0이 안되게 만들 수 있는곳이 있는지
    # 찾아서 선택
    defenses = []
    for r in range(board.size):
      for c in range(board.size):
        if board.status[opponent][r][c] >= Status.DOUBLE_THREE:
          defenses.append((r, c))
    if len(defenses) > 0:
      nears = [[0 for c in range(board.size)] for r in range(board.size)]
      for r, c in defenses:
        sr = r - 4 if r - 4 >= 0 else 0
        sc = c - 4 if c - 4 >= 0 else 0
        er = r + 4 if r + 4 < board.size else board.size - 1
        ec = c + 4 if c + 4 < board.size else board.size - 1
        for r2 in range(sr, er + 1):
          for c2 in range(sc, ec + 1):
            if board.status[stone][r2][c2] is not Status.FORBIDDEN:
              nears[r2][c2] = 1
      defenses = []
      for r in range(board.size):
        for c in range(board.size):
          if nears[r][c] is 1:
            defenses.append((r, c))
      random.shuffle(defenses)
      for r, c in defenses:
        board.putStone(r, c, stone)
        r2, c2 = self._predict(board, opponent, timeout=0.3, log=False)
        board.traceBack()
        if r2 is -1 and c2 is -1:
          pipeWrite('MESSAGE CHOICE DEFENSE.')
          return r, c

    # 그 외에는 가중치에 따라서 랜덤하게 선택한다
    candies = []
    for r in range(board.size):
      for c in range(board.size):
        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue
        if board.status[stone][r][c] >= Status.NEAR:
          candies.append((r, c, board.status[stone][r][c] + random.randrange(1, 10)))
        if board.status[opponent][r][c] >= Status.NEAR:
          candies.append((r, c, board.status[opponent][r][c] + random.randrange(0, 9)))
    random.shuffle(candies)
    candies.sort(key=lambda x: x[2], reverse=True)
    
    pipeWrite('MESSAGE RANDOM CHOICE.')
    return candies[0][0], candies[0][1]


  def _predict(self, board, stone, timeout=1, log=True):
    proc = subprocess.Popen(
      self.xl_path + "\\xl-engine\\Release\\pbrain-xl-engine.exe",
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE
    )

    proc.stdin.write('START 15\n')
    proc.stdin.write('INFO MAX_MEMORY 83886080\n')
    proc.stdin.write('INFO TIMEOUT_TURN 3000\n')
    proc.stdin.write('INFO GAME_TYPE 0\n')
    proc.stdin.write('INFO RULE 4\n')
    proc.stdin.write('INFO TIME_LEFT 30000\n')
    proc.stdin.write('BOARD\n')
    for r, c, stone2, status in board.stack:
      proc.stdin.write('%d,%d,%d\n' % (r, c, 1 if stone2 is stone else 2))
    proc.stdin.write('DONE\n')
    
    timer = Timer(timeout, lambda p: p.kill(), [proc])
    timer.start()
    proc.wait()
    timer.cancel()
    out, err = proc.communicate()

    eveluate = re.findall(r'eveluate=[0-9]+', out)
    depth = re.findall(r'depth=[0-9]+', out)
    pos = re.findall(r'pos=[0-9]+,[0-9]+', out)

    if log:
      lines = out.split('\n')
      for line in lines:
        pipeWrite('MESSAGE %s' % line)

    if len(pos) > 0:
      if len(eveluate) > 0:
        if int(eveluate[0][9:]) is not 0:
          return -1, -1
      r, c = pos[0][4:].split(',')
      r, c = int(r), int(c)
      return r, c

    return -1, -1



import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()
