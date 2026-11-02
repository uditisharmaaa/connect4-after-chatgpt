import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and borders."""
    os.system("clear")
    cols = len(board[0])
    
    # Print column headers
    print("  ", end="")
    for i in range(cols):
        print(chr(65 + i), end="   ")
    print()
    
    # Print board
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_column(col, cols):
    """Check if column input is valid."""
    if len(col) != 1:
        return False
    if not col.isalpha():
        return False
    col_index = ord(col.upper()) - 65
    return 0 <= col_index < cols


def place_checker(board, col_letter, checker):
    """Place checker in column, return True if successful, False if full."""
    col_index = ord(col_letter.upper()) - 65
    
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def check_win(board, row, col, checker):
    """Check if the placed checker creates a winning condition."""
    rows = len(board)
    cols = len(board[0])
    
    # Directions: horizontal, vertical, diagonal1, diagonal2
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        
        if count >= WIN_LENGTH:
            return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(cell != " " for row in board for cell in row)


def get_player_input(cols, board):
    """Get valid column input from player."""
    while True:
        col = input("Enter a column (A-" + chr(65 + cols - 1) + "): ").strip().upper()
        
        if not is_valid_column(col, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(col) - 65
        if board[0][col_index] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    board = initialize_board(ROWS, COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker_symbols = CHECKERS[:NUM_PLAYERS]
    
    print_board(board)
    print(f"Game starts with Player {checker_symbols[current_player]}!\n")
    
    while True:
        checker = checker_symbols[current_player]
        print(f"Player {checker}, please enter a column:")
        col = get_player_input(COLS, board)
        
        col_index = ord(col) - 65
        
        # Place checker and find row
        for row in range(ROWS - 1, -1, -1):
            if board[row][col_index] == " ":
                board[row][col_index] = checker
                break
        
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
