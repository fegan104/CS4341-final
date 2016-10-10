#Board specific variables
UP = (-1, 0)
DN = (1, 0)
RT = (0, 1)
LF = (0, -1)
BLOCK = 3 # this doesn't have to be 3 it's just random
MOVES = [UP, DN, RT, LF]

def valid_moves(mouse, board):
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

b1 = [[1, 1, 1],
	  [1, 1, 1],
	  [1, 1, 1]]

b2 = [[1, 3, 1],
	 [1, 1, 3],
	 [1, 1, 1]]

print valid_moves((1, 1), b1)
print valid_moves((1, 1), b2)
print valid_moves((0, 2), b2)
