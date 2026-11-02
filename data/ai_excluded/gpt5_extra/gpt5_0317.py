import os
import random
import sys

# Constants (submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
CHECKERS = ['X', 'O', 'V', 'H', 'M'][:NUM_PLAYERS]
LETTERS = [chr(ord('A') + i) for i in range(min(COLS, 26))]

def clear_screen():
    os.system('clear')

def create_board(rows, cols):
    return [[' ' for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    clear_screen()
    # Header
    header = '  ' + '   '.join(LETTERS[:len(board[0])])
    print(header)
    print('+' + '---+' * len(board[0]))
    for r in range(len(board)):
        row = '|' + '|'.join(f' {board[r][c]} ' for c in range(len(board[0]))) + '|'
        print(row)
        print('+' + '---+' * len(board[0]))

def valid_column_input(s):
    s = s.strip().upper()
    return len(s) == 1 and s in LETTERS[:COLS]

def drop_checker(board, col_idx, sym):
    # place in lowest available row
    for r in range(ROWS - 1, -1, -1):
        if board[r][col_idx] == ' ':
            board[r][col_idx] = sym
            return r
    return -1  # column full

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def check_win(board, sym):
    directions = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != sym:
                continue
            for dr, dc in directions:
                count = 1
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc) and board[rr][cc] == sym:
                    count += 1
                    if count == 4:
                        return True
                    rr += dr
                    cc += dc
    return False

def board_full(board):
    return all(board[0][c] != ' ' for c in range(COLS))

def main():
    if COLS > 26 or NUM_PLAYERS < 2 or NUM_PLAYERS > 5:
        print("Invalid configuration.", file=sys.stderr)
        return
    board = create_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)

    # Initial board display
    print_board(board)

    while True:
        sym = CHECKERS[current]
        # Prompt for valid column letter
        col_input = ''
        while True:
            col_input = input(f"Player {sym}, please enter a column: ").strip().upper()
            if valid_column_input(col_input):
                break
            # invalid input: reprompt, turn not lost
        col_idx = LETTERS.index(col_input)

        # Try to drop checker
        row = drop_checker(board, col_idx, sym)
        if row == -1:
            # Column full: turn is invalid and lost
            print_board(board)
            print(f"Column {col_input} is full. Player {sym} loses the turn.")
            current = (current + 1) % NUM_PLAYERS
            continue

        # Successful move: show updated board
        print_board(board)

        # Check win/draw
        if check_win(board, sym):
            print(f"Player {sym} won!")
            break
        if board_full(board):
            print("The game is a draw.")
            break

        # Next player
        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
