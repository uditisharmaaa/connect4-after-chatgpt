import os
import random

# Constants
ROWS = 6
COLUMNS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"][:PLAYERS]
COLUMN_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:COLUMNS]

def print_board(board):
    os.system('clear')
    print("  " + "   ".join(COLUMN_LABELS))
    print("+---" * COLUMNS + "+")
    for row in board:
        print("| " + " | ".join(row) + " |")
        print("+---" * COLUMNS + "+")

def create_board(rows, columns):
    return [[" " for _ in range(columns)] for _ in range(rows)]

def is_valid_move(board, column):
    return 0 <= column < COLUMNS and board[0][column] == " "

def get_next_free_row(board, column):
    for r in range(ROWS-1, -1, -1):
        if board[r][column] == " ":
            return r

def play_turn(board, player_checker):
    while True:
        column_letter = input(f"Player {player_checker}, please enter a column: ").upper()
        if column_letter not in COLUMN_LABELS:
            print("Invalid column. Try again.")
            continue

        column = COLUMN_LABELS.index(column_letter)

        if not is_valid_move(board, column):
            print("Column is full or invalid move. Try again.")
            continue

        row = get_next_free_row(board, column)
        board[row][column] = player_checker
        break

def check_win(board, player_checker):
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if board[r][c:c + 4] == [player_checker]*4:
                return True

    # Vertical check
    for r in range(ROWS - 3):
        for c in range(COLUMNS):
            if all(board[r + i][c] == player_checker for i in range(4)):
                return True

    # Diagonal (positive slope) check
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player_checker for i in range(4)):
                return True

    # Diagonal (negative slope) check
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == player_checker for i in range(4)):
                return True

    return False

def check_draw(board):
    return all(board[0][c] != " " for c in range(COLUMNS))

def main():
    board = create_board(ROWS, COLUMNS)
    current_player_index = random.randint(0, PLAYERS - 1)
    print_board(board)

    while True:
        play_turn(board, CHECKERS[current_player_index])
        print_board(board)
        
        # Check for win
        if check_win(board, CHECKERS[current_player_index]):
            print(f"Player {CHECKERS[current_player_index]} won!")
            break

        # Check for draw
        if check_draw(board):
            print("The game is a draw.")
            break

        # Alternate turn
        current_player_index = (current_player_index + 1) % PLAYERS

if __name__ == "__main__":
    main()
