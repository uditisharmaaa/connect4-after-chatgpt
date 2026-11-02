import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board(rows, cols):
    """Create and initialize the board with empty spaces."""
    return [[" " for _ in range(cols)] for _ in range(rows)]


def print_board(board, cols):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(cols):
        print(f"{chr(65 + col):^3}", end=" ")
    print()
    
    # Print board with borders
    for row in board:
        print("+---" * cols + "+")
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+---" * cols + "+")


def is_valid_input(column_letter, cols):
    """Check if the input is valid (single letter within board range)."""
    if len(column_letter) != 1:
        return False
    if not column_letter.isalpha():
        return False
    
    column_index = ord(column_letter.upper()) - ord('A')
    return 0 <= column_index < cols


def get_column_index(column_letter):
    """Convert column letter to column index."""
    return ord(column_letter.upper()) - ord('A')


def can_place_checker(board, col):
    """Check if a checker can be placed in the given column."""
    return board[0][col] == " "


def place_checker(board, col, checker):
    """Place a checker in the given column and return the row it was placed in."""
    # Find the lowest empty row in the column
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return row
    return -1  # Column is full


def check_win(board, row, col, checker, cols):
    """Check if the last placed checker resulted in a win."""
    rows = len(board)
    
    # Check horizontal
    count = 1
    # Check left
    c = col - 1
    while c >= 0 and board[row][c] == checker:
        count += 1
        c -= 1
    # Check right
    c = col + 1
    while c < cols and board[row][c] == checker:
        count += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    r = row - 1
    while r >= 0 and board[r][col] == checker:
        count += 1
        r -= 1
    # Check down
    r = row + 1
    while r < rows and board[r][col] == checker:
        count += 1
        r += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0 and board[r][c] == checker:
        count += 1
        r -= 1
        c -= 1
    # Check down-right
    r, c = row + 1, col + 1
    while r < rows and c < cols and board[r][c] == checker:
        count += 1
        r += 1
        c += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    r, c = row - 1, col + 1
    while r >= 0 and c < cols and board[r][c] == checker:
        count += 1
        r -= 1
        c += 1
    # Check down-left
    r, c = row + 1, col - 1
    while r < rows and c >= 0 and board[r][c] == checker:
        count += 1
        r += 1
        c -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def is_board_full(board):
    """Check if the board is full (draw condition)."""
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_move(current_player, cols):
    """Get valid input from the current player."""
    while True:
        column_letter = input(f"Player {current_player}, please enter a column: ").strip()
        
        if not is_valid_input(column_letter, cols):
            print(f"Invalid input. Please enter a single letter from A to {chr(65 + cols - 1)}.")
            continue
        
        col = get_column_index(column_letter)
        
        if not can_place_checker(board, col):
            print("This column is full. Please choose another column.")
            continue
        
        return col


def play_game(rows, cols, num_players):
    """Main game loop."""
    # Create and initialize the board
    board = create_board(rows, cols)
    
    # Get checkers for the players
    player_checkers = CHECKERS[:num_players]
    
    # Randomly select the first player
    current_player_index = random.randint(0, num_players - 1)
    
    # Print the initial board
    print_board(board, cols)
    
    # Game loop
    while True:
        current_checker = player_checkers[current_player_index]
        current_player = current_checker
        
        # Get player's move
        col = get_player_move(current_player, cols)
        
        # Place the checker and get the row it was placed in
        row = place_checker(board, col, current_checker)
        
        # Print the updated board
        print_board(board, cols)
        
        # Check for win
        if check_win(board, row, col, current_checker, cols):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("It's a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % num_players


if __name__ == "__main__":
    play_game(ROWS, COLS, NUM_PLAYERS)
