import random
import os

# Constants
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
PLAYER_SYMBOLS = ["X", "O", "V", "H", "M"]
NUM_PLAYERS = 2

# Initialize board
def create_board():
    return [[" " for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(c) for c in range(65, 65 + COLS)))
    for row in board:
        print("+---" * COLS + "+")
        print("| " + " | ".join(row) + " |")
    print("+---" * COLS + "+")

# Check for a win
def check_win(board, symbol):
    # Check horizontal
    for row in board:
        for col in range(COLS - 3):
            if row[col] == symbol and row[col + 1] == symbol and row[col + 2] == symbol and row[col + 3] == symbol:
                return True

    # Check vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            if board[row][col] == symbol and board[row + 1][col] == symbol and board[row + 2][col] == symbol and board[row + 3][col] == symbol:
                return True

    # Check diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row + 1][col + 1] == symbol and board[row + 2][col + 2] == symbol and board[row + 3][col + 3] == symbol:
                return True

    # Check diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if board[row][col] == symbol and board[row - 1][col + 1] == symbol and board[row - 2][col + 2] == symbol and board[row - 3][col + 3] == symbol:
                return True

    return False

# Check for a draw
def check_draw(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

# Place checker
def place_checker(board, col, symbol):
    for row in reversed(board):
        if row[col] == " ":
            row[col] = symbol
            return True
    return False

# Get valid user input
def get_valid_input():
    while True:
        try:
            col_input = input("Please enter a column (A-G): ").strip().upper()
            if len(col_input) == 1 and 'A' <= col_input <= 'G':
                col = ord(col_input) - 65
                if col < COLS:
                    return col
            print("Invalid input. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Try again.")

# Game logic
def start_game():
    board = create_board()
    current_player_idx = random.randint(0, NUM_PLAYERS - 1)
    game_over = False

    print_board(board)

    while not game_over:
        symbol = PLAYER_SYMBOLS[current_player_idx]
        print(f"Player {symbol}'s turn.")
        col = get_valid_input()

        if not place_checker(board, col, symbol):
            print("Column is full. Choose another column.")
            continue

        print_board(board)

        if check_win(board, symbol):
            print(f"Player {symbol} won!")
            game_over = True
        elif check_draw(board):
            print("The game is a draw!")
            game_over = True
        else:
            current_player_idx = (current_player_idx + 1) % NUM_PLAYERS

if __name__ == "__main__":
    start_game()
