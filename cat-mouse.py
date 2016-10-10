#Board specific variables
UP = (0, 1)
DN = (0, -1)
RT = (1, 0)
LF = (-1, 0)
BLOCK = 3
MOVES = [UP, DN, RT, LF]

def valid_move(mouse, board):
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
		if 0 < x < width and 0 < y < height and board[x][y] != BLOCK:
			valid.append(mv)

	return valid
