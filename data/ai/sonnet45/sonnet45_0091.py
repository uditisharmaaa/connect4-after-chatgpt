import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
CHECKERS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(column_input):
    """Check if the column input is a valid letter."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    col_index = ord(column_input) - 65
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def is_column_full(board, col_index):
    """Check if a column is completely filled."""
    return board[0][col_index] != " "


def place_checker(board, col_index, checker):
    """Place a checker in the specified column. Returns True if successful, False otherwise."""
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = checker
            return True
    
    return False


def check_win(board, checker):
    """Check if the specified checker has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == checker for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, COLS):
            if all(board[row + i][col - i] == checker for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely filled."""
    return all(board[0][col] != " " for col in range(COLS))


def get_player_input(player_checker):
    """Get and validate player input for column selection."""
    while True:
        column_input = input(f"Player {player_checker}, please enter a column: ")
        
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        return ord(column_input) - 65


def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Select random starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_checker = CHECKERS[current_player_index]
        
        # Get player input
        col_index = get_player_input(current_checker)
        
        # Try to place the checker
        if not place_checker(board, col_index, current_checker):
            print("Column is full. You lose your turn.")
            print_board(board)
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_checker):
            print(f"Player {current_checker} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
