import os
import random

# ----- Constants -----
ROWS = 6
COLS = 7
MAX_PLAYERS = 5
MIN_PLAYERS = 2
NUM_PLAYERS = 2  # always 2 for submission! Change for testing other values
WIN_COUNT = 4
CHECKERS = ['X', 'O', 'V', 'H', 'M']
COL_LABELS = [chr(ord('A') + i) for i in range(COLS)]

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def create_board():
    return [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def print_board(board):
    clear_screen()
    print('  ' + '   '.join(COL_LABELS))
    print('+' + '---+' * COLS)
    for row in board:
        print('|' + '|'.join(' {:1} '.format(cell) for cell in row) + '|')
        print('+' + '---+' * COLS)

def get_valid_input(board):
    while True:
        inp = input().strip().upper()
        if len(inp) != 1 or inp not in COL_LABELS:
            print(f"Invalid input, try again (choose A-{COL_LABELS[-1]}):")
            continue
        col = COL_LABELS.index(inp)
        if board[0][col] != ' ':
            print("Column full! You lose your turn.")
            return None
        else:
            return col

def place_checker(board, col, checker):
    # Place from bottom up
    for row in reversed(range(ROWS)):
        if board[row][col] == ' ':
            board[row][col] = checker
            return row, col
    return None  # should never happen if checked before

def is_within(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

def check_win(board, last_row, last_col, checker):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for dr, dc in directions:
        cnt = 1
        for dir in [1, -1]:
            r, c = last_row, last_col
            while True:
                r += dr * dir
                c += dc * dir
                if is_within(r, c) and board[r][c] == checker:
                    cnt += 1
                else:
                    break
        if cnt >= WIN_COUNT:
            return True
    return False

def board_full(board):
    return all(cell != ' ' for cell in board[0])

def main():
    board = create_board()
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randint(0, NUM_PLAYERS - 1)

    print_board(board)
    print(f"Player {players[current]}, please enter a column:")

    while True:
        col = get_valid_input(board)
        if col is None:  # Column full, lose turn
            current = (current + 1) % NUM_PLAYERS
            print_board(board)
            print(f"Player {players[current]}, please enter a column:")
            continue
        row, col = place_checker(board, col, players[current])
        print_board(board)

        if check_win(board, row, col, players[current]):
            print(f"Player {players[current]} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS
        print(f"Player {players[current]}, please enter a column:")

if __name__ == '__main__':
    main()
