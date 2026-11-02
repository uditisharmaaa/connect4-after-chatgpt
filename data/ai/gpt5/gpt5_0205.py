import os
import random
import sys

# Configuration (changeable, but submission requires 6x7 and 2 players)
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # supports 2..5
CHECKERS = ["X", "O", "V", "H", "M"]

assert 2 <= NUM_PLAYERS <= 5
assert 1 <= COLS <= 26

def clear():
    os.system('clear')

def create_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def print_board(board):
    rows, cols = len(board), len(board[0])
    letters = [chr(ord('A') + i) for i in range(cols)]
    print("  " + "   ".join(letters))
    print("+" + "---+" * cols)
    for r in range(rows):
        print("|" + "|".join(f" {board[r][c]} " for c in range(cols)) + "|")
        print("+" + "---+" * cols)

def lowest_empty_row(board, col):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win_from(board, r, c, sym):
    rows, cols = len(board), len(board[0])
    directions = [(0,1),(1,0),(1,1),(-1,1)]
    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            nr, nc = r + dr*step, c + dc*step
            while in_bounds(nr, nc, rows, cols) and board[nr][nc] == sym:
                count += 1
                if count >= 4:
                    return True
                nr += dr*step
                nc += dc*step
        if count >= 4:
            return True
    return False

def board_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def get_valid_column_input(cols):
    letters = [chr(ord('A') + i) for i in range(cols)]
    while True:
        s = input().strip().upper()
        if len(s) == 1 and s in letters:
            return ord(s) - ord('A')
        print(f"Invalid input. Please enter a letter between A and {letters[-1]}:")

def main():
    board = create_board(ROWS, COLS)
    players = CHECKERS[:NUM_PLAYERS]
    current = random.randrange(NUM_PLAYERS)

    clear()
    print_board(board)

    while True:
        sym = players[current]
        print(f"Player {sym}, please enter a column:")
        col = get_valid_column_input(COLS)

        row = lowest_empty_row(board, col)
        move_made = False
        if row is not None:
            board[row][col] = sym
            move_made = True

        clear()
        print_board(board)

        if move_made:
            if check_win_from(board, row, col, sym):
                print(f"Player {sym} won!")
                break
            if board_full(board):
                print("It's a draw!")
                break
        else:
            print(f"Column {chr(ord('A')+col)} is full. Player {sym} loses the turn.")

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)
