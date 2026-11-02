import os
import random

# Constants for the game
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Supports up to 5 players
PLAYER_CHECKERS = CHECKERS[:PLAYERS]

def create_board(rows, columns):
    """Create an empty game board initialized with whitespaces."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the game board."""
    os.system('clear')  # Clear the terminal screen
    column_labels = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Generate column labels
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(row) + "+")

def get_column_index(input_char, columns):
    """Convert column letter to index. Returns -1 if invalid."""
    if len(input_char) == 1 and input_char.isalpha():
        index = ord(input_char.upper()) - 65  # Convert letter to index
        if 0 <= index < columns:
            return index
    return -1

def drop_checker(board, column_index, checker):
    """Place a checker in the specified column. Returns success status."""
    for row in reversed(board):  # Start from the bottom row
        if row[column_index] == " ":
            row[column_index] = checker
            return True
    return False  # Column is full

def is_winning_move(board, checker):
    """Check if the last move resulted in a win."""
    rows, cols = len(board), len(board[0])

    # Check horizontally, vertically, and diagonally
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == checker:
                # Horizontally
                if c + 3 < cols and all(board[r][c + i] == checker for i in range(4)):
                    return True
                # Vertically
                if r + 3 < rows and all(board[r + i][c] == checker for i in range(4)):
                    return True
                # Diagonally (\ direction)
                if r + 3 < rows and c + 3 < cols and all(board[r + i][c + i] == checker for i in range(4)):
                    return True
                # Diagonally (/ direction)
                if r + 3 < rows and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4)):
                    return True
    return False

def is_draw(board):
    """Check if the board is full, resulting in a draw."""
    return all(cell != " " for row in board for cell in row)

def main():
    # Initialize the game
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, PLAYERS - 1)  # Randomly pick the starting player
    total_moves = 0
    max_moves = ROWS * COLUMNS

    print_board(board)

    # Main game loop
    while total_moves < max_moves:
        player_checker = PLAYER_CHECKERS[current_player]
        print(f"Player {player_checker}, please enter a column:")

        # Get valid input
        while True:
            choice = input().strip()
            col_index = get_column_index(choice, COLUMNS)
            if col_index != -1 and drop_checker(board, col_index, player_checker):
                break
            else:
                print("Invalid input. Please try again:")

        print_board(board)
        total_moves += 1

        # Check win
        if is_winning_move(board, player_checker):
            print(f"Player {player_checker} won!")
            return

        # Check draw
        if is_draw(board):
            print("The game is a draw!")
            return

        # Switch to the next player
        current_player = (current_player + 1) % PLAYERS

    print("The game is a draw!")  # In case the loop ends without a win

if __name__ == "__main__":
    main()
