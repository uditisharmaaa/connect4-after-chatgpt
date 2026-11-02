import os
import random
import string

# ==============================
# CONSTANTS (change if needed)
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2  # Between 2 and 5
CHECKERS = ['X', 'O', 'V', 'H', 'M']
MAX_COLUMNS = 26
WIN_COUNT = 4
# ==============================

def create_board(rows, columns):
    return [[' ' for _ in range(columns)] for _ in range(rows)]

def print_board(board, columns):
    os.system('clear')
    # Print column labels
    labels = [string.ascii_uppercase[i] for i in range(columns)]
    print('  ' + '   '.join(labels))
    print('+' + '---+' * columns)
    for row in board:
        print('| ' + ' | '.join(row) + ' |')
        print('+' + '---+' * columns)

def get_valid_columns(board):
    valid = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid.append(col)
    return valid

def input_column(valid_columns, columns):
    labels = [string.ascii_uppercase[i] for i in range(columns)]
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in labels:
            print("Invalid input! Please enter a valid column label.")
            continue
        col = labels.index(col_input)
        if col not in valid_columns:
            print("Column is full. You lose your turn!")
            return None  # Lose turn if invalid
        return col

def place_checker(board, col, checker):
    # Place checker in the lowest available row in this column
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # Should not happen if checked before

def check_win(board, row, col, checker):
    return (check_line(board, row, col, checker, 0, 1) or   # Horizontal
            check_line(board, row, col, checker, 1, 0) or   # Vertical
            check_line(board, row, col, checker, 1, 1) or   # Diagonal \
            check_line(board, row, col, checker, 1, -1))    # Diagonal /

def check_line(board, row, col, checker, delta_row, delta_col):
    count = 1
    # Check one direction
    count += count_direction(board, row, col, checker, delta_row, delta_col)
    # Check opposite direction
    count += count_direction(board, row, col, checker, -delta_row, -delta_col)
    return count >= WIN_COUNT

def count_direction(board, row, col, checker, delta_row, delta_col):
    r = row + delta_row
    c = col + delta_col
    count = 0
    while (0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker):
        count += 1
        r += delta_row
        c += delta_col
    return count

def board_full(board):
    for cell in board[0]:
        if cell == ' ':
            return False
    return True

def main():
    if COLUMNS > MAX_COLUMNS or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid settings. Exiting.")
        return

    checkers_in_play = CHECKERS[:NUM_PLAYERS]
    board = create_board(ROWS, COLUMNS)
    cols_labels = [string.ascii_uppercase[i] for i in range(COLUMNS)]

    # Randomly choose first player
    current_player = random.randint(0, NUM_PLAYERS-1)
    print_board(board, COLUMNS)
    print(f"Player {checkers_in_play[current_player]}, you start!")
    input("Press enter to start...")

    while True:
        print_board(board, COLUMNS)
        print(f"Player {checkers_in_play[current_player]}", end=', ')
        valid_columns = get_valid_columns(board)
        if not valid_columns:
            print("The board is full! The game is a draw.")
            break

        col = None
        # Get and validate input
        while col is None:
            user_input = input(f"please enter a column: ").strip().upper()
            if len(user_input) != 1 or user_input not in cols_labels:
                print("Invalid input! Please enter a valid column label.")
                continue
            col_idx = cols_labels.index(user_input)
            if col_idx not in valid_columns:
                print("Column is full. You lose your turn!")
                break  # Lose turn if column is full
            col = col_idx
        if col is not None:
            row, col = place_checker(board, col, checkers_in_play[current_player])
            if check_win(board, row, col, checkers_in_play[current_player]):
                print_board(board, COLUMNS)
                print(f"Player {checkers_in_play[current_player]} won!")
                break
        else:
            # Lost turn due to full column
            pass

        if board_full(board):
            print_board(board, COLUMNS)
            print("The board is full! The game is a draw.")
            break

        # Next player
        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
