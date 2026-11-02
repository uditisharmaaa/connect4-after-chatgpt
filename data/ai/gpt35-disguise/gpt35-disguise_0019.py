import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]
WIN_COUNT = 4

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for _ in range(ROWS):
        board.append([" "]*COLS)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "  "
    for i in range(COLS):
        header += " " + letters[i] + "  "
    print(header)
    line = "+---"*COLS + "+"
    for r in range(ROWS):
        print(line)
        row_str = "|"
        for c in range(COLS):
            row_str += " " + board[r][c] + " |"
        print(row_str)
    print(line)

def get_player_input(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col = input(f"Player {player}, please enter a column: ")
        if len(col) != 1:
            continue
        col = col.upper()
        if col not in letters[:COLS]:
            continue
        col_idx = letters.index(col)
        if board[0][col_idx] != " ":
            # column full -> player loses turn
            return None
        return col_idx

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_horiz(board, r, c, checker):
    count = 0
    for col in range(max(0, c-3), min(COLS, c+4)):
        if board[r][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_vert(board, r, c, checker):
    count = 0
    for row in range(max(0, r-3), min(ROWS, r+4)):
        if board[row][c] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_diag1(board, r, c, checker):
    count = 0
    start_row = r - min(r, c, 3)
    start_col = c - min(r, c, 3)
    for i in range(7):
        row = start_row + i
        col = start_col + i
        if row >= ROWS or col >= COLS:
            break
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_diag2(board, r, c, checker):
    count = 0
    min_move = min(r, COLS - 1 - c, 3)
    start_row = r - min_move
    start_col = c + min_move
    for i in range(7):
        row = start_row + i
        col = start_col - i
        if row >= ROWS or col < 0:
            break
        if board[row][col] == checker:
            count += 1
            if count == WIN_COUNT:
                return True
        else:
            count = 0
    return False

def check_win(board, r, c, checker):
    if check_horiz(board, r, c, checker):
        return True
    if check_vert(board, r, c, checker):
        return True
    if check_diag1(board, r, c, checker):
        return True
    if check_diag2(board, r, c, checker):
        return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = CHECKERS[:PLAYERS]
    current = random.randint(0, PLAYERS -1)
    print_board(board)
    while True:
        checker = players[current]
        col = get_player_input(checker, board)
        if col is None:
            # column full, lose turn
            current = (current +1) % PLAYERS
            print_board(board)
            continue
        r, c = place_checker(board, col, checker)
        print_board(board)
        if check_win(board, r, c, checker):
            print(f"Player {checker} won!")
            break
        if check_draw(board):
            print("The game is a draw!")
            break
        current = (current + 1) % PLAYERS

if __name__ == "__main__":
    main()
