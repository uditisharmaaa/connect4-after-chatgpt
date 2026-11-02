import random
import os

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
WIN_LENGTH = 4
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]


def create_board():
    """Create and return an empty board with the specified dimensions."""
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    """Print the current state of the board with column labels."""
    os.system('clear')
    
    # Print column labels
    print("  ", end="")
    for col in range(COLS):
        print(f" {chr(65 + col)}  ", end="")
    print()
    
    # Print horizontal line
    print("+" + "---+" * COLS)
    
    # Print rows from top to bottom
    for row in range(ROWS):
        print("|", end="")
        for col in range(COLS):
            print(f" {board[row][col]} |", end="")
        print()
        print("+" + "---+" * COLS)


def is_valid_column(board, col):
    """Check if the column is valid and has space available."""
    if col < 0 or col >= COLS:
        return False
    # Check if top row of column has space
    return board[0][col] == " "


def drop_checker(board, col, symbol):
    """Drop a checker into the specified column and return the row where it landed."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == " ":
            board[row][col] = symbol
            return row
    return -1


def check_win(board, row, col, symbol):
    """Check if the last move at (row, col) resulted in a win."""
    
    # Check horizontal
    count = 0
    for c in range(COLS):
        if board[row][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check vertical
    count = 0
    for r in range(ROWS):
        if board[r][col] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
    r, c = start_row, start_col
    while r < ROWS and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
                return True
        else:
            count = 0
        r += 1
        c += 1
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
    r, c = start_row, start_col
    while r >= 0 and c < COLS:
        if board[r][c] == symbol:
            count += 1
            if count >= WIN_LENGTH:
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


def get_valid_input(board, player_symbol):
    """Get a valid column input from the player."""
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
            print(f"Invalid input. Please enter a letter between A and {chr(65 + COLS - 1)}.")
            continue
        
        # Check if column has space
        if not is_valid_column(board, col):
            print("Column is full. Please choose another column.")
            continue
        
        return col


def play_game():
    """Main game loop."""
    # Initialize game
    board = create_board()
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        
        # Get valid column from player
        col = get_valid_input(board, current_symbol)
        
        # Drop checker
        row = drop_checker(board, col, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col, current_symbol):
            print(f"Player {current_symbol} won!")
            break
        
        # Check for draw
        if is_board_full(board):
            print("The game is a draw!")
            break
        
        # Move to next player
        current_player_index = (current_player_index + 1) % NUM_PLAYERS


if __name__ == "__main__":
    play_game()
