import os
import random
import sys

# Configurable constants
ROWS = 6
COLS = 7  # max 26
NUM_PLAYERS = 2  # 2..5
CHECKERS = ["X", "O", "V", "H", "M"]

if not (2 <= NUM_PLAYERS <= 5) or COLS > 26:
    print("Invalid configuration."); sys.exit(1)
PLAYERS = CHECKERS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def clear_and_print(board):
    os.system('clear')
    letters = [chr(ord('A') + i) for i in range(len(board[0]))]
    print("  " + "   ".join(letters))
    line = "+" + "+".join(["---"] * len(board[0])) + "+"
    for row in board:
        print(line)
        print("|" + "|".join(f" {ch} " for ch in row) + "|")
    print(line)

def drop_checker(board, col, ch):
    # Try from bottom row upwards
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = ch
            return r
    return None

def in_bounds(r, c, R, C): return 0 <= r < R and 0 <= c < C

def check_win(board, ch):
    R, C = len(board), len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            if board[r][c] != ch: continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r, c
                for _ in range(3):
                    rr += dr; cc += dc
                    if in_bounds(rr, cc, R, C) and board[rr][cc] == ch:
                        cnt += 1
                    else:
                        break
                if cnt == 4:
                    return True
    return False

def board_full(board):
    return all(cell != " " for row in board for cell in row)

def prompt_col(max_col):
    while True:
        s = input("Please enter a column: ").strip().upper()
        if len(s) == 1 and "A" <= s <= chr(ord("A")+max_col-1):
            return ord(s) - ord("A")
        # keep asking until valid (turn not lost)
        print("Invalid input. Use a letter between A and " + chr(ord("A")+max_col-1) + ".")

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    clear_and_print(board)
    while True:
        player = PLAYERS[current]
        print(f"Player {player},", end=" ")
        col = prompt_col(COLS)
        row = drop_checker(board, col, player)
        if row is None:
            # Column full, turn lost
            clear_and_print(board)
            current = (current + 1) % NUM_PLAYERS
            continue
        clear_and_print(board)
        if check_win(board, player):
            print(f"Player {player} won!")
            break
        if board_full(board):
            print("It's a draw!")
            break
        current = (current + 1) % NUM_PLAYERS
        print(f"Player {PLAYERS[current]}, please enter a column:")

if __name__ == "__main__":
    # Initial board display and who starts
    board = make_board(ROWS, COLS)
    os.system('clear')
    clear_and_print(board)
    # Start game fresh so first printed prompt matches example format
    main()
