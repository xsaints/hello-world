# draw board
# place 21 pieces
# human - move 1 piece
#   check if valid move
# comp - move 1 piece
#   check if valid move
# if attacked - check who wins
import random


def create_board():
  board= {}
  for i in range(0,8):
    for j in range(0,9):
      board[(i,j)]= []
  return board    

  
def blank_cells(player):
  if player== 1: # player1
    px= 0 # start at row 0 for player 1
  else:
    px= 5 # start at row 5 for player 2

  blanks= []
  while len(blanks) < 6: # 6 cells need to be blank
    x= random.randint(px, px+2)
    y= random.randint(0,8)
    if (x, y) not in blanks:
      blanks.append((x,y),)
  return blanks
  

def place_pieces(player, board, ranks):  
  if player== 1: # player1
    px= 0 # start at row 0 for player 1
  else:
    px= 5 # start at row 5 for player 2
  
  # blank 6 cells (27 cells, 21 playing pieces
  blanks= blank_cells(player)

  # convert ranks dict to list -- will return ranks only
  li_ranks= list(ranks)
  
  # create list of 0-20 to use to track random numbers generated
  trackr= []
  for i in range(0,21):
    trackr.append(i)
  
  # there are 21 items on trackr, each removed randomly when a rank/piece is
  # attached on an item/cell
  while trackr:
    for i in range(px, px + 3):
      for j in range(0, 9):
        if (i, j) in blanks:
          continue
        
        notFound= True
        while notFound:  
          x= random.randint(0, 20)        
          if x in trackr:
            trackr.remove(x)        
            notFound= False
            board[(i,j)]= [player, li_ranks[x], ranks[li_ranks[x]]]            
  return board

  
def disp_board(board):
  ''' just display the board '''  
  #for k, v in board.items():
  #  print(k, v)

  print('\n\n\t0\t1\t2\t3\t4\t5\t6\t7\t8\n')
  for i in range(0,8):
    #print('\n')
    print(str(i), end='')
    for j in range(0,9):
      cell= board[(i, j)]
      if cell != []:
        if cell[0] == 1:
          mark= 'X'
        elif cell[0] == 2:
          mark= 'Y'
        #else:
        #  mark= '.'
          
        print('\t'+ mark, end= '')
      else:
        print('\t.', end= '')
    print('\n')
  print('\n\n')        
    
    
def player_owns_cell(board, player, pt1):
  cell= board[pt1]
  #print(cell)
  if cell != []:  
    return player == cell[0] 
  else:
    return False # cell is blank and is not owned by player

    
def validxy_atcurrent(pt1, pt2):
  ''' check if p1 can move to p2'''
  x= pt1[0]
  y= pt1[1]

  validxy= []
  if x - 1 >= 0:
    validxy.append((x-1,y),)
  if x + 1 <= 7:
    validxy.append((x+1,y),)
  if y - 1 >= 0:
    validxy.append((x,y-1),)
  if y + 1 <= 8:
    validxy.append((x,y+1),)
  return (pt2 in validxy)


