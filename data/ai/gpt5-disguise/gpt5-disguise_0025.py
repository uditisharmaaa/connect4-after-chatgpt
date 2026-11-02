import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]

COLS = min(COLS, 26)
NUM_PLAYERS = max(2, min(NUM_PLAYERS, 5))
PLAYERS = TOKENS[:NUM_PLAYERS]

def make_board(r, c):
    return [[" " for _ in range(c)] for _ in range(r)]

def print_board(board):
    os.system('clear')
    letters = string.ascii_uppercase[:len(board[0])]
    header = "  " + "   ".join(letters)
    print(header)
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    for row in board:
        print(sep)
        line = "|"
        for cell in row:
            line += " " + cell + " |"
        print(line)
    print(sep)

def col_from_input(s, max_c):
    if len(s) != 1:
        return None
    if not s.isalpha():
        return None
    s = s.upper()
    letters = string.ascii_uppercase[:max_c]
    if s not in letters:
        return None
    return letters.index(s)

def drop_token(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, R, C):
    return 0 <= r < R and 0 <= c < C

def check_win(board):
    R = len(board)
    C = len(board[0])
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    for r in range(R):
        for c in range(C):
            ch = board[r][c]
            if ch == " ":
                continue
            for dr, dc in dirs:
                cnt = 1
                rr, cc = r + dr, c + dc
                while cnt < 4 and in_bounds(rr, cc, R, C) and board[rr][cc] == ch:
                    cnt += 1
                    rr += dr
                    cc += dc
                if cnt == 4:
                    return ch
    return None

def board_full(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = make_board(ROWS, COLS)
    current = random.randrange(NUM_PLAYERS)
    print_board(board)
    while True:
        player_token = PLAYERS[current]
        print(f"Player {player_token}, please enter a column:")
        choice = input().strip()
        col = col_from_input(choice, COLS)
        while col is None:
            print_board(board)
            print("Invalid input. Try again.")
            print(f"Player {player_token}, please enter a column:")
            choice = input().strip()
            col = col_from_input(choice, COLS)

        row_placed = drop_token(board, col, player_token)
        if row_placed is None:
            print_board(board)
            print("Column full. Turn lost.")
            current = (current + 1) % NUM_PLAYERS
            continue

        print_board(board)
        winner = check_win(board)
        if winner is not None:
            print(f"Player {winner} won!")
            break

        if board_full(board):
            print("It's a draw!")
            break

        current = (current + 1) % NUM_PLAYERS

if __name__ == "__main__":
    main()
