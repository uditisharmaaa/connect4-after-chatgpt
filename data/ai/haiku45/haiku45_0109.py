import os
import random

# Constants
COLS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def create_board(rows, cols):
    """Create and return an empty board."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board):
    """Print the board with column labels and borders."""
    os.system('clear')
    cols = len(board[0])
    rows = len(board)
    
    # Print column labels
    print("  ", end="")
    for i in range(cols):
        print(f" {chr(65 + i)} ", end="")
    print()
    
    # Print board with borders
    for row in range(rows):
        print("+---" * cols + "+")
        print("|", end="")
        for col in range(cols):
            print(f" {board[row][col]} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column not full and in bounds)."""
    cols = len(board[0])
    if col < 0 or col >= cols:
        return False
    return board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the lowest available position in the column."""
    rows = len(board)
    for row in range(rows - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return True
    return False


def check_win(board, checker):
    """Check if the given checker has won."""
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-right to bottom-left)
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(len(board[0])))


def get_player_move(cols):
    """Get and validate player input for column selection."""
    while True:
        user_input = input().strip().upper()
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        col = ord(user_input) - ord('A')
        if col < 0 or col >= cols:
            print(f"Invalid input. Please enter a letter between A and {chr(65 + cols - 1)}.")
            continue
        return col


def play_game(rows, cols, num_players):
    """Main game loop."""
    board = create_board(rows, cols)
    checkers = CHECKERS[:num_players]
    current_player = random.randint(0, num_players - 1)
    
    print_board(board)
    
    while True:
        checker = checkers[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        
        col = get_player_move(cols)
        
        if not is_valid_move(board, col):
            print("Column is full or invalid. Try again.")
            print(f"Player {checker}, please enter a column: ", end="")
            continue
        
        place_checker(board, col, checker)
        print_board(board)
        
        if check_win(board, checker):
            print(f"Player {checker} won!")
            return
        
        if is_board_full(board):
            print("It's a draw!")
            return
        
        current_player = (current_player + 1) % num_players


if __name__ == "__main__":
    play_game(ROWS, COLS, PLAYERS)
