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
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f"  {chr(65 + col)} ", end="")
    print()
    
    # Print rows with borders
    for row in range(ROWS):
        print("  " + "+---" * COLS + "+")
        print("  ", end="")
        for col in range(COLS):
            print(f"| {board[row][col]} ", end="")
        print("|")
    
    # Print bottom border
    print("  " + "+---" * COLS + "+")


def is_valid_column(column_input):
    """Check if the column input is a valid letter within range."""
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
    """Check if the specified column is full."""
    return board[0][col_index] != " "


def place_checker(board, col_index, symbol):
    """Place a checker in the specified column and return the row index."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (top-left to bottom-right)
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    count = 0
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (bottom-left to top-right)
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    count = 0
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count == WIN_LENGTH:
                return True
        else:
            count = 0
        r -= 1
        c += 1
    
    return False


def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True


def get_player_move(board, player_symbol):
    """Get and validate player input for their move."""
    while True:
        column_input = input(f"Player {player_symbol}, please enter a column: ")
        
        # Validate input
        if not is_valid_column(column_input):
            print("Invalid input. Please enter a valid column letter.")
            continue
        
        col_index = ord(column_input) - 65
        
        # Check if column is full
        if is_column_full(board, col_index):
            print("Column is full. Please choose another column.")
            continue
        
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
    game_over = False
    while not game_over:
        player_symbol = players[current_player_index]
        
        # Get player move
        col_index = get_player_move(board, player_symbol)
        
        # Place checker
        row_index = place_checker(board, col_index, player_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row_index, col_index, player_symbol):
            print(f"Player {player_symbol} won!")
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
