import os
import random

# Constants for board dimensions and number of players
BOARD_ROWS = 6
BOARD_COLS = 7
NUM_PLAYERS = 2
PLAYER_CHECKERS = ["X", "O", "V", "H", "M"][:NUM_PLAYERS]

# Initialize the board
def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

# Display the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(chr(65 + i) for i in range(len(board[0]))))
    print("+---" * len(board[0]) + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * len(board[0]) + "+")
    print()

# Check if given column input is valid
def validate_column_input(column, board):
    if len(column) != 1 or not column.isalpha():
        return False
    col_index = ord(column.upper()) - 65
    return 0 <= col_index < len(board[0]) and any(row[col_index] == " " for row in board)

# Place checker in the correct row in the column
def place_checker(board, col_index, checker):
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

# Check for a winning condition
def check_win(board, checker):
    rows, cols = len(board), len(board[0])

    # Check horizontal win
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r][c + i] == checker for i in range(4)):
                return True

    # Check vertical win
    for c in range(cols):
        for r in range(rows - 3):
            if all(board[r + i][c] == checker for i in range(4)):
                return True

    # Check diagonal (top-left to bottom-right) win
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i][c + i] == checker for i in range(4)):
                return True

    # Check diagonal (top-right to bottom-left) win
    for r in range(rows - 3):
        for c in range(3, cols):
            if all(board[r + i][c - i] == checker for i in range(4)):
                return True

    return False

# Check if board is full (draw)
def check_draw(board):
    return all(cell != " " for row in board for cell in row)

# Main game loop
def play_connect_4():
    # Initialize board and players
    board = create_board(BOARD_ROWS, BOARD_COLS)
    current_player = random.randint(0, NUM_PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {PLAYER_CHECKERS[current_player]}, it's your turn!")
        column = input("Please enter a column (A-G): ").strip().upper()

        if not validate_column_input(column, board):
            print("Invalid input. Please try again.")
            continue

        col_index = ord(column) - 65
        place_checker(board, col_index, PLAYER_CHECKERS[current_player])

        # Check for win or draw
        if check_win(board, PLAYER_CHECKERS[current_player]):
            print_board(board)
            print(f"Player {PLAYER_CHECKERS[current_player]} won!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        # Switch to the next player
        current_player = (current_player + 1) % NUM_PLAYERS

# Run the game
if __name__ == "__main__":
    play_connect_4()
