import os
import random

# Constants for board dimensions and player checkers
ROWS = 6
COLS = 7
CHECKERS = ['X', 'O', 'V', 'H', 'M']

def create_board():
    """Create a 2D list representing the Connect 4 board."""
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')  # Clear the terminal screen
    print("  " + "   ".join(chr(65 + i) for i in range(COLS)))
    print("+" + "---+" * COLS)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * COLS)

def is_valid_input(column, board):
    """Check if the input column is valid."""
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65  # Convert A-G to 0-6
    return 0 <= col_index < COLS and board[0][col_index] == ' '

def place_checker(board, column, checker):
    """Place the checker in the specified column following the gravity rule."""
    col_index = ord(column.upper()) - 65
    for row in reversed(board):
        if row[col_index] == ' ':
            row[col_index] = checker
            return True
    return False

def check_win(board, checker):
    """Check all possible win conditions (horizontal, vertical, diagonal)."""
    # Check horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonal \
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Check diagonal /
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(board[0][col] != ' ' for col in range(COLS))

def main():
    board = create_board()
    players = CHECKERS[:2]  # Use the first two checkers for a two-player game
    current_player = random.choice(players)  # Randomly select the first player
    
    print_board(board)

    while True:
        print(f"Player {current_player}, please enter a column (A-{chr(65 + COLS - 1)}):")
        column = input().strip().upper()

        if not is_valid_input(column, board):
            print("Invalid input. Please enter a valid column.")
            continue

        place_checker(board, column, current_player)
        print_board(board)

        # Check for win or draw
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player = players[(players.index(current_player) + 1) % len(players)]

if __name__ == "__main__":
    main()
