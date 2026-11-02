import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]  # Checker symbols
BOARD_COLUMNS = [chr(i) for i in range(65, 65 + COLUMNS)]  # A-G columns

# Create the game board
def create_board():
    return [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(BOARD_COLUMNS))  # Print column labels
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

# Check if the move is valid
def is_valid_column(column, board):
    return column in BOARD_COLUMNS and board[0][BOARD_COLUMNS.index(column)] == " "

# Place the checker in the correct position
def place_checker(column, checker, board):
    col_index = BOARD_COLUMNS.index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            break

# Check for a win in all directions
def check_win(board, player):
    # Horizontal check
    for row in board:
        for c in range(COLUMNS - 3):
            if row[c:c+4] == [player] * 4:
                return True

    # Vertical check
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    # Diagonal (bottom-left to top-right)
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    # Diagonal (top-left to bottom-right)
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False

# Check for a draw
def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

# Main Connect 4 game logic
def connect4():
    board = create_board()
    num_players = PLAYERS
    current_player_idx = random.randint(0, num_players - 1)  # Randomly select first player
    print_board(board)

    while True:
        # Determine the current player's turn
        current_player = CHECKERS[current_player_idx]
        print(f"Player {current_player}, please enter a column:")

        # Accept and validate input
        while True:
            column = input().strip().upper()
            if not is_valid_column(column, board):
                print("Invalid column. Please try again:")
            else:
                break

        # Place the checker
        place_checker(column, current_player, board)
        print_board(board)

        # Check for win
        if check_win(board, current_player):
            print(f"Player {current_player} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw!")
            break

        # Switch to the next player
        current_player_idx = (current_player_idx + 1) % num_players

# Run the game
if __name__ == "__main__":
    connect4()
