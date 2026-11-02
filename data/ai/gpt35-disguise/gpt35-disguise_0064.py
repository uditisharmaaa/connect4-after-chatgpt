import os
import random

ROWS = 6
COLS = 7
PLAYERS_NUM = 2
CHECKERS = ["X", "O", "V", "H", "M"]

def clear_screen():
    os.system('clear')

def create_board():
    board = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            row.append(" ")
        board.append(row)
    return board

def print_board(board):
    clear_screen()
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print("  " + "   ".join(letters[:COLS]))
    print("+---"*COLS + "+")
    for r in range(ROWS):
        line = "|"
        for c in range(COLS):
            line += " " + board[r][c] + " |"
        print(line)
        print("+---"*COLS + "+")

def get_player_input(player, board):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while True:
        inp = input(f"Player {CHECKERS[player]}, please enter a column: ").strip().upper()
        if len(inp) != 1:
            continue
        if inp not in letters[:COLS]:
            continue
        col = letters.index(inp)
        if board[0][col] != " ":
            # column full
            return -1  # lose turn
        return col

def place_checker(board, col, checker):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == " ":
            board[r][col] = checker
            return r, col

def check_win(board, r, c, checker):
    # horizontal
    count = 0
    for col in range(COLS):
        if board[r][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # vertical
    count = 0
    for row in range(ROWS):
        if board[row][c] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    # diagonal /
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col < COLS-1:
        start_row -= 1
        start_col += 1
    row = start_row
    col = start_col
    while row < ROWS and col >= 0:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col -= 1
    # diagonal \
    count = 0
    start_row = r
    start_col = c
    while start_row > 0 and start_col > 0:
        start_row -= 1
        start_col -= 1
    row = start_row
    col = start_col
    while row < ROWS and col < COLS:
        if board[row][col] == checker:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
        row += 1
        col += 1
    return False

def is_draw(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == " ":
                return False
    return True

def main():
    board = create_board()
    current_player = random.randint(0, PLAYERS_NUM-1)
    print_board(board)
    while True:
        col = get_player_input(current_player, board)
        if col == -1:
            # lose turn if full column
            current_player = (current_player + 1) % PLAYERS_NUM
            print_board(board)
            continue
        row, col = place_checker(board, col, CHECKERS[current_player])
        print_board(board)
        if check_win(board, row, col, CHECKERS[current_player]):
            print(f"Player {CHECKERS[current_player]} won!")
            break
        if is_draw(board):
            print("Game is a draw!")
            break
        current_player = (current_player + 1) % PLAYERS_NUM

main()
