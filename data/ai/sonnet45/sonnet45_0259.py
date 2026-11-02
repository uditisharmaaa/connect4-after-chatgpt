import random
import os

# Constants for board dimensions and number of players
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4

# Player symbols
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]


def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for i in range(NUM_COLS):
        print(f"{chr(65 + i)}   ", end="")
    print()
    
    # Print rows with borders
    for row in board:
        print("+" + "---+" * NUM_COLS)
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
    print("+" + "---+" * NUM_COLS)


def is_valid_column(col_letter, board):
    """Check if the column input is valid and has space."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper() or not col_letter.isalpha():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - 65
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= NUM_COLS:
        return False
    
    # Check if column has space (top row is not full)
    if board[0][col_index] != " ":
        return False
    
    return True


def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column and return the row where it landed."""
    col_index = ord(col_letter) - 65
    
    # Find the lowest available row in the column
    for row in range(NUM_ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    
    return -1


def check_win(board, symbol):
    """Check if the given symbol has won the game."""
    # Check horizontal
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check vertical
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(NUM_ROWS - WIN_LENGTH + 1):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, NUM_ROWS):
        for col in range(NUM_COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    return all(board[0][col] != " " for col in range(NUM_COLS))


def get_player_input(player_symbol, board):
    """Get valid input from the player."""
    while True:
        col_letter = input(f"Player {player_symbol}, please enter a column: ").strip()
        
        if is_valid_column(col_letter, board):
            return col_letter
        else:
            print("Invalid input. Please enter a valid column letter.")


def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Get player symbols for this game
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_symbol = players[current_player_index]
        
        # Get player input
        col_letter = get_player_input(current_symbol, board)
        
        # Place the checker
        place_checker(board, col_letter, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Move to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
