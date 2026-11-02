import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board(rows, cols):
    """Create and return a board with all cells initialized to empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the Connect 4 board with column labels and borders."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(ord('A') + col)}   ", end="")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    
    print("+---" * cols + "+")


def is_valid_input(col_letter, cols):
    """Check if the input is a valid column letter."""
    if len(col_letter) != 1:
        return False
    
    col_index = ord(col_letter.upper()) - ord('A')
    return 0 <= col_index < cols


def get_column_index(col_letter):
    """Convert column letter to column index."""
    return ord(col_letter.upper()) - ord('A')


def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker, rows):
    """Place a checker in the lowest available position in the column."""
    for row in range(rows - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    return False


def get_player_move(current_player, checkers, cols):
    """Get valid input from the current player."""
    while True:
        col_letter = input(f"Player {checkers[current_player]}, please enter a column: ").strip()
        
        if not is_valid_input(col_letter, cols):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = get_column_index(col_letter)
        return col_index


def check_horizontal_win(board, rows, cols, checker):
    """Check if there's a horizontal win for the given checker."""
    for row in range(rows):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_vertical_win(board, rows, cols, checker):
    """Check if there's a vertical win for the given checker."""
    for col in range(cols):
        for row in range(rows - WIN_LENGTH + 1):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    return False


def check_diagonal_win(board, rows, cols, checker):
    """Check if there's a diagonal win for the given checker."""
    # Check diagonals going down-right
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(cols - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonals going down-left
    for row in range(rows - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, cols):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def check_win(board, rows, cols, checker):
    """Check if the current player has won."""
    return (check_horizontal_win(board, rows, cols, checker) or
            check_vertical_win(board, rows, cols, checker) or
            check_diagonal_win(board, rows, cols, checker))


def is_board_full(board, rows, cols):
    """Check if the board is completely filled."""
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize board
    board = initialize_board(ROWS, COLS)
    checkers = CHECKERS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board, COLS)
    
    # Game loop
    while True:
        # Get player move
        col_index = get_player_move(current_player, checkers, COLS)
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose this turn.")
            current_player = (current_player + 1) % NUM_PLAYERS
            continue
        
        # Place checker
        place_checker(board, col_index, checkers[current_player], ROWS)
        
        # Print board
        print_board(board, COLS)
        
        # Check for win
        if check_win(board, ROWS, COLS, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            break
        
        # Check for draw
        if is_board_full(board, ROWS, COLS):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
