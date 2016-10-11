import random
import numpy as np

def generate_board():
  """ Used to generate a random board with cheese, mouse traps, blocks, and exit door
  
  Return: 
       a board made of 2D array, and the height and width
  """
  width = random.randint(2,10)
  height = random.randint(2,10)
  board = [[0 for x in range(width)] for y in range(height)]
  
  #assign random nos from (0,3) to all places in board  
  for w in range(height):
    for h in range(width):
        board[w][h] = random.randint(0,3)
      
  #marking origin as safe position
  board[0][0] = 0

  #assign one random place in board as finish Goal
  board[random.randint(1,height-1)][random.randint(1,width-1)] = 4

  #if no moves allowed initially then generate new board
  if board[1][0] == 2 or board[1][0] == 3:
    if board[0][1] == 2 or board[0][1] == 3:
      board, height, width = generate_board()
      
  return board, height, width

def q_init(h, w):
	"""Creates a Q with Square all set to 0
	Args:
		h (int): Height of the Q we want to generate
		w (int): Width of the Q

	Returns:
		An HxW matrix of Squares
	"""
	q = []
	for x in range(h):
		q.append([])
		for y in range(w):
			q[x].append(Square())
	return q
   
def valid_moves():
	"""Used to find valid moves for a mouse on a given board.

	Return:
		An array of possible moves.
	"""
	width = len(BOARD)
	height = len(BOARD[0])
	valid = []
	
	#check what moves don't go over the edge or hit a wall
	for mv in MOVES:
		x = MOUSE[0] + mv[0]
		y = MOUSE[1] + mv[1]
		if 0 <= x < width and 0 <= y < height and BOARD[x][y] != BLOCK:
			valid.append(mv)

	return valid

def get_reward(state, action):
	"""Finds the reward for the from the current position making the given move
	Args:
		state (int tuple): the current position
		action (int tuple): the move to make

	Returns:
		the reward value form the board
	"""
	#find tile the move takes us to
	next_sqr = Q[state[0]][state[1]]
	#return a value from our Square based on how we got here
	if action == UP:
		return next_sqr.down
	elif action == DN:
		return next_sqr.up
	elif action == RT:
		return next_sqr.left
	elif action == LF:
		return next_sqr.right

def update_q(state, action):
	"""Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]

	Args:
		state (int tuple): The current position
		action (int tuple): The move we want to make
	"""
	GAMMA = 0.8
	#What are all possible squares we could get to and what move gets us there 
	#((destination_state tuple), (move tuple))
	possible = []
	for m in valid_moves():
		next_sqr = (MOUSE[0] + m[0], MOUSE[1] + m[1])
		possible.append((next_sqr, m))
	#Best move
	MAX = max(map(lambda s: get_reward(s[0], s[1]), possible))
	#Reward
	R = get_reward(state, action)
	new_q = R + GAMMA * MAX

	if action == UP:
		Q[state[0]][state[1]].down = new_q
	elif action == DN:
		Q[state[0]][state[1]].up = new_q
	elif action == RT:
		Q[state[0]][state[1]].left = new_q
	elif action == LF:
		Q[state[0]][state[1]].right = new_q

class Square:
	up = 0
	down = 0
	left = 0
	right = 0

	def __repr__(self):
		return 'SQR(%s, %s, %s, %s)' % (self.up, self.right, self.down, self.left)
#Board variables
START = 0
CHEESE = 1
TRAP = 2
BLOCK = 3
GOAL = 4
#Move action variables
UP = (-1, 0)
DN = (1, 0)
RT = (0, 1)
LF = (0, -1)
MOVES = [UP, DN, RT, LF]

#The random board for our program
BOARD, H, W = generate_board()
print np.matrix(BOARD)
#Mouse
MOUSE = (0, 0)
#initialize our Q matrix
Q = q_init(H, W)
update_q((0, 0), DN)
