import os
import random

# Constants
BOARD_COLS = 7  # Number of columns (A-G)
BOARD_ROWS = 6  # Number of rows
NUM_PLAYERS = 2  # Number of players (2-5)
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Player checkers

def initialize_board():
    """Create and return an empty board with specified dimensions."""
    return [[' ' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    # Print column headers (A, B, C, ...)
    headers = [chr(ord('A') + i) for i in range(BOARD_COLS)]
    print("  " + "   ".join(headers))
    
    # Print each row with borders
    border = "+" + ("---+" * BOARD_COLS)
    for row in board:
        print(border)
        print("| " + " | ".join(cell for cell in row) + " |")
    print(border)

def is_valid_column(column):
    """Check if the input column is valid (uppercase letter within board range)."""
    if len(column) != 1:
        return False
    col_char = column[0].upper()
    return 'A' <= col_char <= chr(ord('A') + BOARD_COLS - 1)

def get_column_index(column):
    """Convert column letter (A, B, etc.) to a 0-based index."""
    return ord(column.upper()) - ord('A')

def place_checker(board, column_index, checker):
    """
    Place the checker in the lowest available row of the specified column.
    Returns True if placement was successful, False otherwise (column full).
    """
    for row in range(BOARD_ROWS-1, -1, -1):
        if board[row][column_index] == ' ':
            board[row][column_index] = checker
            return True
    return False

def check_winner(board, checker):
    """Check if the specified checker has won by forming 4 in a row."""
    directions = [
        (0, 1),  # Horizontal
        (1, 0),  # Vertical
        (1, 1),  # Diagonal down-right
        (1, -1)  # Diagonal down-left
    ]
    
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == checker:
                for dr, dc in directions:
                    count = 1
                    for i in range(1, 4):
                        r, c = row + dr * i, col + dc * i
                        if 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS and board[r][c] == checker:
                            count += 1
                        else:
                            break
                    if count >= 4:
                        return True
    return False

def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    return all(cell != ' ' for row in board for cell in row)

def play_game():
    """Main function to play the Connect 4 game."""
    board = initialize_board()
    current_player = random.randint(0, NUM_PLAYERS - 1)
    
    while True:
        print_board(board)
        checker = PLAYERS[current_player]
        print(f"Player {checker}, please enter a column: ", end="")
        column_input = input().strip().upper()
        
        if not is_valid_column(column_input):
            print("Invalid input! Please enter a column letter (A-G).")
            continue
        
        col_index = get_column_index(column_input)
        if not place_checker(board, col_index, checker):
            print(f"Column {column_input} is full! You lose your turn.")
        
        # Check for win or draw
        if check_winner(board, checker):
            print_board(board)
            print(f"Player {checker} won!")
            break
        elif is_board_full(board):
            print_board(board)
            print("Game ended in a draw!")
            break
        
        # Switch to next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    play_game()
