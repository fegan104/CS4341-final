import random
#Board 
""" 
#0 - safe position
#1 - cheese
#2 = mouse trap
#3 = bloackage
#4 = finish Goal

"""
#Board specific variables
UP = (-1, 0)
DN = (1, 0)
RT = (0, 1)
LF = (0, -1)
BLOCK = 3 # this doesn't have to be 3 it's just random
MOVES = [UP, DN, RT, LF]
#The random board for our program
BOARD, H, W = generate_board()
#initialize our Q matrix
Q = q_init(H, W)

def q_init(h, w):
	q = [][]
	for x in xrange(h):
		for y in xrange(w):
			q.append(Square())

class Square(self):
	up, down, left, right = 0

 
def generate_board():
  """ Used to generate a random board with cheese, mouse traps, blocks, and exit door
  
  Return: 
       a board made of 2D array, and the height and width
  """
  width = random.randint(2,10)
  height = random.randint(2,10)
  board = [[0 for x in range(height)] for y in range(width)]
  
  #assign random nos from (0,3) to all places in board  
  for w in range(width):
    for h in range(height):
        board[w][h] = random.randint(0,3)
      
  #marking origin as safe position
  board[0][0] = 0

  #assign one random place in board as finish Goal
  board[random.randint(1,width-1)][random.randint(1,height-1)] = 4

  #if no moves allowed initially then generate new board
  if board[1][0] == 2 or board[1][0] == 3:
    if board[0][1] == 2 or board[0][1] == 3:
      board = generate_board()
      
  return (board, height, width)
   
def valid_moves(mouse):
	"""Used to find valid moves for a mouse on a given board.

	Args:
		mouse (int[]): A tuple of mouse coordinates on a board.
		board (int[][]): A rectangular matrix of encoded baord-square values.

	Return:
		An array of possible moves.
	"""
	width = len(board)
	height = len(board[0])
	valid = []
	
	#check what moves don't go over the edge or hit a wall
	for mv in MOVES:
		x = mouse[0] + mv[0]
		y = mouse[1] + mv[1]
		if 0 <= x < width and 0 <= y < height and board[x][y] != BLOCK:
			valid.append(mv)

	return valid

def get_reward(state, action):
	"""Finds the reward for e from the current position making the given mov
	Args:
		state (int tuple): the current position
		action (int tuple): the move to make

	Returns:
		the reward value form teh board
	"""
	return 0

def update_q(state, action):
	"""Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]

	Args:
		state (int tuple): The current position
		action (int tuple): The move we want to make
	"""
	Q[state[0]][state[1]]

b1 = [[1, 1, 1],
	  [1, 1, 1],
	  [1, 1, 1]]
b2 = [[1, 3, 1],
	 [1, 1, 3],
	 [1, 1, 1]]

print valid_moves((1, 1), b1)
print valid_moves((1, 1), b2)
print valid_moves((0, 2), b2)
