import os
import random

# Constants for the game configuration
ROWS = 6
COLS = 7
PLAYERS = ['X', 'O', 'V', 'H', 'M']  # Up to 5 players

def create_board():
    """Create a 2D board initialized with spaces."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clears the terminal for a clean view
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))  # Column labels A to G
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column):
    """Check if the input is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < COLS

def find_next_empty_row(board, col):
    """Find the next empty row in the specified column."""
    for row in range(ROWS - 1, -1, -1):  # Start from the bottom
        if board[row][col] == ' ':
            return row
    return -1  # No empty space available

def drop_checker(board, col, checker):
    """Drop the checker in the specified column."""
    row = find_next_empty_row(board, col)
    if row != -1:
        board[row][col] = checker
        return True
    return False

def check_winner(board, checker):
    """Check for a winner in the current board."""
    # Check horizontal locations
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical locations
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check positively sloped diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True
    
    # Check negatively sloped diagonals
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r - i][c + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, indicating a draw."""
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    board = create_board()
    current_player = random.choice(PLAYERS)
    turn = 0

    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-G):")
        column_input = input().strip()

        if not is_valid_input(column_input):
            print("Invalid input. Please enter a valid column (A-G).")
            continue
        
        col_index = ord(column_input.upper()) - 65

        if not drop_checker(board, col_index, current_player):
            print("Column is full. Please choose another column.")
            continue

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        
        if check_draw(board):
            print("The game is a draw!")
            break
        
        # Switch to the next player
        turn = (turn + 1) % len(PLAYERS)
        current_player = PLAYERS[turn]

# Run the main program
if __name__ == "__main__":
    main()
