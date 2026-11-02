import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
EMPTY = " "
COLUMN_LABELS = [chr(65 + i) for i in range(COLS)]

# Initialize the board
def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]

# Print the board
def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

# Validate player input
def is_valid_input(column, board):
    return column in COLUMN_LABELS and any(row[COLUMN_LABELS.index(column)] == EMPTY for row in board)

# Drop checker in the chosen column
def drop_checker(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_index] == EMPTY:
            row[col_index] = checker
            break

# Check for a win condition
def check_win(board, checker):
    def four_in_a_row(line): return any(line[i:i+4] == [checker]*4 for i in range(len(line) - 3))
    
    # Check horizontal and vertical
    for r in range(ROWS):
        if four_in_a_row(board[r]):
            return True
    for c in range(COLS):
        if four_in_a_row([board[r][c] for r in range(ROWS)]):
            return True
    
    # Check diagonals
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == checker for i in range(4)) or all(board[r+i][c+3-i] == checker for i in range(4)):
                return True
    return False

# Check for a draw
def is_draw(board):
    return all(row[c] != EMPTY for row in board for c in range(COLS))

# Main game function
def connect4():
    board = create_board()
    current_player = random.randint(0, PLAYERS - 1)

    while True:
        print_board(board)
        print(f"Player {CHECKERS[current_player]}, please enter a column:")

        column = input().strip().upper()
        if not is_valid_input(column, board):
            print("Invalid input, try again.")
            continue

        drop_checker(board, column, CHECKERS[current_player])

        if check_win(board, CHECKERS[current_player]):
            print_board(board)
            print(f"Player {CHECKERS[current_player]} won!")
            break

        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = (current_player + 1) % PLAYERS

# Run the game
if __name__ == "__main__":
    connect4()
