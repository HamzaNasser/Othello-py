import time
import pyautogui as py
from copy import deepcopy
import pyautogui as py
import time


def get_stability(grid, color):
    # Initialize a variable to store the stability score
    stability = 0
    
    # Loop through the rows of the grid
    for i in range(len(grid)):
        # Loop through the columns of the grid
        for j in range(len(grid[i])):
            # Check if the current position is occupied by a piece of the given color
            if grid[i][j] == color:
                # Check if the current position is a corner
                if (i == 0 or i == len(grid)-1) and (j == 0 or j == len(grid[i])-1):
                    # Add a high value to the stability score
                    stability += 100
                # Check if the current position is on the edge of the board
                elif i == 0 or i == len(grid)-1 or j == 0 or j == len(grid[i])-1:
                    # Add a moderate value to the stability score
                    stability += 50
                else:
                    # Add a low value to the stability score
                    stability += 10
    
    # Return the stability score
    return stability

def get_score(grid, color):
    # Initialize variables to store the scores for each player
    my_score, opponent_score = 0, 0
    values = [[100, -50, 30, 10, 10, 30, -50, 100],
          [-50, -80, -10, -10, -10, -10, -80, -50],
          [30, -10, 15, 3, 3, 15, -10, 30],
          [10, -10, 3, 3, 3, 3, -10, 10],
          [10, -10, 3, 3, 3, 3, -10, 10],
          [30, -10, 15, 3, 3, 15, -10, 30],
          [-50, -80, -10, -10, -10, -10, -80, -50],
          [100, -50, 30, 10, 10, 30, -50, 100]]

    
    # Loop through the rows of the grid
    for i in range(len(grid)):
        # Loop through the columns of the grid
        for j in range(len(grid[i])):
            # Check if the current position is occupied by a piece
            if grid[i][j] != '.':
                # Check if the piece is the same color as the current player
                if grid[i][j] == color:
                    # Add the value of the piece to the current player's score
                    my_score += values[i][j]
                else:
                    # Add the value of the piece to the opponent's score
                    opponent_score += values[i][j]
    
    # Calculate the mobility of each player
    my_mobility = len(get_valid_moves(grid, color))
    opponent_mobility = len(get_valid_moves(grid, get_opposite_color(color)))
    
    # Calculate the stability of each player's pieces
    my_stability = get_stability(grid, color)
    opponent_stability = get_stability(grid, get_opposite_color(color))
    
    # Return the score for the current player
    return my_score + my_mobility + my_stability - opponent_score - opponent_mobility - opponent_stability


def get_best_move(grid, color, depth, alpha, beta, maximize):
    # Base case: if the depth is 0 or the game is over, return the score
    if depth == 0 or game_over(grid):
        return get_score(grid, color)

    # Initialize the best score
    best_score = float('-inf') if maximize else float('inf')

    # Get the list of valid moves for the current player
    valid_moves = get_valid_moves(grid, color)

    # Loop through the valid moves
    for move in valid_moves:
        # Make the move and get the resulting grid
        new_grid = make_move(deepcopy(grid), move, color)

        # Recursively search the resulting grid
        score = get_best_move(new_grid, get_opposite_color(color), depth - 1, alpha, beta, not maximize)

        # Update the best score if necessary
        print('Updating Best score')
        if maximize:
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            print(best_score, move)
        else:
            best_score = min(best_score, score)
            beta = min(beta, best_score)

        # Prune the search if the alpha value is greater than or equal to the beta value
        if alpha >= beta:
            break

    # Return the best score
    return best_score



def get_opposite_color(color):
    if color == 'B':
        return 'W'
    else:
        return 'B'

def get_valid_moves(grid, color):
    # Initialize a list to store the valid moves

    valid_moves = []
    
    # Loop through the rows of the grid
    for i in range(len(grid)):
        # Loop through the columns of the grid
        for j in range(len(grid[i])):
            # Check if the current position is empty
            if grid[i][j] == '.':
                # Check the eight directions around the current position
                # to see if any of them contain the opposite color
                for x, y in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
                    # Initialize variables to store the position and the number of pieces flipped
                    pos, pieces_flipped = (i+x, j+y), 0
                    # Check if the position is on the board and contains the opposite color
                    while 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[i]) and grid[pos[0]][pos[1]] == get_opposite_color(color):
                        # Update the position and the number of pieces flipped
                        pos, pieces_flipped = (pos[0]+x, pos[1]+y), pieces_flipped+1
                    # Check if the position is on the board and contains the same color as the current player
                    if 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[i]) and grid[pos[0]][pos[1]] == color and pieces_flipped > 0:
                        # If so, add the current position as a valid move
                        valid_moves.append((i, j))
                        break
    
    # Return the list of valid moves
    return valid_moves


def determine_winner(grid):
    # Count the number of black and white discs on the board
    black_count = 0
    white_count = 0
    for row in grid:
        for cell in row:
            if cell == "B":
                black_count += 1
            elif cell == "W":
                white_count += 1

    # Determine the winner based on the disc count
    if black_count > white_count:
        return "B"
    elif white_count > black_count:
        return "W"
    else:
        return "T"




