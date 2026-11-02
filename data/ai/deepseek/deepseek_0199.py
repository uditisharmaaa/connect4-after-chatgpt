import os
import random

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

def initialize_board():
    """Initialize an empty game board with specified dimensions."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the game board with column labels and borders."""
    # Clear the screen before printing
    os.system('clear')
    
    # Print column headers
    print("  " + "   ".join(chr(65 + i) for i in range(BOARD_COLS)))
    
    # Print the board rows with borders
    border = "+" + ("---+" * BOARD_COLS)
    for row in board:
        print(border)
        print("|" + "|".join(f" {cell} " for cell in row) + "|")
    print(border)

def get_valid_column(board):
    """Prompt the current player for a valid column input."""
    while True:
        col_input = input(f"Player {current_player}, please enter a column: ").upper()
        if len(col_input) != 1 or not col_input.isalpha():
            print("Invalid input. Please enter a single letter from A to " + chr(65 + BOARD_COLS - 1))
            continue
        
        col = ord(col_input) - 65
        if col < 0 or col >= BOARD_COLS:
            print("Column out of bounds. Please choose a column from A to " + chr(65 + BOARD_COLS - 1))
            continue
        
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col

def place_checker(board, col, checker):
    """Place the checker in the specified column at the lowest available row."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1

def check_win(board, row, col, checker):
    """Check if placing the checker at (row, col) results in a win."""
    directions = [
        (0, 1),  # horizontal
        (1, 0),  # vertical
        (1, 1),  # diagonal down-right
        (1, -1)   # diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        # Check in the positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Check in the negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        # If count >= 4, win
        if count >= 4:
            return True
    return False

def is_draw(board):
    """Check if the game is a draw (all cells filled)."""
    return all(cell != " " for row in board for cell in row)

# Initialize the game
board = initialize_board()
current_player = random.choice(range(NUM_PLAYERS))
print_board(board)

# Main game loop
while True:
    col = get_valid_column(board)
    row = place_checker(board, col, PLAYER_CHECKERS[current_player])
    print_board(board)
    
    if check_win(board, row, col, PLAYER_CHECKERS[current_player]):
        print(f"Player {PLAYER_CHECKERS[current_player]} won!")
        break
    
    if is_draw(board):
        print("Game ended in a draw!")
        break
    
    # Switch players
    current_player = (current_player + 1) % NUM_PLAYERS
