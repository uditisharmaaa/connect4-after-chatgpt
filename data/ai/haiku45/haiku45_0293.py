import os
import random

# Global constants
COLUMNS = 7
ROWS = 6
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLUMNS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print board rows
    for row in range(ROWS):
        print("+---" * COLUMNS + "+")
        print("|", end="")
        for col in range(COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLUMNS + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    return 0 <= col < COLUMNS and board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the lowest available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_winner(board, checker):
    """Check if the given checker has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLUMNS))


def get_valid_input(current_player):
    """Get and validate user input for column selection."""
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not ('A' <= user_input <= chr(64 + COLUMNS)):
            print(f"Invalid column. Please enter a letter between A and {chr(64 + COLUMNS)}.")
            continue
        
        col = ord(user_input) - ord('A')
        return col


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    print(f"Starting player: {CHECKERS[current_player_index]}\n")
    
    while True:
        current_checker = CHECKERS[current_player_index]
        col = get_valid_input(current_checker)
        
        if not is_valid_move(board, col):
            print("Column is full or invalid. Try another column.\n")
            continue
        
        place_checker(board, col, current_checker)
        print_board(board)
        
        if check_winner(board, current_checker):
            print(f"Player {current_checker} won!")
            return
        
        if is_board_full(board):
            print("It's a draw!")
            return
        
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
