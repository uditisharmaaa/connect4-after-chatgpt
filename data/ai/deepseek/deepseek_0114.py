import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
PLAYER_CHECKS = ['X', 'O', 'V', 'H', 'M']  # Checkers for up to 5 players

def initialize_board():
    """Initialize the Connect 4 board with empty spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board with borders and column labels."""
    os.system('clear')  # Clear the screen before printing the board
    # Print column labels (A, B, C, ...)
    print('  ' + '   '.join([chr(65 + i) for i in range(COLS)]))
    # Print the board rows with borders
    for row in range(ROWS):
        print('+---+' * COLS)
        print('| ' + ' | '.join(board[row]) + ' |')
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid (A, B, ..., G, etc.)."""
    if len(col) != 1:
        return False
    return col.upper() in [chr(65 + i) for i in range(COLS)]

def place_checker(board, col, checker):
    """Place the checker in the lowest empty row of the specified column.
    Returns True if placement was successful, False otherwise."""
    col_idx = ord(col.upper()) - 65  # Convert column letter to index (A -> 0, B -> 1, etc.)
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom row
        if board[row][col_idx] == ' ':
            board[row][col_idx] = checker
            return True
    return False  # Column is full

def check_winner(board, checker):
    """Check if the current player has connected 4 checkers in any direction."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row][col+1] == checker and 
                board[row][col+2] == checker and 
                board[row][col+3] == checker):
                return True
    # Check vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if (board[row][col] == checker and 
                board[row+1][col] == checker and 
                board[row+2][col] == checker and 
                board[row+3][col] == checker):
                return True
    # Check diagonal (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row+1][col+1] == checker and 
                board[row+2][col+2] == checker and 
                board[row+3][col+3] == checker):
                return True
    # Check diagonal (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (board[row][col] == checker and 
                board[row-1][col+1] == checker and 
                board[row-2][col+2] == checker and 
                board[row-3][col+3] == checker):
                return True
    return False  # No winner found

def is_draw(board):
    """Check if the board is full (draw)."""
    for row in board:
        if ' ' in row:
            return False
    return True

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, PLAYERS - 1)  # Randomly choose starting player

    while True:
        print_board(board)
        checker = PLAYER_CHECKS[current_player]
        print(f"Player {checker}, please enter a column: ")
        col = input().strip()

        if not is_valid_column(col):
            print("Invalid input! Please enter a valid column (A, B, C, ...)")
            continue

        if not place_checker(board, col, checker):
            print("Column is full! You lose your turn.")
        else:
            if check_winner(board, checker):
                print_board(board)
                print(f"Player {checker} won!")
                break
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                break

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

if __name__ == "__main__":
    main()
