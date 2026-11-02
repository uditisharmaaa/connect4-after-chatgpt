import os
import random

# Configuration constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current board state."""
    os.system('clear')
    
    # Print column headers
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
    print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    return 0 <= col < COLS and board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the specified column. Return True if successful."""
    if not is_valid_move(board, col):
        return False
    
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLS))


def get_valid_column(player_checker):
    """Get a valid column input from the player."""
    while True:
        user_input = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(ord('A') + COLS - 1)}.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    board = initialize_board()
    players = [CHECKERS[i] for i in range(NUM_PLAYERS)]
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = players[current_player_idx]
        col = get_valid_column(current_checker)
        
        if not place_checker(board, col, current_checker):
            print("Column is full. Please try another column.")
            continue
        
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            return
        
        if is_board_full(board):
            print("It's a draw!")
            return
        
        current_player_idx = (current_player_idx + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
