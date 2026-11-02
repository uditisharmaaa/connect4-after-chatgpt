import random
import os

# Constants
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# List of possible checkers for each player
CHECKERS = ["X", "O", "V", "H", "M"]


def initialize_board():
    """Create and initialize the game board with empty spaces."""
    board = []
    for row in range(BOARD_ROWS):
        board_row = []
        for col in range(BOARD_COLS):
            board_row.append(" ")
        board.append(board_row)
    return board


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(BOARD_COLS):
        print(chr(65 + col) + "   ", end="")
    print()
    
    # Print each row with borders
    for row in range(BOARD_ROWS):
        print("+---" * BOARD_COLS + "+")
        print("|", end="")
        for col in range(BOARD_COLS):
            print(" " + board[row][col] + " |", end="")
        print()
    
    print("+---" * BOARD_COLS + "+")


def get_player_input(current_player):
    """Get and validate the player's column choice."""
    while True:
        user_input = input(f"Player {CHECKERS[current_player]}, please enter a column: ").upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single letter.")
            continue
        
        # Check if input is a valid column letter
        if user_input < 'A' or user_input >= chr(65 + BOARD_COLS):
            print(f"Invalid column. Please enter a letter between A and {chr(64 + BOARD_COLS)}.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - 65
        
        # Check if column is not full
        if board[0][col] != " ":
            print("Column is full. Please choose another column.")
            continue
        
        return col


def place_checker(board, col, current_player):
    """Place the checker in the specified column."""
    # Find the lowest available row in the column
    for row in range(BOARD_ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = CHECKERS[current_player]
            return row
    
    return -1  # Column is full


def check_win(board, row, col, current_player):
    """Check if the current player has won."""
    checker = CHECKERS[current_player]
    
    # Check horizontal
    count = 1
    # Check left
    j = col - 1
    while j >= 0 and board[row][j] == checker:
        count += 1
        j -= 1
    # Check right
    j = col + 1
    while j < BOARD_COLS and board[row][j] == checker:
        count += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check vertical
    count = 1
    # Check up
    i = row - 1
    while i >= 0 and board[i][col] == checker:
        count += 1
        i -= 1
    # Check down
    i = row + 1
    while i < BOARD_ROWS and board[i][col] == checker:
        count += 1
        i += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-left to bottom-right)
    count = 1
    # Check up-left
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0 and board[i][j] == checker:
        count += 1
        i -= 1
        j -= 1
    # Check down-right
    i, j = row + 1, col + 1
    while i < BOARD_ROWS and j < BOARD_COLS and board[i][j] == checker:
        count += 1
        i += 1
        j += 1
    if count >= WIN_LENGTH:
        return True
    
    # Check diagonal (top-right to bottom-left)
    count = 1
    # Check up-right
    i, j = row - 1, col + 1
    while i >= 0 and j < BOARD_COLS and board[i][j] == checker:
        count += 1
        i -= 1
        j += 1
    # Check down-left
    i, j = row + 1, col - 1
    while i < BOARD_ROWS and j >= 0 and board[i][j] == checker:
        count += 1
        i += 1
        j -= 1
    if count >= WIN_LENGTH:
        return True
    
    return False


def check_draw(board):
    """Check if the board is full (draw condition)."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                return False
    return True


def main():
    """Main game loop."""
    # Initialize the board
    board = initialize_board()
    
    # Select a random starting player
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        # Get player input
        col = get_player_input(current_player)
        
        # Place the checker
        row = place_checker(board, col, current_player)
        
        # Print the board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {CHECKERS[current_player]} won!")
            game_over = True
        # Check for draw
        elif check_draw(board):
            print("It's a draw!")
            game_over = True
        else:
            # Switch to the next player
            current_player = (current_player + 1) % NUM_PLAYERS


if __name__ == "__main__":
    main()
