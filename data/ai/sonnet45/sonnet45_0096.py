import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("  +" + "---+" * COLS)
        print("  |", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("  +" + "---+" * COLS)

def is_valid_column(column_input):
    """Check if the column input is a valid uppercase letter."""
    if len(column_input) != 1:
        return False
    if not column_input.isupper():
        return False
    if not column_input.isalpha():
        return False
    col_index = ord(column_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True

def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "

def place_checker(board, col_index, checker):
    """Place a checker in the specified column. Returns the row where it was placed, or -1 if column is full."""
    if is_column_full(board, col_index):
        return -1
    
    # Find the lowest empty row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    
    return -1

def check_win(board, row, col, checker):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == checker:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for col in range(COLS):
        if not is_column_full(board, col):
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_index]
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {current_checker}, please enter a column: ")
            
            if not is_valid_column(column_input):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(column_input) - 65
            
            if is_column_full(board, col_index):
                print("Column is full. You lose your turn.")
                break
            
            # Place the checker
            row = place_checker(board, col_index, current_checker)
            
            if row == -1:
                print("Column is full. You lose your turn.")
                break
            
            print_board(board)
            
            # Check for win
            if check_win(board, row, col_index, current_checker):
                print(f"Player {current_checker} won!")
                return
            
            # Check for draw
            if is_board_full(board):
                print("The game is a draw!")
                return
            
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
