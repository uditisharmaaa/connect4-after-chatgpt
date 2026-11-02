import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    # Print column headers
    header = "  "
    for col in range(COLS):
        header += chr(65 + col) + "   "
    print(header)
    
    # Print board with borders
    for row in board:
        print("+---" * COLS + "+")
        row_str = "|"
        for cell in row:
            row_str += " " + cell + " |"
        print(row_str)
    print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move in the given column is valid."""
    return 0 <= col < COLS and board[0][col] == " "


def place_checker(board, col, checker):
    """Place checker in the lowest available row of the column."""
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
    """Check if the board is full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))


def get_player_move(player_checker):
    """Get and validate player input for column choice."""
    while True:
        move = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        
        if len(move) != 1 or not move.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(move) - ord('A')
        
        if not is_valid_move(board, col):
            print(f"Invalid move. Column {move} is either out of bounds or full.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    checker_list = CHECKERS[:NUM_PLAYERS]
    
    print_board(board)
    
    while True:
        current_checker = checker_list[current_player]
        col = get_player_move(current_checker)
        
        place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    board = initialize_board()
    play_game()
