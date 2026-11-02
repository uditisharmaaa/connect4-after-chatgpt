import os
import random

# Global constants
BOARD_COLUMNS = 7
BOARD_ROWS = 6
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and initialize the game board with empty spaces."""
    board = [[" " for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLUMNS):
        print(f" {chr(65 + col)} ", end=" ")
    print()
    
    # Print board rows
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLUMNS + "+")
        print("|", end="")
        for col in range(BOARD_COLUMNS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * BOARD_COLUMNS + "+")


def get_player_checkers(num_players):
    """Return a list of checkers for the given number of players."""
    return CHECKERS[:num_players]


def get_valid_input(board, current_player, checkers):
    """Get valid column input from the player."""
    while True:
        user_input = input(f"Player {checkers[current_player]}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within board dimensions
        if col < 0 or col >= BOARD_COLUMNS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + BOARD_COLUMNS - 1)}.")
            continue
        
        # Check if column is full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, checker):
    """Place a checker in the specified column."""
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = checker
            return


def check_win(board, last_row, last_col, checker):
    """Check if the last placed checker resulted in a win."""
    # Check horizontal
    count = 1
    # Check left
    col = last_col - 1
    while col >= 0 and board[last_row][col] == checker:
        count += 1
        col -= 1
    # Check right
    col = last_col + 1
    while col < BOARD_COLUMNS and board[last_row][col] == checker:
        count += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    row = last_row - 1
    while row >= 0 and board[row][last_col] == checker:
        count += 1
        row -= 1
    # Check down
    row = last_row + 1
    while row < BOARD_ROWS and board[row][last_col] == checker:
        count += 1
        row += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    row, col = last_row - 1, last_col - 1
    while row >= 0 and col >= 0 and board[row][col] == checker:
        count += 1
        row -= 1
        col -= 1
    # Check down-right
    row, col = last_row + 1, last_col + 1
    while row < BOARD_ROWS and col < BOARD_COLUMNS and board[row][col] == checker:
        count += 1
        row += 1
        col += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    row, col = last_row - 1, last_col + 1
    while row >= 0 and col < BOARD_COLUMNS and board[row][col] == checker:
        count += 1
        row -= 1
        col += 1
    # Check down-left
    row, col = last_row + 1, last_col - 1
    while row < BOARD_ROWS and col >= 0 and board[row][col] == checker:
        count += 1
        row += 1
        col -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def get_last_checker_position(board, col, checker):
    """Find the row where the last checker was placed in the given column."""
    for row in range(BOARD_ROWS):
        if board[row][col] == checker:
            return row
    return -1


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for col in range(BOARD_COLUMNS):
        if board[0][col] == " ":
            return False
    return True


def play_game():
    """Main game loop."""
    board = initialize_board()
    checkers = get_player_checkers(NUM_PLAYERS)
    
    # Randomly select the first player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get valid column input
        col = get_valid_input(board, current_player, checkers)
        
        # Place checker
        place_checker(board, col, checkers[current_player])
        
        # Find the row of the placed checker
        last_row = get_last_checker_position(board, col, checkers[current_player])
        
        # Print board
        print_board(board)
        
        # Check for win
        if check_win(board, last_row, col, checkers[current_player]):
            print(f"Player {checkers[current_player]} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("Draw!")
            game_over = True
        else:
            # Switch to next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
