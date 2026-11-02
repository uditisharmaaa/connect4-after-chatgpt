import os
import random

# Constants
ROWS = 6
COLUMNS = 7
MAX_PLAYERS = 5
PLAYERS = ["X", "O", "V", "H", "M"][:2]  # Adjust for 2 players initially
COLUMN_LABELS = [chr(i) for i in range(65, 65 + COLUMNS)]  # Labels A-G

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

def create_board(rows, columns):
    """Create an empty game board."""
    return [[" " for _ in range(columns)] for _ in range(rows)]

def print_board(board):
    """Display the game board."""
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def is_valid_column(column):
    """Check if a column label is valid."""
    return column in COLUMN_LABELS

def is_column_full(board, col_index):
    """Check if a column is full."""
    return board[0][col_index] != " "

def drop_checker(board, col_index, checker):
    """Drop a checker into the specified column."""
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_winner(board, checker):
    """Check if the current player has won."""
    # Check horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c+i] == checker for i in range(4)):
                return True

    # Check vertical
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r+i][c] == checker for i in range(4)):
                return True

    # Check diagonal (down-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)):
                return True

    # Check diagonal (up-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(board[0][c] != " " for c in range(COLUMNS))

def get_valid_column():
    """Prompt the user for a valid column and return the column index."""
    while True:
        column = input("Please enter a column: ").strip().upper()
        if not is_valid_column(column):
            print("Invalid column! Please try again.")
            continue
        col_index = COLUMN_LABELS.index(column)
        if is_column_full(board, col_index):
            print("Column is full! Please try a different column.")
            continue
        return col_index

# Main game loop
def play_game():
    # Initialization
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, len(PLAYERS) - 1)
    print_board(board)

    # Game loop
    while True:
        current_player = PLAYERS[current_player_index]
        print(f"Player {current_player}, it's your turn!")

        col_index = get_valid_column()
        drop_checker(board, col_index, current_player)
        print_board(board)

        # Check for win
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch to the next player
        current_player_index = (current_player_index + 1) % len(PLAYERS)

# Run the game
if __name__ == "__main__":
    play_game()
