import os
import random

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]

# Functions
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear the terminal
    header = "  " + "   ".join(chr(65 + i) for i in range(len(board[0])))  # Columns as A, B, C...
    print(header)
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")

def is_valid_column(column, cols):
    # Check if the column is within valid range
    return column.isalpha() and len(column) == 1 and 0 <= ord(column.upper()) - 65 < cols

def get_column_from_player(board, cols):
    while True:
        column = input("Please enter a column: ").strip().upper()
        if not is_valid_column(column, cols):
            print("Invalid column. Please enter a valid letter from the available columns.")
            continue
        col_index = ord(column) - 65
        if board[0][col_index] != " ":
            print(f"Column {column} is full. Please choose a different column.")
            continue
        return col_index

def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return

def check_winner(board, symbol):
    rows, cols = len(board), len(board[0])

    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == symbol for i in range(4)):
                return True

    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i][c] == symbol for i in range(4)):
                return True

    # Check diagonal (bottom-left to top-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == symbol for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right)
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i][c + i] == symbol for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main Program
def connect_four():
    # Initialize game board and players
    board = create_board(ROWS, COLS)
    num_players = 2  # Set to 2 as per submission instructions
    players = PLAYER_SYMBOLS[:num_players]

    # Randomly select starting player
    current_player_index = random.randint(0, num_players - 1)

    print_board(board)

    while True:
        current_player = players[current_player_index]
        print(f"Player {current_player}'s turn.")
        col = get_column_from_player(board, COLS)
        place_checker(board, col, current_player)

        print_board(board)

        # Check for win or draw
        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break
        elif check_draw(board):
            print("The game is a draw!")
            break

        # Switch to next player
        current_player_index = (current_player_index + 1) % num_players

# Run the game
if __name__ == "__main__":
    connect_four()
