import os
import random

ROWS = 6
COLS = 7
PLAYERS = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        board.append([" "] * COLS)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(" ", end=" ")
    for c in range(COLS):
        print(letters[c], end="   ")
    print()
    for r in range(ROWS):
        print("+" + "---+" * COLS)
        print("|", end="")
        for c in range(COLS):
            print(" " + board[r][c] + " |", end="")
        print()
    print("+" + "---+" * COLS)

def get_valid_column(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        col = input("Player " + CHECKERS[player] + ", please enter a column: ")
        if len(col) != 1:
            continue
        col = col.upper()
        if col not in letters[:COLS]:
            continue
        col_idx = letters.index(col)
        if board[0][col_idx] != " ":
            # column full
            return -1
        return col_idx

def make_move(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col
    return -1, -1

def check_horiz(board, r, c, checker):
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_vert(board, r, c, checker):
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def check_diag(board, r, c, checker):
    # check \ diagonal
    start_r = r
    start_c = c
    while start_r > 0 and start_c > 0:
        start_r -= 1
        start_c -= 1
    count = 0
    while start_r < ROWS and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r += 1
        start_c += 1

    # check / diagonal
    start_r = r
    start_c = c
    while start_r < ROWS-1 and start_c > 0:
        start_r += 1
        start_c -= 1
    count = 0
    while start_r >= 0 and start_c < COLS:
        if board[start_r][start_c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        start_r -= 1
        start_c += 1

    return False

def check_win(board, r, c, checker):
    if check_horiz(board, r, c, checker):
        return True
    if check_vert(board, r, c, checker):
        return True
    if check_diag(board, r, c, checker):
        return True
    return False

def check_draw(board):
    for c in range(COLS):
        if board[0][c] == " ":
            return False
    return True

def main():
    board = create_board()
    players = PLAYERS
    checkers = CHECKERS[:players]
    current_player = random.randint(0, players - 1)
    print_board(board)

    while True:
        col = get_valid_column(current_player, board)
        if col == -1:
            # lose turn
            current_player = (current_player + 1) % players
            continue
        r, c = make_move(board, col, checkers[current_player])
        print_board(board)
        if check_win(board, r, c, checkers[current_player]):
            print("Player " + checkers[current_player] + " won!")
            break
        if check_draw(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % players


if __name__ == "__main__":
    main()
