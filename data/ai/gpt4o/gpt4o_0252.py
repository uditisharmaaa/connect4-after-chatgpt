import os
import random

# Constants
NUM_ROWS = 6
NUM_COLS = 7
NUM_PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board, cols):
    os.system('clear')
    header = "  " + "   ".join(chr(ord('A') + i) for i in range(cols))
    print(header)
    print("+" + "---+" * cols)
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * cols)

def is_valid_column(column, cols):
    return column.isalpha() and 'A' <= column <= chr(ord('A') + cols - 1)

def get_row_for_column(board, column_index):
    for row_index in range(len(board) - 1, -1, -1):
        if board[row_index][column_index] == " ":
            return row_index
    return None
        
def check_winner(board, rows, cols, checker):
    # Check horizontal, vertical, and diagonals
    for row in range(rows):
        for col in range(cols - 3):
            if all(board[row][col + i] == checker for i in range(4)):
                return True

    for row in range(rows - 3):
        for col in range(cols):
            if all(board[row + i][col] == checker for i in range(4)):
                return True

    for row in range(rows - 3):
        for col in range(cols - 3):
            if all(board[row + i][col + i] == checker for i in range(4)):
                return True

    for row in range(3, rows):
        for col in range(cols - 3):
            if all(board[row - i][col + i] == checker for i in range(4)):
                return True

    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def connect4_game():
    board = create_board(NUM_ROWS, NUM_COLS)
    players_checkers = CHECKERS[:NUM_PLAYERS]
    current_player = random.choice(players_checkers)

    print_board(board, NUM_COLS)

    while True:
        print(f"Player {current_player}, please enter a column:")
        column = input().upper()

        if not is_valid_column(column, NUM_COLS):
            print("Invalid input. Try again.")
            continue

        column_index = ord(column) - ord('A')
        row_index = get_row_for_column(board, column_index)

        if row_index is None:
            print("Column is full. You lose your turn.")
            current_player = players_checkers[(players_checkers.index(current_player) + 1) % NUM_PLAYERS]
            continue

        board[row_index][column_index] = current_player
        print_board(board, NUM_COLS)

        if check_winner(board, NUM_ROWS, NUM_COLS, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = players_checkers[(players_checkers.index(current_player) + 1) % NUM_PLAYERS]

if __name__ == "__main__":
    connect4_game()
