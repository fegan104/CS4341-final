import random
#Board 
""" 
#0 - safe position
#1 - cheese
#2 = mouse trap
#3 = bloackage
#4 = finish Goal

"""

 
def generate_board():
  """ Used to generate a random board with cheese, mouse traps, blocks, and exit door
  
  Return: 
       a board made of 2D array 
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
      
  return board
  
  