def game_over(grid):
    # Define constants for the different colors
    WHITE = 'W'
    BLACK = 'B'
    EMPTY = '.'

    # Check if the board is full
    if not any(EMPTY in row for row in grid):
        return True

    # Check if both players have no legal moves
    if not any(get_valid_moves(grid, WHITE)) and not any(get_valid_moves(grid, BLACK)):
        return True

    return False



def make_move(grid, color, move):
    # Get the row and column of the move
    if move not in list(get_valid_moves(grid,color)):
        return grid
    row, col = move
    
    # Place the piece on the grid
    grid[row][col] = color
    
    # Flip the pieces in all 8 directions
    grid = flip_pieces(grid,color, row, col, -1, 0) # up
    grid = flip_pieces(grid, color, row, col, -1, 1) # up-right
    grid = flip_pieces(grid, color, row, col, 0, 1) # right
    grid = flip_pieces(grid, color, row, col, 1, 1) # down-right
    grid = flip_pieces(grid, color, row, col, 1, 0) # down
    grid = flip_pieces(grid, color, row, col, 1, -1) # down-left
    grid = flip_pieces(grid, color, row, col, 0, -1) # left
    grid = flip_pieces(grid, color, row, col, -1, -1) # up-left
    
    # Return the modified grid
    return grid

def flip_pieces(grid, color, row, col, d_row, d_col):
    # Create a copy of the grid
    new_grid = deepcopy(grid)
    
    # Initialize the variables to store the current position and the opposite color
    current_row, current_col, opposite_color = row+d_row, col+d_col, get_opposite_color(color)
    
    # Return the original grid if the move is invalid
    if not (0 <= current_row < len(grid) and 0 <= current_col < len(grid[0]) and grid[current_row][current_col] == opposite_color):
        return new_grid
    
    # Initialize a flag to indicate if any pieces were flipped
    flipped = False
    
    # Initialize a list to store the positions of the flipped pieces
    flipped_positions = []
    
    # Loop until the edge of the grid is reached or a piece of the same color is encountered
    while 0 <= current_row < len(grid) and 0 <= current_col < len(grid[0]) and grid[current_row][current_col] == opposite_color:
        # Flip the piece
        new_grid[current_row][current_col] = color
        # Add the position to the list
        flipped_positions.append((current_row, current_col))
        # Set the flag to True
        flipped = True
        # Update the current position
        current_row += d_row
        current_col += d_col
    
    # If pieces were flipped, but the last piece was not the same color as the current player,
    # reset the flipped pieces to their original state
    if flipped and 0 <= current_row < len(grid) and 0 <= current_col < len(grid[0]) and grid[current_row][current_col] != color:
        for pos in flipped_positions:
            new_grid[pos[0]][pos[1]] = opposite_color
    
    # Return the resulting grid
    return new_grid



def print_grid(grid):
    # Print the grid
    for row in grid:
        for cell in row:
            if cell == '.':
                print('\033[92m' + cell + '\033[0m', end=' ')
            else:
                print(cell, end=' ')
        print()

def print_grid_best(grid, best_move):
    # Print the grid
    for row in range(8):
        for col in range(8):
            if (row, col) == best_move:
                print('\033[92m' + 'X' + '\033[0m', end=' ')
            else:
                print(".", end=' ')
        print()

def color_square(grid, move):
  # make a copy of the grid
  colored_grid = [row[:] for row in grid]
  # color the specified location
  colored_grid[move[0]][move[1]] = 'X'
  return colored_grid


def print_grid_bestv1(grid, best_move):
  # Color the specified location in the grid
  colored_grid = color_square(grid, best_move)
  # Print the grid
  for row in colored_grid:
    for element in row:
      if element == 'X':
        print('\033[31m' + 'X' + '\033[0m', end=' ')
      elif element == '.':
        print('\033[32m' + element + '\033[0m', end=' ')
      else:
        print(element, end=' ')
    print()

def get_grid():
    # Create an empty 8x8 grid
    grid = [[' ' for _ in range(8)] for _ in range(8)]

    image = py.screenshot()

    # Iterate through each cell in the grid
    for row in range(8):
        for col in range(8):
            # Calculate the x and y position of the current cell
            x = 40 + col * 90
            y = 15 + row * 90
            # Move the mouse to the current cell
            #py.moveTo(x + 660, y + 285)
            # Get the pixel color at the current position
            r, g, b = image.getpixel((x + 660, y + 285))
            color_map = {96: 'B', 235: 'W', 134: '.', 215: 'W', 86: "B"}
            color = color_map.get(r, '.')
            # Set the color of the current cell
            grid[row][col] = color

    return grid



color = 'W'
alpha = -100
beta = 100


grid = get_grid()
print_grid(grid)
print()
mini = get_best_move(grid, color, 5,beta,alpha, True)
print(determine_winner(grid), "is winning")

