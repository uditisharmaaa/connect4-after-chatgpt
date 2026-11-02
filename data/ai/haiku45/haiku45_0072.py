import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Initialize the game board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(column_input, cols):
    """Validate if the column input is valid."""
    if len(column_input) != 1:
        return False
    
    if not column_input.isupper() or not column_input.isalpha():
        return False
    
    col_index = ord(column_input) - ord('A')
    
    if col_index < 0 or col_index >= cols:
        return False
    
    return True


def can_place_checker(board, col_index):
    """Check if a checker can be placed in the given column."""
    return board[0][col_index] == " "


def place_checker(board, col_index, symbol):
    """Place a checker in the specified column and return the row index."""
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1


def check_win(board, rows, cols, row, col, symbol):
    """Check if the last placed checker resulted in a win."""
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == symbol:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == symbol:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == symbol:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == symbol:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == symbol:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == symbol:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == symbol:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == symbol:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board, rows, cols):
    """Check if the board is completely full."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board, COLS)
    
    game_over = False
    winner = None
    
    while not game_over:
        symbol = SYMBOLS[current_player]
        
        # Get valid input from player
        while True:
            column_input = input(f"Player {symbol}, please enter a column: ").strip().upper()
            
            if not is_valid_column(column_input, COLS):
                print("Invalid input. Please enter a valid column letter.")
                continue
            
            col_index = ord(column_input) - ord('A')
            
            if not can_place_checker(board, col_index):
                print("Column is full. Please choose another column.")
                continue
            
            break
        
        # Place the checker
        row = place_checker(board, col_index, symbol)
        
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, ROWS, COLS, row, col_index, symbol):
            print(f"Player {symbol} won!")
            game_over = True
            winner = symbol
        
        # Check for draw
        elif is_board_full(board, ROWS, COLS):
            print("Draw! The board is full.")
            game_over = True
        
        # Move to next player
        if not game_over:
            current_player = (current_player + 1) % NUM_PLAYERS


def main():
    """Entry point of the program."""
    play_game()


if __name__ == "__main__":
    main()
