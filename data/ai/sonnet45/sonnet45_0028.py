import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column labels
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
    print("+" + "---+" * COLS)

def is_valid_column(col_letter, board):
    """Check if the column input is valid."""
    # Check if input is a single character
    if len(col_letter) != 1:
        return False
    
    # Check if it's an uppercase letter
    if not col_letter.isupper():
        return False
    
    # Convert letter to column index
    col_index = ord(col_letter) - ord('A')
    
    # Check if column is within board bounds
    if col_index < 0 or col_index >= COLS:
        return False
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False
    
    return True

def place_checker(board, col_letter, symbol):
    """Place a checker in the specified column."""
    col_index = ord(col_letter) - ord('A')
    
    # Find the lowest available row
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == " ":
            board[row][col_index] = symbol
            return row, col_index
    
    return -1, -1

def check_win(board, row, col, symbol):
    """Check if the last move resulted in a win."""
    # Check horizontal
    if check_direction(board, row, col, symbol, 0, 1):
        return True
    
    # Check vertical
    if check_direction(board, row, col, symbol, 1, 0):
        return True
    
    # Check diagonal (top-left to bottom-right)
    if check_direction(board, row, col, symbol, 1, 1):
        return True
    
    # Check diagonal (bottom-left to top-right)
    if check_direction(board, row, col, symbol, -1, 1):
        return True
    
    return False

def check_direction(board, row, col, symbol, delta_row, delta_col):
    """Check for WIN_LENGTH consecutive symbols in a given direction."""
    count = 1  # Count the placed checker
    
    # Check in positive direction
    r, c = row + delta_row, col + delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r += delta_row
        c += delta_col
    
    # Check in negative direction
    r, c = row - delta_row, col - delta_col
    while 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == symbol:
        count += 1
        r -= delta_row
        c -= delta_col
    
    return count >= WIN_LENGTH

def is_board_full(board):
    """Check if the board is completely full."""
    for col in range(COLS):
        if board[0][col] == " ":
            return False
    return True

def get_player_input(player_symbol, board):
    """Get and validate player input."""
    while True:
        col_letter = input(f"Player {player_symbol}, please enter a column: ").upper()
        
        if is_valid_column(col_letter, board):
            return col_letter
        else:
            print("Invalid input. Please enter a valid column letter.")

def play_game():
    """Main game loop."""
    # Initialize board
    board = create_board()
    
    # Select players
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    game_over = False
    while not game_over:
        current_player = players[current_player_index]
        
        # Get player input
        col_letter = get_player_input(current_player, board)
        
        # Place checker
        row, col = place_checker(board, col_letter, current_player)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_player):
            print(f"Player {current_player} won!")
            game_over = True
        # Check for draw
        elif is_board_full(board):
            print("The game is a draw!")
            game_over = True
        else:
            # Switch to next player
            current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