def check_win(board, player, pt1, pt2):
  ''' 
  Any one of the player's pieces can capture the opposing Flag. This includes the player's own Flag.
  Any piece eliminates the Private except the Spy and the Flag.

  Officers eliminate other officers that are lower in rank (e.g. a Four-Star General eliminates a Lieutenant Colonel).
  A Spy eliminates all officers (including the Five-Star General). Only the Private can eliminate the Spy.
  If both pieces are of the same rank, both are removed from the board (often called a "split" by most players and arbiters).
  If a Flag challenges the opponent's Flag, the challenging Flag prevails and wins the game.

  If a Flag reaches the opposite end or farthest rank of the board, the opponent has one turn left although it is not announced. After the turn, the player reveals the Flag. If the Flag was not challenged, the player wins the game. If it was challenged, the player loses.
  '''
  player  = board[pt1]
  defender= board[pt2]
  
  print('Player   {}'.format(player))
  print('Defender {}'.format(defender))  
  
  #player_wins= [True, 1] # 97 both sides lost, 98 defender wins final, 99 player/attacker wins final
  winner= [0, 0] # [player, how won]: 0,0- no winner yet, 99 there is a winner already

  if defender[1]== 'FL': # any player piece vs Flag, player wins and ends game(99)
    winner[0]= player[1]
    winner[1]= 99

  # player Spy or Flag vs Private, Private wins
  elif defender[1] in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6') and player[1] in ('S1', 'S2', 'FL'):
    winner[0]= defender[0]
    if player[1]== 'FL':
      winner[1]= 99

  elif player[2] > defender[2]: # General vs Colonel, player wins
    winner[0]= player[0]
    #if defender[1]== 'FL': # flag
    #  winner[1]= 99 # player wins, flag of defender captured
  '''  
  elif player[2]== defender[2]: # same value
    winner[0] = 0
    if defender[1]== 'FL': # flag
      winner[0]= player[0] # player wins, flag of defender captured
      winner[1]= 99
  '''  
  elif player[2] < defender[2]: # Colonel vs General, defender wins
    winner[0]= defender[0]
    if player[1]== 'FL': # Colonel vs Flag, defender wins and ends game(99)
      winner[1]= 99
  '''
  if winner[1] != 99:
    if player== 1 and player[1]== 'FL' and pt2[0] == 7:
      winner[0]= player
      winner[1]= 99
    elif player== 2 and player[1]== 'FL' and pt2[0] == 0:
      winner[0]= player
      winner[1]= 99
  '''
  
  
  
  if winner[0]== 0: # nobody won
    p1.append(board[pt1])
    p2.append(board[pt2])    
    board[pt1]= []
    board[pt2]= []
    
  elif winner[0]== player[0]:
    p2.append(board[pt2])  
    board[pt2]= board[pt1]
    board[pt1]= []
    if winner[1]== 99:
      print('Player {} wins!!!'.format(player[0]))
    
  elif winner[0]== defender[0]: # if attacker does not win, the attacking piece is removed
    p1.append(board[pt1])
    board[pt1]= []
    if winner[1]== 99:    
      print('Player {} wins!!!'.format(defender[0]))
  return winner[1]    
  
  
def is_move_ok(board, player, pt1, pt2):
  ok0= (pt1 != pt2) #pt1 and pt2 shld be different
  
  cell= board[pt1]  
  print(cell)
  ok1= (player == cell[0]) #player must own cell to be moved
  
  ok2= validxy_atcurrent(pt1, pt2) # move from pt1 to pt2 must be valid

  ok3, ok4= (True, True) # ok4 is for if need check win
  cell2= board[pt2]
  if cell2 != []:
    ok3= (cell2[0] != player)  # should not be moving to friendly cell
  else:
    # target cell is blank, so move the contents to it and blank from cell
    board[pt2]= board[pt1]
    board[pt1]= []
    ok4= False  # empty target cell, no need to check who wins
  
  if not ok0:
    print('Error. Same cell, not moving.')
  if not ok1:
    print('Player {} does not own this cell'.format(player))
  if not ok2:
    print('Cannot jump to {})'.format(pt2))
  if not ok3:
    print('Cannot move to occupied friend cell.')
  print('\n')
  return (ok0, ok1, ok2, ok3, ok4)


def playerX_moves(board, player):
  move_ok= False
  while not move_ok:
    print('Player {} move: '.format(player))
    pt1= input(' From: ')
    pt2= input(' To  : ')

    # change inputted string coordinates to tuples
    pt1= (int(pt1[0]), int(pt1[2]))      
    pt2= (int(pt2[0]), int(pt2[2]))
    
    ok_list= is_move_ok(board, player, pt1, pt2)
    move_ok= ok_list[0] and ok_list[1] and ok_list[2] and ok_list[3]
    
  x= 0
  if move_ok and ok_list[4]:
    x= check_win(board, player, pt1, pt2)
  return x
  
  
#board= {}
ranks= {'GA':15, 'G4':14, 'LG':13, 'MG':12, 'BG':11,
  'CO':10, 'LC':9, 'MA':8, 'CA':7, '1L':6,
  '2L':5, 'SG':4,
  'P1':3, 'P2':3, 'P3':3, 'P4':3, 'P5':3, 'P6':3,
  'S1':16, 'S2':16, 'FL': 1}
p1= [] 
p2= []

if __name__ == '__main__':  
  # create the playing board
  board= create_board()
  
  # arrange pieces on the board for each player and show board
  for player in range(1,3):  
    board= place_pieces(player, board, ranks)      
  disp_board(board)
    
  playing= True  
  while playing:
    for player in range(1,3):
      if playerX_moves(board, player) == 99: 
          playing= False
          break
        
    '''    
    ans= input('\nGo again? y/No ')
    if ans.upper() == 'NO':
      print('...Exiting game. Bye!')
      playing= False    
    ''' 
    print('\n')