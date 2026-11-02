import random
import os

# Global constants
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
    
    # Print bottom border
    print("+" + "---+" * COLS)


def is_valid_column(col_letter, board):
    """Check if the column letter is valid and has space."""
    # Check if input is a single uppercase letter
    if len(col_letter) != 1 or not col_letter.isupper():
        return False, "Invalid input. Please enter an uppercase letter."
    
    # Check if column is within board range
    col_index = ord(col_letter) - ord('A')
    if col_index < 0 or col_index >= COLS:
        return False, f"Column out of range. Please enter a letter between A and {chr(65 + COLS - 1)}."
    
    # Check if column has space
    if board[0][col_index] != " ":
        return False, "Column is full. Please choose another column."
    
    return True, col_index


def place_checker(board, col_index, symbol):
    """Place a checker in the specified column and return the row where it landed."""
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
    
    # Check diagonal (bottom-left to top-right)
    count = 0
    start_row = row - min(row, col)
    start_col = col - min(row, col)
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
    
    # Check diagonal (top-left to bottom-right)
    count = 0
    start_row = row + min(ROWS - 1 - row, col)
    start_col = col - min(ROWS - 1 - row, col)
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


def play_game():
    """Main game loop."""
    # Initialize the board
    board = create_board()
    
    # Get player symbols
    players = [PLAYER_SYMBOLS[i] for i in range(NUM_PLAYERS)]
    
    # Randomly select the starting player
    current_player_index = random.randint(0, NUM_PLAYERS - 1)
    
    # Print initial board
    print_board(board)
    
    # Game loop
    while True:
        current_symbol = players[current_player_index]
        
        # Get valid input from player
        while True:
            col_input = input(f"Player {current_symbol}, please enter a column: ")
            valid, result = is_valid_column(col_input, board)
            
            if valid:
                col_index = result
                break
            else:
                print(result)
        
        # Place the checker
        row = place_checker(board, col_index, current_symbol)
        
        # Print updated board
        print_board(board)
        
        # Check for win
        if check_win(board, row, col_index, current_symbol):
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
