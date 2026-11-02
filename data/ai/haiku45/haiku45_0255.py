import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(ord('A') + col)}  ", end="")
    print()
    
    # Print board with separators
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * COLS + "+")


def is_valid_input(column_letter, board):
    """
    Validate if the input is a valid column letter and if the column is not full.
    Returns the column index or -1 if invalid.
    """
    if len(column_letter) != 1:
        return -1
    
    if not column_letter.isalpha():
        return -1
    
    column_index = ord(column_letter.upper()) - ord('A')
    
    if column_index < 0 or column_index >= COLS:
        return -1
    
    # Check if column is full
    if board[0][column_index] != " ":
        return -1
    
    return column_index


def place_checker(board, column_index, symbol):
    """Place a checker in the specified column. Returns True if successful."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][column_index] == " ":
            board[row][column_index] = symbol
            return True
    return False


def check_win(board, row, col, symbol):
    """Check if the last placed checker at (row, col) resulted in a win."""
    directions = [
        (0, 1),   # Horizontal
        (1, 0),   # Vertical
        (1, 1),   # Diagonal down-right
        (1, -1)   # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def get_row_of_placement(board, col):
    """Get the row index where a checker would be placed in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def play_game():
    """Main game loop."""
    board = initialize_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    game_over = False
    
    while not game_over:
        current_symbol = SYMBOLS[current_player_index]
        current_player_number = current_player_index + 1
        
        # Get valid input from player
        valid_move = False
        while not valid_move:
            user_input = input(f"Player {current_symbol}, please enter a column: ").strip().upper()
            column_index = is_valid_input(user_input, board)
            
            if column_index == -1:
                print("Invalid input. Please enter a valid column letter (A-G) that is not full.")
                continue
            
            valid_move = True
        
        # Place checker
        row = get_row_of_placement(board, column_index)
        place_checker(board, column_index, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, column_index, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("It's a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
