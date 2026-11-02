import os
import random

# Global constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end="")
    print()
    
    # Print board rows
    for row in board:
        print("+---" * COLS + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * COLS + "+")


def get_next_available_row(board, col):
    """Return the next available row in the column, or -1 if full."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1


def is_valid_input(user_input, board):
    """Validate user input."""
    if len(user_input) != 1:
        return False
    if not user_input.isalpha():
        return False
    col = ord(user_input.upper()) - ord('A')
    if col < 0 or col >= COLS:
        return False
    if get_next_available_row(board, col) == -1:
        return False
    return True


def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    row = get_next_available_row(board, col)
    if row != -1:
        board[row][col] = checker


def check_win(board, checker):
    """Check if the checker has won."""
    # Check horizontally
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertically
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonally (top-right to bottom-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is full."""
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """Main game loop."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    print_board(board)
    
    while True:
        checker = CHECKERS[current_player]
        
        # Get valid input from player
        while True:
            user_input = input(f"Player {checker}, please enter a column: ").strip()
            if is_valid_input(user_input, board):
                col = ord(user_input.upper()) - ord('A')
                break
            print("Invalid input. Please try again.")
        
        # Place checker
        place_checker(board, col, checker)
        print_board(board)
        
        # Check for win
        if check_win(board, checker):
            print(f"Player {checker} won!")
            return
        
        # Check for draw
        if is_board_full(board):
            print("Draw!")
            return
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
