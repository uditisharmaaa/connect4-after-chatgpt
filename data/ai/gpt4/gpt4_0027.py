import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = [chr(65 + i) for i in range(COLUMNS)]  # A, B, C, ...

def clear_screen():
    os.system('clear')

def create_board():
    """Initialize the board with empty spaces."""
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

def print_board(board):
    """Prints the game board with column labels."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def get_column_choice(player_checker):
    """Prompts the current player for a column choice, validates input."""
    while True:
        choice = input(f"Player {player_checker}, please enter a column: ").strip().upper()
        if choice not in COLUMN_LABELS:
            print("Invalid column. Please enter a letter corresponding to a valid column.")
        else:
            col_index = COLUMN_LABELS.index(choice)
            if board[0][col_index] != " ":
                print("Column is full. Choose a different column.")
            else:
                return col_index

def drop_checker(board, col_index, checker):
    """Drops a checker into the specified column."""
    for row in reversed(board):  # Start from bottom row
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_winner(board, checker):
    """Checks if the player with the given checker has won."""
    # Horizontal
    for row in board:
        for col in range(COLUMNS - 3):
            if row[col:col + 4] == [checker] * 4:
                return True

    # Vertical
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    # Diagonal (top-right to bottom-left)
    for row in range(ROWS - 3):
        for col in range(3, COLUMNS):
            if all(board[row + i][col - i] == checker for i in range(4)):
                return True

    return False

def check_draw(board):
    """Checks if the game is a draw (board is fully occupied)."""
    return all(board[0][col] != " " for col in range(COLUMNS))

# Main game logic
def connect_4():
    global board
    board = create_board()

    # Randomly choose a starting player
    current_player = random.randint(0, PLAYERS - 1)

    # Game loop
    while True:
        print_board(board)
        col_index = get_column_choice(CHECKERS[current_player])
        drop_checker(board, col_index, CHECKERS[current_player])

        # Check for win
        if check_winner(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        # Check for draw
        if check_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        # Switch to next player
        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect_4()
