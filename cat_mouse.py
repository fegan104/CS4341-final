import sys
import os
clear = lambda: os.system('clear')

import random
import numpy as np
from time import sleep

# Board variables
START = 0
CHEESE = 1
TRAP = 2
BLOCK = 3
GOAL = 4
MOUSE = 5

# Reward constants
CHEESE_REWARD = 100
TRAP_REWARD = -500
GOAL_REWARD = 500

# Move action variables
UP = (-1, 0)
DN = (1, 0)
RT = (0, 1)
LF = (0, -1)
MOVES = [UP, DN, RT, LF]

class Square:
	up = 0
	down = 0
	left = 0
	right = 0

	def __repr__(self):
		return 'SQR(%s, %s, %s, %s)' % (self.up, self.right, self.down, self.left)

def generate_board1():
	board =  [[0,3,0,4,0],
	         [0,1,2,2,0],
	         [0,0,3,1,0],
	         [2,0,0,2,0],
	         [3,1,0,0,0]]
	return (board, len(board), len(board[0]))

def generate_board2():
	board =  [[0,3,0,4,0],
	          [0,1,2,2,0],
	          [0,0,3,1,0],
	          [2,0,0,2,0],
	          [3,1,0,0,0]]
	return (board, len(board), len(board[0]))

def generate_board3():
	board =  [[0,0,0,0,0],
	          [0,1,0,2,0],
	          [3,2,0,1,0],
	          [2,0,2,2,0],
	          [3,1,0,0,4]]
	return (board, len(board), len(board[0]))

def generate_board():
  """ Used to generate a random board with cheese, mouse traps, blocks, and exit door
  
  Return: 
	   a board made of 2D array, and the height and width
  """
  width = random.randint(2,10)
  height = random.randint(2,10)
  height = width
  board = [[0 for x in range(width)] for y in range(height)]
  
  #assign random nos from (0,3) to all places in board  
  for w in range(height):
	for h in range(width):
		x = random.randint(0, 3)
		board[w][h] = x 
	  
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
   
def valid_moves(mouse):
	"""Used to find valid moves for a mouse on a given board.

	Return:
		An array of possible moves.
	"""
	width = len(BOARD[0])
	height = len(BOARD)
	valid = []
	
	#check what moves don't go over the edge or hit a wall
	for mv in MOVES:
		x = mouse[0] + mv[0]
		y = mouse[1] + mv[1]
		"""
		print x,y
		print "width:"
		print width,height
		"""
		if 0 <= x <= width - 1 and 0 <= y <= height - 1:
			if BOARD[x][y] != BLOCK:
				valid.append(mv)

	return valid

def get_reward(state, action):
	#TODO find reward from Q or Board?
	"""Finds the reward for the from the current position making the given move
	Args:
		state (int tuple): the current position
		action (int tuple): the move to make

	Returns:
		the reward value form the board
	"""
	newState = state
	newState = (newState[0] + action[0] , newState[1] + action[1])
	rewardValue = 0

	currentPossition = BOARD[ newState[0] ][ newState[1] ]

	if currentPossition == CHEESE:
		rewardValue = CHEESE_REWARD
	elif currentPossition == TRAP:
		rewardValue = TRAP_REWARD	
	elif currentPossition == GOAL:
		rewardValue = GOAL_REWARD
	else: # No reward given
		rewardValue = 0

	return rewardValue

def update_q(state, action):
	"""Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]

	Args:
		state (int tuple): The current position
		action (int tuple): The move we want to make
	"""
	GAMMA = 0.5
	#What are all possible squares we could get to and what move gets us there 
	#((destination_state tuple), (move tuple))
	possible = []
	"""
	for m in valid_moves(state):
		next_sqr = (state[0] + m[0], state[1] + m[1])
		possible.append((next_sqr, m))
	"""
	next_state = (state[0] + action[0], state[1] + action[1])

	for m in valid_moves(next_state):
		if m == UP:
			possible.append(Q[next_state[0]][next_state[1]].up)
		elif m == DN:
			possible.append(Q[next_state[0]][next_state[1]].down)
		elif m == RT:
			possible.append(Q[next_state[0]][next_state[1]].right)
		elif m == LF:
			possible.append(Q[next_state[0]][next_state[1]].left)

	MAX = max(possible)

	if MAX == 0:
		while True:
			MAX = possible[random.randint(0,len(possible)-1)]
			if(MAX == 0):
				break

	#Best move
	#TODO Max[Q(next state, all actions)] what is this
	#MAX = max(map(lambda s: get_reward(state, s[1]), possible))
	#Reward
	R = get_reward(state, action)
	new_q = R + GAMMA * MAX

	if action == UP:
		Q[state[0]][state[1]].up = new_q
	elif action == DN:
		Q[state[0]][state[1]].down = new_q
	elif action == RT:
		Q[state[0]][state[1]].right = new_q
	elif action == LF:
		Q[state[0]][state[1]].left = new_q

def symbolConvert(val):
	"""
	Converts board variables into graphic symbols
	"""
	if val == BLOCK:
		return ' '
	elif val == CHEESE:
		return '+'
	elif val == TRAP:
		return 'x'
	elif val == START:
		return '.'
	elif val == GOAL:
		return 'G'
	elif val == MOUSE:
		return 'o'
	else:
		return val

