import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+" + "---+" * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's a letter
    if not col_letter.isalpha():
        return False
    
    # Convert to uppercase and get column index
    col_letter = col_letter.upper()
    col_index = ord(col_letter) - 65
    
    # Check if column is within board range
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column."""
    col_index = ord(col_letter.upper()) - 65
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row, col_index
    
    return -1, -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def play_game():
    """Main game loop."""
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get valid input from player
        valid_input = False
        while not valid_input:
            col_input = input(f"Player {current_symbol}, please enter a column: ")
            
            if is_valid_column(col_input, board):
                valid_input = True
            else:
                print("Invalid input. Please try again.")
        
        # Place checker
        row, col = place_checker(board, col_input.upper(), current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
