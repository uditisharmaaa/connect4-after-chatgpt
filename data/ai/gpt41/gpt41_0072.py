import os
import random
import string
import sys

# --- CONSTANTS ---
BOARD_ROWS = 6
BOARD_COLS = 7   # max 26 supported
N_PLAYERS = 2    # can be set between 2-5

CHECKERS = ['X', 'O', 'V', 'H', 'M']
WIN_LENGTH = 4

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    cols = len(board[0])
    rows = len(board)
    column_labels = '  ' + '   '.join(string.ascii_uppercase[:cols])
    sep = '+' + '---+' * cols
    print(column_labels)
    for r in range(rows):
        print(sep)
        print('|' + '|'.join(f' {cell} ' for cell in board[r]) + '|')
    print(sep)

def get_valid_columns(board):
    valid_cols = []
    for col in range(len(board[0])):
        if board[0][col] == ' ':
            valid_cols.append(col)
    return valid_cols

def drop_checker(board, col, checker):
    """ Place checker in column col, return (row, col) if successful, else None."""
    for row in reversed(range(len(board))):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None

def is_full(board):
    return all(cell != ' ' for cell in board[0])

def check_win(board, row, col, checker):
    """ Check horizontally, vertically and both diagonals for a win from (row,col). """
    directions = [ (0,1), (1,0), (1,1), (1,-1) ] # horiz, vert, diag /, diag \
    for dr, dc in directions:
        count = 1
        # Forward direction
        r, c = row + dr, col + dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r += dr
            c += dc
        # Backward direction
        r, c = row - dr, col - dc
        while 0 <= r < len(board) and 0 <= c < len(board[0]) and board[r][c] == checker:
            count += 1
            r -= dr
            c -= dc
        if count >= WIN_LENGTH:
            return True
    return False

def input_column(valid_columns, cols):
    while True:
        col_input = input("Please enter a column: ").strip().upper()
        if len(col_input) != 1 or col_input not in string.ascii_uppercase[:cols]:
            print("Invalid column. Try a letter between A and {}.".format(string.ascii_uppercase[cols-1]))
            continue
        col = string.ascii_uppercase.index(col_input)
        if col not in valid_columns:
            print("Column is full. Turn will be lost.")
            return None
        return col

def main():
    board = create_board(BOARD_ROWS, BOARD_COLS)
    players = CHECKERS[:N_PLAYERS]
    current = random.randint(0, N_PLAYERS - 1)
    clear_screen()
    print_board(board)
    print(f"Player {players[current]}'s turn to start!")

    while True:
        player = players[current]
        print(f"Player {player},", end=' ')

        valid_cols = get_valid_columns(board)
        col = input_column(valid_cols, BOARD_COLS)

        if col is None:
            # Invalid input or full column: lose the turn
            current = (current + 1) % N_PLAYERS
            clear_screen()
            print_board(board)
            continue

        pos = drop_checker(board, col, player)
        clear_screen()
        print_board(board)

        if pos:
            row, col_actual = pos
            if check_win(board, row, col_actual, player):
                print(f"Player {player} won!")
                break
            elif is_full(board):
                print("It's a draw!")
                break
            current = (current + 1) % N_PLAYERS
        else:
            # Should not reach here; handled in input_column
            print("Column is full. Turn will be lost.")
            current = (current + 1) % N_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame aborted.")
