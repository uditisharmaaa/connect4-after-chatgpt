import os
import random

# Constants
ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
COLUMN_LABELS = [chr(65 + i) for i in range(COLS)]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    print("  " + "   ".join(COLUMN_LABELS[:COLS]))
    print("+---" * COLS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLS + "+")

def is_valid_move(board, column):
    return column in COLUMN_LABELS[:COLS] and any(row[COLUMN_LABELS.index(column)] == " " for row in board)

def make_move(board, column, checker):
    col_index = COLUMN_LABELS.index(column)
    for row in reversed(board):
        if row[col_index] == " ":
            row[col_index] = checker
            return

def check_winner(board, checker):
    # Check horizontal, vertical, and diagonal
    for r in range(ROWS):
        for c in range(COLS):
            if (
                c + 3 < COLS and all(board[r][c + i] == checker for i in range(4)) or
                r + 3 < ROWS and all(board[r + i][c] == checker for i in range(4)) or
                r + 3 < ROWS and c + 3 < COLS and all(board[r + i][c + i] == checker for i in range(4)) or
                r + 3 < ROWS and c - 3 >= 0 and all(board[r + i][c - i] == checker for i in range(4))
            ):
                return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:PLAYERS]
    current_turn = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        current_player = players[current_turn]
        print(f"Player {current_player}, please enter a column:")
        column = input().strip().upper()

        if not is_valid_move(board, column):
            print("Invalid move. Try again.")
            continue

        make_move(board, column, current_player)
        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_player} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_turn = (current_turn + 1) % PLAYERS

if __name__ == "__main__":
    main()
