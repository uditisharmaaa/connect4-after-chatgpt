import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_COUNT = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column headers
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print each row with borders
    for row in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(column_input):
    """Check if the column input is a valid letter within board range."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    col_index = ord(column_input) - ord('A')
    return 0 <= col_index < COLS


def get_column_input(player_symbol):
    """Get valid column input from the player."""
    while True:
        column_input = input(f"Player {player_symbol}, please enter a column: ")
        if is_valid_column(column_input):
            return ord(column_input) - ord('A')
        else:
            print("Invalid input. Please enter a valid column letter.")


def place_checker(board, col, player_symbol):
    """
    Place a checker in the specified column.
    Returns True if successful, False if column is full.
    """
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = player_symbol
            return True
    return False


def check_win(board, player_symbol):
    """Check if the specified player has won."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row][col + i] == player_symbol for i in range(WIN_COUNT)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS):
            if all(board[row + i][col] == player_symbol for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal (down-right)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(COLS - WIN_COUNT + 1):
            if all(board[row + i][col + i] == player_symbol for i in range(WIN_COUNT)):
                return True
    
    # Check diagonal (down-left)
    for row in range(ROWS - WIN_COUNT + 1):
        for col in range(WIN_COUNT - 1, COLS):
            if all(board[row + i][col - i] == player_symbol for i in range(WIN_COUNT)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(COLS))


def play_game():
    """Main game loop."""
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get player input
        col = get_column_input(current_player)
        
        # Try to place the checker
        if not place_checker(board, col, current_player):
            print("Column is full! You lose your turn.")
            current_player_index = (current_player_index + 1) % NUM_PLAYERS
            continue
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
