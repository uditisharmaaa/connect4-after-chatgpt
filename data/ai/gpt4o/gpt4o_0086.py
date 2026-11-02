import os
import random

# Constants
NUM_ROWS = 6
NUM_COLUMNS = 7
MAX_PLAYERS = 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
# For submission
CURRENT_NUM_PLAYERS = 2

def init_board(rows, columns):
    """Initialize the game board with whitespaces."""
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Print the current state of the board."""
    os.system('clear')
    column_labels = "  ".join(chr(65 + i) for i in range(len(board[0])))
    print(column_labels)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def get_valid_column(board):
    """Prompt and validate the user's column choice."""
    while True:
        choice = input("Please enter a column: ").strip().upper()
        if choice and len(choice) == 1 and choice in 'ABCDEFG':
            column_index = ord(choice) - 65
            if board[0][column_index] == ' ':
                return column_index
            else:
                print("Column is full, please select another column.")
        else:
            print("Invalid input. Please enter a valid column letter (A-G).")

def place_checker(board, column, checker):
    """Place the checker in the chosen column."""
    for row in reversed(board):
        if row[column] == ' ':
            row[column] = checker
            break

def check_win(board, checker):
    """Check if the current player has won the game."""
    # Check horizontally, vertically, and diagonally
    num_rows = len(board)
    num_columns = len(board[0])

    # Horizontal check
    for row in board:
        for col in range(num_columns - 3):
            if all(row[col + i] == checker for i in range(4)):
                return True

    # Vertical check
    for col in range(num_columns):
        for row in range(num_rows - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal checks
    # Positive diagonals (bottom-left to top-right)
    for row in range(num_rows - 3):
        for col in range(num_columns - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Negative diagonals (top-left to bottom-right)
    for row in range(3, num_rows):
        for col in range(num_columns - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Check if the game ended in a draw."""
    for row in board:
        if ' ' in row:
            return False
    return True

def play_game():
    """Main game function."""
    board = init_board(NUM_ROWS, NUM_COLUMNS)
    current_players = CHECKERS[:CURRENT_NUM_PLAYERS]
    current_player = random.choice(current_players)

    print_board(board)
    
    while True:
        print(f"Player {current_player}, it's your turn.")
        column = get_valid_column(board)
        place_checker(board, column, current_player)
        print_board(board)

        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        if check_draw(board):
            print("The game ended in a draw!")
            break

        # Alternate player turn
        current_player_idx = current_players.index(current_player)
        current_player = current_players[(current_player_idx + 1) % CURRENT_NUM_PLAYERS]

# Start the game
play_game()
