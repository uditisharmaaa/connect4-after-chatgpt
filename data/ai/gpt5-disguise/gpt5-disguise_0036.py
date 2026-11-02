import os
import random
import string

ROWS = 6
COLS = 7
NUM_PLAYERS = 2
TOKENS = ["X", "O", "V", "H", "M"]
WIN_LEN = 4

def make_board(rows, cols):
    return [[" " for _ in range(cols)] for _ in range(rows)]

def clear_screen():
    os.system('clear')

def print_board(board):
    letters = string.ascii_uppercase[:len(board[0])]
    header = "  " + "   ".join(list(letters))
    sep = "+" + "+".join(["---"] * len(board[0])) + "+"
    print(header)
    print(sep)
    for r in range(len(board)):
        rowcells = []
        for c in range(len(board[0])):
            rowcells.append(board[r][c])
        print("| " + " | ".join(rowcells) + " |")
        print(sep)

def get_input(cols):
    letters = string.ascii_uppercase[:cols]
    while True:
        s = input().strip()
        if len(s) != 1:
            print("Invalid input. Enter a single letter for the column:")
            continue
        ch = s.upper()
        if ch not in letters:
            print("Invalid column. Choose between " + letters[0] + " and " + letters[-1] + ":")
            continue
        return letters.index(ch)

def place(board, col, token):
    for r in range(len(board) - 1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = token
            return r
    return None

def in_bounds(r, c, rows, cols):
    return 0 <= r < rows and 0 <= c < cols

def check_win(board, r, c, token):
    dirs = [(0,1),(1,0),(1,1),(1,-1)]
    rows = len(board)
    cols = len(board[0])
    for dr, dc in dirs:
        count = 1
        rr, cc = r + dr, c + dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr += dr
            cc += dc
        rr, cc = r - dr, c - dc
        while in_bounds(rr, cc, rows, cols) and board[rr][cc] == token:
            count += 1
            rr -= dr
            cc -= dc
        if count >= WIN_LEN:
            return True
    return False

def check_draw(board):
    for c in range(len(board[0])):
        if board[0][c] == " ":
            return False
    return True

def main():
    cols = min(COLS, 26)
    players = max(2, min(NUM_PLAYERS, 5))
    tokens = TOKENS[:players]
    board = make_board(ROWS, cols)
    turn = random.randrange(players)

    clear_screen()
    print_board(board)
    print(f"Player {tokens[turn]}, please enter a column:")

    while True:
        col = get_input(cols)
        row = place(board, col, tokens[turn])
        if row is None:
            clear_screen()
            print_board(board)
            print(f"Column full. Player {tokens[turn]} loses the turn.")
            turn = (turn + 1) % players
            print(f"Player {tokens[turn]}, please enter a column:")
            continue

        clear_screen()
        print_board(board)

        if check_win(board, row, col, tokens[turn]):
            print(f"Player {tokens[turn]} won!")
            break

        if check_draw(board):
            print("It's a draw!")
            break

        turn = (turn + 1) % players
        print(f"Player {tokens[turn]}, please enter a column:")

if __name__ == "__main__":
    main()
