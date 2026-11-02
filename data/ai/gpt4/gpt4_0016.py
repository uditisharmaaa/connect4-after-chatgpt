import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"]
EMPTY_SPACE = " "

def create_board(rows, cols):
    """Creates an empty game board."""
    return [[EMPTY_SPACE for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    """Prints the Connect 4 board."""
    os.system('clear')
    column_labels = "  " + "   ".join([chr(65 + i) for i in range(len(board[0]))])  # A, B, C...
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_columns(board):
    """Returns a list of columns that are not full."""
    return [col for col in range(len(board[0])) if board[0][col] == EMPTY_SPACE]

def player_move(board, current_player):
    """Handles the current player's move."""
    valid_columns = get_valid_columns(board)
    while True:
        try:
            column = input(f"Player {PLAYER_CHECKERS[current_player]}, please enter a column: ").upper()
            col_index = ord(column) - 65  # Convert column letter to index
            if col_index not in valid_columns:
                raise ValueError
            return col_index
        except (ValueError, IndexError):
            print("Invalid input. Please choose a valid non-full column (A-G).")

def place_checker(board, col, checker):
    """Places a checker in the selected column."""
    for row in reversed(board):
        if row[col] == EMPTY_SPACE:
            row[col] = checker
            break

def check_for_winner(board, checker):
    """Checks if the given checker has won."""
    rows, cols = len(board), len(board[0])
    
    # Check horizontally
    for row in board:
        for col in range(cols - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Check vertically
    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Check diagonally (/)
    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    # Check diagonally (\)
    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Checks if the game is a draw."""
    return all(cell != EMPTY_SPACE for row in board for cell in row)

def main():
    # Initialize game variables
    board = create_board(ROWS, COLS)
    number_of_players = 2  # Set to 2 for submission, adjustable for more players
    current_player = random.randint(0, number_of_players - 1)
    game_over = False

    # Print initial board
    print_board(board)

    # Main game loop
    while not game_over:
        col = player_move(board, current_player)
        place_checker(board, col, PLAYER_CHECKERS[current_player])
        print_board(board)

        # Check for winner
        if check_for_winner(board, PLAYER_CHECKERS[current_player]):
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            game_over = True
            continue

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            game_over = True
            continue

        # Switch to next player
        current_player = (current_player + 1) % number_of_players

if __name__ == "__main__":
    main()
