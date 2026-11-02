import os
import random

# Constants
ROWS = 6
COLS = 7
NUM_PLAYERS = 2
PLAYERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def initialize_board():
    """Create an empty board with the given dimensions."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the board with the current state."""
    # Clear the screen
    os.system('clear')
    
    # Print column headers (A, B, C, etc.)
    print('  ' + '   '.join(chr(65 + i) for i in range(COLS)))
    
    # Print the board rows
    for row in board:
        print('+---+' * COLS)
        print('| ' + ' | '.join(row) + ' |')
    
    # Print bottom border
    print('+---+' * COLS)

def is_valid_column(col):
    """Check if the column input is valid (a letter within bounds)."""
    if len(col) != 1:
        return False
    col = col.upper()
    return col.isalpha() and 'A' <= col <= chr(65 + COLS - 1)

def place_checker(board, col, checker):
    """
    Place the checker in the lowest available row in the specified column.
    Returns True if placement was successful, False otherwise.
    """
    col_index = ord(col.upper()) - ord('A')
    for row in range(ROWS - 1, -1, -1):
        if board[row][col_index] == ' ':
            board[row][col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check if the current player has won by having 4 in a row in any direction."""
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

    # Check diagonal down-right
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (board[row][col] == checker and
                board[row+1][col+1] == checker and
                board[row+2][col+2] == checker and
                board[row+3][col+3] == checker):
                return True

    # Check diagonal down-left
    for row in range(ROWS - 3):
        for col in range(3, COLS):
            if (board[row][col] == checker and
                board[row+1][col-1] == checker and
                board[row+2][col-2] == checker and
                board[row+3][col-3] == checker):
                return True

    return False

def is_draw(board):
    """Check if the board is full (draw)."""
    return all(cell != ' ' for row in board for cell in row)

def main():
    """Main function to run the Connect 4 game."""
    board = initialize_board()
    current_player = random.choice(PLAYERS)
    
    while True:
        print_board(board)
        print(f"Player {current_player}, please enter a column:")
        
        # Get column input and validate
        col = input().strip()
        while not is_valid_column(col):
            print("Invalid input. Please enter a valid column (A-G):")
            col = input().strip()
        col = col.upper()
        
        # Place the checker
        if place_checker(board, col, current_player):
            # Check for win after placing
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} won!")
                break
            # Check for draw
            if is_draw(board):
                print_board(board)
                print("Game ended in a draw!")
                break
            # Switch to next player
            current_player = PLAYERS[(PLAYERS.index(current_player) + 1) % NUM_PLAYERS]
        else:
            print("Column is full. Try another column.")

if __name__ == "__main__":
    main()