def printLegend():
	"""
	Print the legend
	"""
	print "MAP LEGEND"
	print " '", symbolConvert(BLOCK), "': no possible paths (barrier)"
	print " '", symbolConvert(CHEESE), "': cheese"
	print " '", symbolConvert(TRAP), "': trap"
	print " '", symbolConvert(START), "': normal path"
	print " '", symbolConvert(GOAL), "': goal!!!"
	print

def print_move(move, mouse):
	if move == UP:
		print "UP" + " from " + str(mouse)
	elif move == DN:
		print "DOWN" + " from " + str(mouse)
	elif move == RT:
		print "RIGHT" + " from " + str(mouse)
	elif move == LF:
		print "LEFT" + " from " + str(mouse)

def printBoard(board, mouse):
	"""
	Print the board
	"""
	width = len(board[0])
	height = len(board)

	print
	print "BOARD"
	print
	print '  ',
	for w in xrange(-1, width):
		print '-',
	print

	for h in xrange(0, height):
		print '  |',
		for w in xrange(0, width):
			val = board[h][w]
			if h == mouse[0] and w == mouse[1]:
				val = MOUSE

			print symbolConvert(val),

			
		print '|',
		print

	print '  ',
	for w in xrange(-1, width):
		print '-',
	print
	print

def get_updated_mouse(mouse, move):
	""" Returns the coordinates for a mouse after performing the move.
	"""
	next_mouse = (mouse[0] + move[0], mouse[1] + move[1])
	return next_mouse

def find_best_move(mouse):
	possible = []
	for mv in valid_moves(mouse):
		#print_move(mv,mouse)
		if mv == UP:
			possible.append(Q[mouse[0]][mouse[1]].up)
		elif mv == DN:
			possible.append(Q[mouse[0]][mouse[1]].down)
		elif mv == RT:
			possible.append(Q[mouse[0]][mouse[1]].right)
		elif mv == LF:
			possible.append(Q[mouse[0]][mouse[1]].left)
	# print(possible)
	#printprintBoard(BOARD)
	qval = max(possible)
	moves = []
	validMoves = valid_moves(mouse)

	if qval == 0:
		if(Q[mouse[0]][mouse[1]].up == 0) and UP in validMoves:
			moves.append(UP)
		if Q[mouse[0]][mouse[1]].down == 0 and DN in validMoves:
			moves.append(DN)
		if Q[mouse[0]][mouse[1]].right ==0 and RT in validMoves:
			moves.append(RT)
		if Q[mouse[0]][mouse[1]].left ==0 and LF in validMoves:
			moves.append(LF)

		return moves[random.randint(0,len(moves)-1)]


	
	if qval == 	Q[mouse[0]][mouse[1]].up and UP in validMoves:
		return UP
	elif qval == Q[mouse[0]][mouse[1]].down and DN in validMoves:
		return DN
	elif qval == Q[mouse[0]][mouse[1]].right and RT in validMoves:
		return RT
	elif qval == Q[mouse[0]][mouse[1]].left and LF in validMoves:
		return LF


	"""
	possible = []
	for mv in valid_moves(mouse):
		if mv == UP:
			possible.append((Q[mouse[0]+mv[0]][mouse[1]+mv[1]].down, UP))
		elif mv == DN:
			possible.append((Q[mouse[0]+mv[0]][mouse[1]+mv[1]].up, DN))
		elif mv == RT:
			possible.append((Q[mouse[0]+mv[0]][mouse[1]+mv[1]].left, RT))
		elif mv == LF:
			possible.append((Q[mouse[0]+mv[0]][mouse[1]+mv[1]].right, LF))
	return sorted(possible, key=lambda p: p[0])[-1][1]
	"""

def printAll(i, next_move, mouse, board):
	clear()
	printLegend()
	print_move(next_move, mouse)
	printBoard(board, mouse)
	print " ", i, "out of 20000 moves"
	print
	print

def learn(board, mouse):
	"""
	1. Set the gamma parameter, and environment rewards in matrix R.

	2. Initialize matrix Q to zero.
	
	3. For each episode:
	
	Select a random initial state.
	
	Do While the goal state hasn't been reached.
	
	Select one among all possible actions for the current state.
	Using this possible action, consider going to the next state.
	Get maximum Q value for this next state based on all possible actions.
	Compute: Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]
	Set the next state as the current state.
	End Do
	
	End For
	"""
	i = 0
	done = False
	moves = []
	mouseStart = False
	while i < 20000:
		#TODO make random move sometimes
		if (board[mouse[0]][mouse[1]] == TRAP or board[mouse[0]][mouse[1]] ==  GOAL):
			#print moves
			moves = []
			mouse = (0, 0)
		else:
			next_move = find_best_move(mouse)

			if i > 19950 and i < 19980:
				printAll(i, next_move, mouse, board)
				sleep(0.05)
			elif i > 19980:
				printAll(i, next_move, mouse, board)
				sleep(0.3)

			moves.append(next_move)
			update_q(mouse, next_move)
			if board[mouse[0]][mouse[1]] == CHEESE:
				BOARD[mouse[0]][mouse[1]] = START
			mouse = get_updated_mouse(mouse, next_move)
		i += 1
	return 0

#The random board for our program

BOARD, H, W = generate_board()
# printBoard(BOARD, mouse)

# initialize our Q matrix
Q = q_init(H, W)
#Learn the board
learn(BOARD, (0, 0))








