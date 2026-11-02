import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols in order
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the game board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"{chr(65 + col)}   ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("+---" * COLS + "+")
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
    print("+---" * COLS + "+")


def is_valid_column(column_input):
    """Check if the column input is a valid letter."""
    if len(column_input) != 1:
        return False
    if not column_input.isalpha():
        return False
    if not column_input.isupper():
        return False
    col_index = ord(column_input) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False
    return True


def is_column_full(board, col_index):
    """Check if a column is completely full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, symbol):
    """Place a checker in the specified column. Returns True if successful, False otherwise."""
    if is_column_full(board, col_index):
        return False
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return True
    
    return False


def check_win(board, symbol):
    """Check if the given symbol has won the game."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full (draw condition)."""
    return all(board[0][col] != " " for col in range(COLS))


def get_player_move(board, player_symbol):
    """Get a valid move from the player."""
    while True:
        column_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Validate input
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(column_input) - ord('A')
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. You lose your turn.")
            return None
        
        return col_index


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Set up players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_player = players[current_player_index]
        
        # Get player move
        col_index = get_player_move(board, current_player)
        
        # Place checker (None means column was full, player loses turn)
        if col_index is not None:
            place_checker(board, col_index, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if col_index is not None and check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
