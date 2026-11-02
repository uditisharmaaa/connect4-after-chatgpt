import os
import random

# Global constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the board with column labels and formatting."""
    os.system('clear')
    
    # Print column labels
    print("  " + "   ".join([chr(ord('A') + i) for i in range(COLS)]))
    
    # Print top border
    print("+---" * COLS + "+")
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+---" * COLS + "+")


def is_valid_move(board, col):
    """Check if a move is valid (column exists and has space)."""
    return 0 <= col < COLS and board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the lowest available row of the column."""
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


def get_player_move(board, player_name):
    """Get a valid move from the player."""
    while True:
        user_input = input(f"Player {player_name}, please enter a column: ").strip().upper()
        
        if len(user_input) != 1 or not user_input.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue
        
        col = ord(user_input) - ord('A')
        
        if not is_valid_move(board, col):
            print("Invalid move. Column is out of range or full.")
            continue
        
        return col


def main():
    """Main game loop."""
    board = initialize_board()
    checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        player_checker = checkers[current_player]
        col = get_player_move(board, player_checker)
        place_checker(board, col, player_checker)
        print_board(board)
        
        if check_win(board, player_checker):
            print(f"Player {player_checker} won!")
            break
        
        if is_board_full(board):
            print("It's a draw!")
            break
        
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
