from copy import copy, deepcopy
from board import Stone, Status
import random

class Brain:
  def __init__(self):
    pass


  def minimax(self, board, stone, maxDepth, depth, isDebug=False):
    if depth > maxDepth:
      return (5, depth)

    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    size = board.size

    dangers = []
    attacks = []
    defends = []
    possibles = []

    # 바로 끝나는 경우
    for r in range(size):
      for c in range(size):
        if board.status[stone][r][c] is Status.FIVE:
          return (10, depth)

        if board.status[opponent][r][c] is Status.FIVE:
          dangers.append((r, c))

        if (
          board.status[stone][r][c] is Status.STRAIGHT_FOUR or
          board.status[stone][r][c] is Status.DOUBLE_FOUR or
          board.status[stone][r][c] is Status.FOUR or 
          board.status[stone][r][c] is Status.DOUBLE_THREE or
          board.status[stone][r][c] is Status.THREE
        ):
          attacks.append((r, c, board.status[stone][r][c]))

        if (
          board.status[opponent][r][c] is Status.STRAIGHT_FOUR or
          board.status[opponent][r][c] is Status.DOUBLE_FOUR or
          board.status[opponent][r][c] is Status.FOUR or 
          board.status[stone][r][c] is Status.DOUBLE_THREE
          # board.status[stone][r][c] is Status.DOUBLE_THREE
        ):
          defends.append((r, c, board.status[opponent][r][c]))

        if board.status[stone][r][c] is not Status.FORBIDDEN:
          possibles.append((r, c))


    # 이곳에 안 두면 지는 경우
    # 어쩔 수 없이 두고 결과 리턴
    for r, c in dangers:
      st = deepcopy(board.status)
      board.putStone(r, c, stone)
      val, d = self.minimax(board, opponent, maxDepth, depth + 1)
      board.data[r][c] = 0
      board.status = st
      return (10 - val, d)
      

    # 공격 루트가 있으면 우선 순위에 따라 공격해보고 이기는 곳이 있으면 리턴
    attacks.sort(key=lambda x : x[2], reverse=True)
    for r, c, stat in attacks:
      st = deepcopy(board.status)
      board.putStone(r, c, stone)
      val, d = self.minimax(board, opponent, maxDepth, depth + 1)
      board.data[r][c] = 0
      board.status = st
      if val is 0:
        return 10, d


    return (5, depth)
    # TODO: 
    # 상대방 공격 루트가 있으면 막을 수 있는지 체크
    # depth를 넓히면 막다가도 역공해버릴 수도 있지만, 
    # 일단 작은 뎁스로 막는지 성공하면 바로 return하여 성능 높이자
    if len(defends) > 0:
      random.shuffle(possibles)
      minD = maxDepth
      for r, c in possibles:
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        val, d = self.minimax(board, opponent, maxDepth, depth + 1)
        board.data[r][c] = 0
        board.status = st
        if val < 10:  # 내가 이기거나 비기면 바로 리턴. depth를 늘리면 내가 이기는 경우가 있을때 리턴 가능
          return 10 - val, d
        else: # 내가 지는 경우 최소 몇전째 depth에서 지는지 기록
          if minD > d:
            minD = d

      # 최소 비기는 경우가 없을 때 지는 것이므로 지는 경우로 리턴
      return 0, minD
    
    # 그 외 판단이 어려운 경우 비긴다고 가정
    return (5, depth)
 

  def predict(self, board, stone):
    # 앞으로 N수 앞까지 봐서 점수가 가장 높은 곳 중에 predict 시키자
    opponent = Stone.WHITE if stone is Stone.BLACK else Stone.BLACK
    score = [[(0, 0) for r in range(board.size)] for c in range(board.size)]

    for r in range(board.size):
      for c in range(board.size):
        if board.status[stone][r][c] is Status.FORBIDDEN:
          continue

        if board.status[stone][r][c] is Status.FIVE:
          score[r][c] = (10, 0)
          continue

        # 상대방이 5를 만들 수 있는 경우를 고려 안해도 되는 이유가
        # 어차피 그 곳을 안막는 모든 다른 수는 0점이 될 것이고 그 곳만 5점 또는 10점이 될 것이므로
        # 내 입장만 고려하면 된다!

        # 여기 둔 경우 상대방이 뭘 두더라도 내가 최대로 뽑을 수 있는 점수를 기록한다
        st = deepcopy(board.status)
        board.putStone(r, c, stone)
        val, d = self.minimax(board, opponent, 4, 1, r is 7 and c is 4) # 앞으로 5수를 더 두어본다
        score[r][c] = (10 - val, d)
        board.data[r][c] = 0
        board.status = st

    for c in range(board.size):
      str1 = ''
      for r in range(board.size):
        str1 = str1 + ('(%2d,%2d)' % score[r][c])
      pipeWrite('MESSAGE %s' % str1)

    return 0, 0



import sys
def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()

