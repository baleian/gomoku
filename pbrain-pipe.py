import sys
from board import Board, Stone
from rule import Renju
from brain import Brain



################################################################################
# Global Values
################################################################################
mBoard = Board(size=15, rule=Renju())
mBrain = Brain()
myStone = Stone.NONE
opStone = Stone.NONE
################################################################################


def start(cmd):
  boardSize = int(cmd[1])
  if boardSize is not 15:
    pipeWrite('ERROR Unsupport size of board, supported size is 15!')
    return

  mBoard.init(size=boardSize)

  global myStone, opStone
  myStone = Stone.WHITE
  opStone = Stone.BLACK
  pipeWrite('OK')


def begin(cmd):
  global myStone, opStone
  myStone = Stone.BLACK
  opStone = Stone.WHITE

  mid = mBoard.size / 2
  if mBoard.putStone(mid, mid, myStone) is False:
    pipeWrite('ERROR not valid begin position %d,%d' % (mid, mid))
    return
  pipeWrite("%d,%d" % (mid, mid))


def turn(cmd):
  r, c = cmd[1].split(',')
  r, c = int(r), int (c)
  if mBoard.putStone(r, c, opStone) is False:
    pipeWrite('ERROR not valid turn input %s,%s' % (r, c))
    return
  
  # mBoard.debugPrint()
  # r, c = raw_input().split(',')
  # r, c = int(r), int (c)
  r, c = mBrain.predict(mBoard, myStone)
  if mBoard.putStone(r, c, myStone) is False:
    pipeWrite('ERROR not valid predict result %s,%s' % (r, c))
    return
  pipeWrite("%d,%d" % (r, c))
  # mBoard.debugPrint()
  

def board(cmd):
  mBoard.init()
  isFirst = True
  whostone = {1: None, 2: None}

  while True:
    cmd = raw_input()
    if cmd == 'DONE':
      break    
    r, c, who = cmd.split(',')
    r, c, who = int(r), int(c), int(who)

    if isFirst:
      isFirst = False
      global myStone, opStone
      if who is 1:
        myStone, opStone = Stone.BLACK, Stone.WHITE
      else:
        myStone, opStone = Stone.WHITE, Stone.BLACK  
      whostone[1], whostone[2] = myStone, opStone

    if mBoard.putStone(r, c, whostone[who]) is False:
      pipeWrite('ERROR not valid board input %s,%s,%s' % (r, c, who))
      return

  r, c = mBrain.predict(mBoard, myStone)
  if mBoard.putStone(r, c, myStone) is False:
    pipeWrite('ERROR not valid predict result %s,%s' % (r, c))
    return
  pipeWrite("%d,%d" % (r, c))


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
    'FOLDER': info_folder,
    'EVALUATE': info_evaluate
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
  mBoard.rule = Renju()


def info_game_type(tmp=None):
  return


def info_time_left(tmp=None):
  return


def info_folder(path):
  mBrain.xl_path = path


def info_evaluate(tmp=None):
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
    # pipeWrite('MESSAGE input cmd: %s' % cmd)
    cmd = cmd.split()
    cmdMain.get(cmd[0], unknownCmd)(cmd)
###############################################################################
