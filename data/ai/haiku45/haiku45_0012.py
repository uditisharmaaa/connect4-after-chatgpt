import os
import random

# Constants
COLS = 7
ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and return an empty board with all spaces."""
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board with borders
    for row in range(ROWS):
        # Top border
        print("+", end="")
        for col in range(COLS):
            print("---+", end="")
        print()
        
        # Row content
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Bottom border
    print("+", end="")
    for col in range(COLS):
        print("---+", end="")
    print()


def get_valid_column():
    """Get a valid column input from the user."""
    while True:
        user_input = input("Please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col_index = ord(user_input) - ord('A')
        
        # Check if column is within board bounds
        if col_index < 0 or col_index >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        return col_index


def is_column_full(board, col):
    """Check if a column is completely filled."""
    return board[0][col] != " "


def place_checker(board, col, checker):
    """Place a checker in the specified column and return the row where it was placed."""
    # Find the lowest empty row in the column
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    
    return -1  # Column is full


def check_horizontal_win(board, row, col, checker):
    """Check if there is a horizontal win from the placed checker."""
    count = 1
    
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    
    # Check right
    c = col + 1
    while c < COLS and board[row][c] == checker:
        count += 1
        c += 1
    
    return count >= WIN_LENGTH


def check_vertical_win(board, row, col, checker):
    """Check if there is a vertical win from the placed checker."""
    count = 1
    
    # Check down
    r = row + 1
    while r < ROWS and board[r][col] == checker:
        count += 1
        r += 1
    
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    
    return count >= WIN_LENGTH


def check_diagonal_win(board, row, col, checker):
    """Check if there is a diagonal win (both directions) from the placed checker."""
    # Check diagonal from top-left to bottom-right
    count = 1
    
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    
    # Check down-right
    r, c = row + 1, col + 1
    while r < ROWS and c < COLS and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal from top-right to bottom-left
    count = 1
    
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < COLS and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    
    # Check down-left
    r, c = row + 1, col - 1
    while r < ROWS and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    
    return count >= WIN_LENGTH


def check_win(board, row, col, checker):
    """Check if the placed checker resulted in a win."""
    return (check_horizontal_win(board, row, col, checker) or
            check_vertical_win(board, row, col, checker) or
            check_diagonal_win(board, row, col, checker))


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == " ":
                return False
    return True


def play_game():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    current_checker = CHECKERS[current_player_index]
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        # Ask current player for input
        print(f"Player {current_checker}, please enter a column: ", end="")
        col = get_valid_column()
        
        # Check if column is full
        if is_column_full(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        # Place checker
        row = place_checker(board, col, current_checker)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS
        current_checker = CHECKERS[current_player_index]


if __name__ == "__main__":
    play_game()
