import os
import random

# Constants
ROWS = 6
COLUMNS = 7
NUM_PLAYERS = 2
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    os.system('clear')
    headers = '  '.join(chr(65 + i) for i in range(len(board[0])))
    row_line = '+---' * len(board[0]) + '+'
    print('  ' + headers)
    for row in board:
        print(row_line)
        print('|' + '|'.join(f" {cell} " for cell in row) + '|')
    print(row_line)

def is_valid_column(column):
    return column.isalpha() and 0 <= ord(column.upper()) - 65 < COLUMNS

def place_checker(board, col, player):
    col_idx = ord(col.upper()) - 65
    for row in reversed(board):
        if row[col_idx] == ' ':
            row[col_idx] = CHECKERS[player]
            return True
    return False

def check_winner(board, player):
    check_str = CHECKERS[player] * 4

    # Horizontal check
    for row in board:
        if check_str in ''.join(row):
            return True
            
    # Vertical check
    for col in range(COLUMNS):
        col_values = ''.join([board[row][col] for row in range(ROWS)])
        if check_str in col_values:
            return True

    # Diagonal checks
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            # Positive diagonal
            pos_diag = ''.join([board[row + i][col + i] for i in range(4)])
            if pos_diag == check_str:
                return True
            # Negative diagonal
            if row >= 3:
                neg_diag = ''.join([board[row - i][col + i] for i in range(4)])
                if neg_diag == check_str:
                    return True
    
    return False

def is_draw(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board(ROWS, COLUMNS)
    current_player = random.randint(0, NUM_PLAYERS - 1)
    print_board(board)

    while True:
        current_checker = CHECKERS[current_player]
        col = input(f"Player {current_checker}, please enter a column: ").strip()
        if not is_valid_column(col):
            print("Invalid input.")
            continue

        if not place_checker(board, col, current_player):
            print("Column is full.")
            continue

        print_board(board)

        if check_winner(board, current_player):
            print(f"Player {current_checker} won!")
            break

        if is_draw(board):
            print("The game is a draw!")
            break

        current_player = (current_player + 1) % NUM_PLAYERS

if __name__ == '__main__':
    main()
