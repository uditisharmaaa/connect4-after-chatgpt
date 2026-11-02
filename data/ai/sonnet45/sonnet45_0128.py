import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

def create_board():
    """Create and return an empty game board."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    
    # Print column letters
    print("  ", end="")
    for i in range(COLS):
        print(f" {chr(65 + i)}  ", end="")
    print()
    
    # Print horizontal separator
    print("+" + "---+" * COLS)
    
    # Print each row
    for row in board:
        print("|", end="")
        for cell in row:
            print(f" {cell} |", end="")
        print()
        print("+" + "---+" * COLS)

def is_valid_move(board, col):
    """Check if a move is valid (column has space)."""
    if col < 0 or col >= COLS:
        return False
    return board[0][col] == " "

def get_next_row(board, col):
    """Find the next available row in the given column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            return row
    return -1

def place_checker(board, col, symbol):
    """Place a checker in the specified column."""
    row = get_next_row(board, col)
    if row != -1:
        board[row][col] = symbol
        return True
    return False

def check_horizontal(board, symbol):
    """Check for horizontal win."""
    for row in range(ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    return False

def check_vertical(board, symbol):
    """Check for vertical win."""
    for col in range(COLS):
        for row in range(ROWS - WIN_LENGTH + 1):
            if all(board[row + i][col] == symbol for i in range(WIN_LENGTH)):
                return True
    return False

def check_diagonal(board, symbol):
    """Check for diagonal wins (both directions)."""
    # Check diagonal (bottom-left to top-right)
    for row in range(WIN_LENGTH - 1, ROWS):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row - i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    # Check diagonal (top-left to bottom-right)
    for row in range(ROWS - WIN_LENGTH + 1):
        for col in range(COLS - WIN_LENGTH + 1):
            if all(board[row + i][col + i] == symbol for i in range(WIN_LENGTH)):
                return True
    
    return False

def check_win(board, symbol):
    """Check if the player with given symbol has won."""
    return (check_horizontal(board, symbol) or 
            check_vertical(board, symbol) or 
            check_diagonal(board, symbol))

def is_board_full(board):
    """Check if the board is completely filled."""
    return all(board[0][col] != " " for col in range(COLS))

def get_valid_input(board, player_symbol):
    """Get and validate player input."""
    while True:
        user_input = input(f"Player {player_symbol}, please enter a column: ").strip().upper()
        
        # Check if input is a single character
        if len(user_input) != 1:
            print("Invalid input. Please enter a single column letter.")
            continue
        
        # Check if input is a letter
        if not user_input.isalpha():
            print("Invalid input. Please enter a letter.")
            continue
        
        # Convert letter to column index
        col = ord(user_input) - ord('A')
        
        # Check if column is within bounds
        if col < 0 or col >= COLS:
            print(f"Invalid column. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_move(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col

def play_game():
    """Main game loop."""
    board = create_board()
    players = PLAYER_SYMBOLS[:NUM_PLAYERS]
    
    # Randomly select first player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        
        # Get valid input from player
        col = get_valid_input(board, current_symbol)
        
        # Place checker
        place_checker(board, col, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Switch to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
