import os
import random

# Constants
COLUMNS = 7
ROWS = 6
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_LENGTH = 4


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and grid."""
    os.system('clear')
    
    # Print column labels
    print("  " + "   ".join([chr(65 + i) for i in range(COLUMNS)]))
    
    # Print top border
    print("+" + "+".join(["---" for _ in range(COLUMNS)]) + "+")
    
    # Print rows
    for row in board:
        print("|" + "|".join([f" {cell} " for cell in row]) + "|")
        print("+" + "+".join(["---" for _ in range(COLUMNS)]) + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column exists and not full)."""
    if col < 0 or col >= COLUMNS:
        return False
    return board[0][col] == " "


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
        for col in range(COLUMNS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for col in range(COLUMNS):
        for row in range(ROWS - WIN_LENGTH + 1):
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
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLUMNS))


def get_column_input(current_player):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {current_player}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not is_valid_move(board, col):
            print("Invalid move. Column is out of bounds or full.")
            continue
        
        return col


def main():
    """Main game loop."""
    board = initialize_board()
    checkers_list = CHECKERS[:PLAYERS]
    current_player_index = random.randint(0, PLAYERS - 1)
    
    print_board(board)
    
    while True:
        current_checker = checkers_list[current_player_index]
        col = get_column_input(current_checker)
        
        place_checker(board, col, current_checker)
        print_board(board)
        
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        if is_board_full(board):
            print("Draw!")
            break
        
        current_player_index = (current_player_index + 1) % PLAYERS


if __name__ == "__main__":
    main()
