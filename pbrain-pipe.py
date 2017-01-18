import sys
from board import Board, Stone
from rule import Renju
from brain import Brain


def start(cmd):
  boardSize = int(cmd[1])
  if boardSize is not 15:
    pipeWrite('ERROR Unsupport size of board, supported size is 15!')
    return

  board.init(size=boardSize)

  global myStone, opStone
  myStone = Stone.WHITE
  opStone = Stone.BLACK
  pipeWrite('OK')


def begin(cmd):
  global myStone, opStone
  myStone = Stone.BLACK
  opStone = Stone.WHITE

  mid = board.size / 2
  if board.putStone(mid, mid, myStone) is False:
    pipeWrite('ERROR not valid begin position %d,%d' % (mid, mid))
    return
  pipeWrite("%d,%d" % (mid, mid))


def turn(cmd):
  r, c = cmd[1].split(',')
  # r, c = brain.predict(board, opStone)
  # r, c = raw_input().split(',')
  # r, c = int(r), int (c)
  if board.putStone(int(r), int(c), opStone) is False:
    pipeWrite('ERROR not valid turn input %s,%s' % (int(r), int(c)))
    return
  # print 'after stone=', opStone, 'pos=', r, ',', c
  # board.debugPrint()
  # raw_input()
  
  r, c = brain.predict(board, myStone)
  # r, c = raw_input().split(',')
  # r, c = int(r), int (c)
  if board.putStone(r, c, myStone) is False:
    pipeWrite('ERROR not valid predict result %s,%s' % (r, c))
    return
  # print 'after stone=', myStone, 'pos=', r, ',', c
  # board.debugPrint()
  # raw_input()
  pipeWrite("%d,%d" % (r, c))
  


def board(cmd):
  while True:
    cmd = raw_input()
    pipeWrite('MESSAGE board cmd: %s' % cmd)
    if cmd is 'DONE': 
      return
    r, c, who = cmd.split(',')
    if who is 1:
      if board.putStone(r, c, myStone) is False:
        break
    elif who is 2:
      if board.putStone(r, c, opStone) is False:
        break
    else:
      break

  pipeWrite('ERROR Error while updating board!')


def about(cmd):
  pipeWrite('BeomPaGo v1.0, Beomjoon Lee<balein90@gmail.com>')


def end(cmd):
  sys.exit(0)


def info(cmd):
  cmdInfo = {
    'MAX_MEMORY': info_max_memory, 
    'TIMEOUT_MATCH': info_timeout_match, 
    'TIMEOUT_TURN': info_timeout_turn,
    'RULE': info_rule,
    'GAME_TYPE': info_game_type,
    'TIME_LEFT': info_time_left,
    'FOLDER': info_folder
  }

  cmdInfo.get(cmd[1], unknownCmd)(cmd[2])
  

def info_max_memory(mem):
  if int(mem) < 0:
    pipeWrite('ERROR Unsupport range of max_memory!')
    return


def info_timeout_match(time):
  if int(time) < 0:
    pipeWrite('ERROR Unsupport range of timeout_match!')
    return 


def info_timeout_turn(time):
  if int(time) < 0:
    pipeWrite('ERROR Unsupport range of timeout_turn!')
    return


def info_rule(type):
  if int(type) is not 4:
    pipeWrite('ERROR Unsupport rule, supported rule is renju & single game!')
    return
  board.rule = Renju()


def info_game_type(tmp=None):
  return


def info_time_left(tmp=None):
  return


def info_folder(tmp=None):
  return


def unknownCmd(tmp=None):
  pipeWrite('ERROR Unknown Command!')


def pipeWrite(str):
  sys.stdout.write(str)
  sys.stdout.write('\n')
  sys.stdout.flush()




###############################################################################
# Main
###############################################################################
board = Board(size=15, rule=Renju())
brain = Brain()
myStone = Stone.NONE
opStone = Stone.NONE


if __name__ == "__main__":
  cmdMain = {
    'INFO': info,
    'START': start, 
    'BEGIN': begin, 
    'TURN': turn, 
    'BOARD': board,
    'ABOUT': about, 
    'END': end
  }

  while True:
    cmd = raw_input().upper()
    pipeWrite('MESSAGE input cmd: %s' % cmd)
    cmd = cmd.split()
    cmdMain.get(cmd[0], unknownCmd)(cmd)
###############################################################################
