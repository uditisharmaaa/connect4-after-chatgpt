import os
import random

# Constants
BOARD_COLS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]


def print_board(board):
    """Print the board with column labels and borders."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(f" {chr(ord('A') + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")
        print("|", end="")
        for col in range(BOARD_COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * BOARD_COLS + "+")


def is_valid_column(col_letter, board):
    """Check if column input is valid and not full."""
    if len(col_letter) != 1 or not col_letter.isalpha():
        return False
    
    col_index = ord(col_letter.upper()) - ord('A')
    
    if col_index < 0 or col_index >= BOARD_COLS:
        return False
    
    if board[0][col_index] != " ":
        return False
    
    return True


def get_column_index(col_letter):
    """Convert column letter to index."""
    return ord(col_letter.upper()) - ord('A')


def place_checker(board, col_index, checker):
    """Place checker in column and return row index, or -1 if column is full."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return row
    return -1


def check_win(board, row, col, checker):
    """Check if the last placed checker at (row, col) creates a win."""
    directions = [
        (0, 1),    # Horizontal
        (1, 0),    # Vertical
        (1, 1),    # Diagonal down-right
        (1, -1)    # Diagonal down-left
    ]
    
    for dr, dc in directions:
        count = 1
        
        # Check in positive direction
        r, c = row + dr, col + dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check in negative direction
        r, c = row - dr, col - dc
        while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if board is completely full."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            col_letter = input(f"Player {checker}, please enter a column: ").strip()
            if is_valid_column(col_letter, board):
                break
            print("Invalid input. Please enter a valid column letter.")
        
        col_index = get_column_index(col_letter)
        row = place_checker(board, col_index, checker)
        
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, checker):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
