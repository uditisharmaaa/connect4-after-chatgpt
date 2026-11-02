import os
import random

# Configuration constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
SYMBOLS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "


def place_checker(board, col, symbol):
    """Place a checker in the given column and return the row where it was placed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last placed checker at (row, col) creates a winning condition."""
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for dr, dc in directions:
        count = 1
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
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
    return all(board[0][col] != " " for col in range(COLS))


def get_column_input(current_player):
    """Get and validate column input from the player."""
    while True:
        try:
            user_input = input(f"Player {SYMBOLS[current_player]}, please enter a column: ").strip().upper()
            
            if len(user_input) != 1:
                print("Invalid input. Please enter a single letter.")
                continue
            
            if not user_input.isalpha():
                print("Invalid input. Please enter a letter.")
                continue
            
            col = ord(user_input) - ord('A')
            
            if col < 0 or col >= COLS:
                print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
                continue
            
            if not is_valid_move(board, col):
                print("This column is full. Please choose another column.")
                continue
            
            return col
        except Exception:
            print("Invalid input. Please try again.")


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        # Get player input
        col = get_column_input(current_player)
        
        # Place checker
        row = place_checker(board, col, SYMBOLS[current_player])
        
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, SYMBOLS[current_player]):
            print(f"Player {SYMBOLS[current_player]} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            return
        
        # Move to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
